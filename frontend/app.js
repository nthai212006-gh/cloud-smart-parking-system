/**
 * SMART PARKING SYSTEM - ENTERPRISE POS JAVASCRIPT
 * Tích hợp trực tiếp Amazon API Gateway REST API (/checkin, /checkout)
 * Quản lý trạng thái xe trong bãi (State Management), Bộ lọc biển số và Smart Plate Resolution
 * Sinh viên: Lê Cao Việt Tín (24110354) & Nguyễn Trung Hải (24110207)
 */

document.addEventListener("DOMContentLoaded", () => {
  // ============================================================================
  // 1. CONFIGURATION & STATE MANAGEMENT
  // ============================================================================
  const STORAGE_ENDPOINT_KEY = "smart_parking_api_endpoint";
  const STORAGE_VEHICLES_KEY = "smart_parking_active_vehicles";
  const DEFAULT_API_ENDPOINT = "https://fdbsdxyto1.execute-api.us-east-1.amazonaws.com/dev";

  let apiBaseUrl = localStorage.getItem(STORAGE_ENDPOINT_KEY) || DEFAULT_API_ENDPOINT;
  let activeVehicles = [];

  try {
    const saved = localStorage.getItem(STORAGE_VEHICLES_KEY);
    activeVehicles = saved ? JSON.parse(saved) : [];
  } catch (err) {
    console.warn("Lỗi đọc activeVehicles từ localStorage:", err);
    activeVehicles = [];
  }

  let checkinBase64 = null;
  let checkoutBase64 = null;
  let lastTicketId = null;

  // DOM Elements - Header & Clock
  const digitalClockTime = document.getElementById("digitalClockTime");
  const digitalClockDate = document.getElementById("digitalClockDate");
  const activeVehiclesCount = document.getElementById("activeVehiclesCount");
  const tableVehiclesBadge = document.getElementById("tableVehiclesBadge");

  // DOM Elements - Check-in Lane
  const checkinForm = document.getElementById("checkinForm");
  const checkinFileInput = document.getElementById("checkinFileInput");
  const checkinPlaceholder = document.getElementById("checkinPlaceholder");
  const checkinPreview = document.getElementById("checkinPreview");
  const checkinSubmitBtn = document.getElementById("checkinSubmitBtn");
  const checkinSpinner = document.getElementById("checkinSpinner");
  const resetCheckinBtn = document.getElementById("resetCheckinBtn");
  const checkinResult = document.getElementById("checkinResult");
  const resCheckinPlate = document.getElementById("resCheckinPlate");
  const resTicketId = document.getElementById("resTicketId");
  const resVehicleType = document.getElementById("resVehicleType");
  const resCheckinTime = document.getElementById("resCheckinTime");
  const unknownNotice = document.getElementById("unknownNotice");
  const labelMotor = document.getElementById("labelMotor");
  const labelCar = document.getElementById("labelCar");

  // DOM Elements - Check-out Lane
  const checkoutForm = document.getElementById("checkoutForm");
  const checkoutTicketInput = document.getElementById("checkoutTicketInput");
  const pasteLastTicketBtn = document.getElementById("pasteLastTicketBtn");
  const checkoutFileInput = document.getElementById("checkoutFileInput");
  const checkoutPlaceholder = document.getElementById("checkoutPlaceholder");
  const checkoutPreview = document.getElementById("checkoutPreview");
  const checkoutSubmitBtn = document.getElementById("checkoutSubmitBtn");
  const checkoutSpinner = document.getElementById("checkoutSpinner");
  const resetCheckoutBtn = document.getElementById("resetCheckoutBtn");
  const checkoutResult = document.getElementById("checkoutResult");
  const resCheckoutPlate = document.getElementById("resCheckoutPlate");
  const resCheckoutHours = document.getElementById("resCheckoutHours");
  const resCheckoutFee = document.getElementById("resCheckoutFee");
  const resCheckoutTime = document.getElementById("resCheckoutTime");
  const resCheckoutCheckinTime = document.getElementById("resCheckoutCheckinTime");
  const resolvedPlateHint = document.getElementById("resolvedPlateHint");

  // DOM Elements - Active Vehicles Table
  const activeVehiclesTableBody = document.getElementById("activeVehiclesTableBody");
  const filterVehicleInput = document.getElementById("filterVehicleInput");
  const clearAllVehiclesBtn = document.getElementById("clearAllVehiclesBtn");

  // DOM Elements - Settings Modal & Toast
  const openSettingsBtn = document.getElementById("openSettingsBtn");
  const closeSettingsBtn = document.getElementById("closeSettingsBtn");
  const settingsModal = document.getElementById("settingsModal");
  const apiEndpointInput = document.getElementById("apiEndpointInput");
  const saveEndpointBtn = document.getElementById("saveEndpointBtn");
  const resetEndpointBtn = document.getElementById("resetEndpointBtn");
  const toast = document.getElementById("toastNotification");

  // ============================================================================
  // 2. HELPER UTILITIES & REGEX FILTERS
  // ============================================================================

  /**
   * Cắt chuỗi rác camera an ninh & chuẩn hóa biển số Việt Nam
   */
  function extractCleanPlate(rawText) {
    if (!rawText || rawText === "UNKNOWN") return "UNKNOWN";
    const clean = rawText.replace(/[^A-Z0-9]/gi, "").toUpperCase();
    const match = clean.match(/^([0-9]{2}[A-Z]{1,2}[0-9]{4,5})/);
    if (match) return match[1];
    return clean.substring(0, 10);
  }

  /**
   * Nhận diện ô tìm kiếm thông minh: Cho phép nhập Biển số HOẶC UUID
   */
  function resolveTicketId(inputValue) {
    if (!inputValue) return "";
    const trimmed = inputValue.trim();
    const uuidRegex = /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/;
    if (uuidRegex.test(trimmed)) return trimmed;

    // Tìm trong danh sách xe đang trong bãi theo biển số
    const cleanSearch = trimmed.replace(/[^A-Z0-9]/gi, "").toUpperCase();
    const found = activeVehicles.find((v) => {
      const vPlate = (v.plateNumber || "").replace(/[^A-Z0-9]/gi, "").toUpperCase();
      return vPlate === cleanSearch || (cleanSearch.length >= 4 && vPlate.includes(cleanSearch));
    });

    if (found) {
      return found.ticketId;
    }
    return trimmed;
  }

  function showToast(message, type = "success") {
    toast.textContent = message;
    toast.className = `pos-toast toast-${type}`;
    toast.classList.remove("hidden");
    setTimeout(() => {
      toast.classList.add("hidden");
    }, 4500);
  }

  function formatDateTime(isoString) {
    if (!isoString) return "--";
    try {
      const dt = new Date(isoString);
      return dt.toLocaleString("vi-VN", {
        timeZone: "Asia/Ho_Chi_Minh",
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
      });
    } catch {
      return isoString;
    }
  }

  function calculateParkedDuration(checkinIso) {
    if (!checkinIso) return "--";
    try {
      const checkinDt = new Date(checkinIso);
      const now = new Date();
      const diffMs = Math.max(0, now - checkinDt);
      const diffMinutes = Math.floor(diffMs / (1000 * 60));
      const hours = Math.floor(diffMinutes / 60);
      const minutes = diffMinutes % 60;
      if (hours === 0) return `${minutes} phút`;
      return `${hours} giờ ${minutes} phút`;
    } catch {
      return "--";
    }
  }

  function formatCurrency(amount) {
    const num = Number(amount) || 0;
    return num.toLocaleString("vi-VN") + " VNĐ";
  }

  function convertFileToBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = (err) => reject(err);
      reader.readAsDataURL(file);
    });
  }

  // ============================================================================
  // 3. FORM RESET & CAMERA VIEWPORT HANDLERS (KHÔNG BAO GIỜ BỊ ĐƠ ẢNH)
  // ============================================================================
  function resetCheckinForm(clearResults = false) {
    checkinFileInput.value = "";
    checkinBase64 = null;
    checkinPreview.src = "";
    checkinPreview.classList.add("hidden");
    checkinPlaceholder.classList.remove("hidden");
    if (clearResults) {
      checkinResult.classList.add("hidden");
    }
  }

  function resetCheckoutForm(clearResults = false) {
    checkoutTicketInput.value = "";
    checkoutFileInput.value = "";
    checkoutBase64 = null;
    checkoutPreview.src = "";
    checkoutPreview.classList.add("hidden");
    checkoutPlaceholder.classList.remove("hidden");
    resolvedPlateHint.classList.add("hidden");
    resolvedPlateHint.textContent = "";
    if (clearResults) {
      checkoutResult.classList.add("hidden");
    }
  }

  resetCheckinBtn.addEventListener("click", () => {
    resetCheckinForm(true);
    showToast("Đã làm mới form Làn Vào!", "success");
  });

  resetCheckoutBtn.addEventListener("click", () => {
    resetCheckoutForm(true);
    showToast("Đã làm mới form Làn Ra!", "success");
  });

  // Handle file uploads
  checkinFileInput.addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (file.size > 5 * 1024 * 1024) {
      showToast("Kích thước ảnh vượt quá 5MB. Vui lòng chọn ảnh nhỏ hơn!", "error");
      checkinFileInput.value = "";
      return;
    }

    try {
      checkinBase64 = await convertFileToBase64(file);
      checkinPreview.src = checkinBase64;
      checkinPreview.classList.remove("hidden");
      checkinPlaceholder.classList.add("hidden");
    } catch (err) {
      showToast("Lỗi khi đọc file ảnh: " + err.message, "error");
    }
  });

  checkoutFileInput.addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (file.size > 5 * 1024 * 1024) {
      showToast("Kích thước ảnh vượt quá 5MB. Vui lòng chọn ảnh nhỏ hơn!", "error");
      checkoutFileInput.value = "";
      return;
    }

    try {
      checkoutBase64 = await convertFileToBase64(file);
      checkoutPreview.src = checkoutBase64;
      checkoutPreview.classList.remove("hidden");
      checkoutPlaceholder.classList.add("hidden");
    } catch (err) {
      showToast("Lỗi khi đọc file ảnh: " + err.message, "error");
    }
  });

  // Radio button styling
  document.querySelectorAll('input[name="vehicleType"]').forEach((radio) => {
    radio.addEventListener("change", (e) => {
      if (e.target.value === "MOTORBIKE") {
        labelMotor.classList.add("active");
        labelCar.classList.remove("active");
      } else {
        labelCar.classList.add("active");
        labelMotor.classList.remove("active");
      }
    });
  });

  // Real-time plate resolver hint on typing
  checkoutTicketInput.addEventListener("input", (e) => {
    const val = e.target.value.trim();
    if (!val) {
      resolvedPlateHint.classList.add("hidden");
      return;
    }

    const uuidRegex = /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/;
    if (uuidRegex.test(val)) {
      const matchVehicle = activeVehicles.find((v) => v.ticketId === val);
      if (matchVehicle) {
        resolvedPlateHint.textContent = `✓ Khớp mã vé: Biển số ${matchVehicle.plateNumber} (${matchVehicle.vehicleType === "MOTORBIKE" ? "Xe máy" : "Ô tô"})`;
        resolvedPlateHint.classList.remove("hidden");
      } else {
        resolvedPlateHint.classList.add("hidden");
      }
    } else {
      const clean = val.replace(/[^A-Z0-9]/gi, "").toUpperCase();
      const matchVehicle = activeVehicles.find((v) => {
        const p = (v.plateNumber || "").replace(/[^A-Z0-9]/gi, "").toUpperCase();
        return p === clean || (clean.length >= 3 && p.includes(clean));
      });

      if (matchVehicle) {
        resolvedPlateHint.textContent = `✓ Đã nhận diện xe trong bãi: ${matchVehicle.plateNumber} (Vé: ${matchVehicle.ticketId.substring(0, 8)}...)`;
        resolvedPlateHint.classList.remove("hidden");
      } else {
        resolvedPlateHint.classList.add("hidden");
      }
    }
  });

  pasteLastTicketBtn.addEventListener("click", () => {
    if (lastTicketId) {
      checkoutTicketInput.value = lastTicketId;
      checkoutTicketInput.dispatchEvent(new Event("input"));
      showToast("Đã dán mã vé vừa tạo!");
    } else {
      showToast("Chưa có vé nào được tạo trong phiên này!", "error");
    }
  });

  // ============================================================================
  // 4. ACTIVE VEHICLES TABLE RENDERING & PERSISTENCE
  // ============================================================================
  function saveActiveVehicles() {
    try {
      localStorage.setItem(STORAGE_VEHICLES_KEY, JSON.stringify(activeVehicles));
    } catch (e) {
      console.warn("Lỗi lưu activeVehicles vào localStorage:", e);
    }
    updateVehiclesCountBadge();
  }

  function updateVehiclesCountBadge() {
    const count = activeVehicles.length;
    activeVehiclesCount.textContent = count;
    tableVehiclesBadge.textContent = `${count} xe`;
  }

  function renderActiveVehiclesTable(filterQuery = "") {
    const query = filterQuery.trim().toLowerCase();
    const filtered = activeVehicles.filter((v) => {
      if (!query) return true;
      const plate = (v.plateNumber || "").toLowerCase();
      const ticket = (v.ticketId || "").toLowerCase();
      return plate.includes(query) || ticket.includes(query);
    });

    if (filtered.length === 0) {
      activeVehiclesTableBody.innerHTML = `
        <tr class="empty-row">
          <td colspan="7">
            ${query ? "Không tìm thấy xe nào phù hợp với bộ lọc." : "Hiện chưa có xe nào trong bãi. Vui lòng thực hiện Check-in ở Làn 1."}
          </td>
        </tr>
      `;
      return;
    }

    activeVehiclesTableBody.innerHTML = filtered.map((v, index) => {
      const plateDisplay = v.plateNumber === "UNKNOWN"
        ? `<span class="table-plate-badge" style="background:#fee2e2;color:#991b1b;border-color:#fca5a5;">UNKNOWN</span>`
        : `<span class="table-plate-badge">${v.plateNumber}</span>`;

      const typeLabel = v.vehicleType === "MOTORBIKE" ? "Xe máy" : "Ô tô";
      const parkedDuration = calculateParkedDuration(v.checkinTime);

      return `
        <tr>
          <td><strong>${index + 1}</strong></td>
          <td>${plateDisplay}</td>
          <td>${typeLabel}</td>
          <td>${formatDateTime(v.checkinTime)}</td>
          <td><strong>${parkedDuration}</strong></td>
          <td><code class="mono" title="${v.ticketId}">${v.ticketId.substring(0, 13)}...</code></td>
          <td style="text-align: center;">
            <button class="btn-row-checkout" data-ticket="${v.ticketId}" data-plate="${v.plateNumber}">
              ➔ Cho Xe Ra
            </button>
          </td>
        </tr>
      `;
    }).join("");

    // Attach 1-click checkout click listeners
    activeVehiclesTableBody.querySelectorAll(".btn-row-checkout").forEach((btn) => {
      btn.addEventListener("click", () => {
        const tId = btn.getAttribute("data-ticket");
        const pNum = btn.getAttribute("data-plate");
        checkoutTicketInput.value = tId;
        checkoutTicketInput.dispatchEvent(new Event("input"));
        checkoutTicketInput.focus();
        showToast(`Đã nạp xe [${pNum}] vào Làn Ra. Nhấn "TÍNH CƯỚC & CHO XE RA" để hoàn tất!`);
        window.scrollTo({ top: 0, behavior: "smooth" });
      });
    });
  }

  filterVehicleInput.addEventListener("input", (e) => {
    renderActiveVehiclesTable(e.target.value);
  });

  clearAllVehiclesBtn.addEventListener("click", () => {
    if (confirm("Bạn có chắc chắn muốn dọn sạch danh sách xe trong bộ nhớ tạm trình duyệt?")) {
      activeVehicles = [];
      saveActiveVehicles();
      renderActiveVehiclesTable();
      showToast("Đã dọn sạch danh sách xe!");
    }
  });

  // ============================================================================
  // 5. SUBMIT CHECK-IN (XE VÀO)
  // ============================================================================
  checkinForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (!checkinBase64) {
      showToast("Vui lòng chụp hoặc chọn ảnh xe vào làn trước khi cấp vé!", "error");
      return;
    }

    const vehicleType = document.querySelector('input[name="vehicleType"]:checked').value;
    const url = `${apiBaseUrl}/checkin`;

    checkinSubmitBtn.disabled = true;
    checkinSpinner.classList.remove("hidden");

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          image: checkinBase64,
          vehicleType: vehicleType
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `HTTP ${response.status}: Lỗi máy chủ tiếp nhận`);
      }

      // Xử lý làm sạch biển số
      const rawPlate = data.plateNumber || "UNKNOWN";
      const cleanPlate = extractCleanPlate(rawPlate);

      lastTicketId = data.ticketId;
      resCheckinPlate.textContent = cleanPlate;
      resTicketId.textContent = data.ticketId;
      resVehicleType.textContent = data.vehicleType === "MOTORBIKE" ? "Xe máy (MOTORBIKE)" : "Ô tô (CAR)";
      resCheckinTime.textContent = formatDateTime(data.checkinTime);

      if (cleanPlate === "UNKNOWN") {
        unknownNotice.classList.remove("hidden");
        showToast("Cấp vé thành công! (Ảnh mờ - Cần bảo vệ đối chiếu)", "success");
      } else {
        unknownNotice.classList.add("hidden");
        showToast(`Cấp vé thành công! Biển số: ${cleanPlate}`);
      }

      checkinResult.classList.remove("hidden");

      // Cập nhật State danh sách xe đang trong bãi
      const newVehicle = {
        ticketId: data.ticketId,
        plateNumber: cleanPlate,
        rawPlate: rawPlate,
        vehicleType: data.vehicleType,
        checkinTime: data.checkinTime,
        status: "PARKED"
      };

      activeVehicles.unshift(newVehicle);
      saveActiveVehicles();
      renderActiveVehiclesTable(filterVehicleInput.value);

      // Reset camera viewport để sẵn sàng chụp xe kế tiếp (không bị đơ ảnh)
      resetCheckinForm(false);

    } catch (err) {
      showToast(`Lỗi Check-in: ${err.message}`, "error");
    } finally {
      checkinSubmitBtn.disabled = false;
      checkinSpinner.classList.add("hidden");
    }
  });

  // ============================================================================
  // 6. SUBMIT CHECK-OUT (XE RA & TÍNH TIỀN)
  // ============================================================================
  checkoutForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const rawInput = checkoutTicketInput.value.trim();
    if (!rawInput) {
      showToast("Vui lòng nhập biển số xe hoặc mã vé cần thanh toán!", "error");
      return;
    }

    // Nhận diện mã vé thông minh
    const ticketId = resolveTicketId(rawInput);
    const url = `${apiBaseUrl}/checkout`;
    const payload = { ticketId: ticketId };
    if (checkoutBase64) {
      payload.image = checkoutBase64;
    }

    checkoutSubmitBtn.disabled = true;
    checkoutSpinner.classList.remove("hidden");

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (!response.ok) {
        if (response.status === 400) {
          throw new Error(data.error || "Vé này đã được thanh toán và hoàn tất trước đó!");
        } else if (response.status === 404) {
          throw new Error(`Không tìm thấy mã vé trong hệ thống: ${ticketId}`);
        } else {
          throw new Error(data.error || `HTTP ${response.status}: Lỗi đối soát cước`);
        }
      }

      // Xử lý hiển thị kết quả thu cước
      const cleanPlate = extractCleanPlate(data.plateNumber);
      resCheckoutFee.textContent = formatCurrency(data.fee);
      resCheckoutPlate.textContent = cleanPlate || "UNKNOWN";
      resCheckoutHours.textContent = `${data.totalHours || 1} giờ`;
      resCheckoutCheckinTime.textContent = formatDateTime(data.checkinTime);
      resCheckoutTime.textContent = formatDateTime(data.checkoutTime);

      checkoutResult.classList.remove("hidden");
      showToast(`Thanh toán hoàn tất! Cước: ${formatCurrency(data.fee)} &bull; Mở Barie`);

      // Xóa xe khỏi danh sách đang trong bãi
      activeVehicles = activeVehicles.filter((v) => v.ticketId !== ticketId);
      saveActiveVehicles();
      renderActiveVehiclesTable(filterVehicleInput.value);

      // Reset camera form xe ra để đón xe tiếp theo
      resetCheckoutForm(false);

    } catch (err) {
      showToast(`Lỗi Check-out: ${err.message}`, "error");
    } finally {
      checkoutSubmitBtn.disabled = false;
      checkoutSpinner.classList.add("hidden");
    }
  });

  // ============================================================================
  // 7. SETTINGS MODAL & CLOCK INITIALIZATION
  // ============================================================================
  function updateDigitalClock() {
    const now = new Date();
    digitalClockTime.textContent = now.toLocaleTimeString("vi-VN", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: false
    });
    digitalClockDate.textContent = now.toLocaleDateString("vi-VN", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric"
    });
  }

  setInterval(updateDigitalClock, 1000);
  updateDigitalClock();

  // Settings modal handlers
  openSettingsBtn.addEventListener("click", () => {
    apiEndpointInput.value = apiBaseUrl;
    settingsModal.classList.remove("hidden");
  });

  closeSettingsBtn.addEventListener("click", () => {
    settingsModal.classList.add("hidden");
  });

  saveEndpointBtn.addEventListener("click", () => {
    const val = apiEndpointInput.value.trim().replace(/\/+$/, "");
    if (!val.startsWith("http")) {
      showToast("URL API không hợp lệ! Phải bắt đầu bằng https://", "error");
      return;
    }
    apiBaseUrl = val;
    localStorage.setItem(STORAGE_ENDPOINT_KEY, apiBaseUrl);
    settingsModal.classList.add("hidden");
    showToast("Đã lưu cấu hình API Endpoint mới!");
  });

  resetEndpointBtn.addEventListener("click", () => {
    apiBaseUrl = DEFAULT_API_ENDPOINT;
    apiEndpointInput.value = DEFAULT_API_ENDPOINT;
    localStorage.removeItem(STORAGE_ENDPOINT_KEY);
    showToast("Đã khôi phục URL API mặc định!");
  });

  // Initial table render
  updateVehiclesCountBadge();
  renderActiveVehiclesTable();
});

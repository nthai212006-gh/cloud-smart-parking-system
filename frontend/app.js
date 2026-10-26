/**
 * SMART PARKING DASHBOARD - FRONTEND JAVASCRIPT
 * Tích hợp trực tiếp Amazon API Gateway REST API (/checkin, /checkout)
 * Sinh viên: Lê Cao Việt Tín (24110354) · GVHD: ThS. Huỳnh Xuân Phụng
 */

document.addEventListener("DOMContentLoaded", () => {
  // ============================================================================
  // 1. STATE & CONFIGURATION
  // ============================================================================
  const STORAGE_KEY = "smart_parking_api_endpoint";
  const defaultEndpoint = "https://fdbsdxyto1.execute-api.us-east-1.amazonaws.com/dev";
  let apiBaseUrl = localStorage.getItem(STORAGE_KEY) || defaultEndpoint;

  let checkinBase64 = null;
  let checkoutBase64 = null;
  let lastTicketId = null;

  // DOM Elements - Config
  const apiEndpointInput = document.getElementById("apiEndpointInput");
  const saveEndpointBtn = document.getElementById("saveEndpointBtn");
  const toggleConfigBtn = document.getElementById("toggleConfigBtn");
  const configBody = document.getElementById("configBody");

  // DOM Elements - Check-in
  const checkinForm = document.getElementById("checkinForm");
  const checkinFileInput = document.getElementById("checkinFileInput");
  const checkinPlaceholder = document.getElementById("checkinPlaceholder");
  const checkinPreview = document.getElementById("checkinPreview");
  const checkinSubmitBtn = document.getElementById("checkinSubmitBtn");
  const checkinSpinner = document.getElementById("checkinSpinner");
  const checkinResult = document.getElementById("checkinResult");
  const resCheckinPlate = document.getElementById("resCheckinPlate");
  const resTicketId = document.getElementById("resTicketId");
  const resVehicleType = document.getElementById("resVehicleType");
  const resCheckinTime = document.getElementById("resCheckinTime");
  const unknownNotice = document.getElementById("unknownNotice");
  const copyTicketBtn = document.getElementById("copyTicketBtn");

  // DOM Elements - Radio cards
  const labelMotor = document.getElementById("labelMotor");
  const labelCar = document.getElementById("labelCar");

  // DOM Elements - Check-out
  const checkoutForm = document.getElementById("checkoutForm");
  const checkoutTicketInput = document.getElementById("checkoutTicketInput");
  const pasteLastTicketBtn = document.getElementById("pasteLastTicketBtn");
  const checkoutFileInput = document.getElementById("checkoutFileInput");
  const checkoutPlaceholder = document.getElementById("checkoutPlaceholder");
  const checkoutPreview = document.getElementById("checkoutPreview");
  const checkoutSubmitBtn = document.getElementById("checkoutSubmitBtn");
  const checkoutSpinner = document.getElementById("checkoutSpinner");
  const checkoutResult = document.getElementById("checkoutResult");
  const resCheckoutPlate = document.getElementById("resCheckoutPlate");
  const resCheckoutHours = document.getElementById("resCheckoutHours");
  const resCheckoutFee = document.getElementById("resCheckoutFee");
  const resCheckoutTime = document.getElementById("resCheckoutTime");
  const resCheckoutCheckinTime = document.getElementById("resCheckoutCheckinTime");

  const toast = document.getElementById("toastNotification");

  // Khởi tạo giá trị input endpoint
  apiEndpointInput.value = apiBaseUrl;

  // ============================================================================
  // 2. HELPER FUNCTIONS
  // ============================================================================
  function showToast(message, type = "success") {
    toast.textContent = message;
    toast.className = `toast toast-${type}`;
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
  // 3. EVENT LISTENERS - CONFIGURATION
  // ============================================================================
  toggleConfigBtn.addEventListener("click", () => {
    configBody.classList.toggle("hidden");
  });

  saveEndpointBtn.addEventListener("click", () => {
    const val = apiEndpointInput.value.trim().replace(/\/+$/, "");
    if (!val.startsWith("http")) {
      showToast("URL Endpoint không hợp lệ! Phải bắt đầu bằng https://", "error");
      return;
    }
    apiBaseUrl = val;
    localStorage.setItem(STORAGE_KEY, apiBaseUrl);
    showToast("Đã lưu API Gateway Endpoint mới thành công!");
  });

  // Radio card select styling
  document.querySelectorAll('input[name="vehicleType"]').forEach((radio) => {
    radio.addEventListener("change", (e) => {
      if (e.target.value === "MOTORBIKE") {
        labelMotor.classList.add("selected");
        labelCar.classList.remove("selected");
      } else {
        labelCar.classList.add("selected");
        labelMotor.classList.remove("selected");
      }
    });
  });

  // ============================================================================
  // 4. IMAGE UPLOAD & PREVIEW
  // ============================================================================
  checkinFileInput.addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (file.size > 5 * 1024 * 1024) {
      showToast("File ảnh vượt quá 5MB. Vui lòng chọn ảnh nhỏ hơn!", "error");
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
      showToast("File ảnh vượt quá 5MB. Vui lòng chọn ảnh nhỏ hơn!", "error");
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

  // Copy Ticket ID
  copyTicketBtn.addEventListener("click", () => {
    if (lastTicketId) {
      navigator.clipboard.writeText(lastTicketId).then(() => {
        showToast("Đã sao chép mã vé vào bộ nhớ tạm!");
      });
    }
  });

  // Paste last ticket to checkout
  pasteLastTicketBtn.addEventListener("click", () => {
    if (lastTicketId) {
      checkoutTicketInput.value = lastTicketId;
      showToast("Đã dán mã vé vừa tạo!");
    } else {
      showToast("Chưa có vé nào được tạo trong phiên này!", "error");
    }
  });

  // ============================================================================
  // 5. SUBMIT CHECK-IN (XE VÀO)
  // ============================================================================
  checkinForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (!checkinBase64) {
      showToast("Vui lòng tải lên ảnh xe vào bãi trước khi tạo vé!", "error");
      return;
    }

    const vehicleType = document.querySelector('input[name="vehicleType"]:checked').value;
    const url = `${apiBaseUrl}/checkin`;

    // UI Loading state
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
        throw new Error(data.error || `HTTP ${response.status}: Lỗi máy chủ`);
      }

      // Xử lý dữ liệu trả về thành công
      lastTicketId = data.ticketId;
      resCheckinPlate.textContent = data.plateNumber || "UNKNOWN";
      resTicketId.textContent = data.ticketId;
      resVehicleType.textContent = data.vehicleType === "MOTORBIKE" ? "Xe máy (MOTORBIKE)" : "Ô tô (CAR)";
      resCheckinTime.textContent = formatDateTime(data.checkinTime);

      if (data.plateNumber === "UNKNOWN") {
        unknownNotice.classList.remove("hidden");
        showToast("Tạo vé thành công (Ảnh mờ - Biển số UNKNOWN)!", "success");
      } else {
        unknownNotice.classList.add("hidden");
        showToast(`Tạo vé thành công! Biển số: ${data.plateNumber}`);
      }

      // Hiển thị khung kết quả
      checkinResult.classList.remove("hidden");

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

    const ticketId = checkoutTicketInput.value.trim();
    if (!ticketId) {
      showToast("Vui lòng nhập mã vé xe cần thanh toán!", "error");
      return;
    }

    const url = `${apiBaseUrl}/checkout`;
    const payload = { ticketId: ticketId };
    if (checkoutBase64) {
      payload.image = checkoutBase64;
    }

    // UI Loading state
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
          throw new Error("Vé này đã được thanh toán và hoàn tất trước đó!");
        } else if (response.status === 404) {
          throw new Error(`Không tìm thấy mã vé: ${ticketId}`);
        } else {
          throw new Error(data.error || `HTTP ${response.status}: Lỗi thanh toán`);
        }
      }

      // Cập nhật kết quả thanh toán
      resCheckoutFee.textContent = formatCurrency(data.fee);
      resCheckoutPlate.textContent = data.plateNumber || "UNKNOWN";
      resCheckoutHours.textContent = `${data.totalHours || 1} giờ`;
      resCheckoutCheckinTime.textContent = formatDateTime(data.checkinTime);
      resCheckoutTime.textContent = formatDateTime(data.checkoutTime);

      checkoutResult.classList.remove("hidden");
      showToast(`Thanh toán thành công! Tiền cước: ${formatCurrency(data.fee)}`);

    } catch (err) {
      showToast(`Lỗi Check-out: ${err.message}`, "error");
    } finally {
      checkoutSubmitBtn.disabled = false;
      checkoutSpinner.classList.add("hidden");
    }
  });
});

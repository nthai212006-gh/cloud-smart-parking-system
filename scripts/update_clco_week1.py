import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def update_clco_report():
    file_path = r"c:\Users\T14 GEN2\Documents\cloud-smart-parking-system\CLCO_WEEK1.docx"
    doc = Document(file_path)

    # 1. CẬP NHẬT TABLE 0 (Bảng thông tin đề tài đầu tiên)
    tbl0 = doc.tables[0]
    for row in tbl0.rows:
        if "github" in row.cells[0].text.lower():
            row.cells[1].text = (
                "https://github.com/nthai212006-gh/cloud-smart-parking-system\n"
                "(Nhánh dev - Chi tiết link commit và file cụ thể xem tại Mục 2 và Mục 7)"
            )
            for p in row.cells[1].paragraphs:
                for r in p.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(10)
                    r.font.color.rgb = RGBColor(0, 102, 204)

    # 2. CẬP NHẬT BẢNG PHÂN CÔNG CÔNG VIỆC (Tìm bảng theo tiêu đề cột)
    tbl_task = None
    for t in doc.tables:
        if len(t.rows) > 0 and "thành viên thực hiện" in t.rows[0].cells[0].text.lower():
            tbl_task = t
            break

    if tbl_task:
        print("Found task table!")
        # Ô của Lê Cao Việt Tín (row 1, col 1)
        cell_tin = tbl_task.rows[1].cells[1]
        cell_tin.text = (
            "• Nhiệm vụ: Nghiên cứu AWS Rekognition; Viết thuật toán Regex bóc tách biển số; "
            "Thiết kế kiến trúc Serverless; Viết code Lambda checkin/checkout; Cấu hình API Gateway OpenAPI spec.\n\n"
            "• Minh chứng Commit cụ thể:\n"
            "  Commit cb85da8: https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/cb85da8\n\n"
            "• Minh chứng File mã nguồn trực tiếp (blob):\n"
            "  - checkin.py: https://github.com/nthai212006-gh/cloud-smart-parking-system/blob/dev/backend/checkin.py\n"
            "  - checkout.py: https://github.com/nthai212006-gh/cloud-smart-parking-system/blob/dev/backend/checkout.py\n"
            "  - test_plate_regex.py: https://github.com/nthai212006-gh/cloud-smart-parking-system/blob/dev/scripts/test_plate_regex.py\n"
            "  - Tài liệu kiến trúc: https://github.com/nthai212006-gh/cloud-smart-parking-system/blob/dev/docs/THIET_KE_KIEN_TRUC_HE_THONG.md"
        )
        for p in cell_tin.paragraphs:
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8.5)
                if "http" in r.text:
                    r.font.color.rgb = RGBColor(0, 102, 204)

        # Ô của Nguyễn Trung Hải (row 2, col 1)
        cell_hai = tbl_task.rows[2].cells[1]
        cell_hai.text = (
            "• Nhiệm vụ: Khởi tạo hạ tầng S3 & DynamoDB trên Learner Lab; Thiết lập chuẩn Tagging; "
            "Thu thập và xử lý 120 ảnh test (che mờ PII mặt người); Viết script tự động hóa; Chụp minh chứng console.\n\n"
            "• Minh chứng Commit cụ thể:\n"
            "  - Commit 41ec17b (Script setup S3/DynamoDB): https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/41ec17b\n"
            "  - Commit a2d46cd (Bộ 120 ảnh test dataset): https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/a2d46cd\n"
            "  - Commit 6c5728a (API Gateway OpenAPI spec): https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/6c5728a\n"
            "  - Commit b43ca19 (Minh chứng console AWS): https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/b43ca19\n\n"
            "• Minh chứng File / Thư mục mã nguồn trực tiếp (blob):\n"
            "  - setup_aws_resources.py: https://github.com/nthai212006-gh/cloud-smart-parking-system/blob/dev/scripts/setup_aws_resources.py\n"
            "  - api_gateway_openapi.json: https://github.com/nthai212006-gh/cloud-smart-parking-system/blob/dev/backend/api_gateway_openapi.json\n"
            "  - Thư mục test-images/: https://github.com/nthai212006-gh/cloud-smart-parking-system/tree/dev/test-images\n"
            "  - Thư mục evidence/week1/: https://github.com/nthai212006-gh/cloud-smart-parking-system/tree/dev/evidence/week1"
        )
        for p in cell_hai.paragraphs:
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8.5)
                if "http" in r.text:
                    r.font.color.rgb = RGBColor(0, 102, 204)
    else:
        print("Warning: task table not found!")

    # 3. BỔ SUNG BẢNG LINK CHI TIẾT VÀO MỤC 2
    # Tìm Table 1 (cây thư mục)
    tbl_tree = None
    for t in doc.tables:
        if len(t.rows) > 0 and "cloud-smart-parking-system" in t.rows[0].cells[0].text:
            tbl_tree = t
            break

    # Đoạn văn giới thiệu bảng
    new_p = doc.add_paragraph()
    new_p.paragraph_format.space_before = Pt(14)
    new_p.paragraph_format.space_after = Pt(6)
    r_title = new_p.add_run("Bảng tổng hợp liên kết trực tiếp (Direct Blob Links) và Commit minh chứng cụ thể trên GitHub:")
    r_title.bold = True
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(11)
    r_title.font.color.rgb = RGBColor(16, 74, 150)

    # Chèn bảng liên kết
    link_data = [
        (
            "1",
            "Lambda Check-in Core\n(Nhận diện biển số, tạo ticket)",
            "Lê Cao Việt Tín\n(25110159)",
            "Commit cb85da8:\nhttps://github.com/nthai212006-gh/cloud-smart-parking-system/commit/cb85da8",
            "backend/checkin.py:\nhttps://github.com/nthai212006-gh/cloud-smart-parking-system/blob/dev/backend/checkin.py"
        ),
        (
            "2",
            "Lambda Check-out Core\n(Xử lý xe ra, tính phí theo block)",
            "Lê Cao Việt Tín\n(25110159)",
            "Commit cb85da8:\nhttps://github.com/nthai212006-gh/cloud-smart-parking-system/commit/cb85da8",
            "backend/checkout.py:\nhttps://github.com/nthai212006-gh/cloud-smart-parking-system/blob/dev/backend/checkout.py"
        ),
        (
            "3",
            "Thiết kế Kiến trúc Serverless\n(Tài liệu kiến trúc hệ thống)",
            "Lê Cao Việt Tín\n(25110159)",
            "Commit cb85da8:\nhttps://github.com/nthai212006-gh/cloud-smart-parking-system/commit/cb85da8",
            "docs/THIET_KE_KIEN_TRUC_HE_THONG.md:\nhttps://github.com/nthai212006-gh/cloud-smart-parking-system/blob/dev/docs/THIET_KE_KIEN_TRUC_HE_THONG.md"
        ),
        (
            "4",
            "Kiểm thử Regex Biển số VN\n(Bộ regex OCR biển số xe)",
            "Lê Cao Việt Tín\n(25110159)",
            "Commit cb85da8:\nhttps://github.com/nthai212006-gh/cloud-smart-parking-system/commit/cb85da8",
            "scripts/test_plate_regex.py:\nhttps://github.com/nthai212006-gh/cloud-smart-parking-system/blob/dev/scripts/test_plate_regex.py"
        ),
        (
            "5",
            "Khởi tạo Hạ tầng S3 & DynamoDB\n(Script tự động hóa cấu hình)",
            "Nguyễn Trung Hải\n(24110207)",
            "Commit 41ec17b:\nhttps://github.com/nthai212006-gh/cloud-smart-parking-system/commit/41ec17b",
            "scripts/setup_aws_resources.py:\nhttps://github.com/nthai212006-gh/cloud-smart-parking-system/blob/dev/scripts/setup_aws_resources.py"
        ),
        (
            "6",
            "Bộ 120 ảnh test che mờ PII\n(Thu thập, tiền xử lý & bảo mật)",
            "Nguyễn Trung Hải\n(24110207)",
            "Commit a2d46cd:\nhttps://github.com/nthai212006-gh/cloud-smart-parking-system/commit/a2d46cd",
            "Thư mục test-images/:\nhttps://github.com/nthai212006-gh/cloud-smart-parking-system/tree/dev/test-images"
        ),
        (
            "7",
            "Đặc tả REST API Gateway\n(OpenAPI 3.0 / Swagger spec)",
            "Nguyễn Trung Hải\n(24110207)",
            "Commit 6c5728a:\nhttps://github.com/nthai212006-gh/cloud-smart-parking-system/commit/6c5728a",
            "backend/api_gateway_openapi.json:\nhttps://github.com/nthai212006-gh/cloud-smart-parking-system/blob/dev/backend/api_gateway_openapi.json"
        ),
        (
            "8",
            "Minh chứng AWS Console & Cost\n(Ảnh chụp S3, DynamoDB, Billing)",
            "Nguyễn Trung Hải\n(24110207)",
            "Commit b43ca19:\nhttps://github.com/nthai212006-gh/cloud-smart-parking-system/commit/b43ca19",
            "Thư mục evidence/week1/:\nhttps://github.com/nthai212006-gh/cloud-smart-parking-system/tree/dev/evidence/week1"
        )
    ]

    new_tbl = doc.add_table(rows=len(link_data) + 1, cols=5)
    new_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    new_tbl.autofit = False

    headers = ["STT", "Hạng mục / Chức năng kỹ thuật", "Thành viên phụ trách", "Minh chứng Commit cụ thể", "Minh chứng File mã nguồn (blob)"]
    header_widths = [Inches(0.4), Inches(1.8), Inches(1.2), Inches(1.6), Inches(1.8)]

    # Format header row
    hdr_row = new_tbl.rows[0]
    for j, h in enumerate(headers):
        c = hdr_row.cells[j]
        c.width = header_widths[j]
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(c, "104A96")
        set_cell_margins(c, 80, 80, 80, 80)

    # Format data rows
    for i, row_data in enumerate(link_data):
        row = new_tbl.rows[i + 1]
        for j, val in enumerate(row_data):
            c = row.cells[j]
            c.width = header_widths[j]
            p = c.paragraphs[0]
            if j == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if j in (0, 1):
                r.bold = True
            if "http" in val:
                r.font.color.rgb = RGBColor(0, 102, 204)
            bg = "F4F8FC" if i % 2 == 1 else "FFFFFF"
            set_cell_background(c, bg)
            set_cell_margins(c, 60, 60, 60, 60)

    if tbl_tree:
        tbl_tree._element.addnext(new_p._element)
        new_p._element.addnext(new_tbl._element)

    # 4. BỔ SUNG LINK VÀO CÁC MỤC KỸ THUẬT 5.1, 5.2, 5.3, 5.4, 6
    for p in doc.paragraphs:
        txt = p.text
        if "5.1. Đặc tả Amazon API Gateway (OpenAPI 3.0)" in txt:
            p.add_run(
                "\n  → Link file spec trên Git (blob): https://github.com/nthai212006-gh/cloud-smart-parking-system/blob/dev/backend/api_gateway_openapi.json\n"
                "  → Commit minh chứng: https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/6c5728a"
            ).font.color.rgb = RGBColor(0, 102, 204)
        elif "5.2. Hàm Lambda xử lý xe vào (backend/checkin.py)" in txt:
            p.add_run(
                "\n  → Link file code trên Git (blob): https://github.com/nthai212006-gh/cloud-smart-parking-system/blob/dev/backend/checkin.py\n"
                "  → Commit minh chứng: https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/cb85da8"
            ).font.color.rgb = RGBColor(0, 102, 204)
        elif "5.3. Hàm Lambda xử lý xe ra & Thuật toán tính phí (backend/checkout.py)" in txt:
            p.add_run(
                "\n  → Link file code trên Git (blob): https://github.com/nthai212006-gh/cloud-smart-parking-system/blob/dev/backend/checkout.py\n"
                "  → Commit minh chứng: https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/cb85da8"
            ).font.color.rgb = RGBColor(0, 102, 204)
        elif "5.4. Giải thuật Regex bóc tách biển số xe (scripts/test_plate_regex.py)" in txt:
            p.add_run(
                "\n  → Link file code trên Git (blob): https://github.com/nthai212006-gh/cloud-smart-parking-system/blob/dev/scripts/test_plate_regex.py\n"
                "  → Commit minh chứng: https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/cb85da8"
            ).font.color.rgb = RGBColor(0, 102, 204)
        elif "6. BỘ DỮ LIỆU THỬ NGHIỆM VÀ QUY CHUẨN BẢO MẬT PII" in txt:
            p.add_run(
                "\n  → Link thư mục 120 ảnh trên Git: https://github.com/nthai212006-gh/cloud-smart-parking-system/tree/dev/test-images\n"
                "  → Commit minh chứng dataset: https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/a2d46cd"
            ).font.color.rgb = RGBColor(0, 102, 204)

    # Lưu đè vào file CLCO_WEEK1.docx
    doc.save(file_path)
    print("CLCO_WEEK1.docx updated successfully with full blob & commit links!")

if __name__ == "__main__":
    update_clco_report()

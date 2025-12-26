# Reading & Writing EDU — Full Package (Frontend + Backend starter)

## 1) FRONTEND (HTML)
- Các file .html nằm ngay thư mục gốc.
- File dùng chung gọi API: `app.js`

### Cấu hình bắt buộc
1) Mở `app.js`
2) Thay:
   `PASTE_WEB_APP_URL_HERE`
   bằng URL Web App Apps Script của anh.

> Em đã normalize mọi URL Apps Script trong HTML về cùng placeholder:
`https://script.google.com/macros/s/PASTE_WEB_APP_URL_HERE/exec`
=> Anh chỉ cần thay 1 lần (hoặc Find/Replace toàn dự án).

## 2) BACKEND (Apps Script)
- File backend nằm ở: `backend/Code.gs`
- Copy toàn bộ nội dung `backend/Code.gs` vào Apps Script (Code.gs)
- Deploy Web App:
  - Execute as: Me
  - Who has access: Anyone

### Sheets SSOT
Khi chạy lần đầu, script sẽ tự tạo các sheet:
TEACHERS, CLASSES, STUDENTS, TASKS, SUBMISSIONS, RESULTS, MESSAGES, SESSIONS, AI_LOGS

## 3) Luồng chạy nhanh
1) GV: vào `login.html` -> Đăng ký/Đăng nhập
2) GV: `teacher-dashboard.html` -> tạo lớp -> import học sinh (tạo mã HS)
3) HS/PH: `login.html` -> chọn lớp + nhập mã HS -> vào `student-dashboard.html` hoặc `parent-dashboard.html`
4) GV: giao bài `giaobai-dochieu.html` / `giaobai-viet.html`
5) HS: làm bài `student-reading.html` / `student-write.html` -> nộp
6) GV: xem bài cần chấm `danhsach-bai-can-cham.html` -> chấm `xembailamcuahocsinh.html`
7) Điểm: `sodiem.html` ; Thống kê: `thongke.html`
8) Sổ liên lạc: `parent-dashboard.html` (PH) và (GV) có thể dùng messages.* trong backend

## 4) Ghi chú
- Đây là bản "starter SSOT Unified" để anh chạy khép kín CORE.
- AI actions đã có contract trong chat; backend hiện trả lỗi "AI chưa bật" để tránh phát sinh chi phí khi anh chưa cấu hình key.

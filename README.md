# English Garden

## Clone và bắt đầu

Yêu cầu Python 3.10+ và trình duyệt hiện đại. Không cần tải database hoặc cài thư viện Python ngoài.

```sh
git clone <repository-url>
cd <repository-directory>
python server.py
```

Mở http://127.0.0.1:8765. Lần chạy đầu tự tạo SQLite riêng và ba bài mẫu: học tập, IT và giao tiếp. Tiến độ của người khác không nằm trong repository. Trên Windows có thể chạy `start.bat`.

## Dùng AI làm người dạy

Mở thư mục dự án bằng công cụ AI có quyền đọc/ghi tệp và nhắn: “Đọc AGENTS.md và docs/AI_GUIDE.md, hướng dẫn tôi học; khi tôi yêu cầu thêm kiến thức hãy ghi trực tiếp vào DB.” Các công cụ không tự đọc AGENTS.md cần được yêu cầu đọc rõ ràng.

Quy trình đầy đủ: [hướng dẫn AI](docs/AI_GUIDE.md). Bạn có thể yêu cầu chủ đề, số từ, giải thích lỗi hoặc bài luyện tiếp theo. AI đọc tiến độ từ SQLite trong môi trường của bạn; web không tự kết nối dịch vụ AI.

## Git và dữ liệu cá nhân

Repository chỉ chứa mã nguồn, hướng dẫn và nội dung mẫu công khai. `.gitignore` loại DB SQLite (cả WAL/SHM/journal), thư mục data, backup, export, log và tệp môi trường. Không dùng `git add -f` với các tệp này. Nếu đổi DATABASE_PATH, vẫn giữ tệp DB ngoài thư mục public `web/`.

Push lần đầu sau khi tạo repository trống trên dịch vụ Git:

```sh
git remote add origin <your-repository-url>
git push -u origin main
```

Không ghi token truy cập vào URL remote hoặc mã nguồn. Sao lưu DB riêng, không qua Git.

## Phạm vi ngữ pháp

Hiện có hiện tại đơn (cơ bản A1–A2 và mục mở rộng) và nhờ vả với Could you. Mỗi bài có mục lục bấm được, công thức, ví dụ Anh–Việt, lưu ý và nguồn tham khảo. Đây chưa phải giáo trình toàn bộ ngữ pháp tiếng Anh; AI bổ sung từng chủ đề theo cùng tiêu chuẩn trong AI_GUIDE.

Web cá nhân học và ôn tiếng Anh. HTML/CSS/JavaScript + Python + SQLite, không cần thư viện ngoài.

## Chạy

Nhấp đúp start.bat hoặc chạy `python server.py`, mở http://127.0.0.1:8765.

## Tính năng

Trang hôm nay, thư viện bài học theo ngày, từ vựng có tìm kiếm và nghe mẫu, ngữ pháp, trắc nghiệm / tự viết / nghe rồi viết và giải thích. Ôn từ theo lịch 1–3–7–14–30–60 ngày. Mục lỗi cần ôn cho phép thử lại câu sai gần nhất. Nhật ký, ghi chú, thời gian và lịch sử trả lời lưu trong SQLite.

## Trợ lý thêm nội dung

Bạn chỉ cần bảo trợ lý thêm kiến thức trong chat. Trợ lý ghi trực tiếp SQLite bằng server.save_lesson hoặc `python manage.py add <file>`. Không có màn hình hoặc API nhập bài học. Web nhận bài mới sau khoảng 15 giây khi không đang làm bài. DB trống được tạo bài đầu tiên.

Trợ lý chỉ cập nhật được DB mà phiên làm việc có quyền truy cập. Khi deploy cần quyền truy cập DB trên máy chủ để cập nhật dữ liệu ở đó.

## Deploy sau

Biến môi trường HOST (mặc định 127.0.0.1), PORT (8765), DATABASE_PATH (data/learning.sqlite3). Chạy sau reverse proxy HTTPS. Bản cá nhân hiện chưa có tài khoản; cấu hình đăng nhập tại proxy nếu đưa lên trực tuyến. Không hỗ trợ phân tách dữ liệu nhiều người.

Docker: `docker build -t english-garden .` rồi `docker run -p 8765:8765 -v english-garden-data:/data english-garden`.

SQLite cần ổ lưu bền vững. Dừng server rồi sao chép DB để sao lưu/khôi phục. JSON xuất ở nhật ký chỉ để đọc, chưa có khôi phục JSON.

## Giới hạn

Nghe mẫu dùng giọng trình duyệt. Chưa có nhận diện/khoanh vùng ảnh hoặc chấm phát âm. Bài tự viết chấm theo đáp án và các biến thể accepted; câu tương đương khác có thể cần trợ lý kiểm tra lại trong chat. Không gọi API AI tự động.

Ngày học UTC+7. Thời gian tính khi tab hiển thị và có tương tác trong hai phút gần nhất, gửi mỗi khoảng 15 giây.

## Kiểm tra

`python -m unittest -v test_server.py`

`node --check web/app.js`

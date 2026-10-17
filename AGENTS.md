# English Garden

Web cá nhân để người dùng học và ôn tiếng Anh. Người dùng triển khai sau.

## Lưu kiến thức

Khi người dùng yêu cầu thêm/lưu kiến thức đã dạy, hãy tự soạn nội dung đúng cấu trúc `sample.json`, kiểm tra nội dung và ghi trực tiếp vào SQLite bằng `server.save_lesson` trong transaction, hoặc dùng `python manage.py add <file>`.
Không yêu cầu người dùng nhập JSON, tải tệp hay thao tác màn hình quản trị. Không thêm màn hình nhập kiến thức vào web.
Người dùng bắt đầu với 20 từ. Khi học xong, họ có thể yêu cầu số từ mới và chủ đề bất kỳ trong chat; soạn bài theo yêu cầu rồi ghi trực tiếp DB. Ưu tiên tránh lặp từ đã học trừ khi người dùng muốn ôn.
Đọc tiến độ từ SQLite để điều chỉnh bài và giải thích lỗi khi người dùng yêu cầu. Không ghi đè hay xóa tiến độ cũ.
Ngữ pháp cần trình bày bằng `grammar.sections` thay vì một đoạn dài: tách cách dùng, bảng công thức (`columns`, `rows`), ví dụ Anh–Việt (`examples` gồm `en`, `vi`) và lưu ý (`items`, `hint`, `contrast` gồm `wrong`, `right`). Mỗi section có `title`. Giữ `body` làm nội dung dự phòng.
Tổ chức bài theo `topic`. Người dùng ưu tiên nhiều bài luyện sau mỗi nội dung, gồm tiếng Anh IT và giao tiếp đời thường. Mỗi từ nên có nhận biết nghĩa, nhớ từ và nghe; mẫu câu nằm trong `phrases` (`en`, `vi`, `context`). Câu hỏi có `category`: `grammar`, `vocabulary`, `conversation` và `group` để lọc theo dạng bài. Giữ nguyên thứ tự câu cũ khi bổ sung để không làm sai chỉ số và lịch sử.
DB mặc định `data/learning.sqlite3`; có thể đổi bằng `DATABASE_PATH`. Chỉ có thể cập nhật DB mà môi trường hiện tại truy cập được; không khẳng định đã ghi DB online nếu chưa có quyền truy cập.

## Kiểm tra

`python -m unittest -v test_server.py`
`node --check web/app.js`

## Bản clone mới và hỗ trợ AI

Đọc và tuân thủ [docs/AI_GUIDE.md](docs/AI_GUIDE.md) trước khi hỗ trợ người học. Đó là quy trình dạy, tiêu chuẩn chính xác, schema và cách ghi DB. DB và dữ liệu cá nhân không thuộc Git. Mã nguồn chương trình học công khai khác với lịch sử riêng; không tự chuyển dữ liệu cá nhân sang mã nguồn. Không force-add tệp bị ignore.

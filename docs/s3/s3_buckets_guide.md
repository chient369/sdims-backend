# Hướng dẫn sử dụng S3 Buckets trong SDIMS

## Giới thiệu

SDIMS sử dụng Amazon S3 (Simple Storage Service) để lưu trữ tài liệu, file uploads và các tài nguyên static khác. Tài liệu này mô tả cách thức hoạt động của các S3 buckets, quy ước đặt tên và cách sử dụng các APIs liên quan.

## Cấu trúc S3 Buckets

Hệ thống sử dụng ba S3 buckets chính:

1. **Attachments Bucket** (`sdims-attachments-<stage>-<account-id>`):
   - Mục đích: Lưu trữ các tài liệu đính kèm liên quan đến hợp đồng, opportunities, và các tài liệu khác
   - Sử dụng trong: Quản lý hợp đồng, Quản lý cơ hội, Upload tài liệu khác

2. **Profile Images Bucket** (`sdims-profile-images-<stage>-<account-id>`):
   - Mục đích: Lưu trữ ảnh đại diện của người dùng/nhân viên
   - Sử dụng trong: Quản lý nhân sự, Hồ sơ người dùng

3. **Backup Bucket** (`sdims-backups-<stage>-<account-id>`):
   - Mục đích: Lưu trữ các bản sao lưu dữ liệu
   - Sử dụng trong: Các công việc backup tự động, Backup thủ công

## Quy ước đặt tên Objects/Files

### Trong Attachments Bucket

Format: `<folder_path>/<timestamp>-<file_name>`

Ví dụ:
- `contracts/1684123456-contract-abc123.pdf`
- `opportunities/1684567890-proposal-xyz-client.docx`

Các folder path chính:
- `contracts`: Tài liệu liên quan đến hợp đồng
- `opportunities`: Tài liệu liên quan đến cơ hội kinh doanh
- `reports`: Báo cáo
- `invoices`: Hóa đơn
- `employees`: Tài liệu liên quan đến nhân viên (không phải hình ảnh profile)

### Trong Profile Images Bucket

Format: `<employee_id>/<timestamp>-<image_name>`

Ví dụ:
- `emp123/1684123456-profile-photo.jpg`
- `emp456/1684567890-avatar.png`

### Trong Backup Bucket

Format: `<backup_type>/<date>/<filename>`

Ví dụ:
- `dynamodb/2025-04-01/sdims-main-table-backup.json`
- `configurations/2025-04-01/system-configs.json`

## Sử dụng Presigned URLs

SDIMS sử dụng Presigned URLs để upload và download files một cách an toàn mà không cần truy cập trực tiếp vào S3 bucket.

### Tạo Upload URL

**Endpoint:** `POST /api/v1/files/upload-url`

**Request Body:**
```json
{
  "fileName": "document.pdf",
  "contentType": "application/pdf",
  "folderPath": "contracts"
}
```

**Response:**
```json
{
  "uploadUrl": "https://s3.amazonaws.com/...",
  "key": "contracts/1684123456-document.pdf"
}
```

**Cách sử dụng:**
1. Gọi API để lấy upload URL
2. Sử dụng URL này để upload file trực tiếp lên S3 với phương thức PUT
3. Lưu `key` được trả về để tham chiếu đến file trong tương lai

**Ví dụ HTTP request để upload file:**
```
PUT <uploadUrl> HTTP/1.1
Content-Type: application/pdf
Content-Length: <file_size>

<file_data>
```

### Tạo Download URL

**Endpoint:** `GET /api/v1/files/download-url?key=<file_key>`

**Response:**
```json
{
  "downloadUrl": "https://s3.amazonaws.com/...",
  "key": "contracts/1684123456-document.pdf"
}
```

**Cách sử dụng:**
1. Gọi API để lấy download URL
2. Sử dụng URL này để tải file (redirect người dùng, hoặc tải xuống bằng HTTP GET)

## Hiệu lực (Expiration) của Presigned URLs

- Upload URLs có hiệu lực trong **1 giờ (3600 giây)** kể từ khi tạo
- Download URLs có hiệu lực trong **1 giờ (3600 giây)** kể từ khi tạo

## Best Practices

1. **Quản lý dữ liệu nhạy cảm**:
   - Luôn kiểm tra quyền truy cập trước khi cấp Presigned URL
   - Không lưu trữ thông tin nhạy cảm trong tên file

2. **Tối ưu hiệu suất**:
   - Nén file lớn trước khi upload
   - Giới hạn kích thước file nếu cần

3. **Quản lý vòng đời**:
   - Tài liệu cũ sẽ tự động chuyển sang lớp lưu trữ STANDARD_IA sau 30 ngày
   - Backup sẽ bị xóa sau 365 ngày

4. **Kiểm soát chi phí**:
   - Xóa các file tạm thời hoặc không cần thiết
   - Cân nhắc loại lưu trữ phù hợp cho từng loại file

## Xử lý lỗi phổ biến

1. **Presigned URL hết hạn**:
   - Lỗi 403 Forbidden
   - Giải pháp: Tạo URL mới

2. **File không tồn tại**:
   - Lỗi 404 Not Found
   - Giải pháp: Kiểm tra key file

3. **Lỗi CORS**:
   - Giải pháp: Đảm bảo domain của bạn đã được cấu hình trong CORS policy của bucket

## Lưu ý bảo mật

- Tất cả các buckets đều được cấu hình để:
  - Block public access
  - Yêu cầu SSL/TLS connections (HTTPS)
  - Mã hóa server-side với AES-256
  - Không thể truy cập trực tiếp mà không có presigned URL hoặc quyền IAM phù hợp 
# Tài liệu DynamoDB cho SDIMS

## Giới thiệu

Thư mục này chứa tài liệu về thiết kế và sử dụng DynamoDB trong dự án SDIMS. DynamoDB được triển khai theo thiết kế single-table, cho phép lưu trữ tất cả các loại thực thể trong một bảng duy nhất và truy vấn hiệu quả thông qua các index được định nghĩa trước.

## Cấu trúc thư mục

- `database_structure.md`: Mô tả cấu trúc chung của DynamoDB, bao gồm quy ước đặt tên, cấu trúc khóa và mô hình dữ liệu
- `access_patterns.md`: Chi tiết các mẫu truy cập (access patterns) để truy vấn và cập nhật dữ liệu

## Triển khai DynamoDB

DynamoDB được định nghĩa trong file CloudFormation `template.yaml` ở thư mục gốc với ba Global Secondary Indexes (GSI) để hỗ trợ các trường hợp truy vấn khác nhau:

- **GSI1**: Truy vấn theo loại thực thể và thuộc tính chính
- **GSI2**: Truy vấn theo trạng thái hoặc thuộc tính phụ
- **GSI3**: Truy vấn theo các mối quan hệ giữa các thực thể

## Khởi tạo dữ liệu

Để khởi tạo dữ liệu cho DynamoDB, bạn có thể sử dụng script trong `src/scripts/init_dynamodb.py`:

```bash
# Tạo bảng và khởi tạo dữ liệu cơ bản
python src/scripts/init_dynamodb.py --stage dev --create-table

# Khởi tạo dữ liệu với file seed
python src/scripts/init_dynamodb.py --stage dev --seed-file seeds/sample_data.json

# Buộc khởi tạo lại dữ liệu nếu bảng đã có dữ liệu
python src/scripts/init_dynamodb.py --stage dev --force
```

## Tạo dữ liệu mẫu

Để tạo dữ liệu mẫu cho việc kiểm thử, bạn có thể sử dụng script trong `src/scripts/generate_seed_data.py`:

```bash
python src/scripts/generate_seed_data.py
```

Script này sẽ tạo dữ liệu mẫu cho các loại thực thể khác nhau và lưu vào file `seeds/sample_data.json`.

## Sử dụng DynamoDB trong code

DynamoDB được truy cập thông qua lớp `DynamoDBRepository` được định nghĩa trong `src/common/dynamodb.py`. Lớp này cung cấp các phương thức để tương tác với DynamoDB một cách dễ dàng:

```python
from common.dynamodb import dynamodb_repo

# Lấy item theo primary key
user = dynamodb_repo.get_item("USER#123", "METADATA#123")

# Truy vấn items
employees = dynamodb_repo.query(
    key_condition_expression="GSI2PK = :pk",
    expression_attribute_values={
        ":pk": "EMPLOYEE_STATUS#Available"
    },
    index_name="GSI2"
)

# Thêm item mới
dynamodb_repo.put_item({
    'PK': 'USER#123',
    'SK': 'METADATA#123',
    'GSI1PK': 'USER',
    'GSI1SK': 'username',
    # ...các trường khác
})
```

## Lưu ý quan trọng

1. **Denormalization**: Dữ liệu có thể được sao chép (denormalized) giữa các items để tối ưu truy vấn. Khi cập nhật dữ liệu, cần đảm bảo cập nhật tất cả các bản sao.

2. **Transactions**: Sử dụng transactions khi cần cập nhật nhiều items liên quan để đảm bảo tính nhất quán.

3. **Mô hình hóa**: Tuân thủ các quy ước về cấu trúc khóa và indexes để đảm bảo truy vấn hiệu quả.

4. **Capacity**: Theo dõi capacity units và điều chỉnh khi cần để tối ưu chi phí và hiệu suất.

5. **Auto Scaling**: DynamoDB được cấu hình với auto scaling để tự động điều chỉnh capacity units theo tải.

## Tài liệu tham khảo

- [DynamoDB Single-Table Design Pattern](https://www.alexdebrie.com/posts/dynamodb-single-table/)
- [AWS DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
- [Best Practices for DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html) 
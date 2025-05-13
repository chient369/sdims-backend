# Tài liệu cấu trúc DynamoDB SDIMS

## Tổng quan

SDIMS sử dụng thiết kế DynamoDB single-table để lưu trữ tất cả dữ liệu trong một bảng duy nhất. Thiết kế này mang lại nhiều lợi ích:

- Giảm số lượng bảng phải quản lý
- Cho phép truy vấn dữ liệu có liên quan trong một lần gọi
- Tối ưu chi phí và hiệu suất

## Cấu trúc khóa

### Khóa chính (Primary Key)

Bảng sử dụng khóa kết hợp (composite key) bao gồm:

- **PK (Partition Key)**: Xác định phân vùng dữ liệu theo loại thực thể và ID
- **SK (Sort Key)**: Sắp xếp dữ liệu trong cùng một phân vùng

### Global Secondary Indexes (GSI)

Bảng có 3 GSI để hỗ trợ các access pattern khác nhau:

- **GSI1**: Truy vấn theo loại thực thể và thuộc tính chính
- **GSI2**: Truy vấn theo trạng thái hoặc thuộc tính phụ
- **GSI3**: Truy vấn theo các mối quan hệ giữa các thực thể

## Quy ước đặt tên khóa

### Khóa phân vùng (PK)

- Khóa phân vùng tuân theo định dạng: `<ENTITY_TYPE>#<ID>`
- Ví dụ: `USER#123`, `EMPLOYEE#456`, `CONTRACT#789`

### Khóa sắp xếp (SK)

- SK được sử dụng để xác định loại item hoặc mối quan hệ
- Các định dạng phổ biến:
  - `METADATA#<ID>`: Lưu trữ thông tin chính của thực thể
  - `<RELATED_ENTITY>#<ID>`: Lưu trữ mối quan hệ với thực thể khác
  - `<TIME_BASED_ENTITY>#<TIMESTAMP>`: Lưu trữ các sự kiện theo thời gian

### GSI Keys

- GSI1PK: Thường là loại thực thể, ví dụ: `USER`, `EMPLOYEE`, `CONTRACT`
- GSI1SK: Thuộc tính chính để sắp xếp, ví dụ: name, username, email
- GSI2PK: Thường là loại với trạng thái, ví dụ: `EMPLOYEE_STATUS#Available`
- GSI2SK: Thuộc tính phụ để sắp xếp, thường theo thời gian hoặc tên
- GSI3PK: Thường là ID của thực thể liên quan
- GSI3SK: Loại thực thể chính hoặc thông tin liên quan khác

## Mô hình dữ liệu

### User và Authorization

```
PK: USER#<id>
SK: METADATA#<id>
GSI1PK: USER
GSI1SK: <username>
GSI2PK: USER
GSI2SK: <email>
```

### Employee

```
PK: EMPLOYEE#<id>
SK: METADATA#<id>
GSI1PK: EMPLOYEE
GSI1SK: <employee_code>
GSI2PK: EMPLOYEE_STATUS#<current_status>
GSI2SK: <last_name>#<first_name>
GSI3PK: EMPLOYEE_TEAM#<team_id>
GSI3SK: <last_name>#<first_name>
```

### Project

```
PK: PROJECT#<id>
SK: METADATA#<id>
GSI1PK: PROJECT
GSI1SK: <name>
GSI2PK: PROJECT_STATUS#<status>
GSI2SK: <end_date>
GSI3PK: CONTRACT#<contract_id>
GSI3SK: PROJECT#<id>
```

## Access Patterns

### Truy vấn thực thể theo ID

```python
response = table.get_item(
    Key={
        'PK': 'USER#123',
        'SK': 'METADATA#123'
    }
)
```

### Truy vấn tất cả items của một thực thể

```python
response = table.query(
    KeyConditionExpression='PK = :pk',
    ExpressionAttributeValues={
        ':pk': 'USER#123'
    }
)
```

### Truy vấn theo GSI

Tìm nhân viên theo mã nhân viên:

```python
response = table.query(
    IndexName='GSI1',
    KeyConditionExpression='GSI1PK = :pk AND GSI1SK = :sk',
    ExpressionAttributeValues={
        ':pk': 'EMPLOYEE',
        ':sk': 'EMP001'
    }
)
```

Tìm nhân viên theo trạng thái:

```python
response = table.query(
    IndexName='GSI2',
    KeyConditionExpression='GSI2PK = :pk',
    ExpressionAttributeValues={
        ':pk': 'EMPLOYEE_STATUS#Available'
    }
)
```

Tìm nhân viên theo team:

```python
response = table.query(
    IndexName='GSI3',
    KeyConditionExpression='GSI3PK = :pk',
    ExpressionAttributeValues={
        ':pk': 'EMPLOYEE_TEAM#T123'
    }
)
```

## Thực hành tốt nhất

1. **Denormalize dữ liệu**: Sao chép dữ liệu cần thiết giữa các items để giảm số lượng truy vấn
2. **Kích thước item nhỏ gọn**: Giữ kích thước item dưới 4KB khi có thể
3. **Đảm bảo phân phối đều PK**: Tránh hot partition bằng cách thiết kế PK để phân phối đều
4. **Chỉ truy vấn theo thuộc tính đã được index**: Tránh table scan
5. **Sử dụng batch operations**: Khi cần đọc/ghi nhiều items cùng lúc
6. **Quản lý capacity**: Theo dõi và điều chỉnh capacity cho phù hợp với tải

## Xử lý mối quan hệ

### One-to-One

Sử dụng cùng PK cho cả hai thực thể, với SK khác nhau:

```
PK: USER#123
SK: METADATA#123
...

PK: USER#123
SK: PROFILE#123
...
```

### One-to-Many

Sử dụng PK của thực thể "One" và SK bắt đầu bằng loại thực thể "Many":

```
PK: EMPLOYEE#123
SK: METADATA#123
...

PK: EMPLOYEE#123
SK: PROJECT_HISTORY#1
...

PK: EMPLOYEE#123
SK: PROJECT_HISTORY#2
...
```

### Many-to-Many

Sử dụng cặp items đại diện cho mối quan hệ ở cả hai hướng:

```
PK: EMPLOYEE#123
SK: SKILL#456
...

PK: SKILL#456
SK: EMPLOYEE#123
...
```

## Lưu ý quan trọng

1. Cân nhắc kỹ các access pattern trước khi thêm, sửa, xóa dữ liệu để đảm bảo tính nhất quán
2. Sử dụng transactions khi cần cập nhật nhiều items liên quan
3. Khi cập nhật dữ liệu, nhớ cập nhật tất cả các bản sao (denormalized copies) của dữ liệu đó
4. Đối với dữ liệu lớn, xem xét sử dụng S3 và chỉ lưu tham chiếu trong DynamoDB 
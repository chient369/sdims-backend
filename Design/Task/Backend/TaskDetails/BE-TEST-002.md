**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task viết integration tests | -           | Draft     |

---

## 1. Mục tiêu  
Tài liệu này định nghĩa chi tiết công việc viết integration tests cho hệ thống, đảm bảo các thành phần kết nối với nhau hoạt động một cách chính xác và kiểm tra các luồng nghiệp vụ end-to-end.

# Chi tiết Task: Viết integration tests

## Thông tin chung

**Task ID:** BE-TEST-002  
**Task Name:** Viết integration tests  
**Độ ưu tiên:** Trung bình  
**Phụ thuộc vào:** BE-INF-001, BE-INF-003, BE-INF-004, BE-INF-005, BE-TEST-001  
**Các task phụ thuộc vào task này:** BE-DEPLOY-001  
**Các API:** Tất cả API endpoints

## Mô tả

Task này bao gồm việc phát triển các integration tests để kiểm tra tương tác giữa các thành phần khác nhau của hệ thống, đặc biệt là tương tác giữa Lambda functions, API Gateway, DynamoDB, và S3. Integration tests sẽ tập trung vào việc kiểm tra các luồng nghiệp vụ end-to-end, từ request API tới xử lý dữ liệu và trả về response. Ngoài ra, task cũng bao gồm việc thiết lập môi trường testing tự động để chạy các tests này.

## Chi tiết công việc

### Thiết lập môi trường testing

- [ ] Cấu hình môi trường testing cục bộ:
  - Location: tests/integration/setup/
  - Thiết lập Docker Compose để chạy các dịch vụ cần thiết (DynamoDB Local, Localstack)
  - Tạo scripts khởi động và dừng môi trường testing
  - Khởi tạo dữ liệu test mẫu

- [ ] Xây dựng test runner và framework:
  - Location: tests/integration/
  - Thiết lập pytest fixtures cho integration tests
  - Cấu hình API client để gọi các API endpoints
  - Tạo các utility classes hỗ trợ kiểm tra kết quả và so sánh data

### Viết tests cho authentication flow

- [ ] Viết integration tests cho authentication flow:
  - Location: tests/integration/auth/
  - Test đăng nhập và nhận token JWT
  - Test truy cập các API bị bảo vệ với token hợp lệ
  - Test truy cập API với token không hợp lệ hoặc hết hạn
  - Test refresh token flow
  - Test đăng xuất

### Viết integration tests cho các luồng nghiệp vụ chính

- [ ] Viết tests cho module Quản lý Nhân sự:
  - Location: tests/integration/hrm/
  - Test luồng create-read-update-delete nhân viên
  - Test quản lý skills và skill categories
  - Test tìm kiếm và filter nhân viên
  - Test recommendation nhân viên dựa trên skills

- [ ] Viết tests cho module Quản lý Hiệu suất & Margin:
  - Location: tests/integration/margin/
  - Test luồng import và quản lý chi phí
  - Test tính toán revenue và margin
  - Test xem báo cáo margin với các filter khác nhau

- [ ] Viết tests cho module Quản lý Cơ hội Kinh doanh:
  - Location: tests/integration/opportunity/
  - Test đồng bộ dữ liệu từ Hubspot (sử dụng mock API)
  - Test quản lý cơ hội kinh doanh
  - Test tính toán trạng thái follow-up
  - Test gán leader và quản lý ghi chú

- [ ] Viết tests cho module Quản lý Hợp đồng & Doanh thu:
  - Location: tests/integration/contract/
  - Test luồng create-read-update-delete hợp đồng
  - Test quản lý điều khoản thanh toán
  - Test upload và download file đính kèm
  - Test quản lý nhân sự trong hợp đồng

- [ ] Viết tests cho module Dashboard & Báo cáo:
  - Location: tests/integration/report/
  - Test lấy dữ liệu tổng hợp cho dashboard
  - Test các báo cáo chi tiết với các filter khác nhau

- [ ] Viết tests cho module Quản trị Hệ thống:
  - Location: tests/integration/admin/
  - Test quản lý người dùng và phân quyền
  - Test cấu hình hệ thống
  - Test xem logs

### Viết API tests end-to-end

- [ ] Phát triển bộ API tests tự động:
  - Location: tests/api/
  - Sử dụng Postman/Newman hoặc tools tương tự để tạo bộ API tests
  - Xây dựng test scripts tự động để chạy API tests
  - Tạo các test cases cho tất cả các API endpoints
  - Tạo báo cáo kết quả test

### Tích hợp vào CI/CD

- [ ] Tích hợp integration tests vào CI/CD pipeline:
  - Location: .github/workflows/ hoặc buildspec.yml
  - Cấu hình GitHub Actions hoặc AWS CodeBuild để chạy integration tests
  - Thiết lập môi trường test tự động (DynamoDB Local, Localstack)
  - Tạo báo cáo và lưu kết quả tests

### Tạo Documentation

- [ ] Viết tài liệu hướng dẫn integration testing:
  - Location: docs/testing/integration/
  - Hướng dẫn thiết lập môi trường testing
  - Hướng dẫn viết integration tests
  - Hướng dẫn chạy tests
  - Hướng dẫn đọc và phân tích kết quả tests

## Ví dụ cách viết integration test

Dưới đây là ví dụ về cách viết integration test cho một luồng nghiệp vụ:

```python
# tests/integration/hrm/test_employee_management.py
import pytest
import requests
import json
import uuid

from tests.integration.setup import api_client, auth_headers

class TestEmployeeManagement:
    @pytest.fixture
    def new_employee_data(self):
        employee_id = f"emp-{uuid.uuid4().hex[:8]}"
        return {
            "id": employee_id,
            "name": "Integration Test Employee",
            "email": f"test-{employee_id}@example.com",
            "position": "Software Engineer",
            "department": "Engineering",
            "skills": ["Python", "AWS", "Serverless"]
        }
    
    def test_employee_crud_flow(self, new_employee_data, auth_headers):
        # 1. Create employee
        create_response = api_client.post(
            "/api/v1/employees",
            json=new_employee_data,
            headers=auth_headers
        )
        assert create_response.status_code == 201
        created_employee = create_response.json()
        employee_id = created_employee["id"]
        
        # 2. Read employee
        get_response = api_client.get(
            f"/api/v1/employees/{employee_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 200
        employee = get_response.json()
        assert employee["name"] == new_employee_data["name"]
        assert employee["email"] == new_employee_data["email"]
        
        # 3. Update employee
        update_data = {"position": "Senior Software Engineer"}
        update_response = api_client.put(
            f"/api/v1/employees/{employee_id}",
            json=update_data,
            headers=auth_headers
        )
        assert update_response.status_code == 200
        
        # 4. Verify update
        get_updated_response = api_client.get(
            f"/api/v1/employees/{employee_id}",
            headers=auth_headers
        )
        updated_employee = get_updated_response.json()
        assert updated_employee["position"] == "Senior Software Engineer"
        
        # 5. Delete employee
        delete_response = api_client.delete(
            f"/api/v1/employees/{employee_id}",
            headers=auth_headers
        )
        assert delete_response.status_code == 204
        
        # 6. Verify deletion
        get_deleted_response = api_client.get(
            f"/api/v1/employees/{employee_id}",
            headers=auth_headers
        )
        assert get_deleted_response.status_code == 404
```

## Tiêu chí hoàn thành

1. Môi trường testing cục bộ được thiết lập và có thể sử dụng dễ dàng
2. Integration tests đã được viết cho tất cả các luồng nghiệp vụ chính
3. API tests end-to-end đã được viết cho tất cả các API endpoints
4. Tests kiểm tra toàn diện các use cases của hệ thống
5. Tests có thể chạy tự động trong môi trường CI/CD
6. Tài liệu hướng dẫn integration testing đã được hoàn thiện

## Ước tính thời gian

- 10-12 ngày làm việc

## Ghi chú

- Integration tests nên tập trung vào các luồng nghiệp vụ chính, không cần kiểm tra tất cả các edge cases (đã được kiểm tra trong unit tests)
- Sử dụng cách tiếp cận "pyramid testing" để đảm bảo coverage tốt nhưng không quá tốn thời gian chạy tests
- Cân nhắc sử dụng parallelization để tăng tốc độ chạy tests khi cần thiết
- Luôn reset dữ liệu test sau mỗi test case để đảm bảo tính độc lập của các tests
- Sử dụng các công cụ như DynamoDB Local và Localstack thay vì dịch vụ AWS thật để tránh chi phí và phụ thuộc vào mạng 
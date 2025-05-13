**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-08-01 | Chiến Trần Văn | Định nghĩa chi tiết task xây dựng CI/CD pipeline | -           | Draft     |
| 1.1     | 2024-08-01 | Chiến Trần Văn | Cập nhật sử dụng Python thay vì Node.js | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết các công việc cần thực hiện để thiết lập quy trình CI/CD pipeline cho việc triển khai tự động ứng dụng serverless backend sử dụng Python.

# Chi tiết Task: BE-INF-002 - Xây dựng CI/CD pipeline cho deployment

## Thông tin chung

**Task ID:** BE-INF-002  
**Task Name:** Xây dựng CI/CD pipeline cho deployment  
**Độ ưu tiên:** Cao (High Priority)  
**Phụ thuộc vào:** BE-INF-001  
**Các task phụ thuộc vào task này:** Không có

## Mô tả

Task này bao gồm việc thiết lập quy trình CI/CD (Continuous Integration/Continuous Deployment) để tự động hóa quá trình testing, build và triển khai dự án lên môi trường AWS. Quy trình CI/CD sẽ được cấu hình để có thể triển khai lên các môi trường khác nhau (dev, staging, production) dựa trên các nhánh Git tương ứng.

## Chi tiết công việc

### Lựa chọn công cụ CI/CD
- [ ] Quyết định sử dụng GitHub Actions (được đề xuất do dự án có thể đang sử dụng GitHub)
- [ ] Hoặc, nếu cần, xem xét các giải pháp thay thế như AWS CodePipeline, GitLab CI/CD

### Thiết lập GitHub Actions

- [ ] Tạo thư mục `.github/workflows` trong dự án
- [ ] Tạo file workflow cho môi trường dev:
  ```yaml
  # .github/workflows/dev-deploy.yml
  name: Deploy to Development
  
  on:
    push:
      branches: [ develop ]
  
  jobs:
    deploy:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Set up Python
          uses: actions/setup-python@v4
          with:
            python-version: '3.13'
        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
            pip install pytest black pylint pytest-cov
            if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        - name: Lint with pylint
          run: |
            pylint --disable=C0111,C0103,C0303,C0330 src/
        - name: Format check with black
          run: |
            black --check src/
        - name: Test with pytest
          run: |
            pytest --cov=src tests/
        - name: Install AWS SAM CLI
          run: |
            pip install aws-sam-cli
        - name: Configure AWS credentials
          uses: aws-actions/configure-aws-credentials@v1
          with:
            aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
            aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
            aws-region: ap-southeast-1
        - name: Deploy with SAM
          run: |
            sam build
            sam deploy --config-env default --no-confirm-changeset --no-fail-on-empty-changeset
  ```

- [ ] Tạo file workflow cho môi trường staging:
  ```yaml
  # .github/workflows/staging-deploy.yml
  name: Deploy to Staging
  
  on:
    push:
      branches: [ staging ]
  
  jobs:
    deploy:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Set up Python
          uses: actions/setup-python@v4
          with:
            python-version: '3.13'
        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
            pip install pytest black pylint pytest-cov
            if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        - name: Lint with pylint
          run: |
            pylint --disable=C0111,C0103,C0303,C0330 src/
        - name: Format check with black
          run: |
            black --check src/
        - name: Test with pytest
          run: |
            pytest --cov=src tests/
        - name: Install AWS SAM CLI
          run: |
            pip install aws-sam-cli
        - name: Configure AWS credentials
          uses: aws-actions/configure-aws-credentials@v1
          with:
            aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
            aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
            aws-region: ap-southeast-1
        - name: Deploy with SAM
          run: |
            sam build
            sam deploy --config-env staging --no-confirm-changeset --no-fail-on-empty-changeset
  ```

- [ ] Tạo file workflow cho môi trường production:
  ```yaml
  # .github/workflows/prod-deploy.yml
  name: Deploy to Production
  
  on:
    push:
      branches: [ main ]
    workflow_dispatch:
      inputs:
        confirm:
          description: 'Xác nhận triển khai lên môi trường production?'
          required: true
          default: 'no'
          
  jobs:
    deploy:
      runs-on: ubuntu-latest
      if: github.event.inputs.confirm == 'yes' || github.event_name == 'push'
      steps:
        - uses: actions/checkout@v3
        - name: Set up Python
          uses: actions/setup-python@v4
          with:
            python-version: '3.13'
        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
            pip install pytest black pylint pytest-cov
            if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        - name: Lint with pylint
          run: |
            pylint --disable=C0111,C0103,C0303,C0330 src/
        - name: Format check with black
          run: |
            black --check src/
        - name: Test with pytest
          run: |
            pytest --cov=src tests/
        - name: Install AWS SAM CLI
          run: |
            pip install aws-sam-cli
        - name: Configure AWS credentials
          uses: aws-actions/configure-aws-credentials@v1
          with:
            aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
            aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
            aws-region: ap-southeast-1
        - name: Deploy with SAM
          run: |
            sam build
            sam deploy --config-env prod --no-confirm-changeset --no-fail-on-empty-changeset
  ```

### Thiết lập Caching

- [ ] Thêm caching cho Python dependencies để tăng tốc workflow:
  ```yaml
  - name: Cache pip packages
    uses: actions/cache@v3
    with:
      path: ~/.cache/pip
      key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
      restore-keys: |
        ${{ runner.os }}-pip-
  ```

### Thiết lập Secrets trong GitHub

- [ ] Thiết lập AWS credentials trong GitHub Secrets:
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY
  - (Tài khoản IAM cần có quyền để triển khai CloudFormation, Lambda, API Gateway, DynamoDB, S3)

### Tạo quy trình phê duyệt (optional)

- [ ] Thiết lập quy trình pull request và code review
  - Tạo template cho pull request
  - Yêu cầu ít nhất 1 người review code trước khi merge
  - Thiết lập các quy tắc bảo vệ branch (protect branch rules)

### Thiết lập notification

- [ ] Cấu hình thông báo khi build thành công/thất bại:
  - Thông báo qua email
  - Hoặc tích hợp với Slack/Discord

### Thiết lập môi trường trong AWS

- [ ] Tạo các IAM Roles cần thiết cho CI/CD pipeline
- [ ] Cấu hình các biến môi trường cho từng stage (dev, staging, prod)
- [ ] Tạo S3 buckets cho việc lưu trữ deployment artifacts

### Viết tài liệu hướng dẫn

- [ ] Tạo tài liệu mô tả quy trình CI/CD:
  - Cách thức hoạt động của pipeline
  - Các bước cần thực hiện khi triển khai lên các môi trường
  - Quy trình xử lý lỗi và rollback
  - Cách kiểm tra logs và monitoring

## Tiêu chí hoàn thành

- CI/CD pipeline được thiết lập và hoạt động cho tất cả các môi trường
- Có thể tự động triển khai lên môi trường dev khi push code lên nhánh develop
- Môi trường staging và production có các bước kiểm soát và phê duyệt
- Tài liệu hướng dẫn về quy trình CI/CD được tạo
- Notifications khi build thành công/thất bại được thiết lập

## Ước tính thời gian

- 2-3 ngày làm việc

## Ghi chú

- Cần có AWS account với quyền tạo và quản lý các dịch vụ cần thiết
- Cần có GitHub repository với quyền admin để thiết lập GitHub Actions
- Môi trường production nên có thêm các bước kiểm tra và phê duyệt trước khi triển khai
- Sử dụng Python 3.13 cho tất cả các môi trường để đảm bảo tính nhất quán
- Cân nhắc thêm các công cụ kiểm tra bảo mật như Bandit trong quy trình CI/CD
- Đảm bảo sử dụng các phiên bản chính xác của các dependencies trong requirements.txt 
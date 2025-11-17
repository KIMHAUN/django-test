# 1. Python 베이스 이미지
FROM python:3.9-slim

# 2. 작업 디렉토리
WORKDIR /app

# 3. 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. requirements.txt 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 5. Django 소스 복사
COPY . /app/

# 6. 정적/미디어 디렉토리 생성
RUN mkdir -p /app/staticfiles /app/media

# 7. 환경 변수
ENV PYTHONUNBUFFERED 1

# 8. 포트
EXPOSE 8000

# 9. 애플리케이션 실행
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

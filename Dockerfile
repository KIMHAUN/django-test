# pull official base image - 도커는 파이썬이 설치되어 있는 이미지를 불러옴(설치된 파이썬 버전 작성)
FROM python:3.13.7

# set work diretory - 프로젝트의 작업 폴더 지정
WORKDIR /app

# set envireonment variables -.pyc 파일을 생성하지 않도록 하고, 버퍼링없이 출력하게 함
ENV PYTHONDONTWRITEBYECODE=1
ENV PYTHONUNBUFFERED=1

# 현재 위치(Dockerfile이 있는 위치)에 있는 파일을 WORKDIR로 복사
COPY . /app/

#install dependencies - requirements.txt에 나열된 라이브러리 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
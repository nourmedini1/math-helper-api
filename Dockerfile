FROM python:3.11.8

RUN apt-get update && apt-get upgrade -y

WORKDIR /src

COPY /src /src

COPY requirements.txt /src/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3775

CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "3775"]
FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install flask pandas

EXPOSE 3000

CMD ["python", "Ecommerce.py"]

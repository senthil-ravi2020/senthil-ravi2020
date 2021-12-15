FROM python:3.8

RUN pip install fastapi uvicorn requests aiofiles

EXPOSE 8081

COPY . /app
#ENV PATH=$PATH:/app
ENV PYTHONPATH "${PYTHONPATH}:/app"


CMD ["uvicorn", "app.main", "--host", "0.0.0.0", "--port", "8081"]
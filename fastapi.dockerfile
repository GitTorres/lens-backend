FROM python:3.8.10
RUN mkdir /app
WORKDIR /app
COPY fastapi/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
RUN rm -rf /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug", "--reload"]

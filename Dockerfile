FROM python:3.8-slim
COPY . /opt/code/
WORKDIR /opt/code/
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]


FROM python:3.9-slim-buster

COPY src/ /
RUN pip install -r requirements.txt
ENV IN_DOCKER "yes"
CMD ["python", "/rent_prices/testPackApp.py"]

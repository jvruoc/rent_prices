FROM python:3.9-slim-buster

COPY ./src /src
RUN pip install -r src/requirements.txt
ENV IN_DOCKER "yes"
CMD ["python", "src/rent_prices/main.py"]

FROM python:3
WORKDIR /src
ADD requirements.txt /src
RUN pip install  -r requirements.txt
ADD . /src
EXPOSE 8000
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]
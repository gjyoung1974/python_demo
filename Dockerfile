ARG BASE_IMAGE_TAG=3

FROM python:$BASE_IMAGE_TAG

RUN echo $(python --version)
COPY . /python_demo
WORKDIR /python_demo
ENV PYTHONPATH /python_demo


RUN pip install -r req.txt

CMD ["./bin/run.py"]

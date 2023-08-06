FROM python:3.9-slim

ARG MODEL_PATH
ARG TRAINED_MODEL_PATH
ARG MODEL_VERSION

ENV MODEL_VERSION ${MODEL_VERSION}

COPY . /model

WORKDIR /model

RUN ls -la

RUN echo "energinetml model serve --host 0.0.0.0 --port 80 --model-file ${TRAINED_MODEL_PATH} --model-version ${MODEL_VERSION}"

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y apt-transport-https
RUN pip3 install --upgrade twine wheel setuptools
RUN pip3 install --upgrade -r /model/requirements.txt

EXPOSE 80

WORKDIR ${MODEL_PATH}

CMD energinetml model serve --host 0.0.0.0 --port 80 --model-file ${TRAINED_MODEL_PATH} --model-version ${MODEL_VERSION}

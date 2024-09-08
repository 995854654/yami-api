FROM ubuntu:20.04

ARG BUILD_DEB_PKGS="unzip"
ARG RUNTIME_DEB_PKGS="zip vim python3.9 python3.9-dev python3-pip iputils-ping curl less"


WORKDIR /root

RUN apt-get update -y && \
    apt-get -y install ${BUILD_DEB_PKGS} ${RUNTIME_DEB_PKGS} --no-install-recommends && \
    rm -rf /usr/bin/python3 && \
    ln -s /usr/bin/python3.9 /usr/bin/python3 && \
    ln -s /usr/bin/python3.9 /usr/bin/python && \
    python3.9 -m pip install pip --upgrade


WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

# 复制项目到app目录
COPY . /app/

EXPOSE 8443/tcp

ENV HOST "0.0.0.0"
ENV PORT 8443

CMD ["python","main.py"]



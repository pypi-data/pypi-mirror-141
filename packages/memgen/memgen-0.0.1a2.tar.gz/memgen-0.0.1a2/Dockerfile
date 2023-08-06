FROM ubuntu:21.10

# https://serverfault.com/a/797318
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt-get install -y python3-pip python3-venv
RUN apt-get install -y git

RUN useradd -m user

USER user

ENV PATH="/home/user/.local/bin:${PATH}"

RUN python3 -m pip install --upgrade pip setuptools wheel build twine setuptools_scm

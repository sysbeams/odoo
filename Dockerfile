FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /app
RUN apt upgrade -y && apt update -y && apt -y install sudo
RUN apt install -y build-essential wget python3-dev python3-venv python3-wheel libfreetype6-dev libxml2-dev libzip-dev \
     libldap2-dev libsasl2-dev python3-setuptools node-less libjpeg-dev zlib1g-dev libpq-dev libxslt1-dev libldap2-dev \
     libtiff5-dev libjpeg8-dev libopenjp2-7-dev liblcms2-dev libwebp-dev libharfbuzz-dev libfribidi-dev libxcb1-dev\
     python3-pip 	
COPY . .
RUN pip3 install setuptools wheel
RUN pip3 install -r requirements.txt
CMD ["python3", "odoo-bin", "-c", "debian/odoo.conf", "-i", "base"]

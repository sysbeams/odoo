FROM ubuntu:22.04
WORKDIR /app
RUN apt upgrade -y && apt update -y
RUN apt install -y python3 python3-pip build-essential wget python3-dev python3-venv python3-wheel libfreetype6-dev libxml2-dev libzip-dev \
     libldap2-dev libsasl2-dev python3-setuptools node-less libjpeg-dev zlib1g-dev libpq-dev libxslt1-dev libldap2-dev \
     libtiff5-dev  libopenjp2-7-dev liblcms2-dev libwebp-dev libharfbuzz-dev libfribidi-dev libxcb1-dev
# RUN useradd -m -d /opt/odoo -U -r -s /bin/bash odoo
# RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.bionic_amd64.deb
# RUN apt install -y ./wkhtmltox_0.12.5-1.bionic_amd64.deb
# RUN sudo su - odoo
# RUN cd /opt/odoo
COPY . .
# RUN python3 -m venv venv
# RUN source venv/bin/activate
RUN pip3 install setuptools wheel
RUN pip3 install -r requirements.txt
# RUN deactivate
# RUN exit
COPY ./debian/odoo.conf /etc/odoo.conf
CMD ["python3", "odoo-bin", "--addons-path=addons", "-d", "odoo"]

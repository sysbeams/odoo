FROM python:3.8
WORKDIR /app
RUN apt upgrade -y && apt update -y
RUN apt install postgresql postgresql-client
EXPOSE 5432
RUN sudo -u postgres createuser -s $USER
RUN createdb $USER
RUN apt install -y build-essential wget python3-dev python3-venv python3-wheel libfreetype6-dev libxml2-dev libzip-dev \
     libldap2-dev libsasl2-dev python3-setuptools node-less libjpeg-dev zlib1g-dev libpq-dev libxslt1-dev libldap2-dev \
     libtiff5-dev libjpeg8-dev libopenjp2-7-dev liblcms2-dev libwebp-dev libharfbuzz-dev libfribidi-dev libxcb1-dev \
COPY . .
RUN pip3 install setuptools wheel
RUN pip3 install -r requirements.txt
EXPOSE 80
COPY debian/odoo.conf /etc/odoo.conf
CMD ["python3", "odoo-bin", "--addons-path=addons", "-d", "odoo"]
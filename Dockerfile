FROM python:3.8
WORKDIR /app
RUN pip install setuptools wheel
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "odoo-bin", "-r", "${POSTGRES_USER}", "-w", "${POSTGRES_PASSWORD}", "--addons-path=addons", "-d", "${POSTGRES_DB}" ]
# Python and Linux Version
FROM python:3.10.0a1-alpine3.12

COPY requirements.txt /app/requirements.txt

# Configure server
RUN set -ex \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt


# Working directory

ADD . .

#EXPOSE 8000

#CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "vendescrow.wsgi:application"]

CMD gunicorn vendescrow.wsgi:application --bind 0.0.0.0:$PORT
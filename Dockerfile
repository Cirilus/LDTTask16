FROM python:3.10.9

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

RUN useradd -rms /bin/bash project && chmod 777 /opt /run

WORKDIR /project

RUN mkdir -p /static && mkdir -p /media && chown -R project:project /project && chmod 777 /project
COPY --chown=project:project . .

RUN pip install -r requirements.txt
USER root

CMD ["gunicorn","-b","0.0.0.0:8000","project.wsgi:application"]

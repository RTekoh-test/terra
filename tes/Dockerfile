FROM python:3

COPY . /terratattle

WORKDIR /terratattle/web

RUN pip install --no-cache-dir -r requirements.txt 

VOLUME ["cache"]

EXPOSE 80

CMD [ "uwsgi", "--ini", "uwsgi.ini" ]

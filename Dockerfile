FROM python:3
RUN mkdir /var/www
RUN mkdir /var/www/starwarsapi
WORKDIR /var/www/starwarsapi
COPY . /var/www/starwarsapi/
RUN pip install -r requirements.txt


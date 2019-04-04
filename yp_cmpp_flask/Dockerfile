FROM python
COPY . /server/
WORKDIR /server
RUN pip install flask
RUN pip install gunicorn
RUN pip install PyMySQL
EXPOSE 9994
CMD gunicorn -b 0.0.0.0:9994 -w 1 server:app


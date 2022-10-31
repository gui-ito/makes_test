RUN apt-get update -y \
    && apt-get install -y python-pip python-dev default-libmysqlclient-dev python-mysqldb

ENV ENVIRONMENT=""
ENV SQLALCHEMY_DATABASE_URI="mysql://{database_user}:{database_pwd}@{database_host}/{database_schema}"

RUN pip install -r requirements.txt
RUN pip install mysqlclient

EXPOSE 5000

CMD ["python", "/opt/makes_test/run.py"]
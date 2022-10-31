# Makes TEST - User Management


## Requirements
You need those things below:
* [Python 3.9+](https://www.python.org/)
* [pip](https://pypi.org/)


## Monitoring
|Tipo|Endpoint| OK
|---|---|---
|API| /health | 200 


## Getting started

#### Define environment variables
Having a MySQL localhost database, you just need to define these environment variables to connect to database:
```
ENVIRONMENT = 'PRODUCTION'
SQLALCHEMY_DATABASE_URI = 'mysql://{database_user}:{database_pwd}@{host}:{port}/{schema}'
```
This variables are in Dockerfile to be defined.

If this environment variables are not set, ```sqlite``` will be used.
#### Run pip install
``` pip install --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt ```

#### To run the application
``` python run.py ```

## Documentation
Running the application locally, you can try this api from its [Swagger UI](https://swagger.io/tools/swagger-ui/).
http://127.0.0.1:5000/apidocs/
# E Study Backend
This repository contains the backend code for E Study.

E Study is an Academic Management System inspired by google classroom. The Application provides basic functionalities for managing data of a class.

## How to Install and Run
Create a virtual enviornment and activate it.

Install the dependencies
```bash
  pip install -r requirements.txt
```
Create a .env file with the following variables.
```bash
SECRET_KEY=#Your Secret
DEBUG=#True or False
DB_NAME=#Database Name
DB_USER=#Database Username
DB_PASSWORD=#Database Password
DB_PORT=#Database Port
DB_HOST=#Database host
```
Migrate the model changes to the database
```bash
  python manage.py migrate
```

Run the server
```bash
  python manage.py runserver
```

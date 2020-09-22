# TravLog REST API

## Steps to get the TravLog API started

1. Create a new directory in your terminal. Clone down this repository by clicking the "Clone or Download" button above, copying the SSH key, and running the following command in your terminal `git clone sshKeyGoesHere`
2. `cd travlogapi`
- `python -m venv travlogEnv`
- `source ./travlogEnv/bin/activate`
3. Install the app's dependencies:
- `pip install -r requirements.txt`
4. Build your database from the existing models:
- `python manage.py makemigrations travlogapi`
- `python manage.py migrate`
5. Fire up your dev server and have some fun!
- `python manage.py runserver`

## Front-End Client
- This API is dependent on the front-end client. You can find it here: https://github.com/ronaldo1618/travlog-react

## Fetch calls

Should you choose leverage this API for your own front-end application, please note that you will need to pass the Token in the headers for most requests.

## ERD

![](https://i.imgur.com/8VE7U85.png)
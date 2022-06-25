# basic_django
Base project with custom user/authentication with rest api included.


# Celery Services
..To start celery worker
> celery -A basic.celery worker --pool=solo -l info

..To start celery-beat
> celery -A basic beat -l info


# Deploy on Heroku
.. To deploy on heroku
>> create file runtime.txt
> python-3.8.10

>> create file Profile
> web: gunicorn basic.wsgi --log-file -

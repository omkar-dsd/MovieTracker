web:python manage.py runserver
web: gunicorn MovieTracker.MovieTracker.wsgi --log-file -
heroku ps:scale web=1

Set the environment variables first

export DATABASE_URL=postgres://(user):(password)@localhost:5432/ooo


Then run run.sh

Create users:
http://localhost:8000/match/admin

Main page:
http://localhost:8000/match

How to update the database:
python manage.py makemigrations
python manage.py migrate

How to create the admin account:
python manage.py createsuperuser

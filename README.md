# jTunes
 
See ./Project Proposal.pdf for project description.

# Using jTunes:

1. You need python already set up.
2. Install postgreSQL: https://www.postgresql.org/download/
3. Create a database: https://www.guru99.com/postgresql-create-database.html
4. Clone this repository
5. Replace the DATABASE variable in /jTunesv2/settings.py with this, changing the dict values as appropriate:
~~~
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'jtunes',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
~~~
6. Open a terminal and cd to the repository clone
7. Run `python -m venv jTunesVenv`
8. Run `.\jTunesVenv\Scripts\activate`
9. Run `pip install django`
10. Run `pip install psycopg2`
11. Run `pip install sqlparse`
12. Run `cd jTunesv2`
13. Run `python manage.py makemigrations`
14. Run `python manage.py migrate`
15. Run `python manage.py runserver`
16. Go to http://127.0.0.1:8000/jTunes in your browser

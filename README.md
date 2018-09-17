# SSPBrnoProjectsWeb
This is repo of team project for our school.


## Installation

* Check out [SSPBrnoProjectsWeb](https://github.com/ocasek/SSPBrnoProjectsWeb)
* `cd` to `SSPBrnoProjectsWeb/web`
* Run:
  `pip install -r requirements.txt`

## How to run

### Starting the server
`python manage.py runserver`

### If you have some issues with DB try
`python manage.py makemigrations`
`python manage.py migrate`


If it doesn't work, check your Python version.

### Admin side of website
Web does not have default admin user to control data. You need to create it.
`python manage.py createsuperuser`

# Julius_App


## Quickstart ##

Make sure you have [pipenv installed](https://docs.pipenv.org/install.html). Then install Django in your virtualenv:

    pip install django==2.2.11
    
Clone this repository
    
    git clone https://github.com/dutraleonardo/julius-app.git
    
To create a new Django project (make sure to change `project_name`)

    django-admin.py startproject -e py,md,yml,ini,example -n Procfile --template python-django-project-template project_name

Install dependence

    make
    
Run project

    make up
    
Stop project 
    
    make stop
    
Create apps for project 

    make startapp name=<APP_NAME>
    mv <APP_NAME> project_name/apps/<APP_NAME>
    
Install packages 

    make install package=<PACKAGE_NAME>
    make build
    
Run tests
    
    make test


Run in heroku
    
    heroku login
    heroku apps:create <PROJECT_NAME>
    heroku config:edit (Add envoriments variables and save)
    git push heroku master
    
A simple user model is defined using email as username.
The account manage is made with [dj-rest-auth](https://dj-rest-auth.readthedocs.io/en/latest/index.html) and 
[django-allauth](https://django-allauth.readthedocs.io/en/latest/).

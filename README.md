### IBU_backend

#### Development setup

- Clone this repo and navigate into the project's directory

  - `$ git clone https://github.com/arthuroe/ibu_backend && cd ibu_backend`

- Create a python3 virtual environment for the project and activate it.

  - To install the virtual environment wrapper `mkvirtualenv` you can follow [this](https://jamie.curle.io/installing-pip-virtualenv-and-virtualenvwrapper-on-os-x).
  - `$ mkvirtualenv --py=python3 fp`

- Copy `.env.sample` into `.env` in the base folder of the project. You should adjust it according to your own local settings.

- Install the project's requirements

  - `$ pip install -r requirements.txt`

- Setup postgresql database

  - `$ create a database`
  - `$ create user`

- Run Migrations for the database

  - `$ python3 manage.py db init`
  - `$ python3 manage.py db migrate`
  - `$ python3 manage.py db upgrade`

- Export the environment variables in the .env

  - `$ export $(cat .env)`


- Run the application
  - `$ flask run`

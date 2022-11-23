# Points Transfer
## Installation

- Clone the repository

- Setup Environment Variables;

  - On `\pointsTransfer\pointsTransfer`

    - Import or create a **.env** file

      - Variables needed for **this project**:

        - **SECRET_KEY**=<Django generated secret key ([not the default](https://humberto.io/blog/tldr-generate-django-secret-key/))>

          **ALLOWED_HOSTS**=<allowed hosts IP's and/or domain name>

          **CSRF_TRUSTED_ORIGINS**=< Trusted request origins full URL or IP>

          **DEBUG**=True (remove this one for production mode)

- Run initial management commands

  - On `\pointsTransfer\pointsTransfer`
    - Create the database Migrations
      - `python .\manage.py makemigrations` 
    - Run the Migrations
      - `python .\manage.py migrate`
    
- Create a Super User for testing
  - On `\pointsTransfer\pointsTransfer`
    - ` python .\manage.py createsuperuser` 

- Run the project
  - On `\pointsTransfer\pointsTransfer`
    - ` python .\manage.py runserver`
    
- Access the admin panel
  - Go to http://localhost:8000
    - Port may differ if you change it on "runserver" command.
  
### Docker File: Build and run application image only

- First step

- Build application image 
  - `docker build --tag points-transfer .`
- Run application image 
  - `docker run --publish 8000:8000 points-transfer`

- Second step

- Run initial management commands

  - Open interactive terminal on
    - `docker exec -it points-transfer /bin/bash`
    - Create the database Migrations
      - `python .\manage.py makemigrations` 
    - Run the Migrations
      - `python .\manage.py migrate`
    - Create a Super User for testing
      - `python .\manage.py createsuperuser` 
 
- Access the admin panel
  - Go to 127.0.0.1:8000
    - Port may differ if you change it on "runserver" command.

### Docker Compose: Build and run application, database and other services

- First step

  - Build services (application and database)
    - `docker-compose build`
  - Run services (application and database)
    - `docker-compose up`

- Second step 

 - Run initial management commands

  - Open interactive terminal on
    - `docker exec -it points-transfer /bin/bash`
 
  - Create the database Migrations
    - `python .\manage.py makemigrations` 
  - Run the Migrations
    - `python .\manage.py migrate`

- Third step 

  - Stop, rebuild and run again the images to apply the changes
    - `docker-compose stop`
    - `docker-compose build`
    - `docker-compose up`
  - Create a Super User for testing
    - `python .\manage.py createsuperuser` 
  
- Access the admin panel
  - Go to 127.0.0.1:8000
    - Port may differ if you change it on "runserver" command.

Obs: If any changes are made to the application code, database or other services, build and run the images again.



# Property Information Management System

This Django application manages property information using Django admin. It allows for storing and managing property details, including images, locations, and amenities.

## Features

- Django-based property management system
- PostgreSQL database integration
- Django ORM for database operations
- Django Admin interface for CRUD operations
- CLI application for data migration from Scrapy project

## Requirements

- Python 3.x
- Django
- PostgreSQL
- psycopg2 (PostgreSQL adapter for Python)

## Revision:
- As in the scrapy project image downloading was missing in my case i have update the project and some changes have been made also in the structure of the project so project link is given below. Requested to run that project before running this django project.

  link: https://github.com/YasinRafin01/Scrapy_Project

## Installation

1. Clone the repository:
   
   ```
   git clone https://github.com/YasinRafin01/Django
   cd Django
   code .
   ```
2. Create a virtual environment and activate it:
  ```
  python3 -m venv venv
  source venv/bin/activate  # On Windows, use venv\Scripts\activate
  ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
## Database Configuration:

1. For Django Database configuration following steps required
   - Open Linux/Mac Terminal and type
     ```
     nano ~/.pg_service.conf
     ```
   - Then put the following configuration, Save and exit
     ```
     [my_service]
     host=localhost
     user=postgres
     dbname= your_database_name
     port= your_port_number
     password= your_password
     ```
2. For Scrapy Databse Connection go to projects config.py and edit the following:
   ```
   DATABASE_URL = "postgresql://username:your_password@localhost:port_number/scrapy_database_name"
   
   ```
3. For Scrapy local image storage go to projects config.py and edit the following with your scrapy image storage directory:
   ```
   SCRAPY_IMAGE_DIR = 'local_storage directory where scrapy images are stored'
   
   ```
## Run Migrations:

   - In the  project run migrations
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
## Data Transfer from Scrapy Database To Django Database through CLI:
   
   1. Run the following command to transfer the existing datas from scrapy database
      ```
      python manage.py migrate_scrapy_data
      ```
   2. As there was no field for Amenities in the Scrapy database I have put another option to fetch Amenities from the website and put it into our Django database of the corresponding hotel for that run the following command:
      ```
      python manage.py update_amenities
      ```
   3. After doing this our images will be stored automatically in a file named `media`. You can go there and check the downloaded images.
      
## CRUD Operation:
   All our datas are now stored in the database. For CRUD operation follow the steps:
   1. First create a superuser by following command:
      ```
      python manage.py createsuperuser
      ```
  2. After creating the superuser do the following:
     
       - Start the Django development server:
            ```
             python manage.py runserver
     
            ```
       - Access the Django Admin interface at `http://localhost:8000/admin/` and log in with your superuser credentials.
         
       - Use the Admin interface to manage property information, including creating, reading, updating, and deleting properties, locations, and amenities.

## Project Structure
- `Django/`
  - `Django_trip/` 
      - `__init__.py`
      - `asgi.py`
      - `settings.py`
      - `urls.py`
      - `wsgi.py`
  - `Hotel_info/`
      - `management/`
        - `commands/`
           - `migrate_scrapy_data.py`
           -  `update_amenities.py`
      - `migrations/`
         - `__init__.py`   
      - `__init__.py` 
      - `admin.py`
      - `apps.py`
      - `models.py` 
      - `tests.py` 
      - `views.py`
  - `.gitignore`
  - `config.py`
  - `manage.py`
  - `requirements.txt`



## Models

- Property
- Location
- Amenity
- Image

For detailed model structures, please refer to the `models.py` file in the `Hotel_info` app.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.


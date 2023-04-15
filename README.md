# MAKTABA CHALLENGE

## Description
This is a program attempts to manage big data.

## Requirements
- Python 3.6 or higher
- Pip installed on your system
- Git installed on your system

Install Python 3.6 or higher from [here](https://www.python.org/downloads/). Or use the following command in the terminal:
```
$ sudo apt install python3
$ sudo apt install python3-pip

```

## Installation
Clone the repository to your local machine:
```
$ git clone https://github.com/PatrickMamsery/maktaba_challenge.git
```

## Setup
For unix systems, run the following commands in the terminal:
```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

## Running the program
Navigate to the project directory.
To run the program, run the following commands in the terminal:
```
$ python3 manage.py migrate
``` 
This creates a minimal database with the necessary tables.
```
$ python3 manage.py createsuperuser
```
This creates a superuser with the necessary permissions to access the admin panel.

Then start the development server. Run the following command in the terminal:
```
$ python3 manage.py runserver
```
You can now access the admin panel at `http://localhost:8000/`

## Usage
To use the program, you need to upload a csv file containing the data. But first you need to be logged in. You can login using credentials input while creating the superuser.

The logged-in user will be directed to upload page where they can upload any CSV file, view it and then save it to the database. The user can also view the data in the database.

<!-- ## Testing
To run the tests, run the following command in the terminal:
```
$ python3 manage.py test
``` -->
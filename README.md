
MobileStop

This project is an e-commerce website for selling mobile phones and related accessories. The website features a user-friendly interface where customers can browse the available products, read detailed descriptions, and view high-quality images. Customers can add products to their cart and proceed to checkout, where they can securely complete their purchase. The website is built using HTML, CSS, and JavaScript, with a backend powered by a server-side programming language such as PHP or Python. This project aims to provide a seamless online shopping experience for customers looking to purchase mobile phones and accessories.

## Technologies Used in project.
Django Framework (Backend)
HTML, CSS, JS (FrontEnd)
Django REST (API Fetching.)

## Features
- Welcome Landing Page
- Products Category Page.
- About Us Page.
- Contact Us page.
- User Profile.
- User Login and Register.
- Add To Cart & Buy Now option.
- RazorPay Payment Option.
- Mobile Searching.
- Change Passowrd.

## Software Required.
- Django
- Python (Version - 3.10.7)
- VS Code
- Postgres

## Installation Steps
- Install all the required softwares properly.

Open the "mobileStop" folder in any code editor (Ex: VS Code).

Now open the terminal in the editor.

To install all of Python's required packages and libraries, we must execute:

```cmd
pip install -r requirements.txt (For windows)

pip3 install -r requirements.txt (For Mac)
```
- After the installation of all packages.

- Setup Postgres by :-
```code
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": <NAME_OF_YOUR_DATABASE>,
        "USER": "postgres",
        "PASSWORD": <PASSWORD>,
        "HOST": "localhost",
        "PORT": "<PORT NO>",
    }
}
```
- After the database is created. Run the following commands for migrations.
```cmd
python manage.py makemigrations
python manage.py migrate
```
- Now you can run the server by the command.
```cmd
python manage.py runserver
```
- A link will occur in terminal by clicking on it or simply type in your browser (Prefer - Chrome)
```code
localhost:8000
```

**Note**
Create the Virtualenv for good practice.
First register yourself, then Login
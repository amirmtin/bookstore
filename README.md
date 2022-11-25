# bookstore site

<img src="https://static.djangoproject.com/img/icon-touch.e4872c4da341.png">

### prerequisite :
- python 3.8
- postresql

## run localy

1. create environment variables
    - SECRET_KEY
    - DB_NAME
    - DB_USER
    - DB_HOST
    - DB_PORT
    - DB_PASSWORD
    - EMAIL_HOST_USER
    - EMAIL_HOST_PASSWORD
    - IDPAY_API_KEY
2. clone repository
```
git clone https://github.com/amirmtin/bookstore
cd bookstore
```
3. create virtualenv and activate
```
python -m virtualenv env
   
# in linux and mac 
source env/bin/activate
   
# in windows
./env/Scripts/activate
```
4. install packages 
```
pip install -r requirements.txt
```
5. setup database
```
python manage.py makemigrations
python manage.py migrate
```
6. run server
```
python manage.py runserver
```
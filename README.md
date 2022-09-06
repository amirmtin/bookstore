<h1 align="center"> 
  bookstore site
</h1>

<img src="https://static.djangoproject.com/img/icon-touch.e4872c4da341.png">
<img src="https://getbootstrap.com/docs/5.0/assets/img/favicons/apple-touch-icon.png">
<h3 align="center"> 
   bookstore website developed with django and bootstrap
</h3>
<h3 align="center"> 
    run locally
</h3>
  
  
first add your gmail, password and IDPAY API_TOKEN to *core/settings.py* lines 145 and 147


```console
# clone repository
amirmtin@linuxmint:~$ git clone https://github.com/amirmtin/bookstore
amirmtin@linuxmint:~$ cd bookstore

# create virtualenv
amirmtin@linuxmint:~$ python -m virtualenv env

# active env
amirmtin@linuxmint:~$ source env/bin/activate

# install packages
amirmtin@linuxmint:~$ pip install -r requirements.txt

# create database
amirmtin@linuxmint:~$ python manage.py makemigrations
amirmtin@linuxmint:~$ python manage.py migrate

# run
amirmtin@linuxmint:~$ python manage.py runserver

```
  
<h2 align="center"> 
    screen shots
</h2>

<img src="./screenshot/Workspace 1_001.png"> 
<br><br><br><br>
<img src="./screenshot/Workspace 1_002.png">
<br><br><br><br>
<img src="./screenshot/Workspace 1_003.png">


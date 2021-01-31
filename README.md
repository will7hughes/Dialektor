## Installation and Setup

As usual, start with a git clone, <br>
```
git clone https://github.com/will7hughes/Dialektor.git
```
### Setup Docker for Local Development
To understand the decision to use Docker for our development environment. Read this article: https://www.untangled.dev/2020/05/30/why-docker-local-development/ <br>
Then, to get the basics of what Docker is, read this https://vsupalov.com/6-docker-basics/ <br>

Install Docker Desktop: https://www.docker.com/products/docker-desktop <br>
Follow installation prompts from docker desktop for extra configuration setup. For example, I had to copy/paste and run a powershell command for WSL. I also had to do step 4 from this site: https://docs.microsoft.com/en-us/windows/wsl/install-win10#step-4---download-the-linux-kernel-update-package. <br>
Restart your computer, if prompted to. <br>

We will follow the setup tutorial here with slight modifications of database and user names. Below is the exact command list: https://www.untangled.dev/2020/06/06/docker-django-local-dev/ <br>

Start up the contianer
```
docker-compose up
```
Verify that there are two containers up 
```
docker ps
```
Connect to the `db` docker container in a seperate terminal/powershell window
```
docker-compose exec db sh
```
Open `psql` as user `postgres`
```
su - postgres -c psql
```
Create the database
```
CREATE DATABASE dialektorlocaldb
```
Create the user
```
CREATE USER dialektoruser WITH PASSWORD 'password'
```
Setup user roles
```
ALTER ROLE dialektoruser SET client_encoding TO 'utf8'
ALTER ROLE dialektoruser SET default_transaction_isolation TO 'read committed'
ALTER ROLE dialektoruser SET timezone TO 'UTC'
```
Grant user privileges
```
GRANT ALL PRIVILEGES ON DATABASE dialektorlocaldb TO dialektoruser
```
The `db` docker container is now configured with a database named, `dialektorlocaldb` and a user, `dialektoruser`<br>
We will now setup the `web` docker container<br>
Exit `psql` and `db` docker OR open a new terminal\powershell<br>
Exit `psql`
```
\q
```
Exit `db` container
```
exit
```
Enter the `web` container<br>
```
docker-compose exec web sh
```
Apply database migrations. This creates the tables defined in our django application and creates them in our PostgreSQL database we just configured.
```
python manage.py migrate
```
Create a superuser to login to the django admin console
```
python manage.py createsuperuser
```
You can now go to `http://localhost:8000/admin` and login with the superuser you created<br>
If you forget your password. Just re-run the createsuper command above<br>
You have now completely setup the development environment<br>

# STOP The rest of the instructions are under revision
#### Activate virtual python environment
Windows:
```
venv\Scripts\activate.bat
```
#### Install requirements
Make sure you are invoking pip with python3 and not python 2.7<br>
Depending on how you have setup pip, you can use pip3 to invoke as python3<br>
I choose to be extra verbose and specify with the below command<br>
Windows:
```
python3 -m pip install -r requirements.txt
```

#### Start Development Local Server
Windows:
```cmd
python manage.py runserver
```

linux
```bash
chmod +x manage.py 
./manage.py runserver
```
After this step the Development server will start working. 
You should be able to see the website on 
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)


#### Run Unit Tests
```bash
python manage.py test
```

#### Deployment on google cloud:
Each time after few feature implemented, I will be updating it to the Google cloud.
I am thinking to assign a version number to each upload as something like a release version. 

If you like to try it on your own google cloud account, I suggest you to follow the instructions on 
this link:

[Deploying a Django Application to Google App Engine](https://medium.com/@BennettGarner/deploying-a-django-application-to-google-app-engine-f9c91a30bd35)

# Dialektor Development Team
Group APYZ CS 4263 Software Engineering Capstone Project
Group 11 CS 4273 Software Engineering Capstone Project

Under supervision of:<br> 
Dr. Rafal Jabrzemski

TEAM: APYZ

Adam Gracy<br>
Phillip Voss<br>
Yashar G. Ahari<br>
Zachary Arani<br>

TEAM: 11

Will Hughes<br>
Lieu Dean<br>
Jason Myers<br>

[what is Dialektor](./Documentation/Dialektor.md)

### Version Info
Current version on Google Cloud: Beta-0 
[dialekt.appspot.com_version_Beta-0](https://dialekt.appspot.com/)

About Version Beta-0:<br>
Beta-0 is the almost finished version of the final product, lacking the final cosmetic touches and the researchers page and functionality. The sound recording, playback, storage, profile, collection all functional. 

Next version: 1.0.0

### Important notes: 

#### Google Cloud
You may notice there are 3 files that are not part of a usual 
Django app. 
1. app.yaml <br>
This files contains the configuration to run the app in google cloud app engine.
2. requirements.txt <br> 
This is the file that can get by ```pip freeze > requirements.txt```. Contains all the project python dependencies.
Google cloud will look for this file and install all the listed packages.
3. main.py <br>
Google app engine looks for this file to starts the our application. In this file, we just restate our 
wsgi choice. 

This is a great article about the process:<br>
[Deploying a Django Application to Google App Engine](https://medium.com/@BennettGarner/deploying-a-django-application-to-google-app-engine-f9c91a30bd35)




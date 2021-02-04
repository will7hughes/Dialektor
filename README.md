
# Dialektor
Version: 1.0.1<br>

Table of Contents
=================

<!--ts-->
   * [Setup Docker for Local Development](#setup-docker-for-local-development)
   * [Visual Studio Code Setup](#visual-studio-code-setup)
   * [Development Lifecyle](#Development-Lifecyle)
   * [Command Reference List](#Command-Reference-List)
      * [Docker](#Docker)
      * [Django](#Django)
      * [GitHub](#GitHub)
   * [Dialektor Development Team](#Dialektor-Development-Team)
<!--te-->

Setup Docker for Local Development
============

As usual, start with a git clone <br>
```
git clone https://github.com/will7hughes/Dialektor.git
```
Change directory to the Dialektor project
```
cd Dialektor
```
Install Docker Desktop<br>
https://www.docker.com/products/docker-desktop <br>

Follow installation prompts from docker desktop for `extra configuration setup`. <br>
For example, I had to copy/paste and run a `powershell command for WSL`. <br>
I also had to do `step 4` from this site: https://docs.microsoft.com/en-us/windows/wsl/install-win10#step-4---download-the-linux-kernel-update-package. <br>

Restart your computer

Create the container
```
docker-compose create
```
Startup the container
```
docker-compose up
```
Verify that there are two containers up `db` and `web`
```
docker ps
```
Enter the `web` container<br>
```
docker-compose exec web sh
```
Create first time migrations on the personal app. <br>
This create the tables defined in models.py and creates them in our PostgreSQL database.<br>
You only have to do this for first time setup<br>
Every other time you just do the migrations without specifying the `personal` app<br>
Django will know that `personal` app exists and will make the migration along with the `default` app
```
python manage.py makemigrations personal
python manage.py migrate personal
```
Apply database migrations to the default app. <br>
This creates the tables defined in our django application and creates them in our PostgreSQL database we just configured.<br>
```
python manage.py makemigrations
python manage.py migrate
```
Create a superuser to login to the django admin console
```
python manage.py createsuperuser
```
Start django localhost website
```
python manage.py runserver
```
You can now go to `http://127.0.0.1:8000/admin` and login with the superuser you created<br>
If you forget your password. Just re-run the createsuper command above<br>
You have now completely setup the development environment<br>
[Table of Contents](#Dialektor)

Visual Studio Code Setup
============
Download Here: https://code.visualstudio.com/download<br>
Install Pluggin Remote - Containers: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers<br>
Make sure Docker is running<br>
If you close Docker with `Ctrl+C` your VS Code window will disconnect<br>
```
docker-compose up
```
If you develop `without being connected` to the Docker you will have to rebuild the docker `web` container for changes to make effect<br>
Note that code changes take immediate effect when you save a file<br>
If you write something that throws an error. You may have to develop locally, `without Docker`<br>
Fix the error. And rebuild the `web` container<br>
To rebuild `web` container run<br>
```
docker-compose build web
```
Once Docker is up and running and is not throwing any errors<br>
Connect to the Docker Container in VS Code<br>
VS Code -> View -> Command Palette -> `search` Attach -> Attach to Running Containers<br>
It will then prompt you to select `db` or `web`<br>
Select `web`<br>
Navigate to the folder<br>
VS Code -> File -> Open Folder -> `/code/` -> Ok<br>
You can now edit and develop right from VS Code as if you were on your local machine<br>
Make sure that you are connected to the `Container` by looking at the bottom left green area <br>
It should say `Container dialektor_web (/web)`<br><br>

Connect to VS Code terminal to startup localhost django website<br>
VS Code -> Terminal -> New Terminal<br>
Change directory
```
cd code
```
Start localhost development website
```
python manage.py runserver
```
You can now go to http://127.0.0.1:8000 to view your localhost website while you develop<br>
You can shutdown the website by going to the console and using the key combination
```
Ctr + C
```
[Table of Contents](#Dialektor)

Development Lifecyle
============
Create a feature branch<br>
DO NOT WORK ON THE MASTER BRANCH ON YOUR LOCAL DEVELOPMENT!!!!!!!!!!!<br>
DO NOT MERGE TO THE MASTER BRANCH ON YOUR LOCAL DEVELOPMENT!!!!!!!!!<br>
DO NOT TOUCH THE MASTER BRANCH ON YOUR LOCAL DEVELOPMENT!!!!!!!!!!<br>
Note that you can run these git commands directly from the VS Code terminal while connected to Docker `web` component
```
git branch 1.0.1-john
```
The naming convention for a feature branch is X.X.X-firstname. <br>
Where X(major)-X(minor)-X(point) are version codes<br><br>
Checkout your feature branch
```
git checkout 1.0.1-john
```
Assign yourself on an issue in Github or create an issue that describes what you will do in this update<br>
Code your update, feature, bug fix, ui fix, etc<br>
Add changes to staging on git<br>
Frequently `add`, and `commit` you code<br>
```
git add *
```
Verify that you are adding the files you have updated
```
git status
```
Commit the changes. Add a descriptive message about a feature, bug fix, ui change, etc.
```
git commit -m "My super duper descriptive message about all the new goodies I just did"
```
Push changes to remote repo. <br>
DO NOT WORK ON THE MASTER BRANCH ON YOUR LOCAL DEVELOPMENT!!!!!!!!!!!<br>
Always develop on a feature branch. For example, `1.0.1-will`<br>
See Development guide above for checking out or creating a feature branch<br>
```
git push origin 1.0.1-will
```
Create a pull request on github<br>
I `Will` will manage the pull requests for the first couple weeks for quality assurance<br>
I will use the pull requests to merge the feature branch into the master branch<br>
I will also be managing Kubernetes deployment until you've made several pull requests and shown you've got that down<br>
Don't worry about production deployment until you've handled local development<br>
[Table of Contents](#Dialektor)

Command Reference List
============

Docker
-----
Startup
```
docker-compose up
```
Create the Container
```
docker-compose create
```
List Running Apps
```
docker ps
```
Enter the `web` App
```
docker-compose exec web sh
```
Enter the `db` App (Local PostgreSQL Database)
```
docker-compose exec db sh
```
Build/Rebuild apps
```
docker-compose build
```

Django
-----
Start Localhost Dev Site at <br>
http://127.0.0.1:8080 <br>
Admin: http://127.0.0.1:8080/admin <br>
NOTE: Must be run inside Docker `web` app<br>
NOTE: Can be run inside Visual Studio Code terminal when VS Code is connected to Docker Container `web` app<br>
```
python manage.py runserver
```
Shutdown Localhost Dev Site<br>
NOTE: Must be used on same terminal/console window that ran the server with the above command
```
Ctrl + C
```
Stage Database Migrations<br>
NOTE: Change out `personal` for whatever app that contains the `models.py` for the Database Model that you have changed<br>
NOTE: You can leave out `personal` to makemigrations for all apps. Provided this is not the first time you are making the migrations<br>
```
python manage.py makemigrations personal
```
Migrate Database<br>
Applies the migrations that were staged from the above command<br>
NOTE: You can leave out `personal` to migrate for all apps. Provided this is not the first time you are migrating<br>
```
python manage.py migrate personal
```
Create Admin<br>
http://127.0.0.1:8080/admin
```
python manage.py createsuperuser
```

GitHub
-----
Create a Branch<br>
```
git branch BRANCH_NAME
```
Checkout Branch
```
git checkout BRANCH_NAME
```
Create and Checkout Branch
```
git checkout -b BRANCH_NAME
```
Add Changes to Staging Area<br>
```
git add *
```
View Staging
```
git status
```
Commit
```
git commit -m "My super duper descriptive message about all the new goodies I just did"
```
Pull
```
git pull origin BRANCH_NAME
```
Push
```
git push origin BRANCH_NAME
```

Dialektor Development Team
============
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
[Table of Contents](#Dialektor)

Sources Cited
============
To understand the decision to use Docker for our development environment. <br>
Read this article: https://www.untangled.dev/2020/05/30/why-docker-local-development/ <br>
Then, to get the basics of what Docker is, read this https://vsupalov.com/6-docker-basics/ <br>
https://www.untangled.dev/2020/06/06/docker-django-local-dev/
[Table of Contents](#Dialektor)

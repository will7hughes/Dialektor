
# Dialektor
Version: 1.0.1<br>

## Setup Docker for Local Development

As usual, start with a git clone <br>
```
git clone https://github.com/will7hughes/Dialektor.git
```
Change directory to the Dialektor project
```
cd Dialektor
```
To understand the decision to use Docker for our development environment. <br>
Read this article: https://www.untangled.dev/2020/05/30/why-docker-local-development/ <br>
Then, to get the basics of what Docker is, read this https://vsupalov.com/6-docker-basics/ <br>

Install Docker Desktop: https://www.docker.com/products/docker-desktop <br>
Follow installation prompts from docker desktop for `extra configuration setup`. <br>
For example, I had to copy/paste and run a `powershell command for WSL`. <br>
I also had to do `step 4` from this site: https://docs.microsoft.com/en-us/windows/wsl/install-win10#step-4---download-the-linux-kernel-update-package. <br>
`Restart your computer`, if prompted to. <br>
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
You can now go to `http://localhost:8080/admin` and login with the superuser you created<br>
If you forget your password. Just re-run the createsuper command above<br>
You have now completely setup the development environment<br>

## Development Lifecyle
Create a feature branch<br>
DO NOT WORK ON THE MASTER BRANCH ON YOUR LOCAL DEVELOPMENT!!!!!!!!!!!<br>
DO NOT MERGE TO THE MASTER BRANCH ON YOUR LOCAL DEVELOPMENT!!!!!!!!!<br>
DO NOT TOUCH THE MASTER BRANCH ON YOUR LOCAL DEVELOPMENT!!!!!!!!!!<br>
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

### Dialektor Development Team
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

## Sources Cited
https://www.untangled.dev/2020/06/06/docker-django-local-dev/

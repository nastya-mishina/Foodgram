# Grocery assistant
### Description:
This is an online service where users can publish recipes, subscribe to publications of other users, add recipes they like to the favorites list, and download a summary list of products needed to prepare one or more selected dishes before going to the store.
### Website address:
http://178.154.214.43/

## Technologies:
- Python 3.8.5
- Django 3.0.5
- Nginx
- Gunicorn
- PostgreSQL

## Features

- CRUD for titles
- CRUD for reviews and comments
- CRUD for genres and categories
- Get reviews for titles
- Get comments for reviews

### Installation and getting started:
- Install Docker on your PC.
- Remove old Docker versions with the command:
```$ sudo apt remove docker docker-engine docker.io containerd runc```
- Updating the list of packages:
```$ sudo apt update```
- Install packages for download via https:
```$ sudo apt install \```
  ```apt-transport-https \```
  ```ca-certificates \```
  ```curl \```
  ```gnupg-agent \```
  ```software-properties-common -y```
- Add a GPG key for authentication during the installation process:
```$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -```
- Add the Docker repository to the apt packages:
```$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"```
- Install Docker and check if it works:
```$ sudo apt install docker-ce docker-compose -y```
```$ sudo systemctl status docker```
- Auto start docker daemon:
```$ sudo systemctl enable docker```

### Application launch:
- Collect image:
```$ docker build -t yamdb .```
- Start container:
```$ docker run -it -p 8000:8000 yamdb```
- Create a file `````.env````` in the root directory, add data there to connect to the database.
- Modifying the file ```settings.py```, so that the values are loaded from environment variables.
- Add to Dockerfile command to run the application through gunicorn.
- Create a file ```docker-compose.yaml``` in the root directory of the project and add deployment instructions.
- We check the workability:
```$ docker-compose up```
- Create a folder ```nginx/``` in the root directory of the project, and in it the file ```default.conf```. 
- In ```settings.py``` add the absolute path to the directory.
- Supplementing the file ```docker-compose.yaml``` container description nginx.
- Deploy containers in the background and rebuild before launch:
```$ docker-compose up -d --build```
- Run migrations:
```$ docker-compose exec web python manage.py migrate --noinput```
- Create superuser:
```$ docker-compose exec web python manage.py createsuperuser```
- Collect statics:
```$ docker-compose exec web python manage.py collectstatic --no-input```
- Create an image with the desired name and tag:
```$ docker build -t mishinaanast/yamdb_praktikum:v2.11.1989 .```
- We log in through the console:
```$ winpty docker login```
- Uploading the image to DockerHub:
```$  docker push mishinaanast/yamdb_praktikum:v2.11.1989```

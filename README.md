# my_django_api_docker_project

### Stack used:
- Python 3.9
- Django 3.2
- Django REST framework  
- nginx  
- mysql 5.7 (could have gone sqlite but not prod worthy)
- pytest
- uWSGI (could also have gone gunicorn)
- Django local in-memory caching
* * *
### For production deploy:
Please be patient as there is a health_check implemented on mysql as Django needs to wait for it to migrate. This stops the issue of database connection issues. Just some experience I have from working with K8s.

This will use a nginx proxy and uWSGI
```
docker-compose --env-file env_files/mysql_production.env -f docker-compose-production.yml up
```
* * *
### For local deploy with reload on change:
This is a "Bonus extra" as I used it for faster development and feel if you have prod you should have local

This runs on the normal manage.py runserver 0.0.0.0:80

```
docker-compose --env-file env_files/mysql_local.env -f docker-compose-local.yml up
```

* * *
### GET Endpoints
Coin List
```
http://localhost/coinList
```
Market Cap
```
http://localhost/marketCap?coin_id={coin_id}&currency={iso code}&date={YYYY/MM/DD}

example:
http://localhost/marketCap?coin_id=ripple&currency=GBP&date=2021/03/12
```
* * *
### Pytest
To run tests just put this command in your terminal
```
docker exec -it my_django_api_docker_project_app_1 pytest -v
```
* * *
### Scale
The app is in a container and making it possible to scale. Seeing it is a docker-compose it can be adjusted to deployed on AWS.
* * *
### uWSGI
This will allow you to add more workers as needed depending on the load.
* * *
### Security:
I have created most of the setups with user privileges and nginx-unprivileged that root user is never exposed as a successful hacking attempt can be devastating if they get root access.

This can be seen in the proxy dockerfile and root dockerfile
* * *
### Take note:

The .env is currently in the repo but should never be visible to the public but as it is a project this will be fine. 

In a real world deploy the .env would have been on the server or added to the folder securely.

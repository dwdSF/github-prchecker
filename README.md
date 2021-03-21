# github-prchecker
Application for checking github user's pull requests



## User manual
  - Clone the repository to your computer
  - Install docker if you don't have it
  - Run docker-compose
```shell
docker-compose up
```
 ## Additional options:

   - The tests cover a few of the app's features
```shell
docker-compose run app sh -c "python manage.py test checker"
```

# Social Media API
Test task

### Project Support Features
* Users can signup and login to their accounts
* Project uses token for authentication
* Swagger documentation to see all the endpoints
* Filtering by using query parameters
* Custom permissions
* Follow and unfollow users
* See your own posts and posts of your following users
### Installation Guide
* Clone this repository [here](https://github.com/Lebwa1337/social-media-api).
* The develop branch is the most stable branch at any given time, ensure you're working from it.
* Run `pip install -r requirements.txt` to install all dependencies
* Create .env file and put your secret key to .env(Watch .env_sample file).<br/>
You can generate this key [here](https://djecrety.ir)

### Usage
To launch project:
* Make sure you do all in installation guide
* Run `python manage.py runserver` or use your IDE interface
* For admin permissions you need to create superuser by running `python manage.py createsuperuser`
* Obtain token in "api/user/login/" endpoint and you good to go

### API Endpoints
Here some crucial endpoints:

| HTTP Verbs | Endpoints                | Action                                                                              |
|-----------|--------------------------|-------------------------------------------------------------------------------------|
| POST      | /api/user/register       | To register your account                                                            |
| POST      | /api/user/login          | To get your access token                                                            |
| POST      | /api/user/logout         | To logout from API                                                                  |
| GET       | /api/user/profile/<int:pk>/ | To see detail info about user(profile)                                              |
| POST      | /api/user/follow         | To follow different user                                                            |
| POST      | /api/user/unfollow       | To unfollow different user                                                          |
| GET   | /api/user/posts          | To see all your posts by default(Use query params filtering)<br/>P.S. Check swagger |
| GET       | /api/doc/swagger         | To see swagger documentation<br/>and all possible endpoints with methods            |


### Technologies Used
* [Django](https://www.djangoproject.com)
* [Django REST framework](https://www.django-rest-framework.org) 

### Database structure
![img.png](demo_files/exported_from_idea.drawio.png)

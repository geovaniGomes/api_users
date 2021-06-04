# API User permissions management

The project consists of having a **user** management where you can select **permissions** and **groups** to users. And the groups have their permissions.


## How to run the projectHow to run the project

- On your terminal type the command:
` docker-compose up --build
`

- To run the tests:
`
docker-compose run web bash
`

After accessing the application container, type the command to run the tests.


`
python manage.py test
`

Wait a while for the test to run.



After the tests are completed, run the command to perform the migrations: ` python manage.py migrate`



Finally, access the website at this link: [http://localhost:8000/](http://localhost:8000/)

# References

- [Documentação do Django](https://docs.djangoproject.com/en/3.2/)
- [Documentação do Django REST framework](https://www.django-rest-framework.org/)
- [Documentação do Factory Boy](https://factoryboy.readthedocs.io/en/stable/)

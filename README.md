# python-rabbitmq-app
 
This is a template for RabbitMQ consumer/producer application. Clone this repo and write your handlers.

#####Don`t forget to lock requirements versions

Prospector pre-commit hook
--------------------------

Prospector tool calls mypy. Mypy must be used from the same venv from sources are executed.
Thus to run prospector as a pre-commit hook it must be called from the same environment.
A solution used here is to use local pre-commit hook which calls prospector from the sh script.

[virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) is used for managing venvs.
If you use another approach change `prospector.sh` to use proper venv for prospector. 

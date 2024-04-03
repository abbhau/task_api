Project Description : This Project asign daily task to the Employer..This project includes all the concept of Api like Pagination, Custom Permissions , loggers, login and Logout functionality of User, activate the User using signals and sending mail..

How to Install and Run the Project:

1) create a virtual enviornment in your local repository and activate it create : virtualenv venv activate : venv\scripts\activate

2) change directory : cd task_pro

3) install all the deprndincies required to the project pip install -r requirnment.txt

4) run the migrate command to create an sqlite database py manage.py migrate

5) run the server by using command py manage.py runserver
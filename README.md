# ELEC5622Healthome
## Announcement
The arduino board code is developed by the group. Since the board code should be tested on the board in time, it is impossible to code seperately. Additionally, there were lots of issues when we coding the arduino board. Some team members who may not take part in the coding, they devoted their time and effors or resolving issues. **HyphenZhao submitted the code on behalf of the whole group.**

## Description
This is an application aimed to monitor people's health at home and predict if they have some disease especially for a diabetes prediction.

## Technology
+ Arduino
+ Python
+ Django

## How to Run a Test?

Notes: The repo has been changed several times. These test instructions only available under this version:
c5eb8bb478f7baa26608e26fbeae3bd6f0714d46
You should fetch this version first to run these instrunctions.

0. Make sure that your laptop has installed Python and Django properly
1. Open a terminal(for Unix or Linux) or a Command Window(for Windows)
2. Change directory into ./Healthome
3. Input command line: python manage.py test diabetes 

## How to Run the Project Locally?
0. Make sure that your laptop has installed Python and Django properly
1. Open a terminal(for Unix or Linux) or a Command Window(for Windows)
2. Change directory into ./Healthome
3. Input command line: python manage.py runserver
4. Open a browser and input this URL: http://localhost:8000/diabetes/

Note that this project is temporarily a simple website without any functions.

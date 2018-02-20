# artist catalog project
this application provides a list of artists with various projects as well as provides a user registration and authentication system. registered users have the ability to post, edit, and delete their own items.

## installation
* use a terminal
* (this program was written in python 2.7)
* download [virtualbox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
* download [vagrant](https://www.vagrantup.com/)


### cloning the code
* to copy the project on your computer, open your terminal and do this: [git clone](https://github.com/afope/africanartists.git) e.g $ `git clone <remote repo> <repo name>`
* clone the project into your vagrant folder
* you will find the **remote repo** link above by clicking on the green *"clone or download"* option in tab above the repository
* then run `cd <repo name>` in your terminal (*<repo name>* is whatever name you gave your repository in the terminal)
* this should open up the folder you just cloned from github
* open up your code editor


## usage
### running the code

to run the code run the following commands in your terminal:
* first run `vagrant up`
* then run `vagrant ssh`
* `python database_setup.py` to set up the database
* `python starterartists.py` to populate the database with default content
* `python main.py` to run the application on your local server
* the program will run on this server in your browser: http://localhost:5000/


## contribution
it's a developing archive of artists in africa and their projects, i'd like to add a search bar. 

## licensing
this code follows the [mit license](https://github.com/angular/angular.js/blob/master/LICENSE)

# Cookbook Application
## Milestone Project 3 
### Overview
This project is a CRUD application that showcases the skills and knowledge I learned while using Python in a data-centric development module. The main idea of ​​this project is to show my understanding of CRUD operations and knowledge of the Flask framework.

### User Experience Design

This website is made for a few different types of users:
1. User who wants to save most favorite recipes in internet.
2. Users who want to learn how to cook.
3. Users looking to change and update their own recipes.


### Features
CRUD is at the heart of this project to interract with an existing database of information, and with subdatbases for storing and displaying this data. I decided not to use charts in recipes because it looks not that good as i expected

The app displays the recipe, method and ingredients for each recipe on its own template page, and also allows the user to define which type of meal it is and allows them to add images to each downloadable recipe. This can also be easily changed by pulling data from the database and analyzing it in pre-filled forms so that the user can view and modify as needed.

I also implemented a feature where the usernames are tied to the recipes they have created, so only they can access the CRUD functions for their own recipes to keep them safe.

#### Potential Future Features

In the future, I would like the project to display reviews after each recipe, with a voting system to see which recipes are more popular and display this on a separate page, ranking from top to bottom.
I still want to implement charts in recipes using D3 or apexcharts.


-------
### Technologies Used
This application will make use of a few different technologies to help create a good user experience and keep load times low. 

1. Python
2. BootStrap
3. Font Awesome
4. MongoDB
5. All technologies list you can see at requirements.txt

### Testing
I needed to ensure correct DB connection.
Also i tested all parts of service separately, and of course I tested responsiveness in the free services.

Manual testing of site responsiveness was carried out on the following phone models:
1. iPhone 6/7, X
2. iPad Air and iPad Pro
3. MacbookPro 13 inches
4. Large screen sizes - Using extra Full HD screen connected to my macbook

-----
### Deployment Write-up
Doing this project took me couple of days, i know I could make it way better, and I hope i will have enough time in the future ti finish it, i see some minuses now, but I really hope that you will enjoy this project.

This project is deployed on Heroku: 
#### Setting Locally
1. Git Clone this application.
2. Mske sure that python3 and pip are installed on your desktop.
3. run ```sudo -H pip3 install -r requirements.txt```
5. run ```python3 app.py```.

##### Guides
The most helpful was Flask original documentation. I can sat literally all documentation of the technoligies I used here were read by me inside and out. 
#### Media
All images of food were sourced from free sources, as I do not own any copyright or ownership of these images.

# Little Munchkins 
[site published here](http://flask-munchkins-app.herokuapp.com/)

Little Munchkins is a website designed for parents to create and share their favourite weaning recipes. Furthermore, users are able to search and bookmark their favourite recipes provided by other users as well!

Am I Responsive?

![](/readmefiles/am-i-responsive.JPG)

Sample recipe content

![](/readmefiles/sample-recipe.JPG)

## UX

### Project Goals
- This project is intended to be a full stack site that manages a common dataset around a particular domain. In this case the domain is weaning recipes. 
- This project uses core developmental framworks such as HTML, CSS, JavaScript, Python, Flask & MongoDb. 
- Users are able to log on and create their own content for others to consume. 
- Users are also able to log on the consume content others have created. 
- Users should be able to create, read, update and delete entities relating to the collections in MongoDb. 

### User Stories

- Site Owner perspective
##### US001 As the product owner I want prospective users/providers to be greeted with an attractive Home Page, that has a simple, intuitive layout.
	- Given a user has navigated to the home page
	- When the page loads
	- Then they are met with an attractive and simple layout with relevant information

##### US002 As the product owner I want users/providers to have the ability to sign into their profile.
	- Given a user has navigated to the home page
	- When they would like to log in
	- Then they are able to navigate to the login page

	- Given the user has navigated to the login page 
	- When they fill in the form correctly 
	- Then they are redirected to their profile url.

	- Given the user has navigated to the login page 
	- When they fill in the form incorrectly 
	- Then they are given enough relevant information on their errors
 
##### US003 As the product owner I want users to be able to navigate to the different elements of the site (where their profile type allows)
	- Given the user has successfully logged in
	- When they are in any part of the site
	- Then they are able to navigate to another part easily

##### US004 As the product owner I want users to be able to contact us when necessary.
	- Given a user has navigated to the site (not necessarily logged in)
	- When they search for contact details
	- Then they are easily available 

##### US005 As the product owner I want to protect my site from malicious attempts to upload large image files.
	- Given a user is somewhere they can upload images
	- When they attempt to upload an image above a certain size
	- Then that file is rejected and they are given a dialog warning

##### US006 As the product owner I want to ensure users are given relevant and accurate informations about site operational or user errors
	- Given an operation within the application is triggered
	- When that operation fails
	- Then the user is given information pertaining to that failure


- Unregistered user perspective
##### US101 As the product owner I want users/providers to be able to register, if they are not already.
	- Given a user has navigated to the home page, and is not registered
	- When they would like to register
	- Then they are able to navigate to the register page

	- Given the user has navigated to the register page 
	- When they fill in the form correctly 
	- Then a profile is created for them and they are redirected to its url.

	- Given the user has navigated to the register page 
	- When they fill in the form incorrectly 
	- Then they are given enough relevant information on their errors

- Registered user perspective
##### US201 As a user I want to be able to login to my profile.
	- Given I have navigated to the site 
	- When I want to log in
	- Then I can easily do so

	- Given I have navigated to the login page
	- When I fill in the form correctly
	- Then I am redirected to my profile

	- Given I have navigated to the login page
	- When I fill in the form incorrectly
	- Then I can see what I have done wrong

- Logged in user perspective
##### US301 As a logged-in user I want to be able to edit my personal information.
	- Given I have succesfully logged in
	- When I am on my profile page
	- Then I can click to edit my profile information

	- Given I am editing my profile information
	- When I make the necessary changes
	- Then I am able to submit those changes

	- Given I am editing my profile information
	- When I decide I no longer wish to make the changes
	- Then I am able to cancel those changes


##### US302 As a logged-in user I want to be able to create new recipes for the site.
	- Given I have successfully logged in
	- When I navigate to the recipe builder	page
	- Then I am able to compile the recipe I want to add

	- Given I have entered data into the recipe builder
	- When I want to preview my recipe
	- Then I am directed to a page where I can see it

	- Given I am entering data into the recipe builder
	- When I want to add a new method step to the recipe
	- Then I can click somewhere to create an extension to the form

	- Given I am entering data into the recipe builder
	- When I want to add a new ingredient to the recipe
	- Then I can click somewhere to create an extension to the form

	- Given I am entering data into the recipe builder
	- When I want to delete a method step to the recipe
	- Then I can click somewhere to remove it from the form

	- Given I am entering data into the recipe builder
	- When I want to delete an ingredient to the recipe
	- Then I can click somewhere to remove it from the form

	- Given I am entering data into the recipe builder
	- When I want to add an image to the recipe
	- Then I can click somewhere to upload an image

	- Given I am entering data into the recipe builder
	- When I want to submit my recipe and the form has been compiled to mimimum validation standards
	- Then that recipe is saved and I am redirected to my profile page where it is visible in "my recipes"

	- Given I am entering data into the recipe builder
	- When I want to submit my recipe and the form has NOT been compiled to mimimum validation standards
	- Then I am prompted to the what the extra information required is

	- Given I am entering data into the recipe builder
	- When I want to reset the form
	- Then I am able to click somewhere and the form is reset to default state


##### US303 As a logged-in user I want to be able to view the recipes I have created.
	- Given I have successfully logged in
	- When I have navigated to my profile page
	- Then I can asily view the recipes I have created

##### US304 As a logged-in user I want to be able to edit the recipes I have created.
	- Given I have clicked on a recipe for editing
	- When the editor form loads
	- Then the data present there correctly refers to the recipe I wish to edit

	- Given I am editing a recipe
	- When I decide I would like to submit the changes
	- Then the recipe is saved and I am redirected to my profile page

	- Given I am editing a recipe
	- When I decide I would like to cancel the changes
	- Then no changes are saved and I am redirected to my profile page

##### US305 As a logged-in user I want to be able to delete the recipes I have created.
	- Given I have successfully logged in
	- When I click on a recipe to edit
	- Then I have somewhere to click to delete the recipe

	- Given I have deleted a recipe
	- When another user who has favourited the recipe logs in
	- Then that recipe is no longer available in their "my favourites" section

##### US306 As a logged-in user I want to be able to search for recipes provided by other users.
	- Given I have successfully logged in
	- When I navigate to the search page
	- Then I can see a search form with inputs 

	- Given I have navigated to the search page
	- When I hit submit with no search parameters
	- Then I am returned all the recipes in the database 

	- Given I have navigated to the search page
	- When I hit submit with a partial word in the name field
	- Then I am returned all the recipes that the database deems relevant to that partial word 

	- Given I have navigated to the search page
	- When I hit submit with a value in the month field
	- Then I am returned all the recipes that the database deems relevant 

 
##### US307 As a logged-in user I want to be able to favourite recipes provided by other users. 
	- Given I have searched for a recipe from another user than myself
	- When I decide I would like to save that recipe
	- Then I have somewhere to click where that recipe is added to "my favourites"

	- Given I have searched for a recipe from another user than myself
	- When I look at the recipe card
	- Then I can see if Ihave already favourited it

##### US308 As a logged-in user I want to be able to see the recipes I have favourited.
	- Given I have successfully logged in
	- When I have navigated to my profile page
	- Then I can see all the recipes I have faavourited in "my favourites" section 

##### US309 As a logged-in user I want to be able to un-favourite the recipes I have favourited.
	- Given I can see a recipe I have favourited 
	- When I decide I no longer wish it to be saved as a favourite
	- Then I have somewhere to click to remove it

##### US310 As a logged-in user I want to be able to log out.
	- Given I have successfully logged in
	- When I decide I wish to log out
	- Then I have somewhere to click where I can log out 

##### US311 As a logged-in user I want to be able to delete my profile.
	- Given I am editing my profile information
	- When I decide I wish to delete my profile
	- Then I am able to delete my profile and all my personal information

### Wireframes

Wireframes were designed using Balsamiq Wireframes and images of the slides can be viewed in the following table:

|    Wireframes   |   
|      :----:     |    
|[home](readmefiles/wireframes/wf-home.JPG)|
|[profile](readmefiles/wireframes/wf-profile.JPG)|
|[builder](readmefiles/wireframes/wf-builder.JPG)|
|[search](readmefiles/wireframes/wf-search.JPG)|
|[recipe card](readmefiles/wireframes/wf-recipecard.JPG)|

### Information Architecture 
This domain is built on two key collections: 
- user
![](/readmefiles/userobj.JPG)

- recipes
![](/readmefiles/recipeobj.JPG)

One key relationship exists between the object: when a user favourites a recipe, the _id is persisted to the "favouites" array field on the user object.  

## Features
**Home**
- Contains a large title tagline and full width/height background. 
- Contains large buttons for login/register.
- Contains some concise information about why a user should sign up.
- Contains a sample recipe card for potential users to view. 

**Header**
- Brand logo, which links to the home page
- Navigation bar with links
	
**Flash Messages**
- Operational messages displayed to the user, which then fade away after a few seconds as to not clutter view

**Footer**
- Contact email address (for demo purposes only)
- Site copyright

**Login**
- Simple validated form with username and password inputs

**Register**
- Validated registration form with fields pertaining to user information

**Profile**
- Profile information, and this is where users can edit this information too. 
- My Recipes: Where users can see the recipes they've created. 
- My Favourites: Where users can see the recipes they've favourited. 

**Search**
- Search form with two search parameters: By name, By months of child, for suitable recipes (neither are required). 

**Recipe Builder**
- Validated form where users can compile a recipe card. 
- Users are able to upload an image for the recipe here. 
- Feature to add and remove steps as desired.
- Feature to add and remove ingredients as desired.
- Button to preview the card before submission.

**Recipe Editor**
- Validated form where users can edit an already created recipe card. 
- Users are able to edit all components of the recipe card.
- Button to preview the card before submission.
- Button to cancel changes.
- Button to delete the recipe.

**Image Storage**
- This app has been developed with a common image storage location in Amazon S3. 

## Technologies

#### Development:
- [GitHub](https://github.com/) - site host.
- [Gitpod](https://gitpod.io/) - dev IDE.

#### content, styling & client logic:
- [HTML5](https://en.wikipedia.org/wiki/HTML5) - site content
- [CSS3](https://en.wikipedia.org/wiki/Cascading_Style_Sheets) - site styling
- [Materialize](https://materializecss.com/about.html) - project layout & additional styling
- [Javascript](https://en.wikipedia.org/wiki/JavaScript) - functional logic

#### Server side
- [Python](https://www.python.org/) 
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - python mirco framework for web app development
- [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) - temlating language for flask
- [Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/) - application tooling for flask
- [wtforms](https://wtforms.readthedocs.io/en/2.3.x/) - forms library for python
- [unittest](https://docs.python.org/3/library/unittest.html) - unit testing library for python

#### Persistence
- [MongoDb](https://www.mongodb.com/cloud/atlas/) - no sql cloud database infrastructure

#### Other Technologies
- [Balsamiq](https://balsamiq.com/) - wireframes and site prototype
- [GoogleFonts](https://fonts.google.com/) - font faces

## Testing

#### Code Validation

- HTML
[Home](https://validator.w3.org/nu/?doc=http%3A%2F%2Fflask-munchkins-app.herokuapp.com%2Fhome)
[Login](https://validator.w3.org/nu/?doc=http%3A%2F%2Fflask-munchkins-app.herokuapp.com%2Flogin)
[Register](https://validator.w3.org/nu/?doc=http%3A%2F%2Fflask-munchkins-app.herokuapp.com%2Fregister)
[Builder](https://validator.w3.org/nu/?doc=http%3A%2F%2Fflask-munchkins-app.herokuapp.com%2Frecipe%2Fbuilder)
[Search](https://validator.w3.org/nu/?doc=http%3A%2F%2Fflask-munchkins-app.herokuapp.com%2Frecipes%2Fsearch)

- [CSS](readmefiles/css-validation.JPG)

- [Javascript](readmefiles/js-validation.JPG) (JSHint)

- Python
[app.py](readmefiles/app-python-validation.JPG)
[app_definitions.py](readmefiles/appdefs-python-validation.JPG)
[app_test.py](readmefiles/apptest-python-validation.JPG)

#### Browser Compatibility
- **Google Chrome** No issues identified;
 
 - **Microsoft Edge** No issues identified;
   
 - **Mozilla Firefox** No issues identified;
    
 - **Opera** No issues identified;

#### Responsiveness Quality Testing  

-   Mobile - 0 issues
![](/readmefiles/mobile/m-testing.JPG)

|     iPhone5    |   
|      :----:    |
|[home](readmefiles/mobile/m-home.JPG)|
|[builder](readmefiles/mobile/m-builder.JPG)|
|[profile](readmefiles/mobile/m-profile.JPG)|
|[search](readmefiles/mobile/m-search.JPG)|
	
-   Tablet - 0 issues
![](/readmefiles/tablet/t-testing.JPG)

|     iPad    |   
|      :----:    |
|[home](readmefiles/tablet/t-home.JPG)|
|[builder](readmefiles/tablet/t-builder.JPG)|
|[profile](readmefiles/tablet/t-profile.JPG)|
|[search](readmefiles/tablet/t-search.JPG)|

-   Desktop - 0 issues
![](/readmefiles/desktop/d-testing.JPG)

|     1920x1200    |   
|      :----:    |
|[home](readmefiles/desktop/d-home.JPG)|
|[builder](readmefiles/desktop/d-builder.JPG)|
|[profile](readmefiles/desktop/d-profile.JPG)|
|[search](readmefiles/desktop/d-search.JPG)|

#### Automated Testing - Python unittest

- In the root of this project you will find the [test_app.py](test_app.py) file. 
- This contains [31 unit tests](/readmefiles/unittest.JPG) for the app.py and app_definitions.py files. 

#### User Story Testing

##### US001 As the product owner I want prospective users/providers to be greeted with an attractive Home Page, that has a simple, intuitive layout. &check;
- Home page has an attractive opaque image. 
- Buttons are positioned centrally and their purpose is obvious.
- Additional imformation is displayed about the sie purpose and content. 
##### US002 As the product owner I want users/providers to have the ability to sign into their profile. &check;
- Login page works efficiently, displaying necessary validation errors and redirection. 
##### US003 As the product owner I want users to be able to navigate to the different elements of the site (where their profile type allows) &check;
- Navbar at the top of the page has the relevant links for users, when logged in or out. On mobile this is available on a sidebar, from a "hamburger" icon.
##### US004 As the product owner I want users to be able to contact us when necessary. &check;
- Email contact details are available in the footer of each page (excluding homepage, that has no footer)
##### US005 As the product owner I want to protect my site from malicious attempts to upload large image files. &check;
- Users are forbidden to upload image files larger than 1MB. 
- If this is attempted the file is rejested and a dialog is presented to the user.
##### US006 As the product owner I want to ensure users are given relevant and accurate informations about site operational or user errors &check;
- The site has two error views for 4XX and 5XX errors that render when an exception is thrown. 
##### US101 As the product owner I want users/providers to be able to register, if they are not already. &check;
- Register form is clear and well validated for the inputs required. 
- Passwords are secured with a secure hash from werkzeug. 
##### US201 As a user I want to be able to login to my profile. &check;
- Login page works efficiently, displaying necessary validation errors and redirection. 
##### US301 As a logged-in user I want to be able to edit my personal information. &check;
- Users are able to edit their personal information on the profile tab by clicking the dit icon. 
- The form is well validated with the necessary redirect on operations. 
##### US302 As a logged-in user I want to be able to create new recipes for the site. &check;
- Users can create new recipes on the "My Recipe Builder" page. 
- The form is well validated on inputs and while all fields are not necessary, there is a minimum content threshold that must be fulfilled. 
- Users can add/remove ingredients and steps for their method. 
- Users can preview their recipe card before submission. 
##### US303 As a logged-in user I want to be able to view the recipes I have created. &check;
- Users can view the recipes they have created on their profile page, under the "My Recipes" section. 
##### US304 As a logged-in user I want to be able to edit the recipes I have created. &check;
- If a recipe was created by the user, then on the recipe card they are given the option to edit. Once clicked this directs them to the "Recipe Editor".
- Users can add/remove content from their recipe as desired. 
##### US305 As a logged-in user I want to be able to delete the recipes I have created. &check;
- Users are able to delete their recipes by clicking edit, then from the recipe editor, clicking delete.
- Upon deletion, the recipe id is removed from the "favourites" array for all users who had favourited it. 
##### US306 As a logged-in user I want to be able to search for recipes provided by other users. &check;
- Users are able to search for other recipes by navigating to the search page. 
- Clicking on submit with no parameters will return all recipes. 
- Users can search by recipe name, which matches on partial strings. (field not required)
- Users can search by age in months for the suitablilty of the recipe (field not required)
##### US307 As a logged-in user I want to be able to favourite recipes provided by other users. &check;
- Upon finding a recipe they like, users are abel to "faviourite" recipe n the recipe card.
- Upon selection, the icon turns green.  
##### US308 As a logged-in user I want to be able to see the recipes I have favourited. &check;
- Favourited recipes are available to the user on the "My Favourites" section of their profile page. 
##### US309 As a logged-in user I want to be able to un-favourite the recipes I have favourited. &check;
- Upon deciding they wish to remove a recipe from their favourites, a user can click the icon to remove it. (turns icon purple)
##### US310 As a logged-in user I want to be able to log out. &check;
- Log out link is available in the navbar. 
##### US311 As a logged-in user I want to be able to delete my profile. &check;
- Users are able to delete their profile by clicking edit profile, then delete. 

**Common Bugs**
- Before S3 Bucket integration took place, Images would not persist on the heroku server, or are removed periodically due to the heroku dynos undergoing ["cycling"](https://help.heroku.com/K1PPS2WM/why-are-my-file-uploads-missing-deleted)
- Intermittently the some browsers will throw a **net::ERR_HTTP2_PROTOCOL_ERROR**. To date I have been unable to resolve this adequately.

## Deployment

This site has been deployed onto the [heroku](https://www.heroku.com/) cloud infrastructure. 

#### To clone from Github

1. In the Github repository click the green **Code** button.
2. Select clone protocol of your choice (SSL/HTTP/CLI)
3. Go to your IDE.
3. Open **Git Bash**.
4. Change the current working directory to the location where you want the cloned directory to be made.
5. Type **git clone**, and then paste the URL copied from GitHub.
6. Press **enter** and the local clone will be created.

#### To run locally
- Once the project has been cloned, open the project in your IDE. 
- Install requirements by running **pip3 install -r requirements.txt**

- Signup or login to your [MongoDB](https://account.mongodb.com/account/) account.
- [This](https://www.freecodecamp.org/news/learn-mongodb-a4ce205e7739/) excellent link provides details on how to get up and running with MongoDb quickly.
- Your database will ned two new collections named: "users" and "recipes".

- If you do not have an AWS account then [this link](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) provides a quick guide to setting one up. 
- Follow [this link](https://docs.aws.amazon.com/quickstarts/latest/s3backup/step-1-create-bucket.html) to set up an S3 bucket, as image uploads will be directed here. 
- Once your bucket is created, you need to add the following json to the CORS section of the permissions section of your bucket. 
;;;
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "GET",
            "HEAD",
            "POST",
            "PUT"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    }
]
;;;
- Also in the permissions section ensure your bucket is publically accessible by turning off **Block public access (bucket settings)**

- Add the following environment variables to an env.py file at the root of the project: 
    - import os
    - os.environ.setdefault("IP", your_ip)
    - os.environ.setdefault("PORT", your_port)
    - os.environ.setdefault("SECRET_KEY", your_secret_key)
    - os.environ.setdefault("MONGO_DB", your_db_name)
    - os.environ.setdefault("MONGO_URI", your_db_uri)
    - os.environ.setdefault("AWS_ACCESS_KEY_ID", your_aws_access_key)
    - os.environ.setdefault("AWS_SECRET_ACCESS_KEY", your_aws_secret_access_key)
    - os.environ.setdefault("S3_BUCKET_NAME", your_s3_bucket_name)

- In your IDE run **python3 app.py" to run the app on a local developement server.


#### To Deploy to Heroku
- Ensure the requirements.txt file is up to date by running in your IDE: **pip3 freeze -- local > requirements.txt**
- Create a ProcFile and add **web: python app.py**
- If you do not have a heroku account, create one [here]("https://www.heroku.com/")
- https://dashboard.heroku.com/apps/<your_app> provides an overview of the deployment.
- Connect the app to your github repository on the deploy tab. 
- In the settings tab, navigate to settings, then reveal config vars.
- Add the environment vairables as prescribed in your local env.py file.
- Ensure the master branch is up to date. 
- Navigate to the dashboard, then deploy tab. 
- Hit deploy branch. 

## Credits
- First and foremost the excellent guidance from the Task Manager walkthrough by [Tim Nelson](https://github.com/TravelTimN)
- Plugin acquired from https://github.com/yckart/jquery-custom-animations for some funky custom animations.  
- coding tips from [W3Schools](https://www.w3schools.com/) & [freecodecamp](https://www.freecodecamp.org/news/) 
- image uploading & aws s3 bucket integration guidance in flask from [miguel grinberg](https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask)

## Acknowledgments
[Precious Ijege](https://www.linkedin.com/in/precious-ijege-908a00168/?originalSubdomain=ng) for all his support and guidance.

I would also like to thank Susan for their feedback and support through this process!

## Disclaimer
This project was completed as part of the Full Stack Developer Milestone 3 project. If you have any questions or issues surrounding copyright please contact me at gavin_rudge@hotmail.co.uk


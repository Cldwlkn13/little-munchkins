# Little Munchkins 
[site published here](http://flask-munchkins-app.herokuapp.com/)

Little Munchkins is a website designed for parents to create and share their favourite weaning recipes. Furthermore, users are able to search and bookmark their favourite recipes provided by other users as well!

## UX

### User Stories

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

## Placeholder
requirements.txt - all of the installed modules

to run app.py locally (single instance) 
1. mysql should be up and running
2. recipe database  loaded - once you have mysql, just opening the dump file will probably automate the creation of tables

3. type:
   uvicorn  app:app

4. Use what ever you want, but I like postman
https://restless-astronaut-77430.postman.co/workspace/My-Workspace~3c02823c-7da4-4052-8215-0b69ba04cf10/collection/22932506-00cbd2a4-9d44-4127-91af-edf6198ff369

just use the recipes(login/create/reset) - you can add stuff into db and play around with it, but don't do anything outside of an account you own - it uses my gmail account and i don't want to lose it

## endpoints
URL https://recipe.naurot.com
### /login
- takes formdata name(string), password(string)
- on success returns Auth bearer token to be passed back on future requests
   
### /create
-   takes formdata name(string), email(string)
-   if duplicate emails, return unsuccessful notification
-   if len(name) < 5, returns unsuccessful notification
-   if name is not unique, returns unsuccessful notification
-   returns notification to check email to continue account creation

### /reset
- should be available irrespective of logged in status
- takes formdata email(string)
- if email not in database, returns invalid credentials
- if the email belongs to a removed (banned) user, returns user has been banned
- returns notification to check email to reset password

### /recipes/view
- returns all viewable recipes in JSON format

### /recipes/ai
- future feature

### /recipes/create
- only logged in user can create recipes
- takes formdata name(string), img(string), instructions(string), ingredients(JSON string)
- requires Auth token acquired at login
- returns notification of success or failure

### /recipes/delete?id={}
- users can only delete their recipes
- takes query parameter of recipe id
- requires auth token acquired at login
- returns notification of success or failure

### /admin/list/user  
- requires auth token acquired at login and auth lvl = 2
- returns list of all users
- primarily used for changing auth lvl or banning

### /admin/list/recipes
//list all not-yet-approved recipes
- requires auth token acquired at login and auth lvl = 2
- returns list of all unviewable recipes
- used to view recipes to either accept or reject

### /admin/list/ingredients
//lists all not-yet-approved ingredients
- requires auth token acquired at login and auth lvl = 2
- returns list of unusable/unapproved ingredients
- used to list ingredients for accepting or rejecting

### /admin/change_auth?id={}&lvl={}
//changes a users auth level
- requires auth token acquired at login and auth lvl = 2
- takes a query parameter of user id(int) and auth lvl(int)
- returns notification of success or failure

### /admin/remove_user?id={}
//bans user from system
- requires auth token acquired at login and auth lvl = 2
- takes a query parameter user id(int)
- returns notification of success or failure

### /admin/recipe/accept?id={}
// if a recipe is eligible to be viewed, makes it viewable
- requires auth token acquired at login and auth lvl = 2
- take a query parameter of recipe id(int)
- returns notification of success or failure

### /admin/recipe/reject?id={}
// rejects a submitted (but not yet approved) recipe
- requires auth token acquired at login and auth lvl = 2
- take a query parameter of recipe id(int)
- returns notification of success or failure

### /admin/ingredient/accept?id={}
// accepts an ingredient for use in recipes. a recipe which has an unaccepted ingredient can not be made viewable
- requires auth token acquired at login and auth lvl = 2
- take a query parameter of recipe id(int)
- returns notification of success or failure

### /admin/recipe/reject?id={}
// this only applies to ingredients that are on the not-yet-approved list (usable=0)
// removes ingredient from ingredient Table
// removes all recipes containing ingredient
// removes all files associated with removed recipes (instruction, images, vectors)
- requires auth token acquired at login and auth lvl = 2
- take a query parameter of ingredient id(int)
- returns notification of success or failure

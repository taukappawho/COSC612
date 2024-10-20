## Files to create MySQL tables for program
-Dump20241017.sql creates all of the tables below

-recipes is the database name
- user - contains user info [name, password, email, auth, id]
- recipe
- ingredients
- recipe_ing

### note: for units in recipe_ing table
- suggest units = ["dash", "slice", "each", "dozen", "ounce", "pound", "tsp", "Tbs", "cup", "pimt", "quart", "gal"] 
- in other words index the units. the table has the index and will return the index of the unit. the frontend will convert the index to a string

scripts has a few scripts i was playing around with
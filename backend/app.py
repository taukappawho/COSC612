from typing import Annotated, List, Optional
from fastapi import FastAPI, Form, File, UploadFile, HTTPException, status, Query, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import pymysql
from passlib.context import CryptContext 
from jose import jwt, JWTError
from datetime import datetime, timedelta
import time
import uuid
import smtplib
from dotenv import load_dotenv
import asyncio
import os
import pandas as pd
import json
from systemd import journal
from collections import defaultdict

load_dotenv()

UNITS = ["slice","dash", "bunch", "dozen","ounce", "tsp", "Tbsp", "cup", "quart", "pound", "gal", "N/A"]

mail_user=os.getenv("MAIL_USER")
mail_pwd=os.getenv("MAIL_PWD")
mail_user = "naurottest@gmail.com"
mail_pwd = "nhic asfe vtxp rcru"
#sercret_key in jwt

app = FastAPI()
origins = [
    "https://recipe.naurot.com/recipes/create",
    "http://194.195.92.140:443",
    "https://194.195.92.140:443",
    "http://recipe.naurot.com",
    "https://recipe.naurot.com",
    "http://bawlmorean.com",
    "https://bawlmorean.com",
    "http://192.168.12.232:3000",
    "https://192.168.12.232:3000",
    "http://localhost:3000",
    "https://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

##### DB Stuff
# Connect to MySQL database
PASSWORD = "not-set-yet"
conn = pymysql.connect(
    host="srv870.hstgr.io",
    user="u882885499_python",
    password="21nohtyP",
    database="u882885499_recipes",
    port=3306,
    autocommit=True
)
# Fetch data from MySQL tables
def fetch_data(query, retries=3):
    cursor = conn.cursor()
    for attempt in range(retries):
       try:
          cursor.execute(query)
          data = cursor.fetchall()
          cursor.close()
          return data
       except (pymysql.err.InterfaceError, pymysql.err.OperationalError) as e:
          journal.send(f"***Fetching - retry",PRIORITY=6)
          if e.args[0] in (2006, 0):
             conn.ping(reconnect=True)
             time.sleep(1)
          else:
             raise
    raise Exception("Failed to fetch data after retries")

#Inserts, Updates, Deletes(?)
def execute_query(query):
    conn = pymysql.connect(
    host="srv870.hstgr.io",
    user="u882885499_python",
    password="21nohtyP",
    database="u882885499_recipes",
    port=3306,
    autocommit=True
)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()

##### hash Stuff
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
def hash_password(password):
    return pwd_context.hash(password)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

##### UUID Stuff
def get_uuid():
    candidate = uuid.uuid4().hex
    asyncio.create_task(schedule_cleanup(candidate))
    return candidate
def verify_uuid(candidate):
    query = f"select name, email, auth, id from user where uuid='{candidate}'"
    response = fetch_data(query)
    return response
def remove_uuid(candidate):
    journal.send("---------- in dlete")
    query = f"select * from user where uuid='{candidate}'"
    response = fetch_data(query)
    if response:
        name, password, email, auth, id, uuid = response[0]
        if password == PASSWORD:
            query = f"delete from user where name='{name}'"
        else:
            query = f"update user set uuid='N' where name='{name}'"
        execute_query(query)     
async def schedule_cleanup(candidate):
    await asyncio.sleep(900)
    if verify_uuid(candidate):
        remove_uuid(candidate)


##### JWT Stuff
# SECRET_KEY = os.getenv("SECRET_KEY")
SECRET_KEY="my_secret_key"
ALGORITHM = "HS256"
SESSION_TOKEN_EXP = 30
MAIL_TOKEN_EXP = 15
def create_token(data,exp):
    encode = data.copy()
    expires = datetime.utcnow() + timedelta(minutes=exp)
    now = datetime.utcnow()
    encode.update({"exp": expires, "iat": now})
    encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    # print("just before verification")
    # print(f"jwt: {encoded_jwt}")
    #TODO remove testing of JWTs once I can create them w/o ....
    try:
        verified_payload = verify_token(encoded_jwt)
        journal.send(f"Verified payload: {verified_payload}",PRIORITY=6)
    except HTTPException as e:
        journal.send(f"Verification failed: {e.detail}")
    return encoded_jwt

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"leeway": 60})
        journal.send(f"verify_token: {payload}",PRIORITY=6)
        user_name = payload.get("sub")
        user_auth = payload.get("auth")
        user_id = payload.get("id")
        if user_name is None or user_auth is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return {"name": user_name, "auth": user_auth, "id": user_id}
    except JWTError as e:
        journal.send(f"JWT Error: {e}")  # Add this line for debugging
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

##### Mail stuff
def send_mail(user, email, route, effect,subject):
    lines = [
        f"From: {'noreply@bawlmorean.com'}", 
        f"To: {email}", 
        f"Subject: {subject}", 
        f"Hello {user},\n",
        f"Please click this link: {route} {effect}"
        ]

    msg = "\r\n".join(lines)
    # Use Gmail's SMTP server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.set_debuglevel(1)
    server.starttls()  # Secure the connection

    # Log in to the server
    server.login(mail_user, mail_pwd)

    # Send the email
    server.sendmail("noreply@bawlmorean.com", email, msg)
    server.quit()
    
templates = Jinja2Templates(directory="templates")

# options route
@app.options("/{path:path}")
async def preflight_handler():
    journal.send("inside of options",  PRIORITY=6)
    return JSONResponse(status_code=200)


@app.post("/login")
async def login(name: Annotated[str, Form()], password: Annotated[str, Form()]):
    journal.send("-"*60)
    journal.send(f"/login name: {name}")
    #retrieve name, password
    #validate name length - return fail on nonconformance
    if len(name) < 5:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        # lookup name in table, get hashed_password

        query = f"select name,auth,id,password from user where name='{name}'"
        response = fetch_data(query)
        if len(response) == 0:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        response = response[0]
        # journal.send(f"pwd: {password}, pwd: {response[3]}")
        if not verify_password(password, response[3]):
            raise HTTPException(status_code=401, detail="Invalid credentials") 
        # print(f"response: {response}")
        token = create_token({"sub": response[0], "auth": response[1], "id": response[2] }, SESSION_TOKEN_EXP)
        # print(f"token: {token}")
        response = JSONResponse(content={"message": "Login successful", "token": token})
        response.headers["Authorization"] = f"Bearer {token}"
        return response
        # return JSONResponse(content={"message": "Login successful", "token": token})
    
@app.post("/create")
    #logged in status status doesn't matter, can't create 2 accounts w/ same email
    #   still - create button shouldn't be present when logged in
    #extract name and email
async def create(name: Annotated[str, Form()], email: Annotated[str, Form()]):
    
    # name must be > 4 characters
    if len(name) < 5:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    #if email in database - fail fast
    query = f"select email, uuid from user where email='{email}'"
    response = fetch_data(query)
    # journal.send(f"----- response: {response}",PRIORITY=6)
    if len(response) > 0 and response[0][1] == "N":
        return {"msg": "account already exists!"}
    
    #if name in database fail with response
    query = f"select name, uuid from user where name='{name}'"
    response = fetch_data(query)
    if len(response) > 0 and response[0][1] == "N":       
        return {"msg": "name already in use"}
    
    #create uuid (uuid4 hex) - links backend --> email --> backend --> user/password --> backend
    unique = get_uuid()
    if len(response) > 0:  # User re-trying to create account
        query = f"UPDATE user SET uuid='{unique}' WHERE name='{name}'"
    else:
        query = f"INSERT INTO user (name, password, email, uuid, auth) VALUES ('{name}', '{PASSWORD}', '{email}', '{unique}', 0)"
    execute_query(query)
    
    #create route with uuid
    route = f"https://recipe.naurot.com/verify?token={unique}"
    
    #send email with link of dynamic route
    send_mail(name, email, route, " to finish creating account.\nLink expires in 15 minutes.", "New Account")
    return ({"status code": 200})

@app.post("/reset")
async def reset(email: Annotated[str, Form()]):
    # print(f"email: {email}")
    query = f"select name, email, uuid, auth from user where email='{email}'"
    # journal.send(query)
    response = fetch_data(query)
    # journal.send(f"-------reset response: {response}")
    if len(response) == 0:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    response = response[0]
    journal.send(f"-----in reset: response[0]: {response}")

    if response[3] == "0":
        return {"msg": f"Account {email} does not exist"}
    
    if len(response[0]) < 5:
        return {"msg": "user has been banned!"}

    unique = get_uuid()
    query = f"UPDATE user SET uuid='{unique}' WHERE name='{response[0]}'"
    execute_query(query)
    
    #create dynamic route
    route = f"https://recipe.naurot.com/verify?token={unique}"
    
    #send email with link of dynamic route
    send_mail(response[0], response[1],route, " to reset password.\nLink expires in 15 minutes.", "Password Reset")
    return ({"status code": 200})


@app.get("/verify", response_class=HTMLResponse)
async def verify(request: Request,token = Query(...)):
    # journal.send(f"----In verify: token: {token}",PRIORITY=6)
    response = verify_uuid(token)
    if response:
        response = response[0]
        if response[2] == "0":
            text = "Create Account"
        else:
            text = "Reset Password"
        # journal.send(f"----In verify: uuid found: true",PRIORITY=6)
        context = {
            "request": request,
            "token": token,
            "text": text
        }
        return templates.TemplateResponse("password.html", context)
    else:
        # journal.send(f"----In verify: uuid found: false",PRIORITY=6)        
        raise HTTPException(status_code=400, detail="Invalid or expired token")

@app.post("/password")
async def password(password: Annotated[str, Form()], token: Annotated[str, Query(...)]):
    journal.send(f"-----In password: ",PRIORITY=6)
    if len(password) < 5:
        journal.send(f"password: `{password}` has length `{len(password)}`",PRIORITY=6)
        raise HTTPException(status_code=401, detail="Error: incorrect password length")
    query = f"select * from user where uuid='{token}'"
    response = fetch_data(query)
    # journal.send(f"-----in password {response}",PRIORITY=6) 
    if len(response) == 0:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    if len(response) > 1:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    response = response[0]
    if response[3] == 0:
        auth = 1
    else:
        auth = response[3]
    # journal.send(f"-----in password {response}",PRIORITY=6)
    password = hash_password(password)
    query = f"update user set uuid='N', auth={auth}, password='{password}' where name='{response[0]}'"
    execute_query(query)

RECIPE_DIRECTORY = "/home/user/backend/recipes"

@app.get("/recipes/view")
def view(ing: List[int] = Query(None)):
    # query params ing_list, (offset, limit)?
    journal.send("--------\nIn recipes/view", PRIORITY=6)
    # changed below with creator
    if ing is None:
        journal.send(f"ing: {ing}", PRIORITY=6)
        query = (
            "SELECT r.name AS recipe_name, r.id AS recipe_id, r.instructions AS instructions, r.creator as creator, i.name AS ingredient_name, i.id AS ingredient_id, "
            "ri.quantity, ri.units FROM recipe r "
            "JOIN recipe_ing ri ON r.id = ri.recipe_id "
            "JOIN ingredients i ON ri.ingredient_id = i.id "
            "WHERE r.viewable = true "
            "ORDER BY r.id, i.id"
        )
    else:
        journal.send(f"ing: {ing}", PRIORITY=6)
        ing_list = ",".join(map(str,ing))
        query = (
            "SELECT r.name AS recipe_name, r.id AS recipe_id, r.instructions AS instructions, r.creator as creator, i.name AS ingredient_name, i.id AS ingredient_id, "
            "ri.quantity, ri.units FROM recipe r "
            "JOIN recipe_ing ri ON r.id = ri.recipe_id "
            "JOIN ingredients i ON ri.ingredient_id = i.id "
            "WHERE r.viewable = true and r.id IN (SELECT recipe_id "
            f"FROM recipe_ing WHERE ingredient_id IN ({ing_list}) "
            f"GROUP BY recipe_id HAVING COUNT(DISTINCT ingredient_id) = {len(ing)}) ORDER BY r.id, i.id")
        journal.send(f"query: {query}")
    response = fetch_data(query)
    df = pd.DataFrame(response, columns=["recipe_name", "recipe_id", "instructions", "creator", "ingredient_name", "ingredient_id", "quantity", "unit"])
    data = df.to_dict(orient="records")
    recipes_dict = defaultdict(lambda: {"name": None, "id": None, "instructions": None, "creator": None, "ingredients": [], "image": None, "instructions": None})
    for row in data:
        recipe_id = row["recipe_id"]
        if recipes_dict[recipe_id]["name"] is None:
            recipes_dict[recipe_id]["name"] = row["recipe_name"]
            recipes_dict[recipe_id]["id"] = recipe_id
    # changed below with creator
            recipes_dict[recipe_id]["creator"] = row["creator"]
            recipes_dict[recipe_id]["instructions"] = row["instructions"]

            # Add file paths if they exist
            image_path = os.path.join(RECIPE_DIRECTORY, f"{recipe_id}.png")
            # instructions_path = os.path.join(RECIPE_DIRECTORY, f"{recipe_id}.txt")
            if os.path.exists(image_path):
                recipes_dict[recipe_id]["image"] = f"/recipes/{recipe_id}.png"
            # if os.path.exists(instructions_path):
            #     recipes_dict[recipe_id]["instructions"] = f"/recipes/{recipe_id}.txt"

        recipes_dict[recipe_id]["ingredients"].append({
            "ingredient_name": row["ingredient_name"],
            "ingredient_id": row["ingredient_id"],
            "quantity": row["quantity"],
            "unit": row["unit"]
        })

    recipes = list(recipes_dict.values())
    output = {"recipes": recipes}

    journal.send(json.dumps(output, indent=2), PRIORITY=6)
    return JSONResponse(content=output)

@app.get("/recipes/ai")
def ai():
    journal.send("--------\nIn recipes/ai",PRIORITY=6)
    #get recipe id passed as param
    #get recipe_id's vector
    #do cosine_similarity on all vectors that aren't this one
    #   rank in descending order
    #   return recipes that map to vectors
    return

@app.get("/recipes/ingredients")
def ingredients():
    journal.send("--------\nIn recipes/ingredients",PRIORITY=6)
    query = f"select name, id from ingredients order by name asc"
    response = fetch_data(query)
    if not response:
        raise HTTPException(status_code=400, detail="Error retrievinbg ingredient list")    
    try:
        data = {row[0]: row[1] for row in response}
    except KeyError:
        raise HTTPException(status_code=500, detail="Unexpected data format from the database")
    return data

def get_JWT(request: Request):
    jwt_token = request.headers.get("Authorization")
    if not jwt_token:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    if not jwt_token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization scheme. Expected 'Bearer <token>'")
    jwt_token = jwt_token[len("Bearer "):].strip()    
    return {"jwt": jwt_token}

@app.post("/recipes/create")
async def create_recipe(
    recipe_name: Annotated[str, Form()],
    instruct: Annotated[str, Form()],
    ingredients: Annotated[str, Form()],
    img: UploadFile = File(...),
    token: dict = Depends(get_JWT),  # Token is validated using the get_JWT function
):
    jwt_token = token["jwt"]
    payload = verify_token(jwt_token)

    if payload.get("auth") < 1:
        raise HTTPException(status_code=401, detail="Invalid token")

    if not recipe_name or not instruct or not ingredients or not img:
        journal.send(f"Exception in create: {recipe_name}, {instruct}, {ingredients}, {img}",PRIORITY=6)
        raise HTTPException(status_code=400, detail="Missing required fields")

    creator = payload.get("id")
    try:
        # Insert recipe into the database
        journal.send("creating recipe",PRIORITY=6)
        query = f"INSERT INTO recipe (name, creator, viewable, instructions) VALUES ('{recipe_name}', {creator}, 0, '{instruct}') RETURNING id"
        recipe_id = fetch_data(query)[0]
        
        if not recipe_id:
            raise HTTPException(status_code=500, detail=f"Failed to create recipe, new id not created: {str(e)}")
        
        recipe_id = recipe_id[0]
        
        try:
            # Save the uploaded file  !!!wait unitl get recipe_id, then save as {recipe_id}.png
            file_location = f"recipes/{recipe_id}.png"
            with open(file_location, "wb") as f:
                f.write(img.file.read())
            
            # Handle ingredients
            journal.send("\tadding ingredients",PRIORITY=6)
            # TODO go through ingredient list finding
            for ingredient in ingredients.split(","):
                ing = ingredient.split(" ")
                query = f"INSERT INTO recipe_ing (recipe_id, ingredient_id, quantity, units) VALUES ({recipe_id}, {ing[0]}, {ing[1]}, {ing[2]})"
                execute_query(query)
                
                
# TODO  gather all ing[0], get ing name, find vector
            return JSONResponse(content={"message": "Recipe created successfully"}, status_code=201)
        except Exception as e:
            journal.send(f"Exception {e}",PRIORITY=6)
            query = f"delete from recipe where id={recipe_id}"
            execute_query(query)
            raise HTTPException(status_code=500, detail=f"Failed to create recipe: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create recipe: {str(e)}")

@app.get("/recipes/create") #??? send create recipes form from here or ???
async def send_form(request: Request, token: dict = Depends(get_JWT)):
    journal.send("--------\nIn Get Recipe Creation Form",PRIORITY=6)
    jwt_token = token["jwt"]
    payload = verify_token(jwt_token)
    auth = payload.get("auth")
    if auth < 1:
        raise HTTPException(status_code=401, detail="Unauthorized attempt to create recipe")
    context = {
    "request": request,
    "token": jwt_token
    }
    return templates.TemplateResponse("create.html", context)

@app.put("/recipes/ingredients")
async def insert_ingredient(ing: str, token: dict=Depends(get_JWT)):
    journal.send(f"attempting to add ingredient: {ing}",PRIORITY=6)
    jwt_token = token["jwt"]
    payload = verify_token(jwt_token)
    auth = payload.get("auth")
    if auth < 1:
        raise HTTPException(status_code=401, detail="Unauthorized attempt to insert ingredient")
    # query = f"insert into ingredients where name='{ing}', usable=0 returning id"
    ing = ing.lower().strip()
    query = f"INSERT INTO `ingredients`(`id`, `name`, `usable`) VALUES ('','{ing}','') returning id, name, usable"
    try:
        response = fetch_data(query)
        journal.send(f"{response}, {response[0]}",PRIORITY=5)
        return {"response": {"data": response[0]}}
    except Exception as e:
        query = f"select * from ingredients where name='{ing}'"
        response = fetch_data(query)
        journal.send(f"{response}, {response[0]}",PRIORITY=5)
        return {"response": {"data": response[0]}}

    
@app.delete("/recipes/delete")
async def delete(id: int, token: dict = Depends(get_JWT)):
    journal.send("--------\nIn recipes/delete",PRIORITY=6)
    jwt_token = token["jwt"]
    payload = verify_token(jwt_token)
    # journal.send(f"payload: {payload}")
    query = f"select creator from recipe where id = {id}"
    response = fetch_data(query)
    # journal.send(f"response: {response}", PRIORITY=6)
    
    if payload.get("id") == response[0][0]:
        query = f"delete from recipe_ing where recipe_id = {id}"
        execute_query(query)
        query = f"delete from recipe where id = {id}"
        execute_query(query)
        # os.remove(f"./recipes/{id}.txt")  --- moved instructions to db
        os.remove(f"./recipes/{id}.png")
        return {"meg": f"successfully removed {id}"}
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
        
    #validate JWT - fail with message
    #get recipe from recipe table (recipe id passed)
    #user id from JWT == creator from recipe - fast fail with message
    #remove instructions, image, vector(?)
    #remove * from recipe_ingredients table where recipe = recipe id
    #remove recipe from recipe table
    #return successful removal


def verify_admin(token):
    payload = verify_token(token)
    name=payload.get("sub")
    auth=payload.get("auth")
    id=payload.get("id")
    if auth < 2:
        raise HTTPException(status_code=401, detail="Not admin")    
    return {"name": name, "auth": auth, "id": id}

@app.get("/admin/list/users")
async def admin_list_users(token: dict = Depends(get_JWT)):
    journal.send("--------\nIn admin_list_users",PRIORITY=6)
    verify_admin(token["jwt"])
    query = "select id, name, email, auth from user"
    response = fetch_data(query)
    return response
       
@app.get("/admin/list/recipes")
async def admin_list_recipes(token: dict = Depends(get_JWT)):
    journal.send("--------\nIn admin_list_recipes",PRIORITY=6)
    verify_admin(token["jwt"])
    query = "select creator, name, id,instructions from recipe where viewable = 0 and id not in (select recipe_id from recipe_ing where ingredient_id in (select id from ingredients where usable = 0))"
    response = fetch_data(query)
    return response
    
@app.get("/admin/list/ingredients")
async def admin_list_ingredients(token: dict = Depends(get_JWT)):
    journal.send("--------\nIn admin_list_ingredients",PRIORITY=6)
    verify_admin(token["jwt"])
    query = "select * from ingredients where usable = 0"
    response = fetch_data(query)
    return response


@app.patch("/admin/change_auth")
async def admin_change_auth(id:int, lvl: int, token: dict = Depends(get_JWT)):
    journal.send("--------\nIn admin_change_auth",PRIORITY=6)
    verify_admin(token["jwt"])
    if (lvl < 0 or lvl > 2):
        raise HTTPException(status_code=400, detail=f"ChangeAuth id={id}, lvl={lvl}. Operation could not be performed")
    query = f"select name from user where id={id}"
    response = fetch_data(query)
    if not response:
        raise HTTPException(status_code=400, detail=f"ChangeAuth id={id}, lvl={lvl}. User[{id}] does not exist")
    try: 
        query = f"update user set auth={lvl} where id={id}"       
        execute_query(query)
        return {"msg": f"user[{id}]['auth'] = {lvl}"}
    except Exception as e:
        journal.send(f"ERROR {e}. did not change auth level to {lvl} for user[{id}]")
        raise HTTPException(status_code=400, detail=f"ChangeAuth id={id}, lvl={lvl}. Operation could not be performed")

@app.patch("/admin/remove_user")
async def admin_remove_user(id: int, token: dict = Depends(get_JWT)):
    journal.send("--------\nIn admin_remove_user",PRIORITY=6)
    verify_admin(token["jwt"])
    query = f"select id from user where id={id}"
    response = fetch_data(query)
    if not response:
        raise HTTPException(status_code=400, detail=f"RemoveUser id={id}. User[{id}] does not exist")
    empty_string = " "
    try:      
        query = f"update user set name='{empty_string}' where id={id}"  
        execute_query(query)
        return {"msg": f"user[{id}]['name'] = {empty_string}"}
    except Exception as e:
        journal.send(f"ERROR {e}. did not remove user[{id}]")
        raise HTTPException(status_code=400, detail=f"RemoveUser id={id}. Operation could not be performed")

@app.patch("/admin/recipe/accept")
# SELECT * FROM `recipe_ing` WHERE recipe_id=1 and ingredient_id in (select id from ingredients where usable=false)
async def admin_recipe_accept(id: int, token: dict = Depends(get_JWT)):
    journal.send("--------\nIn admin_recipe_accept",PRIORITY=6)
    verify_admin(token["jwt"])
    query = f"SELECT recipe_id FROM `recipe_ing` WHERE recipe_id={id} and ingredient_id in (select id from ingredients where usable=0)"
    response = fetch_data(query)
    if response:
        raise HTTPException(status_code=400, detail=f"RecipeAccept id={id}. Operation could not be performed. All ingredients must be usable")
    try:
        query = f"update recipe set viewable = 1 where id = {id}"
        execute_query(query)
        return {"msg": "recipe accepted"}
    except Exception as e:
        journal.send(f"Error attempting to accept recipe[{id}]: {e}")
        raise HTTPException(status_code=400, detail=f"RecipeAccept id={id}. Operation could not be performed")



@app.delete("/admin/recipe/reject")
async def admin_recipe_reject(id: int, token: dict = Depends(get_JWT)):
    journal.send("--------\nIn admin_recipe_reject",PRIORITY=6)
    verify_admin(token["jwt"])
    try:
        # try:
        #     os.remove(f"./recipes/{id}.txt")
        # except FileNotFoundError:
        #     journal.send(f"File ./recipes/{id}.txt not found.", PRIORITY=5)
        
        try:
            os.remove(f"./recipes/{id}.png")
        except FileNotFoundError:
            journal.send(f"File ./recipes/{id}.png not found.", PRIORITY=5)
        query = f"delete from recipe_ing where recipe_id={id}"
        execute_query(query)
        journal.send("\ndeleting recipe. deleted ingredients", PRIORITY=6)
        query = f"delete from recipe where id={id}"
        execute_query(query)
        journal.send("\ndeleting recipe. deleted recipe", PRIORITY=6)
        return {"msg": f"recipe[{id}] deleted"}
    except Exception as e:
        journal.send(f"error in delete recipe[{id}]: {e}")  
        raise HTTPException(status_code=400, detail=f"RecipeReject id={id}. ERROR {e}. Operation could not be performed")

@app.patch("/admin/ingredient/accept")
async def admin_ingredient_accept(id: int, token: dict = Depends(get_JWT)):
    journal.send("--------\nIn admin_ingredient_accept",PRIORITY=6)
    verify_admin(token["jwt"])
    query = f"update ingredients set usable = 1 where id = {id}"
    try:
        execute_query(query)
        return {"msg": "ingredient accepted"}
    except Exception as e:
        journal.send(f"Error attempting to accept ingredient[{id}]: {e}")
        raise HTTPException(status_code=400, detail=f"IngAccept id={id}. ERROR {e}. Operation could not be performed")

@app.delete("/admin/ingredient/reject")
async def admin_ingredient_reject(id: int, token: dict = Depends(get_JWT)):
    journal.send("--------\nIn admin_ingredient_reject",PRIORITY=6)
    verify_admin(token["jwt"])
    query = f"select recipe_id from recipe_ing where ingredient_id={id}"
    try:
        response = fetch_data(query)
        journal.send(f"response: {response}", PRIORITY=6)
        if response:
            for recipe in response:
                recipe_id = recipe[0]
                query = f"delete from recipe_ing where recipe_id={recipe_id}"
                execute_query(query)
                query = f"delete from recipe where id={recipe_id}"
                execute_query(query)
                # try:
                #     os.remove(f"./recipes/{recipe_id}.txt")
                # except FileNotFoundError:
                #     journal.send(f"File ./recipes/{recipe_id}.txt not found.", PRIORITY=5)
                
                try:
                    os.remove(f"./recipes/{recipe_id}.png")
                except FileNotFoundError:
                    journal.send(f"File ./recipes/{recipe_id}.png not found.", PRIORITY=5)

        query = f"delete from ingredients where id={id}"
        execute_query(query)
        return {"msg": f"ingredient[{id}] successfully removed"}
    except Exception as e:
        journal.send(f"IngAccept id={id}. ERROR {e}. Operation could not be performed", PRIORITY=4)
        raise HTTPException(status_code=400, detail=f"IngAccept id={id}. ERROR {e}. Operation could not be performed")
    
@app.get("/recipes/{id}.png")
async def get_image(id: int):
    journal.send("--------\nIn get_image",PRIORITY=6)
    image_path = os.path.join(RECIPE_DIRECTORY, f"{id}.png")
    # Check if the file exists
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Return the image as a response
    return FileResponse(image_path)
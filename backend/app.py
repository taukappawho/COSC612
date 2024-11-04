from typing import Annotated, Optional
from fastapi import FastAPI, Form, HTTPException, status, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
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

mail_user=os.getenv("MAIL_USER")
mail_pwd=os.getenv("MAIL_PWD")
mail_user = "naurottest@gmail.com"
mail_pwd = "nhic asfe vtxp rcru"
#sercret_key in jwt

app = FastAPI()
origins = [
    "http://bawlmorean.com",
    "https://bawlmorean.com",
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
          if e.args[0] in (2006, 0):
             conn.ping(reconnect=True)
             time.sleep(1)
          else:
             raise
    raise Exception("Failed to fetch data after retries")
#Inserts, Updates, Deletes(?)
def execute_query(query):
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
        # print(f"Verified payload: {verified_payload}")
    except HTTPException as e:
        journal.send(f"Verification failed: {e.detail}")
    return encoded_jwt

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"leeway": 60})
        return payload
        # user_info = payload.get("sub")
        # if user_info is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        # return user_info
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

@app.post("/login")
async def login(name: Annotated[str, Form()], password: Annotated[str, Form()]):
    journal.send("******\n******\n******")
    journal.send(f"name: {name}, password: {password}")
    #retrieve name, password
    #validate name length - return fail on nonconformance
    if len(name) < 5:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        # lookup name in table, get hashed_password

        query = f"select name,email,auth,id,password from user where name='{name}'"
        response = fetch_data(query)
        if len(response) == 0:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        response = response[0]
        journal.send(f"pwd: {password}, pwd: {response[4]}")
        if not verify_password(password, response[4]):
            raise HTTPException(status_code=401, detail="Invalid credentials") 
        # print(f"response: {response}")
        token = create_token({"sub": response[0],"email":response[1], "auth": response[2], "id": response[3] }, SESSION_TOKEN_EXP)
        # print(f"token: {token}")
        response = JSONResponse(content={"message": "Login successful"})
        response.headers["Authorization"] = f"Bearer {token}"
        # return response
        return JSONResponse(content={"message": "Login successful", "token": token})
    
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
    journal.send(f"----- response: {response}",PRIORITY=6)
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
async def verify(request: Request ,token = Query(...)):
    journal.send(f"----In verify: token: {token}",PRIORITY=6)
    response = verify_uuid(token)
    if response:
        response = response[0]
        if response[2] == "0":
            text = "Create Account"
        else:
            text = "Reset Password"
        journal.send(f"----In verify: uuid found: true",PRIORITY=6)
        context = {
            "request": request,
            "token": token,
            "text": text
        }
        return templates.TemplateResponse("password.html", context)
    else:
        journal.send(f"----In verify: uuid found: false",PRIORITY=6)        
        raise HTTPException(status_code=400, detail="Invalid or expired token")

@app.post("/password")
async def password(password: Annotated[str, Form()], token: Annotated[str, Query(...)]):
    journal.send(f"-----In password: {password}\n\ttoken: {token}",PRIORITY=6)
    query = f"select * from user where uuid='{token}'"
    response = fetch_data(query)
    journal.send(f"-----in password {response}",PRIORITY=6) 
    if len(response) == 0:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    if len(response) > 1:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    response = response[0]
    if response[3] == 0:
        auth = 1
    else:
        auth = response[3]
    journal.send(f"-----in password {response}",PRIORITY=6)
    password = hash_password(password)
    query = f"update user set uuid='N', auth={auth}, password='{password}' where name='{response[0]}'"
    execute_query(query)

RECIPE_DIRECTORY = "/home/user/backend/recipes"

@app.get("/recipes/view")
def view():
    # query params ing_list, (offset, limit)?
    journal.send("--------\nIn recipes/view", PRIORITY=6)
    
    query = (
        "SELECT r.name AS recipe_name, r.id AS recipe_id, i.name AS ingredient_name, i.id AS ingredient_id, "
        "ri.quantity, ri.units FROM recipe r "
        "JOIN recipe_ing ri ON r.id = ri.recipe_id "
        "JOIN ingredients i ON ri.ingredient_id = i.id "
        "WHERE r.viewable = true "
        "ORDER BY r.id, i.id"
    )
    response = fetch_data(query)
    df = pd.DataFrame(response, columns=["recipe_name", "recipe_id", "ingredient_name", "ingredient_id", "quantity", "unit"])
    data = df.to_dict(orient="records")

    recipes_dict = defaultdict(lambda: {"name": None, "id": None, "ingredients": [], "image": None, "instructions": None})
    for row in data:
        recipe_id = row["recipe_id"]
        if recipes_dict[recipe_id]["name"] is None:
            recipes_dict[recipe_id]["name"] = row["recipe_name"]
            recipes_dict[recipe_id]["id"] = recipe_id

            # Add file paths if they exist
            image_path = os.path.join(RECIPE_DIRECTORY, f"{recipe_id}.png")
            instructions_path = os.path.join(RECIPE_DIRECTORY, f"{recipe_id}.txt")
            if os.path.exists(image_path):
                recipes_dict[recipe_id]["image"] = f"/recipes/{recipe_id}.png"
            if os.path.exists(instructions_path):
                recipes_dict[recipe_id]["instructions"] = f"/recipes/{recipe_id}.txt"

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
def get_JWT(request: Request):
    jwt_token = request.headers.get("Authorization")
    if not jwt_token:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    if jwt_token.startswith("Bearer "):
        jwt_token = jwt_token[7:]
    return {"jwt": jwt_token}

@app.post("/recipes/create")
def create(request: Request):
    journal.send("--------\nIn recipes/create",PRIORITY=6)
    jwt = get_JWT(request)
    payload = verify_token(jwt)
    journal.send(f"payolad: {payload}")
    #validate JWT - fail with message, must be logged in user, auth > 0
    #validate img not null, name != "", instructions > ?, ingredients > 0
    #create embedding of ingredient list
    #add *name,viewable=false,creator={username} to recipe table
    #for all ingredients not in recipe table, prepend with *
    #if any ingredient not in ingredient table, add to recipe table
    #for all ingredients:
    #   add quantity, measurement to recipe_ingredient table with keys from recipe and ingredient tables
    #save files - instructions, image, vector(?)    
    return

@app.delete("/recipes/delete{id}")
async def delete(id):
    journal.send("--------\nIn recipes/delete",PRIORITY=6)
    jwt = get_JWT(request)
    payload = verify_token(jwt)
    journal.send(f"payolad: {payload}")
    #validate JWT - fail with message
    #get recipe from recipe table (recipe id passed)
    #user id from JWT == creator from recipe - fast fail with message
    #remove instructions, image, vector(?)
    #remove * from recipe_ingredients table where recipe = recipe id
    #remove recipe from recipe table
    #return successful removal
    return

@app.auth("/admin/auth")
async def admin_auth():
    journal.send("--------\nIn admin_auth",PRIORITY=6)
    jwt = get_JWT(request)
    payload = verify_token(jwt)
    journal.send(f"payolad: {payload}",PRIORITY=6)
    
    return

@app.auth("/admin/remove_user")
async def admin_remove_user():
    journal.send("--------\nIn admin_remove_user",PRIORITY=6)
    jwt = get_JWT(request)
    payload = verify_token(jwt)
    journal.send(f"payolad: {payload}",PRIORITY=6)
    
    return

@app.auth("/admin/recipe")
async def admin_recipe():
    journal.send("--------\nIn admin_recipe",PRIORITY=6)
    jwt = get_JWT(request)
    payload = verify_token(jwt)
    journal.send(f"payolad: {payload}",PRIORITY=6)
    
    return

@app.auth("/admin/ingredient")
async def admin_ingredient():
    journal.send("--------\nIn admin_ingredient",PRIORITY=6)
    jwt = get_JWT(request)
    payload = verify_token(jwt)
    journal.send(f"payolad: {payload}",PRIORITY=6)
    
    return
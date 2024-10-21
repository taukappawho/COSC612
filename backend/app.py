from typing import Annotated, Optional
from fastapi import FastAPI, Form, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pymysql
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import time
import smtplib
from dotenv import load_dotenv
import os

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
def insert(query):
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()
    

##### hash Stuff
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password):
    return pwd_context.has(password)

##### JWT Stuff
JWT_LIST = []
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
        print(f"Verification failed: {e.detail}")
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
        print(f"JWT Error: {e}")  # Add this line for debugging
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

##### Mail stuff
def send_mail(user, email, route, effect):
    lines = [
        f"From: {'noreply@bawlmorean.com'}", 
        f"To: {email}", 
        "Subject: New Account", 
        f"Howdy {user}",
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


@app.post("/login")
async def login(name: Annotated[str, Form()], password: Annotated[str, Form()]):
    print("******\n******\n******")
    print(f"name: {name}, password: {password}")
    #retrieve name, password
    #validate name length - return fail on nonconformance
    if len(name) < 5:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        # lookup name in table, get hashed_password
        query = f"select name,email,auth,id from user where name='{name}' and password='{password}'"
        # print(f"query: {query}")
        response = fetch_data(query)
        if len(response) == 0:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        response = response[0]
        # print(f"response: {response}")
        token = create_token({"sub": response[0],"email":response[1], "auth": response[2], "id": response[3] }, SESSION_TOKEN_EXP)
        # print(f"token: {token}")
        response = JSONResponse(content={"message": "Login successful"})
        response.headers["Authorization"] = f"Bearer {token}"
        return response

@app.post("/create")
    #logged in status status doesn't matter, can't create 2 accounts w/ same email
    #   still - create button shouldn't be present when logged in
    #extract name and email
async def create(name: Annotated[str, Form()], email: Annotated[str, Form()]):
    # print(f"name: {name}, email: {email}")
    if len(name) < 5:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    #if email in database - fail fast
    query = f"select name,email,auth,id from user where email='{email}'"
    # print(f"query: {query}")
    response = fetch_data(query)
    if len(response) != 0:
        print(f"**************Account: {email} already exists!")
        return {"msg": "account already exists!"}
    query = f"select name,email,auth,id from user where name='{name}'"
    response = fetch_data(query)
    # print(f"query: {query}")
    #     #if name in database fail with response
    if len(response) != 0:
        # print(f"**************Name: {name} already exists!")        
        return {"msg": "name already in use"}
    #create entry in user table - {name},"not-set-yet",{email},{auth="1"}
    query = f"insert into user (name, password, email) values('{name}','Not-set-yet','{email}'"
    print(f"query: {query}")
    # TODO insert(query)
    
    #create email jwt
    email_jwt = create_token({"sub": "create", "name": name, "email": email},MAIL_TOKEN_EXP)
    JWT_LIST.append(email_jwt)
    #TODO create function to remove email_jwt from JWT_LIST in 15 minutes
    
    #create dynamic route
    route = f"https://recipe.naurot.com/verify?token={email_jwt}"
    #TODO create timeout with function to delete route if it still exists after 15 minutes
    #send email with link of dynamic route
    send_mail(name, email, route, " to finish creating account.\nLink expires in 15 minutes.")
    return ({"status code": 200})

@app.post("/reset")
async def reset(email: Annotated[str, Form()]):
    # print(f"email: {email}")
    query = f"select name, email from user where email='{email}'"
    # print(f"query: {query}")
    response = fetch_data(query)
    if len(response) == 0:
        return {"msg": f"Account {email} does not exist"}
    response = response[0]
    print(f"response: {response}")
    if len(response[0]) < 5:
        return {"msg": "user has been banned!"}
    #create dynameic route
    #create email jwt
    email_jwt = create_token({"sub": "reset", "name": response[0],"email": email},MAIL_TOKEN_EXP)
    JWT_LIST.append(email_jwt)
    #TODO create function to remove email_jwt from JWT_LIST in 15 minutes
    
    #create dynamic route
    route = f"https://recipe.naurot.com/verify?token={email_jwt}"
    #create timeout with function to delete route if it still exists after 15 minutes
    
    #send email with link of dynamic route
    send_mail(response[0], response[1],route, " to reset password.\nLink expires in 15 minutes.")
    return ({"status code": 200})

@app.get("/verify")
async def verify(token = Query(...)):
    print("--------\nIn Verify")
    print(f"token: {token}")
    user_info = verify_token(token)
    JWT_LIST.remove(token)
    # return {"message": "Token is valid", "user_info": user_info}
    return f"<html><body><button>Password</button></body></html>"


@app.get("/recipes/view")
def view():
    print("--------\nIn recipes/view")
    #passed {"ingredients": [],"offset": xx, "limit": yy}
    #get above recipes from query
    #return JWT in header
    return ({})

@app.get("/recipes/ai")
def ai():
    print("--------\nIn recipes/ai")
    #get recipe id passed as param
    #get recipe_id's vector
    #do cosine_similarity on all vectors that aren't this one
    #   rank in descending order
    #   return recipes that map to vectors
    return

@app.post("/recipes/create")
def create():
    print("--------\nIn recipes/create")
    #validate JWT - fail with message
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
    print("--------\nIn recipes/delete")
    #validate JWT - fail with message
    #get recipe from recipe table (recipe id passed)
    #user id from JWT == creator from recipe - fast fail with message
    #remove instructions, image, vector(?)
    #remove * from recipe_ingredients table where recipe = recipe id
    #remove recipe from recipe table
    #return successful removal
    return
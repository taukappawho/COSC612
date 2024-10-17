from typing import Annotated, Optional
from fastapi import FastAPI, Form, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
import pymysql
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
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
    host="localhost",
    user="python",
    password="Python12",
    database="recipes"
)
# Fetch data from MySQL tables
def fetch_data(query):
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data
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
        f"From: {"noreply@bawlmorean.com"}", 
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
    print(f"user: {name}, password: {password}")
    #retrieve username, password
    #validate username length - return fail on nonconformance
    if len(name) < 5:
        return {"msg": "name invalid"}
    else:
        # lookup username in table, get hashed_password
        query = f"select name,email,auth,id from user where name = \"{name}\" and password = \"{password}\""
        print(f"query: {query}")
        user = fetch_data(query)
        if len(user) == 0:
            return {"msg": "name/password invalid"}
        user = user[0]
        print(f"user: {user}")
        user_info = {"name": user[0],"email":user[1], "auth": user[2], "id": user[3]}
        print(f"user_info: {user_info}")
        access_token = create_token({"sub": user[0],"email":user[1], "auth": user[2], "id": user[3] }, SESSION_TOKEN_EXP)
        print(f"access_toke: {access_token}")
        return {"access_token": access_token, "token_type": "bearer"}

@app.post("/create")
    #user should not be logged in -- test how??does it matter?
    #extract name and email
async def create(name: Annotated[str, Form()], email: Annotated[str, Form()]):
    print(f"name: {name}, email: {email}")
    if len(name) < 5:
        return {"msg": "name invalid"}
    #if user email in database - fail fast
    query = f"select name,email,auth,id from user where email = \"{email}\""
    print(f"query: {query}")
    if len(fetch_data(query)) != 0:
        return {"msg": "account already exists!"}
    query = f"select name,email,auth,id from user where name = \"{name}\""
    print(f"query: {query}")
        #if name in database fail with response
    if len(fetch_data(query)) != 0:
        return {"msg": "name already in use"}
    #create entry in user table - {name},"not-set-yet",{email},{auth="1"}
    query = f"insert into user (name, password, email) values(\"{name}\",\"Not-set-yet\",\"{email}\""
    print(f"query: {query}")
    # TODO insert(query)
    
    #create email jwt
    email_jwt = create_token({"sub": "create", "name": name, "email": email},MAIL_TOKEN_EXP)
    JWT_LIST.append(email_jwt)
    #TODO create function to remove email_jwt from JWT_LIST in 15 minutes
    
    #create dynamic route
    route = f"http://localhost:8000/verify?token={email_jwt}"
    #create timeout with function to delete route if it still exists after 15 minutes
    #send email with link of dynamic route
    send_mail(name, email, route, " to finish creating account.\nLink expires in 15 minutes.")
    # ***if route used - delete link
    return ({"status code": 200})

@app.post("/reset")
async def reset(email: Annotated[str, Form()]):
    print(f"email: {email}")
    query = f"select name, email from user where email = \"{email}\""
    print(f"query: {query}")
    user = fetch_data(query)
    if len(user) == 0:
        return {"msg": f"Account {email} does not exist"}
    user = user[0]
    print(f"user: {user}")
    if len(user[0]) < 5:
        return {"msg": "user has been banned!"}
    #create dynameic route
    #create email jwt
    email_jwt = create_token({"sub": "reset", "name": user[0],"email": email},MAIL_TOKEN_EXP)
    JWT_LIST.append(email_jwt)
    #TODO create function to remove email_jwt from JWT_LIST in 15 minutes
    
    #create dynamic route
    route = f"http://localhost:8000/verify?token={email_jwt}"
    #create timeout with function to delete route if it still exists after 15 minutes
    send_mail(user[0], user[1],route, " to reset password.\nLink expires in 15 minutes.")
    #send email with link of dynamic route
    #extract email
    #get username from user table using email
    #if {username} == "" fail fast
    #create dynameic route
    #create timeout with function to delete route if it still exists after 15 minutes
    #send email with link of dynamic route
    # ***if route used - delete link
    return ({"status code": 200})

@app.get("/verify")
async def verify(token = Query(...)):
    print(f"token: {token}")
    user_info = verify_token(token)
    JWT_LIST.remove(token)
    # return {"message": "Token is valid", "user_info": user_info}
    return f"<html><body><button>Password</button></body></html>"


@app.get("/recipes/view")
def view():
    #passed {"ingredients": [],"offset": xx, "limit": yy}
    #get above recipes from query
    #return JWT in header
    return ({})

@app.get("/recipes/ai")
def ai():
    #get recipe id passed as param
    #get recipe_id's vector
    #do cosine_similarity on all vectors that aren't this one
    #   rank in descending order
    #   return recipes that map to vectors
    return

@app.post("/recipes/create")
def create():
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

@app.delete("/recipes/delete")
def delete():
    #validate JWT - fail with message
    #get recipe from recipe table (recipe id passed)
    #user id from JWT == creator from recipe - fast fail with message
    #remove instructions, image, vector(?)
    #remove * from recipe_ingredients table where recipe = recipe id
    #remove recipe from recipe table
    #return successful removal
    return




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
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


load_dotenv()

mail_user=os.getenv("MAIL_USER")
mail_pwd=os.getenv("MAIL_PWD")
#mail_user = "naurottest@gmail.com"
#mail_pwd = "nhic asfe vtxp rcru"
#sercret_key in jwt

app = FastAPI()
origins = [
    "http://bawlmorean.com",
    "https://bawlmorean.com",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000"
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
    user="testing",
    password="testpwd",
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
    try:
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = mail_user  # Must use your Gmail address here
        msg['To'] = email
        msg['Subject'] = "Recipe App Account Verification"

        # Create the body of the message
        body = f"""
        Howdy {user},

        Please click this link{effect}:
        {route}

        If you didn't request this, please ignore this email.
        """

        msg.attach(MIMEText(body, 'plain'))

        # Create SMTP session
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.set_debuglevel(1)  # Keep debug output
        server.starttls()

        # Login with your Gmail credentials
        server.login(mail_user, mail_pwd)

        # Send email
        server.sendmail(mail_user, email, msg.as_string())
        server.quit()

        print(f"Successfully sent email to {email}")
        return True

    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        raise e


@app.post("/login")
async def login(name: Annotated[str, Form()], password: Annotated[str, Form()]):
    print(f"\nLogin attempt - name: {name}")

    try:
        if len(name) < 5:
            print("Username too short")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Get user data including hashed password
        query = f"SELECT name, email, auth, id, password FROM user WHERE name='{name}'"
        print(f"Executing query: {query}")
        response = fetch_data(query)

        if len(response) == 0:
            print("User not found in database")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user_data = response[0]
        stored_hash = user_data[4]  # Get the stored hashed password
        print(f"Found user: {user_data[0]}")
        print(f"Stored hash: {stored_hash}")

        # Debug password verification
        try:
            is_valid = pwd_context.verify(password, stored_hash)
            print(f"Password verification result: {is_valid}")
            if not is_valid:
                print("Password verification failed")
                raise HTTPException(status_code=401, detail="Invalid credentials")
        except Exception as verify_error:
            print(f"Error during password verification: {str(verify_error)}")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        print("Password verified successfully")

        # Create token
        token = create_token({
            "sub": user_data[0],
            "email": user_data[1],
            "auth": user_data[2],
            "id": user_data[3]
        }, SESSION_TOKEN_EXP)

        response = JSONResponse(content={"message": "Login successful"})
        response.headers["Authorization"] = f"Bearer {token}"
        return response

    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/create")
async def create(name: Annotated[str, Form()], email: Annotated[str, Form()]):
    if len(name) < 5:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Check if email exists
    query = f"select name,email,auth,id from user where email='{email}'"
    response = fetch_data(query)
    if len(response) != 0:
        return {"msg": "account already exists!"}

    # Check if username exists
    query = f"select name,email,auth,id from user where name='{name}'"
    response = fetch_data(query)
    if len(response) != 0:
        return {"msg": "name already in use"}

    # Fix: Add missing closing parenthesis and set default auth value
    query = f"INSERT INTO user (name, password, email, auth) VALUES ('{name}', 'Not-set-yet', '{email}', 1)"
    print(f"query: {query}")

    try:
        # Uncomment the insert
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()

        # Create email jwt
        email_jwt = create_token({"sub": "create", "name": name, "email": email}, MAIL_TOKEN_EXP)
        JWT_LIST.append(email_jwt)

        # Create dynamic route
        #route = f"https://recipe.naurot.com/verify?token={email_jwt}"
        route = f"http://localhost:3000/verify?token={email_jwt}"

        # Send email
        send_mail(name, email, route, " to finish creating account.\nLink expires in 15 minutes.")
        return {"status": 200, "msg": "Check your email to complete registration"}
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

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
    #route = f"https://recipe.naurot.com/verify?token={email_jwt}"
    #create timeout with function to delete route if it still exists after 15 minutes

     # Use localhost:3000 for frontend testing
    route = f"http://localhost:3000/verify?token={email_jwt}"


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

@app.post("/set-password")
async def set_password(password: Annotated[str, Form()], token: Annotated[str, Form()]):
    try:
        # Verify token
        payload = verify_token(token)
        if token not in JWT_LIST:
            raise HTTPException(status_code=400, detail="Invalid or expired token")

        # Get user info from token
        email = payload.get("email")
        action = payload.get("sub")

        # Hash the new password
        print(f"\nSetting new password for email: {email}")
        hashed_password = pwd_context.hash(password)
        print(f"Generated hash: {hashed_password}")

        # Update password in database
        query = f"UPDATE user SET password = '{hashed_password}' WHERE email = '{email}'"
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()

        # Remove used token
        JWT_LIST.remove(token)

        msg = "Account created successfully" if action == "create" else "Password reset successfully"
        return {"status": 200, "msg": msg}

    except Exception as e:
        print(f"Error in set_password: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


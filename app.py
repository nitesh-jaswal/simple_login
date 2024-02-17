import sqlite3

import bcrypt
import pydantic
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse

DATABASE_FILE = "database.db"

app = FastAPI()


@app.get("/")
async def read_index():
    return FileResponse("static/index.html")


# Function to get database connection
def get_db():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn


class UserLogin(pydantic.BaseModel):
    username: str
    password: pydantic.types.SecretStr


# Endpoint to create a new account
@app.post("/create_account/")
async def create_account(user_details: UserLogin):
    db = get_db()
    hashed_password = bcrypt.hashpw(user_details.password.get_secret_value().encode("utf-8"), bcrypt.gensalt())
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user_details.username, hashed_password))
        db.commit()
        return JSONResponse(content={"message": "Account created successfully"}, status_code=201)
    except sqlite3.IntegrityError:
        db.close()
        raise HTTPException(status_code=400, detail="Username already exists")


# Endpoint to login
@app.post("/login/")
async def login(user_details: UserLogin):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (user_details.username,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(user_details.password.get_secret_value().encode("utf-8"), user["password"]):
            return JSONResponse(content={"message": "Authenticated successfully"}, status_code=200)
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=5555)

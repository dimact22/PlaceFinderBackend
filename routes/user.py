from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, Form, Request, FastAPI
from shemas.apartments_search import Apartments_seach
from shemas.user import User, UserLogin
from db.dbconn import places, users
from functions.transform_address_to_cor import transform
from jose import jwt
from db.hash import Hash

user = APIRouter()

@user.post("/register")
async def create_user(user: User):
    """
    Register a new user

    Creates a new user account with a hashed password. If a user with the provided email already exists, an HTTP 400 error is returned.
    - **name**: The name of the user.
    - **email**: The email address of the user.
    - **password**: The password of the user.
    """

    existing_user = users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    existing_user = users.find_one({"name": user.name})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="A user with this name already exists")
    hashed_password = Hash.bcrypt(user.password)
    user.password = hashed_password
    token = jwt.encode(
            {'sub': user.name}, "test", algorithm='HS256')
    users.insert_one(dict(user))
    return {"status": "Ok", "token": token}

@user.post("/login")
async def login_user(user: UserLogin):
    """
    Login user

    Authenticates a user and returns a JWT token. If the user is not found or the credentials are invalid, an HTTP 400 error is returned.

    - **email**: The email of the user.
    - **password**: The password of the user.
    """

    found_user = users.find_one({"email": user.email})

    if not found_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    if Hash.verify(user.password, found_user["password"]):
        token = jwt.encode(
            {'sub': found_user["name"]}, "test", algorithm='HS256')
        return {"status": "Ok", "token": token}
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")

@user.post("/decode/{token}")
async def decode_tok(token):
    payload = jwt.decode(token, "test", algorithms=["HS256"])
    return str(payload.get("sub"))

@user.post("/appart_search")
async def appart_search(appart_info: Apartments_seach):
    #print(appart_info)
    cords = transform(appart_info.address)
    #print(cords)
    try:
        results = places.aggregate([
            {
                "$geoNear": {
                    "near": {
                        "type": "Point",
                        # Ваши координаты [долгота, широта]
                        "coordinates": cords
                    },
                    "distanceField": "dist.calculated",  # Имя поля, куда будет записано расстояние
                    # Максимальное расстояние в метрах
                    "maxDistance": ((appart_info.radius+0.45) * 1000),
                    "spherical": True,  # Использование сферической модели для вычислений
                    "query": {
                        "type": {
                            "$in": appart_info.app_type  # Фильтрация по типу
                        }
                    }
                }
            },
            {
                "$project": {
                    "name": 1,  # Включить поле name
                    "address": 1,  # Включить поле address
                    "type": 1,  # Включить поле type
                    "location": 1,  # Включить поле location
                    "dist.calculated": 1,  # Включить поле с вычисленным расстоянием
                    '_id': 0  # Исключить поле _id
                }
            }
        ])
        documents = [doc for doc in results]
        documents.extend(cords)
        print(documents)
        return documents
    except Exception as e:
        print(f"An error occurred: {e}")

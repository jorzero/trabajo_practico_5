from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
import uuid

app = FastAPI(
    title="APIs en clase de Mlops 5",
    version="0.0.1"
)


# Modelo de datos para el registro de usuarios
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


# Diccionario para almacenar los usuarios
users = {}


@app.post("/register")
async def register_user(user: UserRegister):
    # Comprobamos si el usuario ya existe
    if any(u for u in users.values() if u['username'] == user.username or u['email'] == user.email):
        return JSONResponse(
            content={"message": "El usuario o correo electrónico ya está registrado."},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Generamos un ID único para el nuevo usuario
    user_id = str(uuid.uuid4())

    # Guardamos el usuario en el diccionario
    users[user_id] = {
        "username": user.username,
        "email": user.email,
        "password": user.password  # En un caso real, la contraseña debería ser encriptada
    }

    # Respuesta de éxito
    return JSONResponse(
        content={
            "message": "Usuario registrado exitosamente.",
            "user_id": user_id
        },
        status_code=status.HTTP_201_CREATED
    )
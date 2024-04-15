from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
import uuid

app = FastAPI(
    title="APIs trabajo en casa Mlops 5",
    version="0.0.3"
)


# Modelo de datos para el registro de usuarios
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

# Modelo de datos para la creación de tareas
class TaskCreate(BaseModel):
    title: str
    description: str
    status: str  # Podría ser 'pendiente', 'en progreso', 'completada'

# Diccionario para almacenar los usuarios y las tareas
users = {}
tasks = {}

@app.post("/register")
async def register_user(user: UserRegister):
    if any(u for u in users.values() if u['username'] == user.username or u['email'] == user.email):
        return JSONResponse(
            content={"message": "El usuario o correo electrónico ya está registrado."},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    user_id = str(uuid.uuid4())
    users[user_id] = {
        "username": user.username,
        "email": user.email,
        "password": user.password  # En un caso real, la contraseña debería ser encriptada
    }
    return JSONResponse(
        content={"message": "Usuario registrado exitosamente.", "user_id": user_id},
        status_code=status.HTTP_201_CREATED
    )

@app.get("/user/{user_id}")
async def get_user(user_id: str):
    if user_id in users:
        return JSONResponse(content=users[user_id], status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={"message": "Usuario no encontrado."}, status_code=status.HTTP_404_NOT_FOUND)

@app.post("/tasks/create")
async def create_task(task: TaskCreate):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "title": task.title,
        "description": task.description,
        "status": task.status
    }
    return JSONResponse(
        content={"message": "Tarea creada exitosamente.", "task_id": task_id},
        status_code=status.HTTP_201_CREATED
    )

from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from schema.user_schema import UserSchema, DataUser
from config.db import engine
from model.users import users
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List

user = APIRouter()

@user.get("/")
def root():
  return {"Message": "Hi there, Fast api here with a router"}

@user.get("/api/user", response_model=List[UserSchema])#aqui se transforma los resultado en una lista para poder motrarlo en pantalla la lista de usuarios
def get_users():
  with engine.connect() as conn:
    result = conn.execute(users.select()).fetchall()
    return result

@user.get("/api/user/{user_id}", response_model=UserSchema)#aqui le decimo que solo debe devolver un solo usuario
def get_user(user_id: str):
  with engine.connect() as conn:
    result = conn.execute(users.select().where(users.c.id == user_id)).first() # la letra C hace referencia a la columna en nuestra  base de datos que en este caso se hace referencia a la columna de id
    return result

@user.post("/api/user", status_code=HTTP_201_CREATED)#el codigo 201 confirma que la ejecucion fue correcta
def create_user(data_user: UserSchema):
  with engine.connect() as conn: # con with nos aseguramos que se cierre nuestra base de datos constantemente
    new_user = data_user.dict()#convertimos la informacion en un object para que pueda ser isertada en la base de datos
    new_user["password"] = generate_password_hash(data_user.password, "pbkdf2:sha256:30", 30)# el 30 significa la cantidad de caracteres que se van a imprimir, no importa si la contraseña es de solo 3 caracteres
    conn.execute(users.insert().values(new_user))#de esta manera insertamos la informacion a la base de datos
    conn.commit()#es necesario hacer el commit para que la informacion quede registrada en la base de datos e
    return Response(status_code=HTTP_201_CREATED)


@user.post("/api/user/login", status_code=200)
def user_login(data_user: DataUser):
  with engine.connect() as conn:
    result = conn.execute(users.select().where(users.c.username == data_user.username)).first()

    if result != None:
      check_passw = check_password_hash(result[3], data_user.password)
      #se crea el siguiente if para comunicar que el password es correcto
      if check_passw:
        return {
          "status": 200,
          "message": "Success"
        }
    #se envia esta respuesta para comunicar que el password no es correcto
    return {
      "status": HTTP_401_UNAUTHORIZED,
       "message": "Access Denied"
    }


@user.put("/api/user/{user_id}", response_model=UserSchema)
def update_user(data_update: UserSchema, user_id: str):
  with engine.connect() as conn:
    encrypt_passw = generate_password_hash(data_update.password, "pbkdf2:sha256:30", 30)
    conn.execute(users.update().values(name=data_update.name, username=data_update.username, password=encrypt_passw).where(users.c.id == user_id))#de esta manera obtenemos los datos que necesitamos para ser actualizados
    result = conn.execute(users.select().where(users.c.id == user_id)).first()
    return result

@user.delete("/api/user/{user_id}", status_code=HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
  with engine.connect() as conn:
    conn.execute(users.delete().where(users.c.id == user_id))
    conn.commit()#para que se pueda ejecutar y registrar algun ca,bio en la base de datos se debe hacer commit()

    return Response(status_code=HTTP_204_NO_CONTENT)

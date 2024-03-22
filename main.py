from fastapi import FastAPI
from router.router import user # esta es la manera de importar un archivo de una carpeta 

app = FastAPI()

app.include_router(user) #incluimos el router que se ha creado en el archivo router.py y se pasa como parametro a app

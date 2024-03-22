from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://ale:1234@localhost:3306/fastapi")#create engine necesita algunos parametros para poder hacer la conexion con la base de datos
                        #mysql+pymysql son modulos que estaremos utilizando para la conexion a nuestra base de datos
                        #despues de los :// le indicamos el usuario, luego la contraseña y luego el host que estamos utilizando y al final el nombre de la base de datos a la que nos estamos conenctado
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
conn = engine.connect()
meta_data = MetaData()

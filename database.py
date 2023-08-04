from sqlmodel import create_engine
import os

# Obtiene la ruta del directorio actual del archivo de código en ejecución:
BASE_DIR = os.path.dirname(os.path.realpath(__file__))


#Combina la ruta del directorio actual (BASE_DIR) con el nombre de la base de datos ('books.db') para obtener la ruta completa del archivo de la base de datos.
conn_str= 'sqlite:///'+os.path.join(BASE_DIR,'database.db')

connect_args = {"check_same_thread": False} #! Sirve para no usar la misma sessión en cada request

engine=create_engine(conn_str,echo=True, connect_args=connect_args,  pool_pre_ping=True)

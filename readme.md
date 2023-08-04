activar enviroment


```bash
source "c:/Users/danny/OneDrive/Escritorio/Gems/dev-env/Scripts/activate"
```

Instalar dependencias
```bash
pip install -r requirements.txt
```

### Para correr el server:
```bash
uvicorn main:app --port 5000 --reload
```

### Create .env file
```bash
cp .env.example .env
```

Para crear la base de datos:
 ```bash
 python create_db.py
  ```

# Alembic

```bash
alembic init migrations
```

Inside the container:
```bash
alembic revision --autogenerate -m "init"
alembic revision --autogenerate -m "create tables"
alembic upgrade head
```
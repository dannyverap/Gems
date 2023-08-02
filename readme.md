

### Para correr el server:
```bash
uvicorn main:app --port 5000 --reload
```

```bash
source "c:/Users/danny/OneDrive/Escritorio/Gems/dev-env/Scripts/activate"
```

### Create .env file
```bash
cp .env.example .env
```

Para crear la base de datos:
 ```bash
 python create_db.py
  ```

Inside the container:
```bash
alembic revision --autogenerate -m "create tables"
alembic upgrade head
```
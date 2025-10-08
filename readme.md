#### Backend proyecto BDs

**Instalar dependencias**
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Crear environment variables en powershell**
```
New-Item -Path . -Name ".env" -ItemType "file"
```

**Crear environment variables en cmd**
```
echo. > .env
```

**Contenido del .env**
```
CREDENTIALS=postgresql+psycopg2://postgres:PASSWORD@localhost:5432/DB_NAME
```

**Ejecutar backend**
```
uvicorn main:app --reload
```

**Actualizar las dependencias**
```
pip freeze > requirements.txt
```

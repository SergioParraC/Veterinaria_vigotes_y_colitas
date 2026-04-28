<em> # 🐾 Veterinaria Django </em>

Proyecto web de gestión para una veterinaria, desarrollado con Django.

## ✨ Requisitos previos

- 🐍 Python **3.8 o superior** (mínimo requerido)
- 📦 pip
- 🧰 Git

## 📚 Dependencias del proyecto

Instaladas desde `requirements.txt` con el comando

```powershell
python -m pip install -r requirements.txt
```

- Django==4.2.30
- Pillow==10.4.0

## 🪟 Cómo iniciar el entorno virtual en Windows (PowerShell)

NOTA: Si ya tienes el entorno virtual, inicialo con este comando:

```powershell
.\env\Scripts\Activate.ps1
```

#### 1) Ubícate en la carpeta del proyecto, desde el explorador de archivos

#### 2) Precionar Shift + click derecho, seleccionar opción "Abrir terminal"

#### 3) Crea el entorno virtual (si aún no existe):

```powershell
python -m venv env
```

#### 4) Activa el entorno virtual:

```powershell
.\env\Scripts\Activate.ps1
```

#### 5) Si PowerShell bloquea scripts, habilita solo la sesión actual y vuelve a activar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\env\Scripts\Activate.ps1
```

#### 6) Instala dependencias:

```powershell
python -m pip install -r requirements.txt
```

## 🚀 Cómo iniciar el proyecto Django

Con el entorno virtual activo:

####1. Inicia el servidor de desarrollo:

```powershell
python manage.py runserver
```

####2. Abre en el navegador:

- http://127.0.0.1:8000/
- Panel admin: http://127.0.0.1:8000/admin/

## 🧩 Composición general de aplicaciones

El proyecto usa la carpeta `Aplicaciones/` para organizar módulos por dominio:

- 🏠 `home`: vistas y rutas de inicio
- 📦 `inventory`: categorías, proveedores y productos de inventario
- 🐶 `pets`: dueños, mascotas, historial médico, citas y vacunas
- 👤 `users`: modelo/lógica relacionada con usuarios del dominio
- 🩺 `veterinary`: funcionalidades veterinarias generales
- 💳 `billing`: módulo de facturación/cobros (base)

Y configuración principal en:

- ⚙️ `config/settings.py`
- 🧭 `config/urls.py`
- 🛠️ `manage.py`

## 🖼️ Uso de la carpeta `media`

La carpeta `media/` almacena archivos subidos por usuarios o por el sistema, por ejemplo:

- Imágenes de productos (`ImageField`)
- Otros archivos de contenido dinámico

En este proyecto:

- `MEDIA_URL = '/media/'`
- `MEDIA_ROOT = os.path.join(BASE_DIR, 'media')`

Durante desarrollo, Django sirve estos archivos mediante la configuración de rutas en `config/urls.py`.

## 🌿 Comandos Git y GitHub (subir repositorio y crear Pull Request)

#### 1) Siempre realiza una actualización de la rama **main** antes de realizar tu desarrollo, y cambia a **main**.

```bash
git checkout main
git pull origin main
```

#### 2) Crea tu rama y realiza los ajustes que requieras hacer.

```bash
git checkout -b nombre_de_tu_rama
```

#### 3) Añade tus cambios y valida que se hayan subido todos tus cambios.

```bash
git status
git add .
git status
```

#### 4) Crea el commit y sube tus cambios al repositorio remoto.

```bash
git commit -m "Comentario de tu commit, se muy breve"
git push -u origin nombre_de_tu_rama
```

#### 5) Crear Pull Request

1. Ir al repositorio en GitHub.
2. Click en **Compare & pull request**.
3. Completar título/descripción y crear PR.

## ✅ Notas rápidas

- Activa siempre el entorno virtual antes de ejecutar comandos de Django.
- Si cambias dependencias, actualiza `requirements.txt`.

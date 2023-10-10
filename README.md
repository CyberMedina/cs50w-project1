# Project1: Lectoria

Lectoria es una aplicación web desarrollada como parte del curso Web50. Esta plataforma permite a los usuarios buscar libros, visualizar datos relevantes como el título, autor, fecha de publicación e imágenes de la portada, además de poder realizar reseñas.

## **IMPORTANTE**
Ya que la base de datos está alojada en Render, tiende a fallar mucho en las consultas. Si la página se queda estancada por más de 15 segundos, por favor recargue manualmente y se solucionará. 

## Tecnologías Utilizadas
- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript (con especial uso de la función Fetch para hacer la página dinámica) y Jinja2 para la renderización de templates.
- **Base de Datos**: PostgreSQL

## Características Principales

- **Autenticación**: Los usuarios deben estar autenticados para acceder a la sección de búsqueda de libros.
- **Búsqueda Dinámica de Libros**: Se proporciona una barra de búsqueda para encontrar libros.
- **Modo Oscuro y Claro**: Los usuarios pueden cambiar entre el modo oscuro y claro a través de un switch.
- **Información Dinámica en la Página de Inicio**: Se muestran datos como el total de libros en el sitio, el total de usuarios registrados y un carousel con los 5 libros con más reseñas.

## Estructura del Proyecto

### Carpeta `static`
Almacena los archivos JavaScript, CSS, SASS y las imágenes utilizadas en el proyecto.

### Carpeta `templates`
Contiene todas las plantillas Jinja2 utilizadas para renderizar las páginas.

### Archivo `.env.template`
Contiene las claves de API necesarias como la de Google Books, la clave de la base de datos PostgreSQL en Render, y las claves para las sesiones de Flask y FlaskWTF.
Por favor borrar el ".template" del nombre para que qeude así ".env".

### Archivo `application.py`
Aloja todo el código necesario para que la aplicación funcione correctamente.

### Archivo `database.txt`
Contiene el script para la creación y configuración de la base de datos PostgreSQL.

### Archivo `db.py`
Gestiona la conexión con la base de datos.

### Archivo `forms.py`
Se encarga de la validación de formularios utilizando FlaskWTF, implementado particularmente en el formulario de registro.

### Archivo `helpers.py`
Incluye código de validaciones adicionales que son llamados dentro de la aplicación.

### Archivo `imports.py`
Aloja el código necesario para importar todos los archivos CSV a la base de datos.

### Archivo `requirements.txt`
Lista todas las dependencias necesarias para que la aplicación funcione correctamente.

## Instalación y Configuración

1. Clonar el repositorio: `git clone https://github.com/usuario/project1.git`
2. Configurar las variables de entorno copiando el archivo `.env.template` a un nuevo archivo llamado `.env` y llenando las claves correspondientes.
3. Ejecutar el script `database.txt` para configurar la base de datos en POSTGRESQL
4. Realizar un entorno virtual: `python -m venv venv`
5. Luego activarlo con: `venv/scripts/activate`
6. Instalar las dependencias con: `pip install -r requirements.txt`
7. Ejecutar la aplicación: `flask run`

## Autor
Jhonatan Jazmil Medina Aguirre

Grupo: D


Proyecto Chatbot de Soporte Técnico

Este repositorio contiene un proyecto para un chatbot de soporte técnico que utiliza Rasa y una base de datos MySQL para proporcionar respuestas a preguntas frecuentes (FAQ). El chatbot busca la respuesta más adecuada en la base de datos según la pregunta del usuario.

Pasos para Configurar y Ejecutar el Proyecto
1. Crear la Tabla en la Base de Datos
  Primero, utiliza el archivo SQL proporcionado (EA_chatbot-20240628.sql) para crear la tabla necesaria en tu base de datos MySQL. Esta tabla almacenará las preguntas y respuestas que el   chatbot utilizará para responder a las consultas de los usuarios.

2. Configurar el Archivo .env
  Utilizar el archivo .env en la raíz del proyecto y configura los parámetros necesarios, tales como:

  SMTP Server: Para configurar el servidor de correo.
  Cuenta de Ticketera: Para gestionar la creación de tickets.
  Datos de Conexión a la Base de Datos: Para conectar con la base de datos MySQL.

3. Construir la Imagen Docker
  Después de configurar el archivo .env, puedes construir la imagen Docker. Este paso compila el proyecto con la nueva configuración.
  "docker build -t rasa_chatbot ."

4. Ejecutar el Contenedor Docker
  Una vez que la imagen Docker se haya creado correctamente, puedes ejecutar el contenedor con la imagen recién creada.
  "docker run -p 5005:5005 rasa_chatbot"

Nota Importante
En la tabla faq creada en la base de datos, se almacenarán las posibles preguntas con sus respuestas. Cuando el usuario haga una pregunta, el sistema buscará la respuesta con el mayor porcentaje de coincidencia. En el futuro, podrás agregar un umbral de coincidencias para mejorar la precisión de las respuestas.


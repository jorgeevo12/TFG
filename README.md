# Asistente Conversacional con RASA

Este repositorio contiene el código y los datos del Trabajo de Fin de Grado (TFG) dedicado a la construcción de asistentes conversacionales usando RASA. El proyecto utiliza dos datasets: **DIHANA** y **MultiWOZ**, y está estructurado siguiendo diferentes enfoques de generación: `PATH_0`, `PATH_A` y `PATH_B`.

---

## 📦 Requisitos

Se recomienda el uso de un entorno virtual para evitar conflictos de dependencias. Para crear y activar uno:

# bash
# Crear el entorno virtual
python -m venv .venv

# Activar en Windows
.venv\Scripts\activate

# Activar en Linux/Mac
source .venv/bin/activate

Luego, instala las dependencias necesarias:
pip install -r requirements.txt



🧠 Ejecutar el Asistente con RASA
Para iniciar el servidor de RASA y permitir conexiones desde otras aplicaciones, utiliza:

rasa run --enable-api --cors "*"

Si deseas especificar un puerto diferente (por ejemplo, el 5006):

rasa run --enable-api --cors "*" --port 5006

Estos comandos deben ejecutarse desde la carpeta donde se encuentre el proyecto de RASA generado (por ejemplo, en dihana_chatbot/chatbot_generated si estás usando ese modelo).



💻 Interfaz de Usuario
En la carpeta IU/ se encuentra una interfaz construida con Streamlit. Para lanzarla:

cd IU
streamlit run chatbot_IU.py

Esta interfaz permite interactuar fácilmente con los modelos entrenados a partir del enfoque PATH_A para ambos datasets.



📁 Estructura del Proyecto

TFG/
|-- data/
|   |-- dihana/
|   |   `-- dihana_dialogues/
|   |       `-- processed_dialogues.json
|   `-- multiwoz_dialogues/
|       `-- processed_dialogues.json
|
|-- dihana_chatbot/
|   |-- chatbot_generated/
|   |   `-- models/
|   |-- PATH_0_chatbot_generated/
|   |   `-- models/
|   |-- PATH_B_chatbot_generated/
|   |   `-- models/
|   |-- results/
|   `-- scripts/
|
|-- multiwoz_chatbot/
|   |-- chatbot_generated/
|   |   `-- models/
|   |-- PATH_0_chatbot_generated/
|   |   `-- models/
|   |-- PATH_B_chatbot_generated/
|   |   `-- models/
|   |-- results/
|   `-- scripts/
|
`-- IU/
    `-- chatbot_IU.py


📝 Notas
Se ha utilizado un archivo .gitignore para excluir automáticamente entornos virtuales .venv/, archivos de prueba innecesarios (*.log, test_*.py) y carpetas pesadas como multiwoz/ o updates/.

Se recomienda entrenar y ejecutar los asistentes dentro de los directorios generados por cada PATH.

Los modelos RASA generados se encuentran en las subcarpetas models/ de cada enfoque.

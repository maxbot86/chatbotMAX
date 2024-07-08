#!/bin/sh

# Inicia el servidor de acciones en segundo plano
rasa run actions &

# Inicia el servidor de Rasa
rasa run --enable-api --cors "*" --port 5005


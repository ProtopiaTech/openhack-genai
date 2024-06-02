#!/bin/bash

# Funkcja do odczytania pliku .env
set_env_variables() {
  while IFS= read -r line; do
    # Pomija puste linie i linie zaczynające się od #
    [[ -z "$line" || "$line" == \#* ]] && continue
    # Dzieli linie na klucz i wartość
    IFS='=' read -r key value <<< "$line"
    # Ustawia zmienną środowiskową w Azure Web App
    az webapp config appsettings set --resource-group $RESOURCE_GROUP --name $WEBAPP_NAME --settings "$key=$value"
  done < "$1"
}

# Wywołanie funkcji z plikiem .env
set_env_variables .env
#!/bin/bash

# Path to the .env file
ENV_PATH="src/.env"

# Load variables from .env file
if [ -f $ENV_PATH ]; then
    export $(cat $ENV_PATH | xargs)
else
    echo ".env file not found at $ENV_PATH"
    exit 1
fi

# Check if variables are set
if [ -z "$STORAGE_ACCOUNT_NAME" ] || [ -z "$STORAGE_CONTAINER_NAME_IN" ]; then
    echo "STORAGE_ACCOUNT_NAME or STORAGE_CONTAINER_NAME_IN is not set in the .env file"
    exit 1
fi

# Path to the directory with files to upload
UPLOAD_PATH="data"

# Check if the directory exists
if [ ! -d "$UPLOAD_PATH" ]; then
    echo "Directory $UPLOAD_PATH does not exist"
    exit 1
fi

# Upload files to the Azure Storage container
for file in $UPLOAD_PATH/*; do
    if [ -f "$file" ]; then
        echo "Uploading $file..."
        az storage blob upload --account-name $STORAGE_ACCOUNT_NAME --container-name $STORAGE_CONTAINER_NAME_IN --file "$file" --name $(basename "$file") --overwrite true
    fi
done

echo "Upload completed."

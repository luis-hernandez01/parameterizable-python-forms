import requests
from fastapi import HTTPException, UploadFile
import os

# URL y token del servicio externo
EXTERNAL_URL = "https://as-aikawayra-file-notif-dev-b1-eastus.azurewebsites.net/api/v1/files/upload"
TOKEN = os.getenv("EXTERNAL_TOKEN", 
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJzdWIiOiIyIiwiZXhwIjoxNzYyOTc2NzYzLCJ0eXBlIjoicmVmcmVzaCJ9."
    "d0mZpuYmBuUYgR3qyLsKkg6F1xffz6kOTufktERP3E4"
)

async def send_file_to_external_service(file: UploadFile) -> dict:
    """
    Envía el archivo al servicio externo de Azure (multipart/form-data).
    """
    try:
        files = {
            "file": (file.filename, file.file, file.content_type),
            "container": (None, "files"),
        }
        # data = {"container": container}
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "accept": "application/json"
        }

        response = requests.post(EXTERNAL_URL, headers=headers, files=files)

        if response.status_code not in (200, 201):
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error del servicio externo: {response.text}"
            )

        return response.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fallo al enviar archivo: {str(e)}")

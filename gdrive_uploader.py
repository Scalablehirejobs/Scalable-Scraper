# gdrive_uploader.py

import toml
import pandas as pd
import datetime
from io import BytesIO
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from googleapiclient.discovery import build

def get_drive_service():
    secrets = st.secrets["google"]
    creds = Credentials(
        token=None,
        refresh_token=secrets["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=secrets["client_id"],
        client_secret=secrets["client_secret"]
    )
    return build("drive", "v3", credentials=creds)

def get_today_filename():
    return "nhs_" + datetime.date.today().isoformat() + ".xlsx"

def find_file(service, filename):
    query = f"name = '{filename}' and mimeType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])
    return files[0] if files else None

def upload_new_file(service, df, filename):
    df = df.sort_values(by="Date Posted", ascending=False)
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    buffer.seek(0)
    media = MediaIoBaseUpload(buffer, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    file_metadata = {'name': filename, 'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()

def update_existing_file(service, file_id, local_df):
    request = service.files().get_media(fileId=file_id)
    fh = BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)

    # Read Excel
    existing_df = pd.read_excel(fh)
    merged_df = pd.concat([existing_df, local_df]).drop_duplicates()
    merged_df = merged_df.sort_values(by="Date Posted", ascending=False)

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        merged_df.to_excel(writer, index=False)
    buffer.seek(0)

    media = MediaIoBaseUpload(buffer, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    service.files().update(fileId=file_id, media_body=media).execute()

def upload_to_drive(df):
    filename = get_today_filename()
    service = get_drive_service()
    file_info = find_file(service, filename)
    if file_info:
        update_existing_file(service, file_info['id'], df)
        return "File updated successfully!"
    else:
        upload_new_file(service, df, filename)
        return "New Excel file uploaded successfully!"

from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import os.path
import constants

def init():
    print("initializing google drive...")
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
    if os.path.exists("drive_token.json"):
        creds = Credentials.from_authorized_user_file("drive_token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("drive_token.json", "w") as token:
            token.write(creds.to_json())

    return creds

def upload_basic(folder_id, filename):
  """Insert new file.
  Returns : Id's of the file uploaded

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  try:
    # create drive api client
    service = build("drive", "v3", credentials=constants.CREDS['drive'])

    file_metadata = {"name": filename, "parents": [ folder_id]}
    media = MediaFileUpload(filename, mimetype="text/csv")
    # pylint: disable=maybe-no-member
    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    print(f'File ID: {file.get("id")}')

  except HttpError as error:
    print(f"An error occurred: {error}")
    file = None

  return file.get("id")


def uploadCSV(folder_id, filename):
    upload_basic(folder_id, filename)
    print('report uploaded successfully.')

def create_folder(parent_id, filename):
  """Create a folder and prints the folder ID
  Returns : Folder Id

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """

  try:
    # create drive api client
    service = build("drive", "v3", credentials=constants.CREDS['drive'])
    file_metadata = {
        "name": filename,
        "mimeType": "application/vnd.google-apps.folder",
        "parents" : [parent_id],
        "owners" : ['example@gmail.com']
    }

    # pylint: disable=maybe-no-member
    file = service.files().create(body=file_metadata, fields="id").execute()
    print(f'Folder ID: "{file.get("id")}".')
    return file.get("id")

  except HttpError as error:
    print(f"An error occurred: {error}")
    return None

def search_file(filename):
  """Search file in drive location

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """

  try:
    # create drive api client
    service = build("drive", "v3", credentials=constants.CREDS['drive'])
    files = []
    page_token = None
    while True:
      # pylint: disable=maybe-no-member
      response = (
          service.files()
          .list(
              q=f"mimeType='application/vnd.google-apps.folder' AND name='{filename}'",
              spaces="drive",
              fields="nextPageToken, files(id, name)",
              pageToken=page_token,
          )
          .execute()
      )
      for file in response.get("files", []):
        # Process change
        print(f'Found file: {file.get("name")}, {file.get("id")}')
      files.extend(response.get("files", []))
      page_token = response.get("nextPageToken", None)
      if page_token is None:
        break

  except HttpError as error:
    print(f"An error occurred: {error}")
    files = None

  return files


def search_file_in_parent(filename, parent_id):
  """Search file in drive location

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """

  try:
    # create drive api client
    service = build("drive", "v3", credentials=constants.CREDS['drive'])
    files = []
    page_token = None
    while True:
      # pylint: disable=maybe-no-member
      response = (
          service.files()
          .list(
              q=f"mimeType='application/vnd.google-apps.folder' AND name='{filename}' AND '{parent_id}' in parents",
              spaces="drive",
              fields="nextPageToken, files(id, name, parents)",
              pageToken=page_token,
          )
          .execute()
      )
      for file in response.get("files", []):
        # Process change
        print(f'Found file: {file.get("name")}, {file.get("id")}')
      files.extend(response.get("files", []))
      page_token = response.get("nextPageToken", None)
      if page_token is None:
        break

  except HttpError as error:
    print(f"An error occurred: {error}")
    files = None

  return files

def get_folder_id_else_create(path):
    folder_tree_list = path.split("/")
    parent_id = None
    for folder_name in folder_tree_list:
        if parent_id:
            folder_metadata = search_file_in_parent(folder_name, parent_id)
        else:
            folder_metadata = search_file(folder_name)
        if len(folder_metadata) == 0:
            parent_id = create_folder(parent_id, folder_name)
        else:
            parent_id = folder_metadata[0]['id']
    return parent_id
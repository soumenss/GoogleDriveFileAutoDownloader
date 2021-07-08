from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import io 
from googleapiclient.http import MediaIoBaseDownload
import sys

# The item to be downloaded should be specified with extension here
downloaditem = 'testimage.jpg'

# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPES = ['https://www.googleapis.com/auth/drive']



creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('drive', 'v3', credentials=creds)

# Call the Drive v3 API
results = service.files().list(fields="nextPageToken, files(id, name)").execute()  # pageSize=10, 
items = results.get('files', [])

# print(items)

if not items:
    print('No files found.')

else:
    # print('Files:')
    for item in items:
        # print(item)
        print(item['name'])
        # print(u'{0} ({1})'.format(item['name'], item['id']))
        if(item['name'] == downloaditem):
        	fileid = item['id']
        	print(fileid)
        	location = 'D:/PythonWithSublime/' + 'test.jpg'
        	request = service.files().get_media(fileId=fileid)
        	# fh = io.BytesIO('wb')
        	fh = io.FileIO(location, 'wb')
        	downloader = MediaIoBaseDownload(fh, request)
        	done = False
        	while done is False:
        		status, done = downloader.next_chunk()
        		sys.stdout.flush()
        		print('Downloaded the file')
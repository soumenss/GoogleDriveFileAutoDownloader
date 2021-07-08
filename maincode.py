from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import io 
from googleapiclient.http import MediaIoBaseDownload
import sys

from time import time, sleep

# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
# This was the previous SCOPES, but couldn't download files

SCOPES = ['https://www.googleapis.com/auth/drive'] # This allows to download
# SCOPES list https://developers.google.com/drive/api/v3/about-auth

# We will start without credentials
creds = None

# Place where the file will be saved with certain name
location = 'D:/PythonWithSublime/' + 'test.jpg'

itemlist = [] # The list where the file names will be stored
timetocheck = 5 # Refresh rate in seconds
count = 0 # Intializing a count

# The file which will be downloaded first will have to be named with this
# The later files will be downloaded automatically
startfile = 'testimage.jpg'

# The extension which will be downloaded regardless of upper or lowercase
requiredext = 'jpg'

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
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

#The loop starts
while True:
	print(count) # To monitor if the code is running

	# Sleep the program for refresh time
	sleep(timetocheck - time() % timetocheck)

	#The credentials are already built
	creds = Credentials.from_authorized_user_file('token.json', SCOPES)

	#Building the service library
	service = build('drive', 'v3', credentials=creds)
	# Call the Drive v3 API
	results = service.files().list(fields="nextPageToken, files(id, name)").execute()
	items = results.get('files', [])

	count = count + 1

	if count == 1:
		# For the first time iteration, list all the files and download the startfile 
		for item in items:
			itemlist.append(item['name'])
			if item['name'].lower() == startfile:
				fileid = item['id']
				request = service.files().get_media(fileId=fileid)

				# location = 'D:/PythonWithSublime/' + item['name']
				# Un-commenting this will download the file with its original name
				
				fh = io.FileIO(location, 'wb')
				downloader = MediaIoBaseDownload(fh, request)
				done = False
				while done is False:
					status, done = downloader.next_chunk()

					# Without this the file is downloaded but not flushed
					sys.stdout.flush()
					print('Downloaded the first file')

	else:
		if not items:
			print('No files found.')
		else:
			for item in items:
				parts = item['name'].split('.')
				ext = parts[-1].lower() # Taking the extension
				# if item['name'] in itemlist:
				# 	print('Not a new file')
				if item['name'] not in itemlist and ext == requiredext:
					itemlist.append(item['name'])
					fileid = item['id']
					request = service.files().get_media(fileId=fileid)

					# location = 'D:/PythonWithSublime/' + item['name']
					fh = io.FileIO(location, 'wb')
					downloader = MediaIoBaseDownload(fh, request)
					done = False
					while done is False:
						status, done = downloader.next_chunk()
						sys.stdout.flush()
						print('Downloaded a new file')
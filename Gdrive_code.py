!pip install -U -q PyDrive

import os
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

# 1. Authenticate and create the PyDrive client.
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

# 2. Read list of all google drive folders and Auto-iterate using the query syntax
df_gdrive_list = pd.read_csv('/content/GoogleDrive_VDC.csv')
for row in df_gdrive_list.itertuples(index=True, name='Pandas'):
    os.chdir('/content/')
    print(row.folder_id, row.dataset)
    file_list = drive.ListFile({'q': "'" + row.folder_id +"' in parents"}).GetList()
    vendor_bucket = row.dataset
    vendor_bucket_path = '/content/' + row.dataset
    os.mkdir(vendor_bucket)
    os.chdir(vendor_bucket_path)
    for f in file_list:
      # 3. Create & download by id.
      print('title: %s, id: %s, size: %s' % (f['title'], f['id'], f['fileSize']))
      fname = f['title']
      print('downloading {}'.format(fname))
      f_ = drive.CreateFile({'id': f['id']})
      f_.GetContentFile(fname)

!zip -r /content/file.zip /content/*
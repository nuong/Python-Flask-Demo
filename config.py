import os

# The secret key is used by Flask to encrypt session cookies.
# [START secret_key]
SECRET_KEY = '\x14\x801\xd2\xd5\xbb\xdb^\x11\x1f\xd8\x1f\xfc\x07\xb0\x1ar\xefh-T\xf2\xe2h'
# [END secret_key]

# Google Cloud Project ID. This can be found on the 'Overview' page at
# https://console.developers.google.com
PROJECT_ID = 'python-flask-demo-241716'

MONGO_URI = 'mongodb://nuongnguyen_user:jxCAj1TAql9N3Knx@cluster0-shard-00-00-fsk2j.mongodb.net:27017,cluster0-shard-00-01-fsk2j.mongodb.net:27017,cluster0-shard-00-02-fsk2j.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true'

# Google Cloud Storage and upload settings.
# Typically, you'll name your bucket the same as your project. To create a
# bucket:
#
#   $ gsutil mb gs://<your-bucket-name>
#
# You also need to make sure that the default ACL is set to public-read,
# otherwise users will not be able to see their upload images:
#
#   $ gsutil defacl set public-read gs://<your-bucket-name>
#
# You can adjust the max content length and allow extensions settings to allow
# larger or more varied file types if desired.
CLOUD_STORAGE_BUCKET = 'python-flask-demo-storage'
MAX_CONTENT_LENGTH = 8 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# OAuth2 configuration.
# This can be generated from the Google Developers Console at
# https://console.developers.google.com/project/_/apiui/credential.
# Note that you will need to add all URLs that your application uses as
# authorized redirect URIs. For example, typically you would add the following:
#
#  * http://localhost:8080/oauth2callback
#  * https://<your-app-id>.appspot.com/oauth2callback.
#
# If you receive a invalid redirect URI error review you settings to ensure
# that the current URI is allowed.
GOOGLE_OAUTH2_CLIENT_ID = \
    '1091996557552-au1vmj54cvjts2u0454u16alo5n6hn67.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = '1q6NqNdEYDKo33GkNIcIfjsk'

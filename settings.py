import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

LOCAL_DEBUG = os.environ.get('LOCAL_DEBUG', False)

CRED_GCP_PATH = './cred_gcp.json'
if not Path(CRED_GCP_PATH).exists():
    with open(CRED_GCP_PATH, 'w', encoding='utf8') as f:
        f.write(os.environ['JSON_GCP'])
CRED_FIREBASE_PATH = './cred_firebase.json'
if not Path(CRED_FIREBASE_PATH).exists():
    with open(CRED_FIREBASE_PATH, 'w', encoding='utf8') as f:
        f.write(os.environ['JSON_FIREBASE'])

MOONSHINE_CHANNEL = os.environ.get('MOONSHINE_CHANNEL', '_')
LINE_API = os.environ['LINE_API']
LINE_HANDLE = os.environ['LINE_HANDLE']
MEME_WEBSITE = os.environ['MEME_WEBSITE']

reaction = {
    '幹一定是': '米咕嘰',
    '一定是': '米咕嘰',
    '沒錢': 'https://i.imgur.com/ahlkzYk.jpg',
    '價格': 'https://i.imgur.com/QGRAiUn.jpg'
}

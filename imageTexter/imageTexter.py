from PIL import Image, ImageDraw, ImageFont
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import os
import time
from io import BytesIO
import requests
import datetime
import settings
from imageTexter.lol.generator import LOLGenerator


class ImageTexter(object):
    def __init__(self):
        cred = credentials.Certificate(settings.CRED_FIREBASE_PATH)
        firebase_admin.initialize_app(cred, {
            'projectId': 'ms-meme',
            'storageBucket': 'ms-meme.appspot.com'
        })

        self.db = firestore.client()
        self.bucket = storage.bucket()

        self.font_path = os.path.join(
            os.path.dirname(__file__),
            'noto.otf'
        )
        self.lol = LOLGenerator()

    def generate(self, source, texts):
        doc_ref = self.db.collection('templates').document(source)

        snapshot = doc_ref.get()
        doc = snapshot.to_dict()

        if doc is None:
            return f'沒有這個詞啦！ 自己加：\n{settings.MEME_WEBSITE}'

        response = requests.get(doc['url'])
        img = BytesIO(response.content)
        image = Image.open(img)
        image_height = image.size[1]
        image_width = image.size[0]
        draw = ImageDraw.Draw(image)

        for idx, text in enumerate(texts):
            font_size = 25
            font = ImageFont.truetype(self.font_path, font_size)
            while font.getsize(text)[0] > image_width:
                font_size -= 1
                font = ImageFont.truetype(self.font_path, font_size)

            text_size = font.getsize(text)

            t_x = (image_width / 2) - (text_size[0] / 2)
            t_y = image_height * 0.98 - text_size[1]
            if len(texts) >= 2 and idx == 0:
                t_y = -3 * font_size / 25.0
            draw.text((t_x - 1, t_y - 1), text, fill='black', font=font)
            draw.text((t_x + 1, t_y - 1), text, fill='black', font=font)
            draw.text((t_x - 1, t_y + 1), text, fill='black', font=font)
            draw.text((t_x + 1, t_y + 1), text, fill='black', font=font)
            draw.text((t_x, t_y), text, fill='white', font=font)

        output = BytesIO()
        image.save(output, format='JPEG', quality=85)
        img.close()

        # UPLOAD
        id = str(time.time()).replace('.', '')
        blob = self.bucket.blob('memes/' + id + '.jpg')
        blob.upload_from_string(output.getvalue(), content_type='image/jpeg')
        blob.make_public()
        public_url = blob.public_url

        output.close()

        # FIRESTORE
        memes_ref = self.db.collection('memes')
        new_meme = memes_ref.add({
            'content': ' '.join(texts),
            'template': source,
            'url': public_url,
            'date': datetime.datetime.now(),
        })

        doc_ref.update({
            'count': doc['count'] + 1,
            'usedBy': doc['usedBy'] + [new_meme[1].id]
        })

        return public_url

    def draw_lol(self):
        image = self.lol.generate()

        output = BytesIO()
        image.save(output, format='JPEG', quality=10)

        # UPLOAD
        id = str(time.time()).replace('.', '')
        blob = self.bucket.blob('others/lol_' + id + '.jpg')
        blob.upload_from_string(output.getvalue(), content_type='image/jpeg')
        blob.make_public()
        public_url = blob.public_url

        output.close()

        return public_url

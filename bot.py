from linebot import LineBotApi
from linebot.models import (
    TextSendMessage, ImageSendMessage, VideoSendMessage
)
import settings


class Bot(object):
    def __init__(self, token):
        self.api = LineBotApi(token)

    def reply(self, token, content):
        if settings.LOCAL_DEBUG:
            print(content)
            return

        # 偵測是不是gfycat訊息
        if content.startswith('_gfycat'):
            name = content.split(' ')[1]
            video_message = VideoSendMessage(
                original_content_url='https://giant.gfycat.com/{}.mp4'.format(name),
                preview_image_url='https://thumbs.gfycat.com/{}-mobile.jpg'.format(name)
            )
            self.api.reply_message(
                token, video_message)
            return
        # 偵測是不是影片訊息
        if content[-3:].lower() in ('mp4', 'mov', 'avi', 'webm'):
            preview = content[:-3] + 'jpg'
            video_message = VideoSendMessage(
                original_content_url=content,
                preview_image_url=preview
            )
            self.api.reply_message(
                token, video_message)
            return
        # 偵測是不是圖片訊息
        ext = content[-3:].lower()
        img_list = ['jpg', 'png', 'gif']
        if ext in img_list:
            image_message = ImageSendMessage(
                original_content_url=content,
                preview_image_url=content
            )
            self.api.reply_message(
                token, image_message)
        else:
            self.api.reply_message(
                token, TextSendMessage(text=content))

import random
import re


class SmartBrain(object):
    def __init__(self):
        self.pat_twoask = r'\A里長.+?([會能是要有]|可以).+?[？?]\Z'
        self.pat_multi = r'(\s[^\s]+)'

    def detect(self, message):
        match = re.search(self.pat_twoask, message)
        if match:
            keyword = match.group(1)
            if random.random() > 0.5:
                if keyword == '要':
                    keyword = '不用'
                elif keyword == '有':
                    keyword = '沒有'
                else:
                    keyword = '不' + keyword
            return keyword

        match = re.findall(self.pat_multi, message)
        if message.startswith('里長幫抽') and len(match) >= 3:
            q = match[0]
            idx = int(round(random.random() * (len(match) - 2.0)))
            ans = match[idx + 1].strip()
            reply = '{}\n{}'.format(q.strip(), ans)
            return reply
        return None

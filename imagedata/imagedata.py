from google.cloud import datastore
import random
import settings


class ImageData(object):
    def __init__(self):
        self.client = datastore.Client.from_service_account_json(
            settings.CRED_GCP_PATH
        )

    def get_entity(self, kind):
        def init_query():
            this_query = self.client.query(kind=from_kind)
            if kind == 'boob':
                this_query.add_filter('boob', '=', True)
            elif kind == 'beauty':
                this_query.add_filter('boob', '=', False)
            return this_query

        print('Connect to Google DataStore...')
        if kind in ['boob', 'beauty']:
            from_kind = 'beauty_images'
        else:
            from_kind = kind
        query = init_query()
        query.order = ['count']

        min_entity = list(query.fetch(1))[0]
        min_count = min_entity['count']

        query = init_query()
        query.add_filter('count', '=', min_count)

        rand_num = int(random.random() * 10000000)
        query.add_filter('rand', '>=', rand_num)
        query.order = ['rand']
        result = list(query.fetch(1))

        if len(result) != 0:
            print('Get Result Successfully.')
            return result[0]
        else:
            print('Empty Result, First Item Instead.')
            query = init_query()
            query.add_filter('count', '=', min_count)
            return list(query.fetch(1))[0]

    def get_image_url(self, kind):
        entity = self.get_entity(kind)
        entity['count'] += 1

        self.client.put(entity)

        return entity['image_url'].replace('http:', 'https:')

    def get_mslife_log(self):
        query = self.client.query(kind='__Stat_Kind__')
        query.add_filter('kind_name', '=', 'mslife')
        all_result = list(query.fetch())
        all_count = all_result[0]['count']
        query = self.client.query(kind='mslife')
        query.add_filter('count', '=', 0)
        query.keys_only()
        get_result = list(query.fetch())
        get_count = len(get_result)
        message = '已抽了{}張圖(影)片\n還有{}張未抽'.format(all_count - get_count, get_count)
        return message

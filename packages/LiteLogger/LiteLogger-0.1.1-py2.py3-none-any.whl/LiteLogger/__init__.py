import json
import logging
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

MAX_POOLSIZE = 100

class LiteLoggerHandler(logging.Handler):
    def __init__(self, stream_name, api_key, url=None, verbose: bool = False):
        '''
        This is the LiteLogger handler. This will direct log messages to the LiteLogger API.
        :param stream_name: The stream name in which to send the log message to
        :param api_key: The API key associated with your account.
        :param url: an alternative URL to send the request to. This is primarily used for running tests or for
                    custom/self-hosted versions of LiteLogger
        :param verbose: print verbose outputs
        '''
        self.url = url or 'https://app.litelogger.com/api/v2/methods/LogStreams.LogItems.add'
        self.api_key = api_key
        self.stream_name = stream_name
        self.verbose = verbose

        self.session = session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json',
            # 'Authorization': f'Bearer {self.api_key}'
            'Bearer': f'{self.api_key}'
        })

        # this will attach retry settings.
        self.session.mount('https://', HTTPAdapter(
            max_retries=Retry(
                total=6,
                backoff_factor=0.5,
                status_forcelist=[403, 500]
            ),
            pool_connections=MAX_POOLSIZE,
            pool_maxsize=MAX_POOLSIZE
        ))

        super().__init__()

    def emit(self, record):
        '''
        This overrides the base class to provide the request to the LL API
        '''

        # Get the time of the record and convert it to milliseconds
        milliseconds_epoc = int(record.created * (1000/1))

        tags = []
        metadata = {}

        if hasattr(record, 'metadata'):
            metadata = record.metadata

        if hasattr(record, 'tags'):
            tags = record.tags

        level_lowercase = str(record.levelname).lower()

        d = json.dumps(
            {
                "stream_name": self.stream_name,
                'msg': record.msg,
                'level': level_lowercase,
                'event_time': milliseconds_epoc,
                'tags': tags,
                'metadata': metadata
            })

        # There is no support yet for formatters, but this is where it would be added.
        # logEntry = self.format(record)

        response = self.session.post(self.url, data=d)

        if self.verbose:
            print(d)
            print(response.content)

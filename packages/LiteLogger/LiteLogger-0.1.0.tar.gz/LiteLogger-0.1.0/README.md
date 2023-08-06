# LiteLogger for Python

This is the official repo of the LiteLogger client for python. This make it easy to integrate LiteLogger into your existing logging infrastructure.

## Installation

`pip install LiteLogger`

## Usage
Below is a simple example. See the 'examples' folder for more comprehensive examples.
```python
import logging
from LiteLogger import LiteLoggerHandler

log = logging.getLogger(__name__)

API_KEY = 'your_api_key'
STREAM_NAME = 'Your Log Stream Name'

# create the LiteLogger Handler
llhandler = LiteLoggerHandler(
	STREAM_NAME,
	API_KEY,
)

# add handler to logger
log.addHandler(llhandler)

log.info('Some Log Message!', extra={
	'metadata': {'some_important_key': 'that keys value'},
	'tags': ['some tag', 'another tag']
})
```

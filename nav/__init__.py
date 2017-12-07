from flask import Flask
from nav.config import Config

app = Flask(__name__)

app.debug = True
app.secret_key = 'Security!'

# update application config
app.config.update(Config)

debug = app.logger.debug
info = app.logger.info

from nav.controller import index, user, link, tag

import os

from .base import *


ALLOWED_HOSTS = []
SECRET_KEY = os.environ.get("SECRET_KEY", "hello")

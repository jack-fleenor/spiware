from uuid import uuid as id
import http.server as http
from tkinter import Tk, Label
from datetime import datetime as dt

log_format = {
  'id': None,
  'timestamp': None,
  'status': None,
  'message': None,
  'type': None,
  'path': None
}

def log(message, type, status, path):
  log_format['id'] = str(id.uuid4())
  log_format['timestamp'] = str(dt.now())
  log_format['message'] = message
  log_format['status'] = status
  log_format['type'] = type
  log_format['path'] = path
  body = log_format
  return body

import os
from datetime import datetime

from constants import GET, HEAD, CONTENT_TYPE, HTTP_VERSION, HTTP_DATE, INDEX_PAGE, SERVER_NAME, OK, \
    METHOD_NOT_ALLOWED, NOT_FOUND, RESPONSE_STATUS, FORBIDDEN, PARENT_DIRECTORY, BYTES_STRING


class Response:

    def __init__(self, request, root_dir, content=None, content_length=None):
        self.code = NOT_FOUND
        self.content = content
        self.content_length = content_length
        self.content_type = CONTENT_TYPE.get(request.get_file_type())
        self.request = request
        self.root_dir = root_dir

    def get_file(self):
        if not self.request.get_allowed:
            self.code = FORBIDDEN
            return

        if self.request.get_method() not in [GET, HEAD]:
            self.code = METHOD_NOT_ALLOWED
            return

        if PARENT_DIRECTORY in self.request.get_url():
            self.code = FORBIDDEN
            return

        filename = os.path.normpath(self.root_dir + self.request.get_path())
        if os.path.isdir(filename):
            self.code = FORBIDDEN

        if not os.path.isfile(filename):
            filename = os.path.join(filename, INDEX_PAGE)

        try:
            with open(filename, 'rb') as f:
                content = f.read()
                self.content = content if self.request.get_method() == GET else BYTES_STRING
                self.content_length = len(content)
                self.code = OK
        except IOError as e:
            pass
            print('FILE NOT FIND: {}'.format(e.filename))

    def send_response(self):
        self.get_file()
        if self.code == OK:
            return (
                       'HTTP/{version} {status}\r\n'
                       'Server: {server}\r\n'
                       'Date: {date}\r\n'
                       'Connection: Close\r\n'
                       'Content-Length: {content_length}\r\n'
                       'Content-Type: {content_type}\r\n\r\n'
                   ).format(
                version=HTTP_VERSION,
                status=RESPONSE_STATUS.get(self.code),
                server=SERVER_NAME,
                date=datetime.utcnow().strftime(HTTP_DATE),
                content_length=self.content_length,
                content_type=self.content_type
            ).encode() + self.content

        return (
            'HTTP/{version} {status}\r\n'
            'Server: {server}\r\n'
            'Date: {date}\r\n'
            'Connection: Close\r\n'
            'Content-Length: 0\r\n\r\n'
        ).format(
            version=HTTP_VERSION,
            status=RESPONSE_STATUS.get(self.code),
            server=SERVER_NAME,
            date=datetime.utcnow().strftime(HTTP_DATE),
        ).encode()

from urllib.parse import unquote, urlparse


class Request:
    def __init__(self, request):
        self.request = request.decode('utf-8')
        print("REQUEST", self.request)
        if len(self.request.split(' ')) < 3:
            self.allowed = True
        else:
            self.allowed = False
            request = request.decode('utf-8').split('\r\n\r\n')[0].split('\r\n')
            self.headers = {tmp.split(': ')[0]: tmp.split(': ')[1] for tmp in request[1:]}
            self.method, uri, self.version_protocol = request[0].split(' ')
            self.host = self.headers.get('Host', '')
            self.url, self.path = urlparse('//' + self.host + uri).geturl(), \
                                  unquote(urlparse('//' + self.host + uri).path)
            self.file_type = self.path.split('.')[-1]

    def get_allowed(self):
        return self.allowed

    def get_headers(self):
        return self.headers

    def get_method(self):
        return self.method

    def get_host(self):
        return self.host

    def get_url(self):
        return self.url

    def get_version_protocol(self):
        return self.version_protocol

    def get_path(self):
        return self.path

    def get_file_type(self):
        return self.file_type
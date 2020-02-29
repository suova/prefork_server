def config():
    with open('/server/httpd.conf') as f:
        settings = {}
        lines = f.read().splitlines()

        for line in lines:
            key, value = line.split(" ")
            settings[key] = value
    return settings

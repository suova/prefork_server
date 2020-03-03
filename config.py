def config():
    with open('httpd.conf') as f:
        settings = {}
        lines = f.read().splitlines()
        for line in lines:
            key, value = line.split(" ")
            settings[key] = value
    return settings

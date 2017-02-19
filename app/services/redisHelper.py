import redis

class RedisHelper(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = redis.StrictRedis(self.host, self.port)

    def append_word(self, word):
        pass

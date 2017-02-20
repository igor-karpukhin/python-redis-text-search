import redis
from uuid import uuid4

class RedisHelper(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = redis.StrictRedis(self.host, self.port)

    def append_text(self, index, text):
        words = text.split(' ')
        self._set_text_index(index, text)
        for w in words:
            self._append_word(w, index)

    def _set_text_index(self, index, text):
        self.connection.set("text:{0}".format(index), text)

    def _append_word(self, word, text_index):
        self.connection.zincrby("word:{0}".format(word), text_index, 1)

    def get_texts_count(self):
        return len(self.connection.keys("text:*"))

    def get_document_by_index(self, index):
        return self.connection.get("text:{0}".format(index))

    def lookup_word(self, word):
        uid = uuid4().hex
        lookup_key = "search:{0}:{1}".format(word, uid)
        self.connection.zunionstore(lookup_key, ["word:{0}".format(word)])
        results = self.connection.zrevrange(lookup_key, 0, -1, False, int)
        self.connection.delete(lookup_key)
        return results


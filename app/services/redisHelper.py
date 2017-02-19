import redis

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
        print "WORD", word
        r = self.connection.zunionstore("search:results",
                                        ["word:{0}".format(word)])
        print "ZSTR", r
        results = self.connection.zrevrange("search:results",
                                            0, -1, True, int)
        print "RSLT", results
        return results

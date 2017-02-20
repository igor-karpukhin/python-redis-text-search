import redis
from uuid import uuid4

class RedisHelper(object):
    """Redis helper class"""

    def __init__(self, host, port):
        """Constructor

        :param host: Redis host
        :param port: Redis port
        """
        self.host = host
        self.port = port
        self.connection = redis.StrictRedis(self.host, self.port)

    def append_text(self, index, text):
        """Append new document by index

        :param index: Document index
        :param text: Document data
        """
        if self._is_index_exist(index):
            return "Index {0} already exists".format(index)

        words = text.split(' ')
        self._set_text_index(index, text)
        for w in words:
            self._append_word(w, index)
        return "Added text for index {0}".format(index)

    def remove_text(self, index):
        """Remove document by index

        :param index: Document index
        """
        text = self.connection.get("text:{0}".format(index))
        if not text:
            return "No text found for index {0}".format(index)

        words = text.split(' ')
        for w in words:
            self._remove_word(w, index)

        self.connection.delete("text:{0}".format(index))
        return "Deleted index: {0}".format(index)

    def _is_index_exist(self, index):
        """Validates if document with index exists

        :param index: Document index
        """
        return True if self.connection.get("text:{0}".format(index)) else False

    def _remove_word(self, word, text_index):
        """Removes one score for given world and document index

        :param word: Word to be removed
        :param text_index: Document index
        """
        self.connection.zincrby("word:{0}".format(word), text_index, -1)

    def _set_text_index(self, index, text):
        """Assings index for a given document

        :param index: Document index
        :param text: Document data
        """
        self.connection.set("text:{0}".format(index), text)

    def _append_word(self, word, text_index):
        """Assings score to given word and document index

        :param word: Word to be added
        :param text_index: Document index
        """
        self.connection.zincrby("word:{0}".format(word), text_index, 1)

    def get_texts_count(self):
        """Returns number of saved texts"""
        return len(self.connection.keys("text:*"))

    def get_document_by_index(self, index):
        """Returns document by its index

        :param index: Document index
        """
        return self.connection.get("text:{0}".format(index))

    def lookup_word(self, word):
        """Performs search over all saved documents for given word
        Returns empty list if no matches found, otherwise returns
        a list of document indexes where a particular word has been found

        :param word: Word to find
        """
        # Unique search value
        uid = uuid4().hex
        # Key to save results
        lookup_key = "search:{0}:{1}".format(word, uid)
        # Make UNION from sets
        self.connection.zunionstore(lookup_key, ["word:{0}".format(word)])
        # Make reversed range with scores for a saved union
        totals = self.connection.zrevrange(lookup_key, 0, -1, True, int)
        # Remove search
        self.connection.delete(lookup_key)
        # Return those entries whose score > 0
        results = filter(lambda x: x[1] > 0, totals)
        return map(lambda x: x[0], results)


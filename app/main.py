#!/usr/bin/python
from flask import Flask, request
import json
import optparse
from services.redisHelper import RedisHelper
import os


app = Flask(__name__)

global redis_host
global redis_port


@app.route("/documents", methods=["GET"])
def documents_get():
    rds = RedisHelper(redis_host, redis_port)
    return json.dumps({"documentsCount": rds.get_texts_count()})


@app.route("/document/<int:index>", methods=["POST"])
def documents_post(index):
    rds = RedisHelper(redis_host, redis_port)
    rds.append_text(index, request.data)
    return json.dumps({"documentIndex": index})


@app.route("/document/<int:index>", methods=["GET"])
def documents_get_by_index(index):
    rds = RedisHelper(redis_host, redis_port)
    return json.dumps({"documentData": rds.get_document_by_index(index)})


@app.route("/document/<int:index>", methods=["DELETE"])
def documents_delete(index):
    return json.dumps({"documentsDeleted": index})


@app.route("/document", methods=["GET"])
def document_search():
    q_word = request.args.get("q")
    if not q_word:
        return json.dumps({"error": "Request has no 'q' parameter"})

    rds = RedisHelper(redis_host, redis_port)
    return json.dumps({"documentsIndexes": rds.lookup_word(q_word)})


if __name__ == "__main__":
    global redis_host
    global redis_port

    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--addr", action="store", dest="addr",
                          default="0.0.0.0", help="IP address to listen")
    opt_parser.add_option("--port", action="store", dest="port",
                          default=os.environ["APPCONF_appPort"],
                          help="port to listen")
    opt_parser.add_option("--rhost", action="store", dest="rhost",
                          default=os.environ["APPCONF_redisHost"],
                          help="Redis host")
    opt_parser.add_option("--rport", action="store", dest="rport",
                          default=os.environ["APPCONF_redisPort"],
                          help="Redis port")
    args, vals = opt_parser.parse_args()

    redis_host = args.rhost
    redis_port = args.rport

    print "Using addr: {0}:{1}".format(args.addr, args.port)
    print "Redis connection: {0}:{1}".format(redis_host, redis_port)
    app.run(args.addr, args.port)


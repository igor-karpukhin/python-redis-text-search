#!/usr/bin/python
from flask import Flask
import json


app = Flask(__name__)


@app.route("/documents", methods=["GET"])
def documents_get():
    return json.dumps({"Document_GET": "get"})


@app.route("/documents/<int:index>", methods=["POST"])
def documents_post(index):
    return json.dumps({"Document_POST": index})


@app.route("/documents/<int:index>", methods=["GET"])
def documents_search(index):
    return json.dumps({"Document_SEARCH": index})


@app.route("/documents/<int:index>", methods=["DELETE"])
def documents_delete(index):
    return json.dumps({"Documents_DELETE": index})


if __name__ == "__main__":
    app.run()

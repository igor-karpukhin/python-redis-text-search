# Description
Service to store texts and search words in them using Redis as a storage.

# Installation
Hit **docker-compose up -d --build** to build container and launch the environment

# API
By default, service will run on port **9000**. Example: **http://127.0.0.1:9000/<api>**

* Show number of saved documents: **/documents**
  * Example: ```curl -v -X GET http://127.0.0.1:9000/documents```
* Index new document: **/document**
  * ``` curl -H "Content-Type: application/json" -X POST -d "the third document text" http://127.0.0.1:9000/document/3```
* Get document by ID: **/document/<id>**
  * ```curl -v -X GET http://127.0.0.1:9000/document/1```
* Search word over all saved documents: **/document?q=<word>**
  * ```curl -v -X GET http://127.0.0.1:8080/document?q=sample```


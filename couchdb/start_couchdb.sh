#!/bin/bash

# cf https://wiki.apache.org/couchdb/Installing_on_Ubuntu
/etc/init.d/couchdb start;
curl http://127.0.0.1:5984/;

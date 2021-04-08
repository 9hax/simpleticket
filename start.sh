#!/bin/bash
cd /opt/simpleticket/simpleticket #chdir to simpleticket
flask run --host=0.0.0.0 --port 80 #run simpleticket using flask dev server, this will be chnaged to apachewsgi in the future

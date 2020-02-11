
# Application Start
# https://docs.tsuru.io/stable/using/procfile.html
#
web: gunicorn -b 0.0.0.0:$PORT -t 60 -k gevent --workers 1 --threads 8 app:app

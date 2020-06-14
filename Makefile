

install:
	- virtualenv -p python3 ../flask-infravideos/build
	- ( \
       . build/bin/activate; \
        pip3 install -r requirements.txt; \
    )
run:
	- ( \
       . build/bin/activate; \
	   FLASK_APP=app.py flask run\
    )
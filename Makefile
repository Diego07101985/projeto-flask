install:
	- virtualenv -p python3 ../projeto-flask/build
	- ( \
       . build/bin/activate; \
        pip3 install -r requirements.txt; \
    )

run:
	- ( \
       . build/bin/activate; \
	   FLASK_APP=app.py  flask run\
    )

migrate:
	- ( \
       . build/bin/activate; \
	   FLASK_APP=app.py  flask db init;\
       FLASK_APP=app.py  flask db migrate;\
       FLASK_APP=app.py  flask db upgrade;\
    )
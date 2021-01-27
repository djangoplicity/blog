bash:
	docker exec -it djangoplicity-blog bash

test:
	docker exec -it djangoplicity-blog coverage run --source='.' manage.py test

coverage-html:
	docker exec -it djangoplicity-blog coverage html
	open ./htmlcov/index.html

test-python27:
	docker exec -it djangoplicity-blog tox -e py27-django111

clean:
	find . -name "*py*cache*" -type d -print0 | xargs -0 rm -fr
	rm -fr static

test:
	flake8 --verbose
	python manage.py check
	python manage.py test --noinput -- --verbose

libupdate:
	pip install -U -r ../requirements/development.txt

staticfiles:
	python manage.py collectstatic

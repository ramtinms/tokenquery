init:
	pip install -r requirements.txt

test:
	python -m unittest discover . "*_test.py" -v
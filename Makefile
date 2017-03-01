init:
	pip install -r requirements.txt

test:
	pip install -r requirements.txt
	python -m unittest discover . "*_test.py" -v
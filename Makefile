setup:
	@python -m pip install -r requirements_test.txt

test:
	@py.test

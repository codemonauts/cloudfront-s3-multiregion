format:
	black -l 120 -t py313 .

test:
	cp config.example.py config.py
	black -l 120 --check -t py313 .
	pylint lambda_function.py

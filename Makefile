.PHONY: clean virtualenv test docker dist dist-upload

clean:
	find . -name '*.py[co]' -delete
	rm -rf tmp

virtualenv:
	virtualenv --prompt '|> braavos <| ' env
	env/bin/pip install -r requirements-dev.txt
	# env/bin/python setup.py develop
	@echo
	@echo "VirtualENV Setup Complete. Now run: source env/bin/activate"
	@echo

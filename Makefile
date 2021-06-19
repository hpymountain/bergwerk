.PHONY: clean virtualenv test docker dist dist-upload

clean:
	find . -name '*.py[co]' -delete
	rm -rf tmp

virtualenv:
	virtualenv --prompt '|> susis env <| ' env
	env/bin/pip install -r requirements-dev.txt
	@echo
	@echo "VirtualENV Setup Complete. Now run: source env/bin/activate"
	@echo

# check that a log-level is set
# for testing purposes at least use info
ifdef debug
log-level = "$(debug)0"
else
log-level = "9999"
endif

test:
	rm -rf tmp/tests
	mkdir -p tmp/tests
	python -m pytest \
		-v \
		--basetemp=tmp/tests \
		--log-cli-level="$(log-level)" \
		-k "$(tests)" \
		tests/$(files)

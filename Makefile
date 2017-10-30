VIRTENV = penv
PYTHON = python3


penv:
	rm -rf $(VIRTENV)
	python3 -m venv $(VIRTENV)
	. $(VIRTENV)/bin/activate; pip install -I --upgrade pip
	. $(VIRTENV)/bin/activate; pip install -I -r req.txt

develop: $(VIRTENV)
	$(PYTHON) setup.py develop

dist: $(VIRTENV)
	$(PYTHON) setup.py sdist $(ARGS)

publish: $(VIRTENV)
	$(PYTHON) setup.py $(ARGS) sdist upload -r nexus

run: $(VIRTENV)
	export PYTHONPATH=.; . penv/bin/activate; ./bin/run.py $(ARGS)

clean:
	find . -name '*.pyc' | xargs rm -rf
	rm -rf $(VIRTENV) dist .cache $(PACKAGE).egg-info
	find . -name __pycache__ | xargs rm -rf

FORCE:

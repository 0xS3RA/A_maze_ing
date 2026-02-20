VENV = venv
PYTHON = python3
VENV_PYTHON = $(VENV)/bin/python
VENV_PIP = $(VENV)/bin/pip
NAME = ./mazegen/a_maze_ing.py
ARG = ./config.txt
REQUIEREMENTS = ./requirements.txt

.PHONY: install run debug clean lint

#make install
install:
	rm -rf $(VENV)
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install -r $(REQUIEREMENTS)	


#make run
run:
	$(VENV)/bin/python $(NAME) $(ARG)


#make debug
debug:
	$(VENV)/bin/python -m pdb $(NAME) $(ARG)

#make clean
clean:
	rm -rf   __pycache__ .mypy_cache *.pyc *.pyo *.swp

#make lint
lint:
	./venv/bin/python -m flake8 $(NAME)
	./venv/bin/python -m mypy $(NAME) \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

install:
	( \
       source venv/bin/activate; \
       pip install -r dev_requirements.txt; \
	   pip install -e .; \
    )

run_nb: install
	( \
       source venv/bin/activate; \
       jupyter lab; \
    )

add_kernel:
	( \
		source venv/bin/activate; \
		python -m ipykernel install --user --name=venv; \
	)
test:
	( \
		clear; \
		pytest -v -ra; \
	)
	
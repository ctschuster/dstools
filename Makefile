default help:
	@echo "usage: make (test|clean)"

install:
	@echo "feature not yet developed"

test:
	@tests/run-tests

clean:
	@echo "Cleaning up python cache directories"
	@/bin/find * -name __pycache__ | xargs /bin/rm -fr

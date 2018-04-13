default help:
	@echo "usage: make (test|test-verbose|clean)"

install:
	@echo "feature not yet developed"

test:
	@tests/run-tests -q

test-verbose:
	@tests/run-tests -v

clean:
	@echo "Cleaning up python cache directories"
	@/bin/find * -name __pycache__ | xargs /bin/rm -fr

prefixdir=$(HOME)


default help:
	@echo "usage: make (test|test-verbose|install|clean)"

install:
	@echo "installing dstools into '${prefixdir}':"
	mkdir -p ${prefixdir}/bin ${prefixdir}/lib/python
	install -m 0755 scripts/ds ${prefixdir}/bin
	install -m 0644 lib/python/*.py ${prefixdir}/lib/python

test:
	@tests/run-tests -q

test-verbose:
	@tests/run-tests -v

clean:
	@echo "Cleaning up python cache files/directories"
	@/bin/find * -name __pycache__ | xargs /bin/rm -fr
	@/bin/find * -name \*.py'[cdo]' | xargs /bin/rm -f

@PHONY: test testwip check nfsup dump

PROJECT = $(shell pwd)

test:
	python -m pytest -xs tests/

testwip:
	python -m pytest -vvxs -m wip tests/

check:
	twine check --strict dist/*

nfsup:
	docker run \
		-v /home/jileon/Dropbox/notes:/var/shares/notes \
		-v $(PROJECT)/exports:/etc/exports:ro \
		--cap-add SYS_ADMIN \
		-p 2049:2049   -p 2049:2049/udp   \
		-p 111:111     -p 111:111/udp     \
		-p 32765:32765 -p 32765:32765/udp \
		-p 32767:32767 -p 32767:32767/udp \
		erichough/nfs-server

dump:
	echo $(PROJECT)

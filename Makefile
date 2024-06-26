SHELL = /bin/bash
BINDIR ?= $(HOME)/bin
SOURCEDIR = $(PWD)
COMPLETIONSDIR = $(HOME)/etc

link:
	@while read -r f; do echo "${BINDIR}/$${f}"; ln -s -f ${SOURCEDIR}/$${f} ${BINDIR}/$${f}; done < <(find * -type f -maxdepth 0 -name "photo-*")
	@while read -r f; do echo "${COMPLETIONSDIR}/$${f}"; ln -s -f ${SOURCEDIR}/$${f} ${COMPLETIONSDIR}/$${f}; done < <(find bash_completion.d -type f -name "photo-*")


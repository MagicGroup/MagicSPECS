#!/bin/bash
git clone git://anongit.freedesktop.org/cairo-ocaml || exit 1
mv cairo-ocaml ocaml-cairo-git$1
tar --exclude-vcs -cJvf ocaml-cairo-git$1.tar.xz ocaml-cairo-git$1
rm ocaml-cairo-git$1 -rf

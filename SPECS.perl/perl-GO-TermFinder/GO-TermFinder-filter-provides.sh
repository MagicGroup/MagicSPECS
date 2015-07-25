#!/bin/sh

@@PERL_PROV@@ "$@" | sed -e '/^perl(Hang)$/d' \
    -e '/^perl(NullHang)$/d'

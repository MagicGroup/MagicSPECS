#! /bin/bash

# This is the mips64el override file for the core/drivers package split.  The
# module directories listed here and in the generic list in filter-modules.sh
# will be moved to the resulting kernel-modules package for this arch.
# Anything not listed in those files will be in the kernel-core package.
#
# Please review the default list in filter-modules.sh before making
# modifications to the overrides below.  If something should be removed across
# all arches, remove it in the default instead of per-arch.

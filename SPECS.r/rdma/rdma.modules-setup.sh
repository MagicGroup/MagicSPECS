#!/bin/bash

check() {
	[ -n "$hostonly" -a -d /sys/class/infiniband_verbs/uverbs0 ] && return 0 || return 255
	return 255
}

depends() {
	return 0
}

install() {
	inst /etc/rdma/rdma.conf
	inst /usr/libexec/rdma-init-kernel
	inst /usr/libexec/rdma-fixup-mtrr.awk
	inst_multiple lspci setpci awk
	inst_rules 98-rdma.rules 70-persistent-ipoib.rules
}

installkernel() {
	instmods =drivers/infiniband
}

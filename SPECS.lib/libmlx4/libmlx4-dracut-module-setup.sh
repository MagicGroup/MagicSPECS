#!/bin/bash

check() {
	[ -f /etc/rdma/mlx4.conf ] || return 1
	# any non-empty, non-commented lines?
	grep -q '^[^#].\+$' /etc/rdma/mlx4.conf || return 1

	return 0
}

depends() {
	return 0
}

install() {
	dracut_install /etc/rdma/mlx4.conf
	dracut_install /usr/libexec/setup-mlx4.sh
}


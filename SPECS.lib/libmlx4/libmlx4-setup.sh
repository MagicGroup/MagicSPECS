#!/bin/bash
dir="/sys/bus/pci/drivers/mlx4_core"
[ ! -d $dir ] && exit 1
pushd $dir
while read device port1 port2 ; do
	[ -d "$device" ] || continue
	[ -z "$port1" ] && continue
	[ -f "$device/mlx4_port2" -a -z "$port2" ] && continue
	[ -f "$device/port_trigger" ] && echo "all" > "$device/port_trigger"
	[ -f "$device/mlx4_port2" ] && echo "$port2" > "$device/mlx4_port2"
	[ -f "$device/mlx4_port1" ] && echo "$port1" > "$device/mlx4_port1"
done
popd

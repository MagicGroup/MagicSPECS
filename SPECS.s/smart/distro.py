if not sysconf.getReadOnly():
    if not sysconf.has("channels"):
        sysconf.set(("channels", "rpm-db"),
                    {"alias": "rpm-db",
                     "type": "rpm-sys",
                     "name": "RPM Database"})

    for kernelseries in ("kernel", "kernel-suspend2", "kernel-tuxonice"):
        for flavour in ("", "-smp", "-bigmem", "-hugemem", "-largesmp", "-PAE", "-xen", "-xen0", "-xenU", "-kdump"):
            pkgconf.setFlag("multi-version", "%s%s" % (kernelseries, flavour))
            pkgconf.setFlag("multi-version", "%s%s-unsupported" % (kernelseries, flavour))
            pkgconf.setFlag("multi-version", "%s%s-devel" % (kernelseries, flavour))
            for clustergfs in ("GFS", "cman", "dlm", "gnbd"):
                pkgconf.setFlag("multi-version", "%s-%s%s" % (clustergfs, kernelseries, flavour))
    pkgconf.setFlag("multi-version", "kernel-source")
    pkgconf.setFlag("multi-version", "kernel-sourcecode")

import os
import os.path

DISTRODIR = "/etc/smart/distro.d"

if os.path.isdir(DISTRODIR):
    for f in map(lambda x: os.path.join(DISTRODIR, x), os.listdir(DISTRODIR)):
        if f.endswith(".py") and os.path.isfile(f):
            execfile(f, {"ctrl": ctrl, "iface": iface, "sysconf": sysconf,
                         "pkgconf": pkgconf, "hooks": hooks})

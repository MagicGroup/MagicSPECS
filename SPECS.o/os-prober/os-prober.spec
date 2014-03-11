Name:           os-prober
Version:        1.48
Release:        4%{?dist}
Summary:        Probes disks on the system for installed operating systems

Group:          System Environment/Base
License:        GPL+
URL:            http://kitenet.net/~joey/code/os-prober/
Source0:        http://ftp.de.debian.org/debian/pool/main/o/os-prober/%{name}_%{version}.tar.gz
# move newns binary outside of os-prober subdirectory, so that debuginfo
# can be automatically generated for it
Patch0:         os-prober-newnsdirfix.patch

Requires:       udev coreutils util-linux
Requires:       /bin/grep /bin/sed /sbin/modprobe

%description
This package detects other OSes available on a system and outputs the results
in a generic machine-readable format. Support for new OSes and Linux
distributions can be added easily. 

%prep
%setup -q -n %{name}
%patch0 -p1 -b .newnsdirfix
find -type f -exec sed -i -e 's|usr/lib|usr/libexec|g' {} \;

%build
make %{?_smp_mflags} CFLAGS="%{optflags}"

%install
install -m 0755 -d %{buildroot}%{_bindir}
install -m 0755 -d %{buildroot}%{_var}/lib/%{name}

install -m 0755 -p os-prober linux-boot-prober %{buildroot}%{_bindir}
install -m 0755 -Dp newns %{buildroot}%{_libexecdir}/newns
install -m 0644 -Dp common.sh %{buildroot}%{_datadir}/%{name}/common.sh

%ifarch m68k
ARCH=m68k
%endif
%ifarch ppc ppc64
ARCH=powerpc
%endif
%ifarch sparc sparc64
ARCH=sparc
%endif
%ifarch %{ix86} x86_64
ARCH=x86
%endif

for probes in os-probes os-probes/mounted os-probes/init \
              linux-boot-probes linux-boot-probes/mounted; do
        install -m 755 -d %{buildroot}%{_libexecdir}/$probes 
        cp -a $probes/common/* %{buildroot}%{_libexecdir}/$probes
        if [ -e "$probes/$ARCH" ]; then 
                cp -a $probes/$ARCH/* %{buildroot}%{_libexecdir}/$probes 
        fi
done
if [ "$ARCH" = x86 ]; then
        install -m 755 -p os-probes/mounted/powerpc/20macosx \
            %{buildroot}%{_libexecdir}/os-probes/mounted
fi

%files
%doc README TODO debian/copyright debian/changelog
%{_bindir}/*
%{_libexecdir}/*
%{_datadir}/%{name}
%{_var}/lib/%{name}

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.48-4
- 为 Magic 3.0 重建

* Sat Jan 21 2012 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.48-3
- Remove dmraid and lvm2 dependency. bug #770393

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 25 2011 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.48-1
- Updated to 1.48 release

* Thu May 19 2011 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.47-1
- Updated to the new upstream version 1.47

* Wed May 04 2011 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.46-2
- Removed obsolete parts (build tag, defattr, etc)
- Added a patch to move newns outside of os-prober subdirectory
- Added required utilities as package requires

* Sat Apr 30 2011 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.46-1
- Updated to 1.46 release

* Tue Feb 22 2011 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.42-2
- Remove executable permission from common.sh

* Thu Feb 17 2011 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.42-1
- Initial version

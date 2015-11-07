%global gittagdate 20140304
%global gittag qemu-slof-%{gittagdate}

Name:           SLOF
Version:        0.1.git%{gittagdate}
Release:        4%{?dist}
Summary:        Slimline Open Firmware

License:        BSD
URL:            http://www.openfirmware.info/SLOF
BuildArch:      noarch

# There are no upstream tarballs.  To prepare a tarball, do:
#
# git clone git://github.com/aik/SLOF.git
# cd SLOF
# git archive -o ../SLOF-%{gittagdate}.tar.gz \
#     --prefix=SLOF-%{gittagdate}/ %{gittag}
Source0:        SLOF-%{gittagdate}.tar.gz

BuildRequires:  gcc-powerpc64-linux-gnu
BuildRequires:  perl(Data::Dumper)


%description
Slimline Open Firmware (SLOF) is initialization and boot source code
based on the IEEE-1275 (Open Firmware) standard, developed by
engineers of the IBM Corporation.

The SLOF source code provides illustrates what's needed to initialize
and boot Linux or a hypervisor on the industry Open Firmware boot
standard.

Note that you normally wouldn't need to install this package
separately.  It is a dependency of qemu-system-ppc64.


%prep
%setup -q -n SLOF-%{gittagdate}


%build
export CROSS="powerpc64-linux-gnu-"
make qemu %{?_smp_mflags} V=2


%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/qemu
cp -a boot_rom.bin $RPM_BUILD_ROOT%{_datadir}/qemu/slof.bin


%files
%doc FlashingSLOF.pdf
%doc LICENSE
%doc README
%dir %{_datadir}/qemu
%{_datadir}/qemu/slof.bin


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.1.git20140304-4
- 为 Magic 3.0 重建

* Sun Jun 22 2014 Liu Di <liudidi@gmail.com> - 0.1.git20140304-3
- 为 Magic 3.0 重建

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.git20140304-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Mar 16 2014 Cole Robinson <crobinso@redhat.com> - 0.1.git20140304-1
- Update to qemu 2.0 version of SLOF

* Tue Nov 19 2013 Cole Robinson <crobinso@redhat.com> - 0.1.git20130827-1
- Update to version intended for qemu 1.7

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.git20130430-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Cole Robinson <crobinso@redhat.com> - 0.1.git20130430-1
- Update to version shipped with qemu 1.5

* Tue Feb 19 2013 Cole Robinson <crobinso@redhat.com> 0.1.git20121018-1
- Update to version shipped with qemu 1.4

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.git20120731-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 16 2012 Paolo Bonzini <pbonzini@redhat.com> - 0.1.git20120731-1
- Move date from release to version.

* Fri Sep 14 2012 Paolo Bonzini <pbonzini@redhat.com> - 0-0.1.git20120731
- SLOF packages is very out of date with respect to what qemu expects (bug #855246)
- SLOF package builds wrong version of SLOF (bug #855236)
- build verbosely

* Tue Jul 31 2012 Richard W.M. Jones <rjones@redhat.com> - 0-0.1.git20120217
- Initial release in Fedora.

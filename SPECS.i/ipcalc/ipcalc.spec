Name: ipcalc
Version: 0.1.2
Release: 3%{?dist}
Summary: IP network address calculator

# This is an updated version of ipcalc originally found
# in Fedora's initscripts at:
# https://fedorahosted.org/releases/i/n/initscripts/

License: GPLv2+
URL: https://github.com/nmav/ipcalc
Source0: https://github.com/nmav/ipcalc/archive/%{version}.tar.gz

BuildRequires: GeoIP-devel
BuildRequires: popt-devel
# Explicitly conflict with older initscript packages that ship ipcalc
Conflicts: initscripts < 9.63
# Obsolete ipcalculator
Obsoletes: ipcalculator < 0.41-20

%description
ipcalc provides a simple way to calculate IP information for a host.
The various options specify what information ipcalc should display
on standard out. Multiple options may be specified.  An IP address to
operate on must always be specified.  Most operations also require a
netmask or a CIDR prefix as well.

%prep
%setup -q

%build
CFLAGS="${CFLAGS:-%optflags}" LIBPATH=%{_libdir} make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 ipcalc %{buildroot}%{_bindir}/
mkdir -p -m 755 %{buildroot}%{_mandir}/man1
install -p -m 644 ipcalc.1 %{buildroot}%{_mandir}/man1

%check
make check

%files

%{_bindir}/ipcalc
%license COPYING
%doc README.md
%{_mandir}/man1/ipcalc.1*

%changelog
* Mon Sep 21 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.1.2-3
- This package obsoletes ipcalculator

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun  9 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.1.2-1
- New upstream release

* Tue May 19 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.1.1-1
- Compatibility fixes (allow a mask of 0)

* Mon May 18 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.1.0-1
- First independent release outside initscripts

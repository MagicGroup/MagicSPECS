Name:           babeltrace
Version:	1.3.0
Release:	2%{?dist}
Summary:        Trace Viewer and Converter, mainly for the Common Trace Format
License:        MIT and GPLv2
URL:            http://www.efficios.com/babeltrace
Source0:        http://www.efficios.com/files/%{name}/%{name}-%{version}.tar.bz2
Group:          Development/Tools

BuildRequires:  bison >= 2.4
BuildRequires:  flex >= 2.5.35
BuildRequires:  glib2-devel >= 2.22.0
BuildRequires:  libuuid-devel
BuildRequires:  libtool >= 2.2, autoconf, automake
BuildRequires:  popt-devel >= 1.13
BuildRequires:  python3-devel
BuildRequires:  swig >= 2.0
# For check
BuildRequires:  perl-Test-Harness
Requires:       lib%{name}%{?_isa} = %{version}-%{release}

%description
This project provides trace read and write libraries, as well as a trace
converter. A plugin can be created for any trace format to allow its conversion
to/from another trace format.

The main format expected to be converted to/from is the Common Trace
Format (CTF). See http://www.efficios.com/ctf.


%package -n lib%{name}
Summary:        Common Trace Format Babel Tower
Group:          Development/Libraries

%description -n lib%{name}
This project provides trace read and write libraries, as well as a trace
converter. A plugin can be created for any trace format to allow its conversion
to/from another trace format.


%package -n lib%{name}-devel
Summary:        Common Trace Format Babel Tower
Group:          Development/Libraries
Requires:       lib%{name}%{?_isa} = %{version}-%{release} glib2-devel

%description -n lib%{name}-devel
This project provides trace read and write libraries, as well as a trace
converter. A plugin can be created for any trace format to allow its conversion
to/from another trace format.


%package -n python3-%{name}
Summary:        Common Trace Format Babel Tower
Group:          Development/Libraries
Requires:       lib%{name}%{?_isa} = %{version}-%{release}

%description -n python3-%{name}
This project provides trace read and write libraries, as well as a trace
converter. A plugin can be created for any trace format to allow its conversion
to/from another trace format.


%prep
%setup -q

%build
#Re-run libtoolize and autoreconf to remove rpath
libtoolize --force --copy
autoreconf -v --install --force
export PYTHON=%{__python3}
%configure --disable-static --enable-python-bindings

make %{?_smp_mflags} V=1

%check
make check

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete
# Clean installed doc
rm -f %{buildroot}/%{_pkgdocdir}/API.txt
rm -f %{buildroot}/%{_pkgdocdir}/LICENSE
rm -f %{buildroot}/%{_pkgdocdir}/gpl-2.0.txt
rm -f %{buildroot}/%{_pkgdocdir}/mit-license.txt
rm -f %{buildroot}/%{_pkgdocdir}/std-ext-lib.txt

%post  -n lib%{name} -p /sbin/ldconfig
%postun -n lib%{name} -p /sbin/ldconfig

%files
%doc ChangeLog
%doc doc/lttng-live.txt
%{_docdir}/babeltrace/API.txt
%{_docdir}/babeltrace/LICENSE
%{_docdir}/babeltrace/gpl-2.0.txt
%{_docdir}/babeltrace/mit-license.txt
%{_docdir}/babeltrace/std-ext-lib.txt
%{_bindir}/%{name}*
%{_mandir}/man1/*.1*

%files -n lib%{name}
%doc doc/API.txt
%doc std-ext-lib.txt
%{!?_licensedir:%global license %%doc}
%license LICENSE gpl-2.0.txt mit-license.txt
%{_libdir}/*.so.*

%files -n lib%{name}-devel
%{_prefix}/include/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/babeltrace.pc
%{_libdir}/pkgconfig/babeltrace-ctf.pc

%files -n python3-%{name}
%{python3_sitelib}/babeltrace.py
%{python3_sitelib}/__pycache__/*
%{python3_sitearch}/


%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.3.0-2
- 更新到 1.3.0

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 1.2.4-3
- 为 Magic 3.0 重建

* Tue Jul 28 2015 Michael Jeanson <mjeanson@gmail.com> - 1.2.4-2
- Added python3 bindings module

* Sun Jul 19 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.4.1
- Update to 1.2.4

* Sun Jul 19 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.1-5
- Fix FTBFS, use %%license

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 27 2014 Yannick Brosseau <yannick.brosseau@gmail.com> - 1.2.1-1
- New upstream release

* Sat Mar 01 2014 Suchakra Sharma <suchakra@fedoraproject.org> - 1.2.0-1
- New upstream release
- Popt patch for babeltrace.pc.in removed. Its fixed in Fedora now
- Add new file (babeltrace-ctf.pc)

* Mon Aug 05 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 1.1.1-3
- Remove reference to versionned docdir (#992011)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 1.1.1-1
- New upstream bugfix release

* Tue May 28 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 1.1.0-1
- New upstream release
- Patch babeltrace.pc to not depends on popt.pc, as it does not exist in Fedora

* Tue Feb 26 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 1.0.3-1
- New upstream release
- Add pkg-config file to devel package (#913895)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 1.0.2-1
- New upstream release

* Tue Jan 15 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 1.0.0-3
- Change documentation directory to proper versionned one. 

* Mon Jan 14 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 1.0.0-2
- Use autoreconf rpath fix because the sed one was breaking the make check
- Use correct tar file version
- Package documentations in the right packages

* Mon Oct 29 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 1.0.0-1
- New upstream release

* Tue Oct 02 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 1.0.0-0.1.rc5
- New upstream release candidate
* Thu Jul 05 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 1.0.0-0.1.rc4
- New package, inspired by the one from OpenSuse 


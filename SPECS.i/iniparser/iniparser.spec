Name:		iniparser
Version:	3.1
Release:	1%{?dist}
Summary:	C library for parsing "INI-style" files

Group:		System Environment/Libraries
License:	MIT
URL:		http://ndevilla.free.fr/%{name}/
Source0:	http://ndevilla.free.fr/%{name}/%{name}-%{version}.tar.gz

%description
iniParser is an ANSI C library to parse "INI-style" files, often used to
hold application configuration information.

%package devel
Summary:	Header files, libraries and development documentation for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q -n %{name}

%build
# remove library rpath from Makefile
sed -i 's|-Wl,-rpath -Wl,/usr/lib||g' Makefile
sed -i 's|-Wl,-rpath,/usr/lib||g' Makefile
# set the CFLAGS to Fedora standard
sed -i 's|^CFLAGS|CFLAGS = %{optflags} -fPIC\nNOCFLAGS|' Makefile
make %{?_smp_mflags} libiniparser.so

%install
# iniParser doesn't have a 'make install' of its own :(
install -d %{buildroot}%{_includedir} %{buildroot}%{_libdir}
install -m 644 -t %{buildroot}%{_includedir}/ src/dictionary.h src/iniparser.h
install -m 755 -t %{buildroot}%{_libdir}/ libiniparser.so.0
ln -s libiniparser.so.0 %{buildroot}%{_libdir}/libiniparser.so

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README LICENSE
%{_libdir}/libiniparser.so.0

%files devel
%{_libdir}/libiniparser.so
%{_includedir}/*.h

%changelog
* Fri Aug 10 2012 Jaromir Capik <jcapik@redhat.com> - 3.1-1
- Update to 3.1
- Minor spec file changes according to the latest guidelines

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Simo Sorce <ssorce@redhat.com> - 3.0-1
- Final 3.0 release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.4.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.3.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.2.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jan 26 2009 Alex Hudson <fedora@alexhudson.com> - 3.0-0.1.b
- change version number to reflect "pre-release" status

* Mon Jan 19 2009 Alex Hudson <fedora@alexhudson.com> - 3.0b-3
- ensure LICENSE file is installed

* Wed Jan 14 2009 Alex Hudson <fedora@alexhudson.com> - 3.0b-2
- respond to review: added -fPIC to cflags, used 'install'

* Tue Jan 13 2009 Alex Hudson <fedora@alexhudson.com> - 3.0b-1
- Initial packaging attempt

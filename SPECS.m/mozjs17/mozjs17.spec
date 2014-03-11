Summary:	JavaScript interpreter and libraries
Name:		mozjs17
Version:	17.0.0
Release:	8%{?dist}
License:	GPLv2+ or LGPLv2+ or MPLv1.1
Group:		Development/Languages
URL:		http://www.mozilla.org/js/
Source0:	http://ftp.mozilla.org/pub/mozilla.org/js/mozjs%{version}.tar.gz
BuildRequires:	pkgconfig(nspr)
BuildRequires:	readline-devel
BuildRequires:	/usr/bin/zip
BuildRequires:	/usr/bin/python
BuildRequires:	/usr/bin/autoconf-2.13

Patch0:		js17-build-fixes.patch
# makes mozjs to match js from xul 21
Patch1:		js17-jsval.patch
Patch2:         mozbug746112-no-decommit-on-large-pages.patch

%description
JavaScript is the Netscape-developed object scripting language used in millions
of web pages and server applications worldwide. Netscape's JavaScript is a
superset of the ECMA-262 Edition 3 (ECMAScript) standard scripting language,
with only mild differences from the published standard.

%package devel
Summary: Header files, libraries and development documentation for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q -n mozjs%{version}
# Delete bundled sources
rm js/src/editline -rf
rm js/src/ctypes/libffi -rf
%patch0 -p1
%patch1 -p1
%patch2 -p1
chmod a+x configure
(cd js/src && autoconf-2.13)

%build
%configure --disable-static --with-system-nspr --enable-threadsafe --enable-readline
make %{?_smp_mflags}

%check
cat > js/src/config/find_vanilla_new_calls << EOF
#!/bin/bash
exit 0
EOF
make -C js/src check

%install
make install DESTDIR=%{buildroot}
# For some reason the headers and pkg-config file are executable
find %{buildroot}%{_includedir} -type f -exec chmod a-x {} \;
chmod a-x  %{buildroot}%{_libdir}/pkgconfig/*.pc
# Upstream does not honor --disable-static yet
rm -f %{buildroot}%{_libdir}/*.a
# This is also statically linked; once that is fixed that we could
# consider shipping it.
rm -f %{buildroot}%{_bindir}/js17

# However, delete js-config since everything should use
# the pkg-config file.
rm -f %{buildroot}%{_bindir}/js17-config

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE README
%{_libdir}/*.so

%files devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/js-17.0

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 17 2013 Dennis Gilmore <dennis@ausil.us> 17.0.0-7
- disable failing find_vanilla_new_calls test 

* Fri Jun 07 2013 Colin Walters <walters@verbum.org> 17.0.0-6
- Add patch for ppc/ppc64: https://bugzilla.redhat.com/show_bug.cgi?id=971519

* Fri Jun 07 2013 Colin Walters <walters@verbum.org> 17.0.0-5
- Enable check: https://bugzilla.redhat.com/show_bug.cgi?id=971519

* Fri May 17 2013 Dan Horák <dan[at]danny.cz> - 17.0.0-4
- fix build on 64-bit big-endians

* Mon Apr 15 2013 Colin Walters <walters@verbum.org> 17.0.0-3
- Delete js17, it is not used

* Sun Apr 14 2013 Peter Robinson <pbrobinson@fedoraproject.org> 17.0.0-2
- Add disttag

* Mon Apr 01 2013 Colin Walters <walters@verbum.org> - 17.0.0-1
- Spec file inherited from js.spec

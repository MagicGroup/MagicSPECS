Summary: A wrapper library for PKCS#11
Name: pakchois
Version: 0.4
Release: 6%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
URL: http://www.manyfish.co.uk/pakchois/
Source0: http://www.manyfish.co.uk/pakchois/pakchois-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext

%description
pakchois is just another PKCS#11 wrapper library. pakchois aims to
provide a thin wrapper over the PKCS#11 interface; offering a
modern object-oriented C interface which does not hide any of the
underlying interface, and avoids dependencies on any cryptography
toolkit.

%package devel
Summary: Development library and C header files for the pakchois library
Group: Development/Libraries
Requires: pkgconfig, pakchois = %{version}-%{release}

%description devel
The development library for the pakchois PKCS#11 wrapper library.

%prep
%setup -q

%build
# The module path used here will pick up opensc, coolkey, and
# gnome-keyring, if they are also installed.  (the path is not
# checked at build time, so those packages do not need to be BRed)
%define pkcs11_path %{_libdir}/pkcs11:%{_libdir}/gnome-keyring:%{_libdir}
%configure --disable-static \
           --enable-module-path=%{pkcs11_path}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS NEWS README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so

%changelog
* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 13 2008 Joe Orton <jorton@redhat.com> 0.4-1
- initial packaging.

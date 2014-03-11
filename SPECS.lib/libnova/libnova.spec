%define sover 14
Name:		libnova
Version:	0.14.0
Release:	2%{?dist}
Summary:	Libnova is a general purpose astronomy & astrodynamics library
Group:		Development/Libraries
License:	LGPLv2+
URL:		http://sourceforge.net/projects/libnova/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Libnova is a general purpose, double precision, celestial mechanics, 
astrometry and astrodynamics library

%package devel
Summary:	Development files for libnova
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Contains library and header files for libnova

%prep
%setup -q


%build
%configure --disable-static
make CFLAGS="$RPM_OPT_FLAGS"  %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc ChangeLog README AUTHORS NEWS COPYING
%{_libdir}/libnova-0.%{sover}.so.0.0.0
%{_libdir}/libnova-0.%{sover}.so.0
%{_bindir}/libnovaconfig

%files devel
%doc COPYING examples/*.c
%{_includedir}/libnova
%{_libdir}/libnova.so


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.14.0-2
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 7 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 0.13.0-2
- Account for bump in soname

* Thu Jan 7 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 0.13.0-1
- New upstream

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.12.1-3
- Autorebuild for GCC 4.3

* Sat Jan 12 2007 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 0.12.1-2
- Made changes to the Groups

* Mon Jan 07 2007 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 0.12.1-1
- Made small changes to make it more complaint with fedora packaging standards

* Thu Jan 04 2007 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 0.12.1-0
- Initial version.


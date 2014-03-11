Summary:	Library for easy parsing of XMP metadata
Name:		exempi
Version:	2.2.0
Release:	2%{?dist}
License:	BSD
Group:		System Environment/Libraries
URL:		http://libopenraw.freedesktop.org/wiki/Exempi
Source0:	http://libopenraw.freedesktop.org/download/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	boost-devel expat-devel zlib-devel pkgconfig

%description
Exempi provides a library for easy parsing of XMP metadata. It is a port of 
Adobe XMP SDK to work on UNIX and to be build with GNU automake.
It includes XMPCore and XMPFiles.

%package devel
Summary:	Headers for developing programs that will use %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
This package contains the libraries and header files needed for
developing with exempi

%prep
%setup -q

%build
%configure LDFLAGS="-L%{_libdir}" CPPFLAGS="-I%{_includedir}"
# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%check
make check

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

rm -rf %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_libdir}/*.a

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog COPYING README
%{_bindir}/exempi
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, -)
%{_includedir}/exempi-2.0/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 2.2.0-2
- 为 Magic 3.0 重建

* Wed Feb 22 2012 Deji Akingunola <dakingun@gmail.com> - 2.2.0-1
- Update to version 2.2.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon May  3 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.1.1-1
- Update to 2.1.1
- Add testsuite execution
- Removed build patch for gcc-4.4 (fixed in upstream)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 04 2009 Deji Akingunola <dakingun@gmail.com> - 2.1.0-2
- Add patch to build with gcc-4.4

* Tue Jan 06 2009 Deji Akingunola <dakingun@gmail.com> - 2.1.0-1
- Update to 2.1.0
    
* Sat May 17 2008 Deji Akingunola <dakingun@gmail.com> - 2.0.1-1
- Update to 2.0.1

* Wed Apr 02 2008 Deji Akingunola <dakingun@gmail.com> - 2.0.0-1
- Update to 2.0.0

* Fri Feb 08 2008 Deji Akingunola <dakingun@gmail.com> - 1.99.9-1
- Update to 1.99.9

* Sun Jan 13 2008 Deji Akingunola <dakingun@gmail.com> - 1.99.7-1
- Update to 1.99.7

* Mon Dec 03 2007 Deji Akingunola <dakingun@gmail.com> - 1.99.5-1
- Update to 1.99.5

* Wed Sep 05 2007 Deji Akingunola <dakingun@gmail.com> - 1.99.4-2
- Rebuild for expat 2.0

* Wed Aug 22 2007 Deji Akingunola <dakingun@gmail.com> - 1.99.4-1
- Update tp 1.99.4

* Tue Jul 10 2007 Deji Akingunola <dakingun@gmail.com> - 1.99.3-1
- Initial packaging for Fedora

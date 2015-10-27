# The base of the version (just major and minor without point)
%global base_version 1.9

Name:           libcutl
Version:        %{base_version}.0
Release:        6%{?dist}
Summary:        C++ utility library from Code Synthesis

Group:          System Environment/Libraries
License:        MIT
URL:            http://www.codesynthesis.com/projects/libcutl/
Source0:        http://www.codesynthesis.com/download/libcutl/%{base_version}/%{name}-%{version}.tar.bz2
Patch0:         libcutl_no_boost_license.patch

# Set BuildRoot for compatibility with EPEL <= 5
# See: http://fedoraproject.org/wiki/EPEL:Packaging#BuildRoot_tag
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# If building on Fedora or RHEL 6/7
%if 0%{?rhel}%{?fedora} >= 6
# Use the system Boost instead of the internal one
BuildRequires: boost-devel
%else
# Otherwise, on RHEL 5 use the EPEL Boost 1.41 instead of the internal one
BuildRequires: boost141-devel
%endif
# Uses pkgconfig
BuildRequires: pkgconfig
BuildRequires: expat-devel


%description
libcutl is a C++ utility library. It contains a collection of generic and
fairly independent components.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0
rm -r cutl/details/boost cutl/details/expat


%build
# Use the system Boost and expat libraries
confopts="--disable-static --with-external-boost --with-external-expat"
# If building on RHEL 5
%if 0%{?rhel}%{?fedora} <= 5
# Use the EPEL Boost 1.41 instead of the standard system one
confopts="$confopts CPPFLAGS=-I%{_includedir}/boost141 LDFLAGS=-L%{_libdir}/boost141"
%endif
%configure $confopts
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc LICENSE
%{_libdir}/libcutl-%{base_version}.so
# Exclude the documentation that doesn't need to be packaged
%exclude %{_datadir}/doc/%{name}/INSTALL
%exclude %{_datadir}/doc/%{name}/LICENSE
%exclude %{_datadir}/doc/%{name}/NEWS
%exclude %{_datadir}/doc/%{name}/README
%exclude %{_datadir}/doc/%{name}/version

%files devel
%doc NEWS
%{_includedir}/cutl/
%{_libdir}/libcutl.so
%{_libdir}/pkgconfig/libcutl.pc


%changelog
* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 1.9.0-6
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 1.9.0-4
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Feb 16 2015 Dave Johansen <davejohansen@gmail.com> 1.9.0-2
- Rebuild for gcc 5.0 C++ ABI change

* Wed Feb 11 2015 Dave Johansen <davejohansen@gmail.com> 1.9.0-1
- Updated to 1.9.0

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 1.8.1-2
- Rebuild for boost 1.57.0

* Wed Sep 03 2014 Dave Johansen <davejohansen@gmail.com> 1.8.1-1
- Updated to 1.8.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 1.8.0-3
- Rebuild for boost 1.55.0

* Fri Mar 14 2014 Dave Johansen <davejohansen@gmail.com> 1.8.0-2
- Use system expat library

* Mon Nov 4 2013 Dave Johansen <davejohansen@gmail.com> 1.8.0-1
- Updated to 1.8.0

* Sat Jul 27 2013 Dave Johansen <davejohansen@gmail.com> 1.7.1-3
- Adding support for building on EL5

* Sat Jul 27 2013 pmachata@redhat.com - 1.7.1-2
- Rebuild for boost 1.54.0

* Tue Jul 23 2013 Dave Johansen <davejohansen@gmail.com> 1.7.1-1
- Initial build

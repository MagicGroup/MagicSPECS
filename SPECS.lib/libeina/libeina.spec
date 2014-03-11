Summary:	Data Type Library
Name:		libeina
Version:	1.7.9
Release:	1%{?dist}
License:	LGPLv2+
Group:		System Environment/Libraries
URL:		http://www.enlightenment.org/
Source:		http://download.enlightenment.org/releases/eina-%{version}.tar.bz2
BuildRequires:	check-devel
BuildRequires:  doxygen
BuildRequires:  pkgconfig
 
%description
Eina is a multi-platform library that provides optimized data types 
and useful tools for projects.

%package	devel
Summary:	Eina headers, documentation and test programs
Group:		System Environment/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description	devel
Headers, test programs and documentation for %{name}.

%prep
%setup -q -n eina-%{version}
# Avoid lib64 rpaths
%if "%{_libdir}" != "/usr/lib"
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
%endif

%build
%configure --disable-static
## Tested export for tests
## export LD_LIBRARY_PATH=$( pwd )/src/lib/.libs/libeina.so

make %{?_smp_mflags} V=1 
#Do we really need docs?
#make doc %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# remove unfinished manpages
#find doc/man/man3 -size -100c -delete

#for l in todo %{name}.dox
#do
# rm -f doc/man/man3/$l.3
#done 

#mkdir -p %{buildroot}%{_mandir}/man3
#install -Dpm0644 doc/man/man3/* %{buildroot}%{_mandir}/man3
# Fix generic manpage naming causing conflict
#mv %{buildroot}%{_mandir}/man3/authors.3 %{buildroot}%{_mandir}/man3/eina-authors.3
# remove libtool archive along with stripping
find %{buildroot}/ -type f  -iname '*.la' -exec rm {} \;
find %{buildroot}/ -type f  -iname '*.a' -exec rm {} \;

## Can be enabled when upstream fixed the tests
## needs --enable-tests with %%configure
##%%check
##make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
# excluding ChangeLog since it does not seem to be updated
%doc AUTHORS COPYING 
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
#%{_mandir}/man3/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%changelog
* Thu Nov 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.9-1
- Update to 1.7.9

* Sat Aug 17 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-1
- Update to 1.7.8
- Update configure flags
- Disable docs

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun  4 2013 Tom Callaway <spot@fedoraproject.org> - 1.7.7-1
- update to 1.7.7

* Fri Apr 19 2013 Tom Callaway <spot@fedoraproject.org> - 1.7.6-1
- update to 1.7.6

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 28 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 1.7.4-1
- update to 1.7.4

* Thu Dec 27 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 1.7.1-1
- update to 1.7.1
- silence rpmlint warnings

* Thu Aug  2 2012 Tom Callaway <spot@fedoraproject.org> - 1.2.1-1
- update to 1.2.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 25 2012 Tom Callaway <spot@fedoraproject.org> - 1.2.0-2
- fix additional manpage conflict due to generic naming

* Mon May  7 2012 Tom Callaway <spot@fedoraproject.org> - 1.2.0-1
- update to 1.2.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 14 2011 Tom Callaway <spot@fedoraproject.org> - 1.0.1-1
- update to 1.0.1

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Thomas Janssen <thomasj@fedoraproject.org> 1.0.0-1
- final 1.0.0 release

* Wed Dec 15 2010 Thomas Janssen <thomasj@fedoraproject.org> 1.0.0-0.1.beta3
- beta 3 release

* Tue Nov 16 2010 Thomas Janssen <thomasj@fedoraproject.org> 1.0.0-0.1.beta2
- beta 2 release

* Fri Nov 05 2010 Thomas Janssen <thomasj@fedoraproject.org> 1.0.0-0.1.beta1
- beta 1 release

* Fri Jul 02 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.9.9.49898-1
- libeina 0.9.9.49898 snapshot release

* Fri Jun 11 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.9.9.49539-1
- libeina 0.9.9.49539 snapshot release

* Tue Feb 23 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.9.9.063-6
- Disabled tests again until they are fixed

* Mon Feb 22 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.9.9.063-5
- Added missing BR doxygen check

* Sun Feb 21 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.9.9.063-4
- added Requires for -devel
- corrected license
- enabled tests

* Fri Feb 19 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.9.9.063-3
- name changed from eina-0 to libeina
- spec fixes

* Mon Feb 15 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.9.9.063-2
- added missing man pages

* Mon Feb 15 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.9.9.063-1
- Initial Fedora release


Name:           Judy
Version:        1.0.5
Release:        3%{?dist}
Summary:        General purpose dynamic array

Group:          System Environment/Libraries
# The source code itself says:
# "GNU Lesser General Public License as published by the
#  Free Software Foundation; either version 2 of the License,
#  or (at your option) any later version."
# This will probably change to LGPLv2 in a future upstream release,
# but until then, LGPLv2+ is the proper license.  Confirmed
# with upstream on 2008/11/28.
License:        LGPLv2+
URL:            http://sourceforge.net/projects/judy/
Source0:        http://downloads.sourceforge.net/judy/Judy-%{version}.tar.gz
Source1:	README.Fedora
# Make tests use shared instead of static libJudy.
Patch0:		Judy-1.0.4-test-shared.patch
# The J1* man pages were incorrectly being symlinked to Judy, rather
# than Judy1.  This patch corrects that.  Submitted upstream 2008/11/27.
Patch1:		Judy-1.0.4-fix-Judy1-mans.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:
#Requires:       

%description
Judy is a C library that provides a state-of-the-art core technology
that implements a sparse dynamic array. Judy arrays are declared
simply with a null pointer. A Judy array consumes memory only when it
is populated, yet can grow to take advantage of all available memory
if desired. Judy's key benefits are scalability, high performance, and
memory efficiency. A Judy array is extensible and can scale up to a
very large number of elements, bounded only by machine memory. Since
Judy is designed as an unbounded array, the size of a Judy array is
not pre-allocated but grows and shrinks dynamically with the array
population.


%package devel
Summary:	Development libraries and headers for Judy
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the development libraries and header files
for developing applications that use the Judy library.


%prep
%setup -q -n judy-%{version}
%patch0 -p1 -b .test-shared
%patch1 -p1 -b .fix-Judy1-mans
cp -p %{SOURCE1} .


%build
%configure --disable-static
make 
#%{?_smp_mflags}
# fails to compile properly with parallel make:
# http://sourceforge.net/tracker/index.php?func=detail&aid=2129019&group_id=55753&atid=478138


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# get rid of static libs and libtool archives
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.{a,la}
# clean out zero length and generated files from doc tree
rm -rf doc/man
rm -f doc/Makefile* doc/ext/README_deliver
[ -s doc/ext/COPYRIGHT ] || rm -f doc/ext/COPYRIGHT
[ -s doc/ext/LICENSE ] || rm -f doc/ext/LICENSE


%check

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README README.Fedora
%{_libdir}/*.so.*


%files devel
%defattr(-,root,root,-)
%doc doc
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/man3/*


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%changelog
* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 1.0.5-3
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.0.5-2
- 为 Magic 3.0 重建

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 13 2008 Charles R. Anderson <cra@wpi.edu> 1.0.4-4
- for Judy1 man page fix, patch Makefile.{am,in} instead of
  relying on autotools to regenerate the latter.
- Add README.Fedora with upstream's license explanation.

* Thu Nov 30 2008 Charles R. Anderson <cra@wpi.edu> 1.0.4-3
- fix Judy1 man page symlinks
- use valid tag License: LGPLv2+ confirmed with upstream
- use version macro in Source0
- remove Makefiles from installed doc tree

* Thu Nov 27 2008 Charles R. Anderson <cra@wpi.edu> 1.0.4-2
- patch tests to run with shared library
- run tests in check section

* Sun Oct 05 2008 Charles R. Anderson <cra@wpi.edu> 1.0.4-1
- Initial package for Fedora

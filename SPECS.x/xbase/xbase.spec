Name:		xbase
Summary: 	XBase compatible database library
Summary(zh_CN.UTF-8): XBase 兼容数据库库
Version: 	3.1.2
Release: 	11%{?dist}
License: 	LGPLv2+
Group: 		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:		http://linux.techass.com/projects/xdb/
Source0:	http://downloads.sourceforge.net/xdb/%{name}64-%{version}.tar.gz
Patch0:		xbase-3.1.2-fixconfig.patch
Patch1:		xbase-3.1.2-gcc44.patch
Patch2:		xbase-2.0.0-ppc.patch
Patch3:		xbase-3.1.2-xbnode.patch
Patch4:		xbase-3.1.2-lesserg.patch
Patch5:		xbase-3.1.2-gcc47.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	doxygen, libtool
Provides:	xbase64 = %{version}-%{release}

%description
XBase is an xbase (i.e. dBase, FoxPro, etc.) compatible C++ class library
originally by Gary Kunkel and others (see the AUTHORS file).

XBase is useful for accessing data in legacy dBase 3 and 4 database files as
well as a general light-weight database engine.  It includes support for
DBF (dBase version 3 and 4) data files, NDX and NTX indexes, and DBT
(dBase version 3 and 4).  It supports file and record locking under *nix
OS's.
%description -l zh_CN.UTF-8
XBase (如 dBase, FoxPro 等)  兼容数据库的 C++ 类库。

%package devel
Summary: XBase development libraries and headers
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Provides: xbase64-devel = %{version}-%{release}

%description devel
Headers and libraries for compiling programs that use the XBase library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package utils
Summary: XBase utilities / tools
Summary(zh_CN.UTF-8): %{name} 的工具
Group: Applications/Databases
Group(zh_CN.UTF-8): 应用程序/数据库
License: GPLv2+
Provides: xbase64-utils = %{version}-%{release}
Requires: %{name} = %{version}-%{release}

%description utils
This package contains various utilities for working with X-Base files:
checkndx (check an NDX file), copydbf (copy a DBF file structure), deletall
(mark all records for deletion), dumphdr (print an X-Base file header),
dumprecs (dump records for an X-Base file), packdbf (pack a database file),
reindex (rebuild an index), undelall (undeletes all deleted records in a file),
zap (remove all records from a DBF file).

%description utils -l zh_CN.UTF-8
%{name} 的工具。

%prep
%setup -q -n %{name}64-%{version}
%patch0 -p1
%patch1 -p1 -b .gcc44
%patch2 -p1
%patch3 -p1
%patch4 -p1 -b .lesserg
%patch5 -p1 -b .gcc47

%build
touch AUTHORS README NEWS
cp -p copying COPYING
autoreconf -i
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la

# Fix files for multilib
touch -r COPYING $RPM_BUILD_ROOT%{_bindir}/xbase-config
touch -r COPYING docs/html/*.html

pushd $RPM_BUILD_ROOT%{_libdir}
ln -s libxbase64.so.1.0.0 libxbase.so.1.0.0
ln -s libxbase64.so.1 libxbase.so.1
ln -s libxbase64.so libxbase.so
popd

pushd $RPM_BUILD_ROOT%{_includedir}
ln -s xbase64 xbase
popd

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%doc COPYING ChangeLog
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, 0755)
%doc docs/html
%{_includedir}/xbase*
%{_bindir}/xbase*-config
%{_libdir}/libxbase*.so

%files utils
%defattr(-, root, root, 0755)
%{_bindir}/checkndx
%{_bindir}/copydbf
%{_bindir}/dbfxtrct
%{_bindir}/deletall
%{_bindir}/dumphdr
%{_bindir}/dumprecs
%{_bindir}/packdbf
%{_bindir}/reindex
%{_bindir}/undelall
%{_bindir}/zap
%{_bindir}/dbfutil1

%changelog
* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.1.2-10
- Rebuilt for GCC 5 C++11 ABI change

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-4
- Rebuilt for c++ ABI breakage

* Thu Jan  5 2012 Tom Callaway <spot@fedoraproject.org> - 3.1.2-3
- Fix gcc 4.7.0 compile

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 19 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.1.2-1
- update to 3.1.2

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jun  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.0-13
- add ppc64 detection in configure (it's in the x86_64 patch)

* Thu Jun  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.0-12
- fix x86_64 detection in configure (FTBFS)

* Tue Mar 11 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.0.0-11
- Fix gcc4.3 patch to not polute global header namespace with
  "using namespace std;"

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.0-10
- Autorebuild for GCC 4.3

* Fri Jan 25 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.0.0-9
- Fix building with gcc 4.3 (also fixes building of xbase using packages)

* Tue Oct 30 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.0-8
- fix multilib conflicts

* Fri Aug 17 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.0.0-7
- Update License tag for new Licensing Guidelines compliance
- Add patch by Bill Nottingham to fix building on ppc64 (bz 239131)
- Don't build and install a static version of the lib
- Put the utilities/tools in a -utils sub package (to make clear they are under
  a different license)

* Mon Sep 11 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.0-6
- rebuild

* Sun Jun  4 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.0-5
- fix header file

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.0-4
- bump for FC-5

* Sun Jul 10 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.0-3
- fix xbase-config --ld (bugzilla 162845)

* Fri Jul  1 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.0-2
- add BuildRequires: doxygen
- remove latex docs (html is fine)

* Thu Jun 16 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.0-1
- initial package for Fedora Extras

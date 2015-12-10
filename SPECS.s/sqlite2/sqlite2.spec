%{!?tcl_version: %global tcl_version %((echo 0; echo 'puts $tcl_version' | tclsh) | tail -1)}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}

Name:           sqlite2
Version:        2.8.17
Release:        18%{?dist}

Summary:        Embeddable SQL engine in a C library
Summary(zh_CN.UTF-8): 嵌入式 SQL 引擎的 C 库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        Public Domain
URL:            http://www.sqlite.org/
Source0:        http://www.sqlite.org/sqlite-%{version}.tar.gz
Patch1:         sqlite-2.8.15.rpath.patch
Patch2:         sqlite-2.8.15-makefile.patch
Patch3:         sqlite-2.8.3.test.rh9.patch
Patch4:         sqlite-64bit-fixes.patch
Patch5:         sqlite-2.8.15-arch-double-differences.patch
Patch6:         sqlite-2.8.17-test.patch
Patch7:         sqlite-2.8.17-tcl.patch
Patch8:         sqlite-2.8.17-ppc64.patch
Patch9:         sqlite-2.8.17-format-security.patch
Patch10:	sqlite-2.8.17-tcl86.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  ncurses-devel, readline-devel, %{_includedir}/tcl.h
Obsoletes:      sqlite < 3, sqlite%{?_isa} < 3

%description
SQLite is a small, fast, embeddable SQL database engine that supports
most of SQL92, including transactions with atomic commit and rollback,
subqueries, compound queries, triggers, and views. A complete database
is stored in a single cross-platform disk file. The native C/C++ API
is simple and easy to use. Bindings for other languages are also
available.

%description -l zh_CN.UTF-8
嵌入式 SQL 引擎的 C 库。

%package        devel
Summary:        Development files for SQLite
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}, pkgconfig
Obsoletes:      sqlite-devel < 3, sqlite-devel%{?_isa} < 3

%description    devel
SQLite is a small, fast, embeddable SQL database engine that supports
most of SQL92, including transactions with atomic commit and rollback,
subqueries, compound queries, triggers, and views.
This package contains static library and header files for developing
applications using sqlite.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。
%package        tcl
Summary:        Tcl bindings for sqlite
Summary(zh_CN.UTF-8): %{name} 的 Tcl 绑定
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires:       tcl(abi) = %{tcl_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      sqlite-tcl < 3, sqlite-tcl%{?_isa} < 3

%description    tcl
SQLite is a small, fast, embeddable SQL database engine that supports
most of SQL92, including transactions with atomic commit and rollback,
subqueries, compound queries, triggers, and views.
This package contains tcl bindings for sqlite.

%description tcl -l zh_CN.UTF-8
%{name} 的 Tcl 绑定。

%prep
%setup -q -n sqlite-%{version}
%patch1 -p1 -b .rpath
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
sed -i.rpath 's!__VERSION__!%{version}!g' Makefile.in
# Patch additional /usr/lib locations where we don't have $(libdir)
# to substitute with.
sed -i.lib 's!@exec_prefix@/lib!%{_libdir}!g' Makefile.in

%build
CFLAGS="$RPM_OPT_FLAGS -DNDEBUG=1"
%configure --enable-utf8 --disable-static
make
make tclsqlite libtclsqlite.la doc

%check
#obs. make test doesn't like root
make test

%install
rm -rf $RPM_BUILD_ROOT
DIRECTORY=$RPM_BUILD_ROOT%{_libdir}/sqlite-%{version}
install -d $DIRECTORY
echo 'package ifneeded sqlite 2 [list load [file join $dir libtclsqlite.so]]' > $DIRECTORY/pkgIndex.tcl

%makeinstall
install -D -m 0644 sqlite.1 $RPM_BUILD_ROOT%{_mandir}/man1/sqlite.1
mkdir -p $RPM_BUILD_ROOT%{tcl_sitearch}
mv -f $DIRECTORY $RPM_BUILD_ROOT%{tcl_sitearch}/sqlite2

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
rm -f $RPM_BUILD_ROOT%{_bindir}/tclsqlite
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/sql*
%{_libdir}/libsql*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%doc README doc/*
%{_libdir}/libsql*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*

%files tcl
%defattr(-,root,root,-)
%doc doc/tclsqlite.html
%{tcl_sitearch}/sqlite2/

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 2.8.17-18
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.8.17-17
- 为 Magic 3.0 重建

* Tue Sep 29 2015 Liu Di <liudidi@gmail.com> - 2.8.17-16
- 为 Magic 3.0 重建

* Sat Sep 19 2015 Liu Di <liudidi@gmail.com> - 2.8.17-15
- 为 Magic 3.0 重建

* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 2.8.17-14
- 为 Magic 3.0 重建

* Sun Dec 08 2013 Robert Scheck <robert@fedoraproject.org> 2.8.17-13
- Solved build failures with "-Werror=format-security" (#1037335)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.17-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.17-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Sep 02 2012 Robert Scheck <robert@fedoraproject.org> - 2.8.17-10
- Use macros to ensure that the correct tcl version is always used

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 23 2012 Robert Scheck <robert@fedoraproject.org> - 2.8.17-8
- Added a patch to avoid segmentation fault of tests on ppc64

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 18 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 2.8.17-5
- Install tcl subpackage in correct place, thanks to hkoba for patch (#516411)
- Use new tclver define, depend on at least tcl 8.5

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 23 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 2.8.17-3
- Add patches to build with new TCL and fix tests (#491726)
  thanks to D. Marlin.
  
* Wed Oct 03 2007 Alex Lancaster <alexl@users.sourceforge.net> 2.8.17-2
- Rebuild for merged Fedora

* Sun Sep 10 2006 Mike McGrath <imlinux@gmail.com> 2.8.17-1
- New upstream source

* Tue Feb 28 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 2.8.16-3
- Rebuild for Fedora Extras 5

* Sat Nov 26 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 2.8.16-2
- Disable static libs

* Fri May 20 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 2.8.16-1
- Name change to sqlite2
- Dropped Epoch
- Added Obsoletes to all subpackages
- Minor cosmetic changes

* Wed Feb 16 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:2.8.16-1
- Update to 2.8.16 bug-fix release + update patches.

* Tue Feb 15 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.8.15-2
- add sqlite-64bit-fixes.patch and sqlite-2.8.15-arch-double-differences.patch
  fixes x86_64; Both were found in a mandrake srpm
- remove exclusive arch ix86; hopefully this fixes ppc also

* Sun Jan 23 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:2.8.15-1
- Add exclusive arch ix86 for now (make test segfaults on x86_64).
- Update makefile patch, $(exec_prefix)/lib -> $(libdir), and
  substitute additional /usr/lib locations in %%prep for multilib
  people to play with.

* Sun Sep 26 2004 Adrian Reber <adrian@lisas.de> - 0:2.8.15-0.fdr.1
- Update to 2.8.15
- Update patches

* Fri Jun 19 2004 Nils O. Selåsdal <NOS@Utel.no> - 0:2.8.14-0.fdr.1
- Update to 2.8.14
- Update patches
- --enable-releasemode
- small spec file tweaks

* Sat Dec 27 2003 Jean-Luc Fontaine <jfontain@free.fr> - 0:2.8.6-0.fdr.6
- in tcl rpm, removed tclsqlite, moved shared library in own sqlite
  sub-directory add added pkgIndex.tcl file to make package dynamically
  loadable in a Tcl interpreter
- in build requirements, work around tcl-devel and tk-devel packages non
  existence in RH 8.0 and 9
- in tcl rpm, added tcl package requirement
- in tcl rpm, post ldconfig is not necessary

* Wed Nov 12 2003 Nils O. Selåsdal <NOS@Utel.no> -  0:2.8.6-0.fdr.5
- BuildRequires tcl-devel
- small .spec tweaks

* Tue Oct 28 2003 Nils O. Selåsdal <NOS@Utel.no> - 0:2.8.6-0.fdr.4
- exclude libtclsqlite.a

* Mon Oct 27 2003 Nils O. Selåsdal <NOS@Utel.no> - 0:2.8.6-0.fdr.3
- Fix readme -> README

* Mon Oct 27 2003 Nils O. Selåsdal <NOS@Utel.no> - 0:2.8.6-0.fdr.2
- Better summary/description
- Add patch for not using rpath
- Add patch that builds tclsqlite (From Anvil's package)
- Add patch that fixes the tests (From Anvil's package)
- New tcl subpackage
- Also make the tests during build
- Build docs, and include them in -devel

* Fri Oct 10 2003 Nils O. Selåsdal <NOS@Utel.no> - 0:2.8.6-0.fdr.1
- Initial RPM release.

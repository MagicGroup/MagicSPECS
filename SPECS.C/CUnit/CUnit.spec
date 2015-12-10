Name:           CUnit
Version:        2.1.3
Release:        11%{?dist}
Summary:        Unit testing framework for C
Summary(zh_CN.UTF-8): C 语言的单元测试框架

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://cunit.sourceforge.net/
# TODO: 404 Not Found
Source0:        http://downloads.sourceforge.net/cunit/%{name}-2.1-3-src.tar.bz2

BuildRequires:  automake

%description 
CUnit is a lightweight system for writing, administering,
and running unit tests in C.  It provides C programmers a basic
testing functionality with a flexible variety of user interfaces.

%description -l zh_CN.UTF-8
这是一个轻量级的系统，可以使用 C 语言编写、管理和运行单元测试。

%package devel
Summary:        Header files and libraries for CUnit development
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel 
The %{name}-devel package contains the header files
and libraries for use with CUnit package.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-2.1-3
find -name *.c -exec chmod -x {} \;

%build
autoconf -f -i
%configure --enable-curses --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f `find %{buildroot} -name *.la`

# add some doc files into the buildroot manually (#1001276)
for f in AUTHORS ChangeLog COPYING NEWS README TODO ; do
    install -p -m0644 -D $f %{buildroot}%{_docdir}/%{name}/${f}
done

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_datadir}/%{name}/
%{_libdir}/libcunit.so.*
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/AUTHORS
%{_docdir}/%{name}/ChangeLog
%{_docdir}/%{name}/COPYING
%{_docdir}/%{name}/NEWS
%{_docdir}/%{name}/README
%{_docdir}/%{name}/TODO

%files devel
%{_docdir}/%{name}/headers/
%{_docdir}/%{name}/*.css
%{_docdir}/%{name}/*.html
%{_includedir}/%{name}/
%{_libdir}/libcunit.so
%{_libdir}/pkgconfig/cunit.pc
%{_mandir}/man3/CUnit.3*

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 2.1.3-11
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 2.1.3-10
- 为 Magic 3.0 重建

* Mon Jun 23 2014 Liu Di <liudidi@gmail.com> - 2.1.3-9
- 为 Magic 3.0 重建

* Sun Sep 29 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 2.1.3-8
- Add %%_isa to -devel base package dependency.
- Headers get installed by "make install", copying them from the HTML
  doc headers dir is not necessary.
- Configure build with --disable-static.
- Drop unneeded spec stuff (buildroot def, removal, clean, pkgconfig dep).
- Using %%defattr is not needed anymore.
- Deduplicate documentation files in unversioned docdir (#1001276).

* Tue Sep 10 2013 Shakthi Kannan <shakthimaan [AT] fedoraproject.org> - 2.1.3-7
- Fix build with unversioned docdir (#1001276)

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Shakthi Kannan <shakthimaan [AT] fedoraproject.org> - 2.1.3-5
- Use header files from doc folder as well
- Enable curses

* Sat Apr 20 2013 Shakthi Kannan <shakthimaan [AT] fedoraproject.org> - 2.1.3-4
- Use autoconf for ARM

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 2 2012 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 2.1.3-1
- Updated to 2.1.3 sources re-run with autoreconf.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 29 2011 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 2.1.2-6
- Changed Group to System Environment/Libraries.
- Remove executable permission from C files.
- Created two separate patches for Makefile and manpage fixes.
- Removed passing datarootdir from configure.

* Thu Jan 20 2011 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 2.1.2-5
- Renamed Source0 to use Fedora sourceforge.net naming guidelines.
- Removed exit call in library patch.
- Use A.B.C version number.

* Thu Jan 20 2011 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 2.1_2-4
- Updated to license LGPLv2+.
- Changed to use BuildRoot.
- Added comments for inclusion of patches.
- Removed inconsistent macro usage.
- Moved man page, HTML documentation to devel package.
- Added AUTHORS, COPYING, README, TODO to doc in base package.
- Used * in man, library inclusion.

* Sun Dec 26 2010 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 2.1_2-3
- Created patch to fix man page warnings and datarootdir settings.
- Added patch to remove exit calls in library.

* Wed Dec 15 2010 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 2.1_2-2
- Moved libcunit.so.* to main package.
- Added post, postun ldconfig.
- Added smp flags for make build.
- Changed datarootdir to datadir.

* Tue Dec 14 2010 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 2.1_2-1
- First CUnit package.


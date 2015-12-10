Name:           cln
Version:	1.3.4
Release:        3%{?dist}
Summary:        Class Library for Numbers
Summary(zh_CN.UTF-8): 数字类库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        GPLv2+
URL:            http://www.ginac.de/CLN/
Source0:        http://www.ginac.de/CLN/%{name}-%{version}.tar.bz2
Patch1:   cln-1.3.4-fix-mips64el.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
BuildRequires:  gmp-devel

%description
A collection of C++ math classes and functions, which are designed for
memory and speed efficiency, and enable type safety and algebraic
syntax.

%description -l zh_CN.UTF-8
一组为内存和速度效率优化的 C++ 数学类和函数，并且带有类型安全和线性语法。

%package devel
Summary:        Development files for programs using the CLN library
Summary(zh_CN.UTF-8): 使用 CLN 库开发程序的开发文件
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release} gmp-devel pkgconfig

%description devel
A collection of C++ math classes and functions, which are designed for
memory and speed efficiency, and enable type safety and algebraic
syntax.

This package is necessary if you wish to develop software based on
the CLN library.

%description devel -l zh_CN.UTF-8
一组为内存和速度效率优化的 C++ 数学类和函数，并且带有类型安全和线性语法。
本软件包包含了基于 CLN 库开发软件所需的文件。

%prep
%setup -q
%patch1 -p1

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%makeinstall
#mkdir -p %{buildroot}%{_docdir}/%{name}-devel-%{version}
#mv %{buildroot}%{_datadir}/dvi/cln.dvi %{buildroot}%{_datadir}/html %{buildroot}%{_docdir}/%{name}-devel-%{version}
rm -f %{buildroot}%{_infodir}/dir

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info --section="Math" %{_infodir}/cln.info.gz %{_infodir}/dir 2>/dev/null || :

%preun devel
if [ "$1" = 0 ]; then
  /sbin/install-info --delete %{_infodir}/cln.info.gz %{_infodir}/dir 2>/dev/null || :
fi

%files
%defattr(-,root,root)
%doc COPYING ChangeLog NEWS README TODO*
%{_libdir}/*.so.*
%{_bindir}/pi
%{_mandir}/man1/pi.1*

%files devel
%defattr(-,root,root)
#%{_docdir}/%{name}-devel-%{version}
%{_libdir}/*.so
%{_libdir}/pkgconfig/cln.pc
%{_includedir}/cln/
%{_infodir}/*.info*
%exclude %{_libdir}/*.la

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1.3.4-3
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.3.4-2
- 更新到 1.3.4

* Wed Mar 12 2014 Liu Di <liudidi@gmail.com> - 1.3.3-1
- 更新到 1.3.3

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.3.2-4
- 为 Magic 3.0 重建

* Sun Mar 25 2012 Liu Di <liudidi@gmail.com> - 1.3.2-3
- 为 Magic 3.0 重建

* Sun Jan 25 2009 Ni Hui <shuizhuyuanluo@126.com> - 1.2.2-0.1mgc
- rebuild for Magic Linux 2.1
- 戊子  十二月三十

* Fri Jan 16 2009 Rakesh Pandit <rakesh@fedoraproject.org> 1.2.2-2
- Bump to solve dependency for ginac-devel

* Tue Apr 29 2008 Quentin Spencer <qspencer@users.sf.net> 1.2.2-1
- Update to 1.2.2.

* Mon Feb 25 2008 Quentin Spencer <qspencer@users.sf.net> 1.2.0-1
- Update to 1.2.0.
- Update License tag.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.13-5
- Autorebuild for GCC 4.3

* Thu Sep 13 2007 Quentin Spencer <qspencer@users.sf.net> 1.1.13-4
- Add pkgconfig as a dependency of -devel.

* Tue Aug 21 2007 Quentin Spencer <qspencer@users.sf.net> 1.1.13-3
- Rebuild for F8.

* Mon Aug 28 2006 Quentin Spencer <qspencer@users.sf.net> 1.1.13-2
- Rebuild for FC-6.

* Thu Aug 17 2006 Quentin Spencer <qspencer@users.sf.net> 1.1.13-1
- New release.

* Mon Feb 13 2006 Quentin Spencer <qspencer@users.sf.net> 1.1.11-5
- Disable static build.
- Enable parallel build.

* Mon Feb 13 2006 Quentin Spencer <qspencer@users.sf.net> 1.1.11-4
- Rebuild for Fedora Extras 5.
- Remove /usr/share/info/dir after install.
- Exclude static libs.

* Mon Jan 16 2006 Quentin Spencer <qspencer@users.sf.net> 1.1.11-3
- Exclude /usr/share/info/dir from package (bug 178660).

* Mon Jan 16 2006 Quentin Spencer <qspencer@users.sf.net> 1.1.11-2
- Update source URL.

* Mon Jan 16 2006 Quentin Spencer <qspencer@users.sf.net> 1.1.11-1
- New upstream release.

* Mon Oct 31 2005 Quentin Spencer <qspencer@users.sf.net> 1.1.10-1
- New upstream release, incorporating previous patch.

* Mon Jun 20 2005 Quentin Spencer <qspencer@users.sf.net> 1.1.9-8
- Rebuild

* Mon Jun 13 2005 Quentin Spencer <qspencer@users.sf.net> 1.1.9-4
- Patched include/cln/string.h to correctly compile on gcc-c++-4.0.0-9

* Fri May 27 2005 Quentin Spencer <qspencer@users.sf.net> 1.1.9-3
- Added gmp-devel to Requires for devel

* Fri May 20 2005 Quentin Spencer <qspencer@users.sf.net> 1.1.9-2
- Added dist tag.

* Wed May 11 2005 Quentin Spencer <qspencer@users.sf.net> 1.1.9-1
- Excluded .la file

* Fri Apr 22 2005 Quentin Spencer <qspencer@users.sf.net> 1.1.9-1
- Added gmp-devel in BuildRequires, fixes in files
- Added release to name in Requires for devel

* Mon Mar 21 2005 Quentin Spencer <qspencer@users.sf.net> 1.1.9-1
- Adapted spec file for Fedora Extras

* Thu Nov 20 2003 Christian Bauer <Christian.Bauer@uni-mainz.de>
  Added pkg-config metadata file to devel package

* Wed Nov  6 2002 Christian Bauer <Christian.Bauer@uni-mainz.de>
  Added HTML and DVI docs to devel package

* Tue Nov  5 2001 Christian Bauer <Christian.Bauer@uni-mainz.de>
  Added Packager

Name:  tubo
Summary:  Library to thread process std-in/std-err/std-out from fork() child
Summary(zh_CN.UTF-8): 处理标准输入/输出/错误的库
Version:  5.0.15
Release:  5%{?dist}
License:  GPLv3+
URL:      http://xffm.org/libtubo.html
Source0:  http://sourceforge.net/projects/xffm/files/libtubo/libtubo0-%{version}.tar.bz2
Group:    Development/Libraries
Group(zh_CN.UTF-8): 开发/库

BuildRequires: gtk-doc
BuildRequires: glib2-devel

%description
The Libtubo library is small and simple function set to enable a process to run 
any other process in the background and communicate via the std-out, 
std-err and std-in file descriptors. 
This library is used by Rodent file-manager but is also available here 
for other programs to use freely

%description -l zh_CN.UTF-8
处理标准输入/输出/错误的库。

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary: HTML documentation of %{name}
Summary(zh_CN.UTF-8): %{name} 的 HTML 文档
BuildArch: noarch
%description doc
This package contains HTML documentation files of %{name}.
%description doc -l zh_CN.UTF-8
%{name} 的 HTML 文档。

%prep
%setup -q -n libtubo0-%{version}

## Fix file-not-utf8 warning
iconv -f iso8859-1 -t utf-8 ChangeLog > ChangeLog.conv && mv -f ChangeLog.conv ChangeLog

%build
%configure --enable-static=no --enable-shared=yes --disable-silent-rules \
 --with-semaphores=no --disable-glibtest --with-examples=no \
 --with-PACKAGE=no
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

## Remove libtool archives
find $RPM_BUILD_ROOT -name '*.la' -delete

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README ChangeLog AUTHORS
%license COPYING
%{_bindir}/tuboexec
%{_libdir}/lib%{name}.so.*
%{_mandir}/man1/tuboexec*

%files devel
%{_includedir}/tubo.*
%{_libdir}/pkgconfig/tubo.pc
%{_libdir}/lib%{name}.so

%files doc
%license COPYING
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/libtubo/


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 5.0.15-5
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 5.0.15-4
- 为 Magic 3.0 重建

* Fri Oct 23 2015 Liu Di <liudidi@gmail.com> - 5.0.15-3
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 09 2015 Antonio Trande <sagitter@fedoraproject.org> - 5.0.15-1
- Update to 5.0.15

* Mon Dec 15 2014 Antonio Trande <sagitter@fedoraproject.org> - 5.0.14-5
- %%license just on Fedora

* Mon Dec 15 2014 Antonio Trande <sagitter@fedoraproject.org> - 5.0.14-4
- Built a doc sub-package
- Added %%license tag

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Dec 20 2013 Antonio Trande <sagitter@fedoraproject.org> 5.0.14-1
- Update to 5.0.14

* Sat Dec 07 2013 Antonio Trande <sagitter@fedoraproject.org> 5.0.13-1
- Update to 5.0.13

* Thu Nov 14 2013 Antonio Trande <sagitter@fedoraproject.org> 5.0.12-1
- Update to 5.0.12
- Added manpages
- Removed norpath patch

* Wed Nov 06 2013 Antonio Trande <sagitter@fedoraproject.org> 5.0.10-2
- Added glib2-devel BR

* Wed Nov 06 2013 Antonio Trande <sagitter@fedoraproject.org> 5.0.10-1
- Update to 5.0.10
- 'example' and 'tuboexec' binaries are now packaged

* Wed Oct 16 2013 Antonio Trande <sagitter@fedoraproject.org> 5.0.7-2
- Added 'gtk-doc' BR
- Package now owns the whole %%{_datadir}/gtk-doc/ directory
- The %%{_datadir}/gtk-doc/ is now packaged in -devel subpackage

* Wed Oct 09 2013 Antonio Trande <sagitter@fedoraproject.org> 5.0.7-2
- Append '--disable-silent-rules' option to %%configure

* Mon Oct 07 2013 Antonio Trande <sagitter@fedoraproject.org> 5.0.7-1
- First package


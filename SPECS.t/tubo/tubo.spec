Name:  tubo
Summary:  Library to thread process std-in/std-err/std-out from fork() child
Version:  5.0.15
Release:  2%{?dist}
License:  GPLv3+
URL:      http://xffm.org/libtubo.html
Source0:  http://sourceforge.net/projects/xffm/files/libtubo/libtubo0-%{version}.tar.bz2
Group:    Development/Libraries

BuildRequires: gtk-doc
BuildRequires: glib2-devel

%description
The Libtubo library is small and simple function set to enable a process to run 
any other process in the background and communicate via the std-out, 
std-err and std-in file descriptors. 
This library is used by Rodent file-manager but is also available here 
for other programs to use freely

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package doc
Summary: HTML documentation of %{name}
BuildArch: noarch
%description doc
This package contains HTML documentation files of %{name}.

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
%if 0%{?fedora}
%license COPYING
%else
%doc COPYING
%endif
%{_bindir}/tuboexec
%{_libdir}/lib%{name}.so.*
%{_mandir}/man1/tuboexec*

%files devel
%{_includedir}/tubo.*
%{_libdir}/pkgconfig/tubo.pc
%{_libdir}/lib%{name}.so

%files doc
%if 0%{?fedora}
%license COPYING
%else
%doc COPYING
%endif
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/libtubo/


%changelog
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


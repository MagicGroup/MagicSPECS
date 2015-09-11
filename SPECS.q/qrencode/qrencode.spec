Name:           qrencode
Version:	3.4.4
Release:	1%{?dist}
Summary:        Generate QR 2D barcodes
Summary(zh_CN.UTF-8): 生成 QR 2D 条形码

License:        LGPLv2+
URL:            http://megaui.net/fukuchi/works/qrencode/index.en.html
Source0:        http://megaui.net/fukuchi/works/qrencode/%{name}-%{version}.tar.gz

BuildRequires:  libpng-devel chrpath


%description
Qrencode is a utility software using libqrencode to encode string data in
a QR Code and save as a PNG image.

%description -l zh_CN.UTF-8
生成 QR 2D 条形码。


%package        devel
Summary:        QR Code encoding library - Development files
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
The qrencode-devel package contains libraries and header files for developing
applications that use qrencode.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        libs
Summary:        QR Code encoding library - Shared libraries
Summary(zh_CN.UTF-8): %{name} 的运行库
Summary(fr):    Bibliothèque d'encodage QR Code - Bibliothèque partagée

%description    libs
The qrencode-libs package contains the shared libraries and header files for
applications that use qrencode.

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%prep
%setup -q


%build
%configure --with-tests
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -rf $RPM_BUILD_ROOT%{_libdir}/libqrencode.la
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/qrencode
magic_rpm_clean.sh

%check
cd ./tests
sh test_all.sh


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%{_bindir}/qrencode
%{_mandir}/man1/qrencode.1*

%files libs
%doc ChangeLog COPYING NEWS README TODO
%{_libdir}/libqrencode.so.*

%files devel
%{_includedir}/qrencode.h
%{_libdir}/libqrencode.so
%{_libdir}/pkgconfig/libqrencode.pc


%changelog
* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 3.4.4-1
- 更新到 3.4.4

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 3.3.1-5
- 为 Magic 3.0 重建

* Fri Sep 21 2012 Matthieu Saulnier <fantom@fedoraproject.org> - 3.3.1-4
- Add libs subpackage (fix RHBZ #856808)

* Thu Aug 16 2012 Matthieu Saulnier <fantom@fedoraproject.org> - 3.3.1-3
- Add French translation in spec file
- Fix incomplete removing Group tags in spec file

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 23 2012 Matthieu Saulnier <fantom@fedoraproject.org> - 3.3.1-1
- update to 3.3.1
- remove "Group" tag in spec file
- fix manfile suffix
- remove patch to fix improper LIBPTHREAD macro in the pkgconfig file:
  - upstream issue

* Sat Feb 25 2012 Peter Gordon <peter@thecodergeek.com> - 3.2.0-3
- Fix applying the LIBPTHREAD patch. (Thanks to Matthieu Saulnier.)

* Thu Feb 23 2012 Peter Gordon <peter@thecodergeek.com> - 3.2.0-2
- Add patch to fix improper LIBPTHREAD macro in the pkgconfig file:
  + fix-LIBPTHREAD-macro.patch
- Resolves: #795582 (qrencode-devel: Malformed pkgconfig file causes build to
  fail ("@LIBPTHREAD@: No such file or directory"))

* Sun Jan 15 2012 Matthieu Saulnier <fantom@fedoraproject.org> - 3.2.0-1
- update to 3.2.0
- remove BuildRoot tag in spec file
- remove "rm -rf $RPM_BUILD_ROOT" at the beginning of %%install section
- remove %%clean section
- remove %%defattr lines
- add a joker for libqrencode.so.* files

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 3.1.1-6
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 13 2010 Tareq Al Jurf <taljurf@fedoraproject.org> - 3.1.1-4
- Fixed the rpath problem.

* Mon Jul 12 2010 Tareq Al Jurf <taljurf@fedoraproject.org> - 3.1.1-3
- Fixed some small spec mistakes.

* Mon Jul 12 2010 Tareq Al Jurf <taljurf@fedoraproject.org> - 3.1.1-2
- Fixed some small errors.

* Thu Jul 08 2010 Tareq Al Jurf <taljurf@fedoraproject.org> - 3.1.1-1
- Initial build.

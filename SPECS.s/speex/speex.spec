%define name     speex
%define ver      1.2
%define betaver  rc2
%define realver  %{ver}%{betaver}
%define rel      0.%{betaver}.2%{?dist}

Summary: An open-source, patent-free speech codec
Summary(zh_CN.UTF-8): 一个开源，自由专利的语音编码
Name: %name
Version: %ver
Release: 0.%{betaver}.1%{?dist}.2
License: BSD
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source: http://downloads.xiph.org/releases/speex/%{name}-%{realver}.tar.gz
URL: http://www.speex.org/
Vendor: Speex
Packager: Jean-Marc Valin (jean-marc.valin@usherbrooke.ca)
BuildRoot: /var/tmp/%{name}-build-root
Docdir: /usr/share/doc

%description
Speex is a patent-free audio codec designed especially for voice (unlike 
Vorbis which targets general audio) signals and providing good narrowband 
and wideband quality. This project aims to be complementary to the Vorbis
codec.

%description -l zh_CN.UTF-8
Speex是一个自由专利音频编码，它设计主要用来处理声音（不像Vorbis目标是一般
音频）信号并提供良好的窄带和宽带质量。这个项目的目标是补充Vorbis编码。

%package devel
Summary:	Speex development files
Summary(zh_CN.UTF-8):	Speex开发文件
Group:		Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:	%{name} = %{version}

%description devel
Speex development files.

%description devel -l zh_CN.UTF-8
Speex开发文件

%prep
%setup -q -n %{name}-%{realver}

%build
export CFLAGS='-O3 -fPIC'
%configure --prefix=/usr --enable-shared --enable-static
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f %{buildroot}%{_libdir}/*.la
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,0)
%doc COPYING AUTHORS ChangeLog NEWS README
%doc doc/manual.pdf
%{_mandir}/man1/speex*.1*
%attr(755,root,root) %{_bindir}/speex*
%attr(755,root,root) %{_libdir}/libspeex*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/speex/speex*.h
%{_datadir}/aclocal/speex.m4
%{_libdir}/pkgconfig/speex.pc
%{_libdir}/libspeex*.a
%{_libdir}/libspeex*.so
%{_docdir}/speex/manual.pdf

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.2-0.rc2.1.2
- 为 Magic 3.0 重建

* Mon Sep 28 2015 Liu Di <liudidi@gmail.com> - 1.2-0.rc2.1.1
- 为 Magic 3.0 重建

* Mon Sep 28 2015 Liu Di <liudidi@gmail.com> - 1.2-0.rc2.1
- 更新到 1.2 rc2

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.2-0.rc1.2.2
- 为 Magic 3.0 重建

* Wed Feb 08 2012 Liu Di <liudidi@gmail.com> - 1.2-0.rc1.2.1
- 为 Magic 3.0 重建

* Wed Jan 10 2007 Liu Di <liudidi@Gmail.com> - 1.2-0.beta1.2mgc
- rebuild for Magic

* Thu Oct 03 2002 Jean-Marc Valin
- A%description -l zh_CN.UTF-8ed devel package inspired from PLD spec file

* Tue Jul 30 2002 Fredrik Rambris <boost@users.sourceforge.net> 0.5.2
- A%description -l zh_CN.UTF-8ed buildroot and docdir and ldconfig. Makes it builadble by non-roots
  and also doesn't write to actual library paths when building.


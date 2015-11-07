Name:           libvisual
Version:        0.4.0
Release:        8%{?dist}
Summary:        Abstraction library for audio visualisation plugins
Summary(zh_CN.UTF-8): 音频可视化插件的抽象库

Group:          Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
License:        LGPL
URL:            http://libvisual.sf.net
Source0:        http://dl.sf.net/libvisual/libvisual-%{version}.tar.bz2
Patch0:		libvisual-0.4.0-format-security.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
Libvisual is an abstraction library that comes between applications and
audio visualisation plugins.

Often when it comes to audio visualisation plugins or programs that create
visuals they do depend on a player or something else, basicly there is no
general framework that enable application developers to easy access cool
audio visualisation plugins. Libvisual wants to change this by providing
an interface towards plugins and applications, through this easy to use
interface applications can easily access plugins and since the drawing is
done by the application it also enables the developer to draw the visual
anywhere he wants.

%description -l zh_CN.UTF-8
Libvisual是一个在应用程序和音频可视化插件之间的抽象库。

%package        devel
Summary:        Development files for libvisual
Summary(zh_CN.UTF-8):	libvisual的开发文件
Group:          Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:       %{name} = %{version}-%{release}

%description    devel
Libvisual is an abstraction library that comes between applications and
audio visualisation plugins.

This package contains the files needed to build an application with libvisual.

%description devel -l zh_CN.UTF-8
Libvisual是一个在应用程序和音频可视化插件之间的抽象库。


这个包包含了使用libvisual开发程序所需要的文件。

%prep
%setup -q
%patch0 -p1

%build
%ifarch i386
export CFLAGS="${RPM_OPT_FLAGS} -mmmx"
%endif
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc README NEWS TODO AUTHORS
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0.4.0-8
- 为 Magic 3.0 重建

* Wed Aug 06 2014 Liu Di <liudidi@gmail.com> - 0.4.0-7
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.4.0-6
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Liu Di <liudidi@gmail.com> - 0.4.0-5
- 为 Magic 3.0 重建

* Fri Sep 15 2006 Liu Di <liudidi@gmail.com> - 0.4.0-1mgc
- update to 0.4.0

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 0.2.0-8
- fix dependency for modular X

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 0.2.0-7
- rebuild for FC5

* Wed Jun 15 2005 Aurelien Bompard <gauret[AT]free.fr> 0.2.0-6
- rebuild

* Wed Jun 15 2005 Aurelien Bompard <gauret[AT]free.fr> 0.2.0-5
- fix build for GCC4

* Thu Jun  9 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 0.2.0-4
- use dist tag for all-arch-rebuild

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 0.2.0-3
- rebuilt

* Mon Feb 14 2005 David Woodhouse <dwmw2@infradead.org> 0.2.0-2
- Fix bogus #if where #ifdef was meant

* Thu Feb 10 2005 Aurelien Bompard <gauret[AT]free.fr> 0.2.0-1
- version 0.2.0
- drop patch

* Sat Nov 27 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.1.7-0.fdr.1
- version 0.1.7

* Thu Oct 21 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.1.6-0.fdr.2
- Apply Adrian Reber's suggestions in bug 2182

* Tue Sep 28 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.1.6-0.fdr.1
- Initial RPM release.

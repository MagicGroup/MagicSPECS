Name:           gnome-video-effects
Version:	0.4.1
Release:        5%{?dist}
Summary:        Collection of GStreamer video effects
Summary(zh_CN.UTF-8): GStreamer 视频效果集合

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        GPLv2
URL:            http://live.gnome.org/GnomeVideoEffects
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        https://download.gnome.org/sources/%{name}/%{majorver}/%{name}-%{version}.tar.xz
Buildarch:      noarch

BuildRequires:  intltool

%description
A collection of GStreamer effects to be used in different GNOME Modules.

%description -l zh_CN.UTF-8
GStreamer 视频效果集合

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh

%files
%defattr(-,root,root,-)
%doc AUTHORS  COPYING NEWS README
%{_datadir}/pkgconfig/gnome-video-effects.pc
%{_datadir}/gnome-video-effects


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.4.1-5
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 0.4.1-4
- 为 Magic 3.0 重建

* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 0.4.1-3
- 更新到 0.4.1

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.3.0-3
- 为 Magic 3.0 重建

* Wed Dec 07 2011 Liu Di <liudidi@gmail.com> - 0.3.0-2
- 为 Magic 3.0 重建

* Thu Mar 10 2011 Yanko Kaneti <yaneti@declera.com> 0.3.0-1
- Update to 0.3.0.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec  6 2010 Yanko Kaneti <yaneti@declera.com> 0.2.0-1
- Update to 0.2.0. New effects.

* Wed Sep  1 2010 Yanko Kaneti <yaneti@declera.com> 0.1.0-1
- Packaged for review

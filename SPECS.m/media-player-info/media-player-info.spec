Name:           media-player-info
Version: 22
Release: 2%{?dist}
Summary:        Data files describing media player capabilities
Summary(zh_CN.UTF-8): 媒体播放器的描述数据文件

Group:          System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
License:        BSD
URL:            http://www.freedesktop.org/wiki/Software/media-player-info
Source0:        http://www.freedesktop.org/software/media-player-info/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  libudev-devel
BuildRequires:  python
Requires:       udev

%description
media-player-info is a repository of data files describing media player
(mostly USB Mass Storage ones) capabilities. These files contain information
about the directory layout to use to add music to these devices, about the
supported file formats, etc.

The package also installs a udev rule to identify media player devices.

%description -l zh_CN.UTF-8
媒体播放器（大部分是 USB）的描述数据文件.


%prep
%setup -q

%build
%configure
make %{?_smp_mflags}
magic_rpm_clean.sh

%install
make install DESTDIR=$RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README NEWS AUTHORS
/usr/share/media-player-info
/usr/lib/udev/rules.d/*
/usr/lib/udev/hwdb.d/20-usb-media-players.hwdb

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 22-2
- 更新到 22

* Fri Aug 22 2014 Liu Di <liudidi@gmail.com> - 21-1
- 更新到 21

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 15 2012 Dan Williams <dcbw@redhat.com> 17-2
- Add HP Veer (fdo #51097)

* Sun Aug 12 2012 Rex Dieter <rdieter@fedoraproject.org> 17-1
- Update to 17

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb  6 2012 Matthias Clasen <mclasen@redhat.com> 16-1
- Update to 16

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> 15-1
- Update to 15

* Wed Jul 20 2011 Matthias Clasen <mclasen@redhat.com> 14-1
- Update to 14

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> 12-1
- Update to version 12

* Fri Nov 12 2010 Matthias Clasen <mclasen@redhat.com> 11-1
- Update to version 11

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> 10-1
- Update to version 10

* Thu Apr 08 2010 Bastien Nocera <bnocera@redhat.com> 6-1
- Update to version 6

* Thu Mar 18 2010 Bastien Nocera <bnocera@redhat.com> 5-1
- Update to version 5

* Tue Sep  1 2009 Matthias Clasen <mclasen@redhat.com> - 3-1
- New upstream tarball with fixed Copyright headers

* Sat Aug 29 2009 Matthias Clasen <mclasen@redhat.com> - 2-1
- Rename to media-player-info

* Thu Aug 27 2009 Matthias Clasen <mclasen@redhat.com> - 1-1
- Initial packaging

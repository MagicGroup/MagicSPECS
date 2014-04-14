%global minorversion 3.0

Name:           gtk-xfce-engine
Version:        3.0.1
Release:        1%{?dist}
Summary:        Xfce GTK theme engine
Summary(zh_CN.UTF-8): Xfce 的 GTK 主题引擎

Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:        GPLv2+
URL:            http://www.xfce.org/
#VCS: git:git://git.xfce.org/xfce/gtk-xfce-engine
Source0:        http://archive.xfce.org/src/xfce/%{name}/%{minorversion}/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  pkgconfig(gtk+-2.0) >= 2.20.0
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.2.0

%description
This package includes the Xfce GTK theme engine with various different themes.

%description -l zh_CN.UTF-8
Xfce 的 GTK 主题引擎。

%prep
%setup -q


%build
%configure --disable-static

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%{_libdir}/gtk-2.0/*/engines/libxfce.so
%{_libdir}/gtk-3.0/*/theming-engines/libxfce.so
%{_datadir}/themes/*


%changelog
* Sat Oct 06 2012 Christoph Wickert <cwickert@fedoraproject.org> - 3.0.1-1
- Update to 3.0.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 28 2012 Christoph Wickert <cwickert@fedoraproject.org> - 3.0.0
- Update to 3.0.0 final

* Sat Apr 14 2012 Kevin Fenzi <kevin@scrye.com> - 2.99.3-1
- Update to 2.99.3

* Mon Apr 02 2012 Kevin Fenzi <kevin@scrye.com> - 2.99.2-1
- Update to 2.99.2

* Wed Jan 04 2012 Christoph Wickert <cwickert@fedoraproject.org> - 2.99.0-2
- Build GTK 3 engine

* Sun Dec 18 2011 Christoph Wickert <cwickert@fedoraproject.org> - 2.99.0-1
- Update to 2.99.0
- Add VCS key

* Sun Sep 11 2011 Christoph Wickert <cwickert@fedoraproject.org> - 2.9.0-1
- Update to 2.9.0

* Sun Mar 06 2011 Christoph Wickert <cwickert@fedoraproject.org> - 2.8.1-1
- Update to 2.8.1
- Include NEWS in %%doc

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 16 2011 Kevin Fenzi <kevin@tummy.com> - 2.8.0-1
- Update to 2.8.0

* Sun Jan 02 2011 Christoph Wickert <cwickert@fedoraproject.org> - 2.7.0-1
- Update to 2.7.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Kevin Fenzi <kevin@tummy.com> - 2.6.0-1
- Update to 2.6.0

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.99.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Kevin Fenzi <kevin@tummy.com> - 2.5.99.1-1
- Update to 2.5.99.1

* Tue Jan 13 2009 Kevin Fenzi <kevin@tummy.com> - 2.5.93-1
- Update to 2.5.93

* Sun Dec 28 2008 Kevin Fenzi <kevin@tummy.com> - 2.5.92-1
- Update to 2.5.92

* Mon Oct 27 2008 Christoph Wickert <cwickert@fedoraproject.org> - 2.4.3-1
- Update to 2.4.3
- Require filesystem package instead of owning %%{_datadir}/themes
- Don't own %%{_libdir}/gtk-2.0/2.10.0/engines/

* Sun Feb 10 2008 Kevin Fenzi <kevin@tummy.com> - 2.4.2-2
- Rebuild for gcc43

* Sun Nov 18 2007 Kevin Fenzi <kevin@tummy.com> - 2.4.2-1
- Update to 2.4.2

* Mon Aug 27 2007 Kevin Fenzi <kevin@tummy.com> - 2.4.1-2
- Update License tag. 

* Wed Apr 11 2007 Kevin Fenzi <kevin@tummy.com> - 2.4.1-1
- Update to 2.4.1

* Sun Jan 21 2007 Kevin Fenzi <kevin@tummy.com> - 2.4.0-1
- Update to 2.4.0

* Thu Nov  9 2006 Kevin Fenzi <kevin@tummy.com> - 2.3.99.2-1
- Update to 2.3.99.2

* Thu Oct  5 2006 Kevin Fenzi <kevin@tummy.com> - 2.3.99.1-3
- Fix defattr

* Wed Oct  4 2006 Kevin Fenzi <kevin@tummy.com> - 2.3.99.1-2
- Bump release for devel checkin

* Sun Sep  3 2006 Kevin Fenzi <kevin@tummy.com> - 2.3.99.1-1
- Update to 2.3.99.1

* Wed Jul 12 2006 Kevin Fenzi <kevin@tummy.com> - 2.3.90.2-1
- Update to 2.3.90.2

* Thu Apr 27 2006 Kevin Fenzi <kevin@tummy.com> - 2.3.90.1-1.fc6
- update to 2.3.90.1

* Thu Feb 16 2006 Kevin Fenzi <kevin@tummy.com> - 2.2.8-2.fc5
- Rebuild for fc5

* Mon Nov  7 2005 Kevin Fenzi <kevin@tummy.com> - 2.2.8-1.fc5
- Update to 2.2.8

* Tue May 17 2005 Kevin Fenzi <kevin@tummy.com> - 2.2.7-1.fc4
- Update to 2.2.7

* Fri Mar 25 2005 Kevin Fenzi <kevin@tummy.com> - 2.2.6-3.fc4
- lowercase Release

* Fri Mar 25 2005 Kevin Fenzi <kevin@tummy.com> - 2.2.6-2.FC4
- Removed unneeded la files

* Tue Mar 15 2005 Kevin Fenzi <kevin@tummy.com> - 2.2.6-1
- Updated to 2.2.6 version

* Tue Mar  8 2005 Kevin Fenzi <kevin@tummy.com> - 2.2.5-2
- Fixed Xfce case

* Sun Mar  6 2005 Kevin Fenzi <kevin@tummy.com> - 2.2.5-1
- Inital Fedora Extras version

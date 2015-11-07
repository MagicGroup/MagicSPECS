%define thunarver 0.9.0

Name:           thunar-media-tags-plugin
Version:        0.2.1
Release:        4%{?dist}
Summary:        Media Tags plugin for the Thunar file manager
Summary(zh_CN.UTF-8): Thunar 文件管理器的媒体标记插件

Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:        GPLv2+
URL:            http://goodies.xfce.org/projects/thunar-plugins/%{name}
Source0:        http://archive.xfce.org/src/thunar-plugins/thunar-media-tags-plugin/0.2/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  Thunar-devel >= %{thunarver}
BuildRequires:  libxml2-devel, gettext, perl(XML::Parser), libtool, xfce4-dev-tools
BuildRequires:  taglib-devel >= 1.4
BuildRequires:  intltool
Requires:       Thunar >= %{thunarver}

%description
This plugin adds special features for media files to the Thunar file manager.
It includes a special media file page for the file properties dialog, a tag 
editor for ID3 or OGG/Vorbis tags and a so-called bulk renamer, which allows 
users to rename multiple audio files at once, based on their tags.

%description -l zh_CN.UTF-8
Thunar 文件管理器的媒体标记插件。

%prep
%setup -q

%build
# Xfce has its own autotools-running-script thingy, if you use autoreconf
# it'll fall apart horribly
xdt-autogen

%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/thunarx-2/%{name}.la
magic_rpm_clean.sh
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README TODO
%{_libdir}/thunarx-2/%{name}.so


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.2.1-4
- 为 Magic 3.0 重建

* Sat Oct 24 2015 Liu Di <liudidi@gmail.com> - 0.2.1-3
- 为 Magic 3.0 重建

* Fri Oct 23 2015 Liu Di <liudidi@gmail.com> - 0.2.1-2
- 为 Magic 3.0 重建

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul  8 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.1.2-13
- add intltool build dep

* Thu Apr 05 2012 Kevin Fenzi <kevin@scrye.com> - 0.1.2-12
- Rebuild for Xfce 4.10

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.1.2-10
- Rebuild for new libpng

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Adam Williamson <awilliam@redhat.com> - 0.1.2-8
- port to exo-1 and thunarx-2, fix an implicit linking issue, and
  a crash: all from Debian maintainer Lionel Le Folgoc

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 20 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.2-5
- Rebuild for Thunar 0.9.93 (Xfce 4.6. Beta 3)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1.2-4
- Autorebuild for GCC 4.3

* Tue Aug 21 2007 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.2-3
- Rebuild for BuildID feature

* Mon Jan 22 2007 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.2-2
- Rebuild for Thunar 0.8.0.

* Sat Jan 20 2007 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.2-1
- Update to 0.1.2.

* Sat Nov 11 2006 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.1-1
- Initial Fedora Extras Version.

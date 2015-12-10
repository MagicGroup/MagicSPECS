Name:           lxmusic
Version:        0.4.4
Release:        10%{?dist}
Summary:        Lightweight XMMS2 client with simple user interface
Summary(zh_CN.UTF-8): 带有简单用户界面的轻量级 XMMS2 客户端

Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
License:        GPLv2+
URL:            http://lxde.org
Source0:        http://downloads.sourceforge.net/lxde/%{name}-%{version}.tar.gz
# As long as there are no plugins, disable the Tools menu
Patch0:         lxmusic-0.3.0-no-tools-menu.patch
Patch1:         lxmusic-0.4.4-libnotify-0.7.0.patch
# https://sourceforge.net/tracker/?func=detail&atid=894869&aid=3038938&group_id=180858
# Patch at http://paste.lisp.org/display/116965/1,1/raw
Patch2:         lxmusic-0.4.4-fix-segfault-in-xmmsv_get_int.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel >= 2.12.0 xmms2-devel >= 0.6
BuildRequires:  desktop-file-utils gettext intltool libnotify-devel
Requires:       xmms2 >= 0.7

%description
LXMusic is a very simple gtk+ XMMS2 client written in pure C. It has very few 
functionality, and can do nothing more than play the music. The UI is very 
clean and simple. This is currently aimed to be used as the default music 
player of LXDE (Lightweight X11 Desktop Environment) project.

%description -l zh_CN.UTF-8
带有简单用户界面的轻量级 XMMS2 客户端。

%prep
%setup -q
%patch0 -p1 -b .no-tools
%patch2 -p1 -b .segfault-in-xmmsv_get_int
%if 0%{?fedora} >= 15
%patch1 -p1 -b .libnotify-0.7.0
%endif

%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
desktop-file-install                                       \
  --delete-original                                        \
  --dir=${RPM_BUILD_ROOT}%{_datadir}/applications          \
  ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop
magic_rpm_clean.sh
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_bindir}/%{name}
%{_datadir}/applications/lxmusic.desktop
%{_datadir}/lxmusic
%{_datadir}/pixmaps/lxmusic.png


%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 0.4.4-10
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.4.4-9
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.4.4-6
- Rebuild for new libpng

* Mon Dec 05 2011 Tom Callaway <spot@fedoraproject.org> - 0.4.4-5
- rebuild for xmms2 0.8

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 25 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.4-3
- Fix segfault in xmmsv_get_int (#634698)

* Wed Nov 17 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.4-2
- Fix for libnotify 0.7.0

* Thu Jun 03 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.4-1
- Update to 0.4.4 with xmms2 0.7.0

* Tue Dec 29 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.2-1
- Update to 0.4.2

* Sun Dec 20 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.1-1
- New upstream release to fix #539729, so we drop the patches

* Wed Dec 16 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.0-2
- Fix crash when emptying large playlists (#539729)

* Sat Sep 05 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.0-1
- Update to 0.4.0

* Tue Aug 11 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.3.0-1
- update to 0.3.0

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 13 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.3-3
- Disable empty tools menu

* Sun Mar 01 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.3-2
- Build Require gtk2-devel

* Sat Dec 20 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.3-1
- Initial Fedora Package

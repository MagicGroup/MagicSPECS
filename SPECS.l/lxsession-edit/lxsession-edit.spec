Name:           lxsession-edit
Version:        0.2.0
Release:        6%{?dist}
Summary:        Simple GUI to configure what’s automatically started in LXDE
Summary(zh_CN.UTF-8): 简单的图形界面来配置 LXDE 中自动启动的程序

Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:        GPLv2+
URL:            http://lxde.org
Source0:        http://downloads.sourceforge.net/lxde/%{name}-%{version}.tar.gz
#VCS: git:git://lxde.git.sourceforge.net/gitroot/lxde/lxsession-edit
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  intltool
Requires:       lxsession >= 0.4.0

%description
LXSession-edit is a tool to manage freedesktop.org compliant desktop session 
autostarts. Currently adding and removing applications from the startup list 
is not yet available, but it will be support in the next release.

%description -l zh_CN.UTF-8
简单的图形界面来配置 LXDE 中自动启动的程序。

%prep
%setup -q
# fix icon in desktop file
# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxsession-edit;a=commit;h=3789a96691eadac9b8f3bf3034a97645860bd138
sed -i 's/^Icon=xfwm4/Icon=session-properties/g' lxsession-edit.desktop.in


%build
%configure
# workaround for FTBFS #539206
touch -r po/Makefile po/stamp-it
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
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
%{_datadir}/applications/lxsession-edit.desktop
%{_datadir}/lxsession-edit/


%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.2.0-6
- 为 Magic 3.0 重建

* Tue Jul 08 2014 Liu Di <liudidi@gmail.com> - 0.2.0-5
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.2.0-2
- Rebuild for new libpng

* Sat Aug 27 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0
- BuildRequire intltool
- Remove all patches as they were either upstreamed of came from upstram

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 31 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.1-4
- Support new config file format

* Mon Nov 23 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.1-3
- Workaround for infinite loop that causes FTBFS (#539206)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 06 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.1-1
- Update to 0.1.1

* Sun Dec 07 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.1-1
- Initial Fedora package

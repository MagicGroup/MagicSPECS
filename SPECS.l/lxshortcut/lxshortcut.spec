Name:           lxshortcut
Version:        0.1.2
Release:        5%{?dist}
Summary:        Small utility to edit application shortcuts
Summary(zh_CN.UTF-8): 编辑应用程序快捷方式的简单工具

Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:        GPLv2+
URL:            http://lxde.org
#VCS: git:git://lxde.git.sourceforge.net/gitroot/lxde/lxshortcut
Source0:        http://downloads.sourceforge.net/lxde/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel
BuildRequires:  gettext
BuildRequires:  intltool

%description
LXShortcut is a small utility to edit application shortcuts created with 
freedesktop.org Desktop Entry spec. Now editing of application shortcuts 
becomes quite easy.

%description -l zh_CN.UTF-8
编辑应用程序快捷方式的简单工具.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
magic_rpm_clean.sh
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ChangeLog COPYING README
%{_bindir}/%{name}
%{_datadir}/%{name}/


%changelog
* Tue Jul 08 2014 Liu Di <liudidi@gmail.com> - 0.1.2-5
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.1.2-2
- Rebuild for new libpng

* Tue Aug 30 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.2-1
- Update to 0.1.2
- BuildRequire intltool

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 23 2009 Christoph Wickert <fedora christoph-wickert de> - 0.1.1-3
- Workaround for infinite loop that causes FTBFS (#539158)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 06 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.1-1
- Update to 0.1.1

* Sun Dec 07 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.1-1
- Initial Fedora package

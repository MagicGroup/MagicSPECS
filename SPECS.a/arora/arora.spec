%define git 1
%define vcsdate 20151028

%define with_gnome 0

Name:           arora
Version:        0.11.1
%if 0%{git}
Release:	0.git%{vcsdate}.%{?dist}.8
%else
Release:        8%{?dist}
%endif
Summary:        A cross platform web browser
Summary(zh_CN): 一个跨平台的网页浏览器

Group:          Applications/Internet
Group(zh_CN):	应用程序/互联网
License:        GPLv2+
URL:            http://code.google.com/p/arora/
%if 0%{git}
# git clone git://github.com/Arora/arora.git
Source0:	%{name}-git%{?vcsdate}.tar.xz
%else
Source0:        http://arora.googlecode.com/files/%{name}-%{version}.tar.gz
%endif
Source1:	make_arora_git_package.sh
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  desktop-file-utils
BuildRequires:  qt4-devel >= 4.4.0
# for gnome default app path
%if %{with_gnome}
BuildRequires:  control-center-devel
%endif

%description
Arora is a simple, cross platform web browser based on the QtWebKit engine.
Currently, Arora is still under development, but it already has support for
browsing and other common features such as web history and bookmarks.

%description -l zh_CN
Arora 是一个简单的，跨平台的网页浏览器，基于 QtWebKit 引擎。

%if %{with_gnome}
%package gnome
Summary:        Better Gnome support for Arora
Summary(zh_CN): Arora 的更好 Gnome 支持
Group:          Applications/Internet
Group(zh_CN):   应用程序/互联网
Requires:       control-center
Requires:       arora

%description gnome
Adds Arora to Preferred Applications list in Gnome Control Center.

%description gnome -l zh_CN
Arora 的更好 Gnome 支持。
%endif

%prep
%if %{vcsdate}
%setup -q -n %{name}-git%{vcsdate}
%else
%setup -q
%endif

%build
qmake-qt4 PREFIX=%{_prefix}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make INSTALL_ROOT=$RPM_BUILD_ROOT install 

desktop-file-install --vendor fedora \
      --dir $RPM_BUILD_ROOT%{_datadir}/applications\
      --delete-original\
      $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS README ChangeLog
%doc LICENSE.GPL2 LICENSE.GPL3
%{_bindir}/arora
%{_bindir}/arora-placesimport
%{_bindir}/htmlToXBel
%{_bindir}/arora-cacheinfo
%{_datadir}/applications/fedora-%{name}.desktop    
%{_datadir}/icons/hicolor/128x128/apps/arora.png
%{_datadir}/icons/hicolor/16x16/apps/arora.png
%{_datadir}/icons/hicolor/32x32/apps/arora.png
%{_datadir}/icons/hicolor/scalable/apps/arora.svg
%{_datadir}/arora
%{_datadir}/pixmaps/arora.xpm
%{_datadir}/man/man1

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com>
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com>
- 更新到 20151028 日期的仓库源码

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com>
- 为 Magic 3.0 重建

* Fri Feb 28 2014 Liu Di <liudidi@gmail.com>
- 更新到 20140228 日期的仓库源码

* Fri Feb 28 2014 Liu Di <liudidi@gmail.com>
- 更新到 20140228 日期的仓库源码

* Fri Feb 28 2014 Liu Di <liudidi@gmail.com>
- 更新到 20140228 日期的仓库源码

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com>
- 为 Magic 3.0 重建



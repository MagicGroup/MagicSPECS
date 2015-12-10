Name: magic-logos
Summary: Magic-related icons and pictures
Summary(zh_CN.UTF-8): Magic 相关的图标和图像
Version: 30.0.0
Release: 4%{?dist}
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
URL: http://git.fedorahosted.org/git/fedora-logos.git/
License: Licensed only for approved usage, see COPYING for details. 

BuildArch: noarch
Obsoletes: redhat-logos
Obsoletes: gnome-logos
Provides: redhat-logos = %{version}-%{release}
Provides: gnome-logos = %{version}-%{release}
Provides: system-logos = %{version}-%{release}

%description
Magic-related icons and pictures

%description -l zh_CN.UTF-8
Magic 相关的图标和图像。

%prep

%build

%install

%post

%postun

%files

%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 30.0.0-4
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 30.0.0-3
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 30.0.0-2
- 为 Magic 3.0 重建



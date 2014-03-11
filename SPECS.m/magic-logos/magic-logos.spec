Name: magic-logos
Summary: Magic-related icons and pictures
Version: 30.0.0
Release: 2%{?dist}
Group: System Environment/Base
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

%prep

%build

%install

%post

%postun

%files

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 30.0.0-2
- 为 Magic 3.0 重建



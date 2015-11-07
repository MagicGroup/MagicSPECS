Name: create
Version: 0.1.3
Release: 4%{?dist}
Summary: Ambiently Sharing Creativity
Summary(zh_CN.UTF-8): 广泛共享创意
License: GPLv2
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://create.freedesktop.org/
Source0: http://create.freedesktop.org/releases/create/%{name}-%{version}.tar.bz2
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
Ambiently Sharing Creativity.

%description -l zh_CN.UTF-8
广泛共享创意。

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix}
scons install PREFIX=%{buildroot}%{_prefix}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_datadir}/*

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.1.3-4
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.1.3-3
- 为 Magic 3.0 重建




Summary: langdao-ce-gb dictionary data files for StarDict2
Summary(zh_CN.UTF-8): StarDict2用的朗道汉英字典
Name:          stardict-langdao-ce-gb
Version:       2.4.2
Release:       4%{?dist}
License:       GPL
Group:         Applications/System
Group(zh_CN.UTF-8):  应用程序/系统
BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:     noarch
Source:        stardict-langdao-ce-gb-2.4.2.tar.bz2
Requires:      stardict

%description
ngdao-ce-gb dictionary data files for StarDict2.

%description -l zh_CN.UTF-8
StarDict2用的朗道汉英字典。

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT/*

mkdir -p $RPM_BUILD_ROOT%{_datadir}/stardict/dic/stardict-langdao-ce-gb-2.4.2
cp * $RPM_BUILD_ROOT%{_datadir}/stardict/dic/stardict-langdao-ce-gb-2.4.2

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_datadir}/stardict/dic/*

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 2.4.2-4
- 为 Magic 3.0 重建

* Fri Feb 10 2012 Liu Di <liudidi@gmail.com> - 2.4.2-3
- 为 Magic 3.0 重建

* Wed Jan 10 2006 Liu Di <liudidi@gmail.com> - 2.4.2-2mgc
- repack for Magic 2.1

Summary: MagicLinux FairytaleWorld Icon Set
Summary(zh_CN.UTF-8): MagicLinux 童话世界图标
Name: FairytaleWorld
Version: 1.0
Release: 8%{?dist}
Source0: %{name}.tar.gz
Vendor: caihua
Packager: KanKer <kanker@163.com>
License: GPL
Url: http://www.magiclinux.org/people/caihua/
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

%description
Caihua's icon set for MagicLinux

%description -l zh_CN.UTF-8
蔡华为 Magic Linux 创作的图标集

%prep
%setup -q -n FairytaleWorld

%build
%install
mkdir -p %{buildroot}/usr/share/icons/
cp -rf ../FairytaleWorld  %{buildroot}/usr/share/icons/


%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}


%files
%defattr(-,root,root)
%{_datadir}/icons/FairytaleWorld/*

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 1.0-8
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 1.0-7
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.0-6
- 为 Magic 3.0 重建

* Sun Sep 16 2007 kde <athena_star {at} 163 {dot} com> - 1.0-4mgc
- move "kdeglobals" config file to magic-kde-config packages

* Sat Feb 5 2005  KanKer <kanker@163.com> 1.0-1mgc
- initilize spec


%define name mount-iso
%define version 1.4
%define release 4%{?dist}

Summary: Service Menu for Mount/Unmount Cd-DVD Image
Summary(zh_CN): 管理 ISO 镜像的右键菜单。
Name: %{name}
Version: %{version}
Release: %{release}.1
Source0: %{name}.tar.bz2
License: GPLv2+
Group: Applications/Archiving
Group(zh_CN): 应用程序/归档
# Not yet real page
Url: http://sourceforge.net/projects/ccd2iso/
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildArch: noarch

%description
Service Menu for Mount/Unmount Cd-DVD Images (ISO, etc...) and to create Images "on the fly"

%description -l zh_CN
管理 ISO 镜像的右键菜单。

%prep
%setup -q -n %name

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_bindir}
install -m 755 src/mountiso.sh %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{kde4_servicesdir}/ServiceMenus
cp -a src/*.desktop %{buildroot}%{kde4_servicesdir}/ServiceMenus


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%_bindir/mountiso.sh
%{kde4_servicesdir}/ServiceMenus/*.desktop

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.4-4.1
- 为 Magic 3.0 重建

* Fri Nov 21 2014 Liu Di <liudidi@gmail.com> - 1.4-3.1
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.4-2
- 为 Magic 3.0 重建



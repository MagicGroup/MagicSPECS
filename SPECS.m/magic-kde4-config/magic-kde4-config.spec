Summary: K Desktop Environment - Configuration files
Summary(zh_CN.UTF-8): K 桌面环境(KDE4) - 配置文件
Name: magic-kde4-config
Version: %{kde4_kdelibs_version}
Release: 1%{?dist}
License: GPL
URL: http://www.magiclinux.org
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
Source0: magic-kde4-config-%{version}.tar.bz2
Requires: kdelibs4, magic-system-config
Conflicts: magic-kde-config
#Requires: konversation

%description

Configuration filess for KDE by MagicLinux.

%description -l zh_CN.UTF-8
MagicLinux 下 KDE 的配置文件。

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

# install config files
cp -rf etc usr %{buildroot}/

%post
## Enable "Start New Session" magic
#grep "^:1" /etc/X11/xdm/Xservers >& /dev/null ||
#echo ":1 local reserve /usr/bin/X :1 -dpi 96" >> /etc/X11/xdm/Xservers
## make kdm and KDE sessions the default, if not otherwise specified
#grep "^DESKTOP=" /etc/sysconfig/desktop >& /dev/null ||
#echo "DESKTOP=KDE4" >> /etc/sysconfig/desktop
#grep "^DISPLAYMANAGER=" /etc/sysconfig/desktop >& /dev/null ||
#echo "DISPLAYMANAGER=KDE4" >> /etc/sysconfig/desktop


%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.3.x.20090614-3
- 为 Magic 3.0 重建


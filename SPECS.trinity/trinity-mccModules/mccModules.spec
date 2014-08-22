# Initial spec file created by autospec ver. 0.8 with rpm 3 compatibility
Summary: Magic Control Center Modules
Summary(zh_CN.UTF-8): Magic 控制中心模块
Name: mccModules
Version: 0.0.1
Release: 1%{?dist}
Group: User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
License: GPL
Source: %{name}-%{version}.tar.bz2
Patch1:	mccModules-0.0.1-tde.patch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-buildroot
# Following are optional fields
URL: http://lovewilliam.bokee.com
Distribution: Magic Linux
# This is not a relocatable package.
#Prefix: /usr
BuildArch: i686
Packager: lovewilliam <lovewilliam@gmail.com>
Requires: qt-devel kdebase
#Obsoletes: 
BuildRequires: qt gcc glib kdelibs-devel kdebase

%description
mccModules are modules for magic control center

%description -l zh_CN.UTF-8
mccModules 是 Magic 控制中心的模块

%prep
%setup -q
%patch1 -p1

%build
cd fcitxconfig
chmod 777 admin/*
make -f admin/Makefile.common
%configure --prefix=/usr
make
cd ..
cd grubui
chmod 777 admin/*
make -f admin/Makefile.common
#automake
%configure --prefix=/usr
make
cd ..
cd mlimecfg
chmod 777 admin/*
make -f admin/Makefile.common
#automake
%configure --prefix=/usr
make
cd ..

%install
rm -rf %{BuildRoot}
mkdir -p $RPM_BUILD_ROOT
cd fcitxconfig
make DESTDIR=$RPM_BUILD_ROOT install
cd ..
cd grubui
make DESTDIR=$RPM_BUILD_ROOT install
cd ..
cd mlimecfg
make DESTDIR=$RPM_BUILD_ROOT install
cd ..

mkdir -p $RPM_BUILD_ROOT/etc/ime
install -m 664 mlimecfg/src/ime/fcitx $RPM_BUILD_ROOT/etc/ime/fcitx
install -m 664 mlimecfg/src/ime/scim $RPM_BUILD_ROOT/etc/ime/scim

mkdir -p $RPM_BUILD_ROOT/usr/share/icons/hicolor/128x128/apps
mkdir -p $RPM_BUILD_ROOT/usr/share/icons/hicolor/64x64/apps
mkdir -p $RPM_BUILD_ROOT/usr/share/icons/hicolor/32x32/apps
mkdir -p $RPM_BUILD_ROOT/usr/share/icons/hicolor/22x22/apps
mkdir -p $RPM_BUILD_ROOT/usr/share/icons/hicolor/16x16/apps

install -m 664 icons/hi128-app-grub.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/128x128/apps/grub.png
install -m 664 icons/hi16-app-grub.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/16x16/apps/grub.png
install -m 664 icons/hi22-app-grub.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/22x22/apps/grub.png
install -m 664 icons/hi32-app-grub.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/32x32/apps/grub.png
install -m 664 icons/hi64-app-grub.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/32x32/apps/grub.png
install -m 664 icons/hi16-app-boot.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/16x16/apps/boot.png
install -m 664 icons/hi16-app-core.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/16x16/apps/core.png
install -m 664 icons/hi16-app-hdd.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/16x16/apps/hdd.png
install -m 664 icons/hi16-app-vmlinuz.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/16x16/apps/vmlinuz.png
install -m 664 icons/hi32-app-qfcitxconfig.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/32x32/apps/qfcitxconfig.png


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"
rm -rf $RPM_BUILD_DIR/%{name}-%{version}


%files
%defattr(-,root,root,-)
/usr
/etc
%exclude /usr/src
%exclude /usr/*/debug*

%changelog
* Thu Aug 21 2008 lovewilliam <lovewilliam@gmail.com>
- 0.0.1

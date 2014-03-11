Name:         powersave
URL:          http://powersave.sourceforge.net/
Summary:      General Powermanagement daemon supporting APM and ACPI and CPU frequency scaling
Summary(zh_CN.UTF-8): 通用电源管理服务，支持APM和ACPI及CPU频率控制
Version:      0.15.20
Group:        System Environment/Daemons
Group(zh_CN.UTF-8):	系统环境/服务
Release:      3%{?dist}
License:      GPL
#Autoreqprov:  on
# for doc
BuildRequires: lynx
BuildRequires: liblazy-devel >= 0.2
Requires:	chkconfig
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Source0:      %{name}-%{version}.tar.bz2
Patch0:		powersave-rcpowersaved-daemon.patch
Patch1:		powersave-0.15.20-gcc4.patch

%package devel
Summary:      Files needed for development with the powersave daemon or general powermanagement
Summary(zh_CN.UTF-8):	使用powersave服务或通用电源管理开发所需要的文件
Requires:     %{name} = %{version}-%{release}
Autoreqprov:  on
Group:        Development/Libraries
Group(zh_CN.UTF-8): 开发/库
%package libs
Summary:      Shared libraries of the powersave daemon
Summary(zh_CN.UTF-8): powersave服务的共享库
Autoreqprov:  on
Group:        System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description
Powersave gives you control over the ACPI power buttons, three user
defined battery states (warning, low, critical) and supports proper
standby/suspend handling.

Additionally it could control the frequency of your processor if it
supports SpeedStep(Intel) or PowerNow(AMD) technology. This will
greatly reduce power consumption and heat production in your system.

Together with the kpowersave and yast2-power-management package it
should be the preferred power managing application.

Authors:
--------
    Thomas Renninger (mail@renninger.de, trenn@suse.de)
    Holger Macht <holger@homac.de>
    Stefan Seyfried <seife@suse.de>

%description -l zh_CN.UTF-8
powersave使你控制ACPI电源按钮，三种用户定义的电池状态（警告，低，临界）
并支持正确的待机/挂起操作。

更进一步的如果你的CPU支持SpeedStep(Intel)或PowerNow(AMD)它还可以控制频率。
这将极大的减少系统的功耗和发热量。

和kpowersav和yast2-power-management包一起它成为首选的电源管理程序。

作者：
-------
    Thomas Renninger (mail@renninger.de, trenn@suse.de)
    Holger Macht <holger@homac.de>
    Stefan Seyfried <seife@suse.de>

%description devel
Files needed for development with the powersave daemon or general
powermanagement.

Authors:
--------
    Thomas Renninger <mail@renninger.de, trenn@suse.de>
    Holger Macht <holger@homac.de>
    Stefan Seyfried <seife@suse.de>

%description devel -l zh_CN.UTF-8
使用powersave服务或通用电源管理开发所需要的文件。

作者：
-------
    Thomas Renninger (mail@renninger.de, trenn@suse.de)
    Holger Macht <holger@homac.de>
    Stefan Seyfried <seife@suse.de>

%description libs
Shared libraries of the powersave daemon. A running powersave daemon is
needed for full functionality of these libraries.

Authors:
--------
    Thomas Renninger <mail@renninger.de, trenn@suse.de>
    Holger Macht <holger@homac.de>
    Stefan Seyfried <seife@suse.de>

%description libs -l zh_CN.UTF-8
powersave服务的共享库。完整的运行powersave服务需要这些库。

作者：
-------
    Thomas Renninger (mail@renninger.de, trenn@suse.de)
    Holger Macht <holger@homac.de>
    Stefan Seyfried <seife@suse.de>

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1

%build

aclocal
autoconf
autoheader
libtoolize --force
automake -a

#autoreconf -fi
./configure \
            --prefix=/usr --libdir=%_libdir \
            --enable-docs --disable-on_ac_power --enable-doc-dir=/usr/share/doc/powersave --mandir=%_mandir --sysconfdir=/etc --with-kde-bindir=/usr/bin --with-gnome-bindir=/usr/bin
make -e 'VERSION_NO="\"%version\""'

%install
rm -rf $RPM_BUILD_ROOT
# Version will be used for link to library: .so.%version, see below in %files
make install -e DESTDIR=%{buildroot} POWERSAVE_LIB_VERSION=%version TRANSLATION_DIR="%_datadir/locale/"
install scripts/rcpowersaved.redhat %buildroot/etc/init.d/powersaved

magic_rpm_clean.sh
%find_lang power-management

%clean
rm -rf $RPM_BUILD_ROOT

%post
chkconfig --add powersaved
chkconfig powersaved off
%preun
chkconfig --del powersaved

%postun

%files -f power-management.lang
%defattr(-,root,root)

%_sbindir/*
%_bindir/powersave
#%_prefix/lib/powersave
%_mandir/*/*
%config /etc/init.d/powersaved
%config /etc/dbus-1/system.d/powersave.conf
/etc/acpi/events.ignore/events.ignore
/etc/powersave
%_docdir/%name

%files devel
%defattr(-,root,root)
%_includedir/*
%_libdir/lib*.la
%_libdir/lib*.a

%files libs
%defattr(-,root,root)
%_libdir/lib*.so*
%_libdir/pkgconfig/*
%_libexecdir/*


%changelog
* Fri Jun 13 2008 Liu Di <liudidi@gmail.com> - 0.15.20-1mgc
- 更新到 0.15.20

* Tue Oct 10 2006 Liu Di <liudidi@gmail.com> - 0.14.0-1mgc
- update to 0.14.0

* Fri Aug 25 2006 Liu Di <liudidi@gmail.com> - 0.13.5-1mgc
- update to 0.13.5

* Mon Jun 11 2006 Liu Di <liudidi@gmail.com> - 0.12.17-1mgc
- update to 0.12.18

* Mon May 15 2006 Liu Di <liudidi@gmail.com> - 0.12.17-1mgc
- update to 0.12.17

%define name    kwine
%define version 0.1
%define release 2%{?dist}


Summary:        Tools set to improve KDE and Wine interoperability.
Summary(zh_CN.UTF-8): 增强KDE和Wine协同性的工具集合
Name:           %{name}
Version:        %{version}
Release:        %{release}
License:        GPL
Vendor:         Magic Linux
URL:            http://kwine.sourceforge.net/
Packager:       Liu Di <ludidi@gmail.com>
Group:          Applications/Emulators
Group(zh_CN.UTF-8):  应用程序/模拟器
Source:         %{name}-%{version}.tar.gz
Patch:          kwine-0.1-admin.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}
Prefix:         %(kde-config --prefix)
Requires:       kdelibs >= 3.1, wine, kwinetools
BuildRequires:  kdelibs-devel >= 3.1, wine-devel, kwinetools

%description
Kwine is a set of tools for Wine and KDE interoperability. It includes frontends tools like Kio_Wine, Kfile_wine, Kwine, and kwine_startmenu, and backends like kwinetools and Kwinedcop, which is a gateway for accessing the Wine API using DCOP.

%description -l zh_CN.UTF-8
Kwine是增强KDE和Wine协同性的工具集合。它包括前端工具比如Kio_Wine, Kfile_wine, Kwine，和kwine_startmenu，和后端工具比如kwinetools和
Kwinedcop，一个使用DCOP访问WineAPI的代理。

%prep
%setup -q
%patch -p1
chmod 777 admin/* 

%build

make -f admin/Makefile.common cvs

CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" \
./configure \
             --prefix=%{prefix} --libdir=%{_libdir}\
                $LOCALFLAGS

#临时措施
sed -i 's/\/include\/tqt/\/include\/tqt \-lqt\-mt \-ltdecore \-ltdeui \-lDCOP \-lkio/g' src/Makefile

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc AUTHORS
%doc COPYING
%doc ChangeLog
%doc INSTALL
%doc README
%doc TODO
%{prefix}/*
%exclude %{prefix}/*/debug*

%changelog
* Tue Aug 29 2006 Liu Di <liudidi@gmail.com> - 0.1-1mgc
- first build for Magic

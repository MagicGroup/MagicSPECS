#
# spec file for package kmymoney (version R14)
#
# Copyright (c) 2014 Trinity Desktop Environment
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif
%define tde_pkg kmymoney
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

# Required for Mageia >= 2: removes the ldflag '--no-undefined'
%define _disable_ld_no_undefined 1

Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	1.0.5
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Personal finance manager for TDE
Summary(zh_CN.UTF-8): TDE 下的个人财务管理程序
Group:		Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz
Source1:		kmymoneytitlelabel.png

Patch1:			trinity-kmymoney-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	libtool

BuildRequires:	recode
BuildRequires:	libofx-devel

# OPENSP support
BuildRequires:	opensp-devel

# TQT3-sqlite3
BuildRequires:	libtqt3-mt-sqlite3
Requires:		libtqt3-mt-sqlite3

Requires:		%{name}-common = %{?epoch:%{epoch}:}%{version}-%{release}


%description
KMyMoney is the Personal Finance Manager for TDE. It operates similar to
MS-Money and Quicken, supports different account types, categorisation of
expenses, QIF import/export, multiple currencies and initial online banking
support.

%description -l zh_CN.UTF-8
TDE 下的个人财务管理程序。

%post
update-desktop-database %{tde_tdeappdir} > /dev/null
/sbin/ldconfig
for f in hicolor locolor Tango oxygen; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done

%postun
update-desktop-database %{tde_tdeappdir} > /dev/null
/sbin/ldconfig
for f in hicolor locolor Tango oxygen; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done

%files
%defattr(-,root,root,-)
%{tde_bindir}/kmymoney
%{tde_bindir}/kmymoney2
%{tde_tdeappdir}/kmymoney2.desktop
%{tde_datadir}/mimelnk/application/x-kmymoney2.desktop
%{tde_datadir}/servicetypes/kmymoneyimporterplugin.desktop
%{tde_datadir}/servicetypes/kmymoneyplugin.desktop
%{tde_libdir}/*.so.*
%{tde_tdelibdir}/kmm_ofximport.la
%{tde_tdelibdir}/kmm_ofximport.so

##########

%package common
Summary:		KMyMoney architecture independent files
Summary(zh_CN.UTF-8): %{name} 的公用文件
Group:			Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具
Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description common
This package contains architecture independent files needed for KMyMoney to
run properly. It also provides KMyMoney documentation. Therefore, unless you
have '%{name}' package installed, you will hardly find this package useful.

%description common -l zh_CN.UTF-8
%{name} 的公用文件。

%files common -f kmymoney2.lang
%defattr(-,root,root,-)
%{tde_datadir}/apps/kmymoney2/
%{tde_datadir}/config.kcfg/kmymoney2.kcfg
%{tde_datadir}/icons/hicolor/*/*/*.png
%dir %{tde_datadir}/icons/Tango/
%dir %{tde_datadir}/icons/Tango/*/
%dir %{tde_datadir}/icons/Tango/*/*/
%{tde_datadir}/icons/Tango/*/*/*.png
%{tde_datadir}/icons/Tango/scalable/*.svgz
%{tde_datadir}/icons/locolor/*/*/*.png
%dir %{tde_datadir}/icons/oxygen/
%dir %{tde_datadir}/icons/oxygen/*/
%dir %{tde_datadir}/icons/oxygen/*/*/
%{tde_datadir}/icons/oxygen/*/*/*.png
%{tde_datadir}/icons/oxygen/scalable/*.svgz
%{tde_tdedocdir}/HTML/en/kmymoney2/
%{tde_mandir}/man1/kmymoney2.*
%{tde_datadir}/apps/kmm_ofximport/
%{tde_datadir}/services/kmm_ofximport.desktop

##########

%package devel
Summary:		KMyMoney development files
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:			Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
This package contains development files needed for KMyMoney plugins.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%files devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/kmymoney/
%{tde_libdir}/libkmm_kdchart.la
%{tde_libdir}/libkmm_mymoney.la
%{tde_libdir}/libkmm_plugin.la
%{tde_libdir}/*.so
%{_libdir}/tqt3/plugins/designer/libkmymoney.so

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%patch1 -p1

%__install -m644 %{SOURCE1} kmymoney2/widgets/

%__cp "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig:${PKG_CONFIG_PATH}"

# Fix strange FTBFS on RHEL4
%if 0%{?rhel} == 4
grep -v "^#~" po/it.po >/tmp/it.po && mv -f /tmp/it.po po/it.po
%endif

# Warning: --enable-final causes FTBFS
%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  --includedir=%{tde_tdeincludedir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --disable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility \
  \
  --with-qmake=%{_bindir}/tqmake \
  --with-qt-dir=%{_libdir}/tqt3 \
  \
  --disable-pdf-docs \
  --enable-ofxplugin \
  --enable-ofxbanking \
  --enable-qtdesigner \
  --disable-sqlite3

%__make %{?_smp_mflags}

%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}
magic_rpm_clean.sh
%find_lang kmymoney2


%clean
%__rm -rf %{buildroot}


%changelog
* Mon Jul 29 2013 Francois Andriot <francois.andriot@free.fr> - 2:1.0.5-1
- Initial release for TDE 14.0.0

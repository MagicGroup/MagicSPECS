#
# spec file for package koffice-i18n (version R14)
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
%define tde_pkg koffice-i18n
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


# Builds all supported languages (not unsupported ones)
%if "%{?TDE_LANGS}" == ""
%define TDE_LANGS zh_CN zh_TW
%endif


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	1.6.3
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}.2
Summary:	Internationalization support for Koffice [Trinity]
Summary(zh_CN.UTF-8): TDE 下 Koffice 的国际化支持
Group:		User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

# Speed build options
%define debug_package %{nil}
%define __spec_install_post %{nil}
AutoReq: no

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz
Patch1:		%{name}-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	findutils
BuildRequires:	gettext

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig

%description
%{summary}.

%description -l zh_CN.UTF-8
TDE 下 Koffice 的国际化支持。

%package Chinese
Summary:		Chinese(zh_CN) (Simplified Chinese) language support for Koffice [Trinity]
Summary(zh_CN.UTF-8): Koffice 的简体中文 (zh_CN) 语言包
Group:			User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Provides: %{name}-zh_CN = %{version}-%{release}
%description Chinese
%{summary}.
%description Chinese -l zh_CN.UTF-8
Koffice 的简体中文 (zh_CN) 语言包。

%package Chinese-Big5
Summary:		Chinese(zh_TW) (Big5) language support for Koffice [Trinity]
Summary(zh_CN.UTF-8): Koffice 的繁体中文 (zh_TW) 语言包
Group:			User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Provides: %{name}-tz_TW = %{version}-%{release}
%description Chinese-Big5
%{summary}.
%description Chinese-Big5 -l zh_CN.UTF-8
Koffice 的繁体中文 (zh_TW) 语言包。


%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%patch1 -p1

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"


%build
export PATH="%{tde_bindir}:${PATH}"

export kde_htmldir="%{tde_tdedocdir}/HTML"

for l in %{TDE_LANGS}; do
  for f in koffice-i18n-${l}/; do
    if [ -d "${f}" ]; then 
      pushd ${f}
      %__sed -i "configure.in" -e "s|AM_CONFIG_HEADER|AC_CONFIG_HEADER|"
      %__make -f "admin/Makefile.common"
      %configure \
        --prefix=%{tde_prefix} \
        --datadir=%{tde_datadir} \
        --docdir=%{tde_tdedocdir}
      %__make %{?_smp_mflags}
      popd
    fi
  done
done

%install
%__rm -rf %{?buildroot}
export PATH="%{tde_bindir}:${PATH}"

for l in %{TDE_LANGS}; do
  for f in koffice-i18n-${l}/; do
    if [ -d "${f}" ] && [ -r "${f}/Makefile" ] ; then 
      %__make install DESTDIR="%{?buildroot}" -C "${f}"
    fi
  done
done

# remove zero-length file
# find "%{buildroot}%{tde_tdedocdir}/HTML" -size 0 -exec rm -f {} \;

%clean
%__rm -rf %{buildroot}

%if "%( grep -w zh_CN <<< '%{TDE_LANGS}' )" != ""
%files Chinese
%defattr(-,root,root,-)
%{tde_datadir}/locale/zh_CN/*
%endif

%if "%( grep -w zh_TW <<< '%{TDE_LANGS}' )" != ""
%files Chinese-Big5
%defattr(-,root,root,-)
%{tde_datadir}/locale/zh_TW/*
%endif


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 2:1.6.3-1.2
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:1.6.3-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:1.6.3-1
- Initial release for TDE 14.0.0

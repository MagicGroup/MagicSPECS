#
# spec file for package k3b-i18n (version R14)
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
%define tde_pkg k3b-i18n
%define tde_prefix /opt/trinity
%define tde_appdir %{tde_datadir}/applications
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


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		1.0.5
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}.1
Summary:		Internationalization support for TDE [Trinity]
Summary(zh_CN.UTF-8): K3B 的国际化支持
Group:			Applications/Archiving
Group(zh_CN.UTF-8): 应用程序/归档
URL:			http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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

BuildRequires:	gettext

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig

Requires(post): coreutils
Requires(postun): coreutils

Requires:		trinity-k3b


%description
K3b provides a comfortable user interface to perform most CD/DVD
burning tasks. While the experienced user can take influence in all
steps of the burning process the beginner may find comfort in the
automatic settings and the reasonable k3b defaults which allow a quick
start.


%package Chinese
Group:			Applications/Archiving
Group(zh_CN.UTF-8): 应用程序/归档
Requires:		trinity-k3b
Summary:		Chinese translations for K3B [Trinity]
Summary(zh_CN.UTF-8): K3B 简体中文语言包

Obsoletes:		trinity-k3b-i18n-zh_CN < %{version}-%{release}
Provides:		trinity-k3b-i18n-zh_CN = %{version}-%{release}

%description Chinese
This package contains the Chinese translations for K3B.
%description Chinese -l zh_CN.UTF-8
K3B 简体中文语言包。

%files Chinese
%defattr(-,root,root,-)
%{tde_datadir}/locale/zh_CN/LC_MESSAGES/*.mo

##########

%package Chinese-Big5
Group:			Applications/Archiving
Group(zh_CN.UTF-8): 应用程序/归档
Requires:		trinity-k3b
Summary:		Chinese-Big5 (zh_TW) translations for K3B [Trinity]
Summary(zh_CN.UTF-8): K3B  繁体中文语言包

Obsoletes:		trinity-k3b-i18n-sv < %{version}-%{release}
Provides:		trinity-k3b-i18n-sv = %{version}-%{release}

%description Chinese-Big5
This package contains the Swedish translations for K3B.

%description -l zh_CN.UTF-8
K3B  繁体中文语言包。

%files Chinese-Big5
%defattr(-,root,root,-)
%{tde_datadir}/locale/zh_TW/LC_MESSAGES/*.mo

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%patch1 -p1

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

./configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --docdir=%{tde_tdedocdir} \
  --includedir=%{tde_tdeincludedir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility

%__make %{?_smp_mflags}


%install
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

%__rm -rf %{buildroot}%{tde_docdir}/*

%__rm -rf %{buildroot}%{tde_datadir}/locale/af/
%__rm -rf %{buildroot}%{tde_datadir}/locale/ar/
%__rm -rf %{buildroot}%{tde_datadir}/locale/bg/
%__rm -rf %{buildroot}%{tde_datadir}/locale/br/
%__rm -rf %{buildroot}%{tde_datadir}/locale/bs/
%__rm -rf %{buildroot}%{tde_datadir}/locale/ca/
%__rm -rf %{buildroot}%{tde_datadir}/locale/cs/
%__rm -rf %{buildroot}%{tde_datadir}/locale/cy/
%__rm -rf %{buildroot}%{tde_datadir}/locale/da/
%__rm -rf %{buildroot}%{tde_datadir}/locale/de/
%__rm -rf %{buildroot}%{tde_datadir}/locale/el/
%__rm -rf %{buildroot}%{tde_datadir}/locale/en_GB/
%__rm -rf %{buildroot}%{tde_datadir}/locale/es/
%__rm -rf %{buildroot}%{tde_datadir}/locale/et/
%__rm -rf %{buildroot}%{tde_datadir}/locale/eu/
%__rm -rf %{buildroot}%{tde_datadir}/locale/fa/
%__rm -rf %{buildroot}%{tde_datadir}/locale/fi/
%__rm -rf %{buildroot}%{tde_datadir}/locale/fr/
%__rm -rf %{buildroot}%{tde_datadir}/locale/ga/
%__rm -rf %{buildroot}%{tde_datadir}/locale/gl/
%__rm -rf %{buildroot}%{tde_datadir}/locale/he/
%__rm -rf %{buildroot}%{tde_datadir}/locale/hi/
%__rm -rf %{buildroot}%{tde_datadir}/locale/hu/
%__rm -rf %{buildroot}%{tde_datadir}/locale/is/
%__rm -rf %{buildroot}%{tde_datadir}/locale/it/
%__rm -rf %{buildroot}%{tde_datadir}/locale/ja/
%__rm -rf %{buildroot}%{tde_datadir}/locale/ka/
%__rm -rf %{buildroot}%{tde_datadir}/locale/km/
%__rm -rf %{buildroot}%{tde_datadir}/locale/lt/
%__rm -rf %{buildroot}%{tde_datadir}/locale/mk/
%__rm -rf %{buildroot}%{tde_datadir}/locale/ms/
%__rm -rf %{buildroot}%{tde_datadir}/locale/nb/
%__rm -rf %{buildroot}%{tde_datadir}/locale/nds/
%__rm -rf %{buildroot}%{tde_datadir}/locale/ne/
%__rm -rf %{buildroot}%{tde_datadir}/locale/nl/
%__rm -rf %{buildroot}%{tde_datadir}/locale/nn/
%__rm -rf %{buildroot}%{tde_datadir}/locale/pa/
%__rm -rf %{buildroot}%{tde_datadir}/locale/pl/
%__rm -rf %{buildroot}%{tde_datadir}/locale/pt/
%__rm -rf %{buildroot}%{tde_datadir}/locale/pt_BR/
%__rm -rf %{buildroot}%{tde_datadir}/locale/ru/
%__rm -rf %{buildroot}%{tde_datadir}/locale/rw/
%__rm -rf %{buildroot}%{tde_datadir}/locale/se/
%__rm -rf %{buildroot}%{tde_datadir}/locale/sk/
%__rm -rf %{buildroot}%{tde_datadir}/locale/sr/
%__rm -rf %{buildroot}%{tde_datadir}/locale/sr@Latn/
%__rm -rf %{buildroot}%{tde_datadir}/locale/sv/
%__rm -rf %{buildroot}%{tde_datadir}/locale/ta/
%__rm -rf %{buildroot}%{tde_datadir}/locale/tr/
%__rm -rf %{buildroot}%{tde_datadir}/locale/uk/
%__rm -rf %{buildroot}%{tde_datadir}/locale/uz/
%__rm -rf %{buildroot}%{tde_datadir}/locale/uz@cyrillic/

%clean
%__rm -rf %{buildroot}


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2:1.0.5-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:1.0.5-1
- Initial release for TDE 14.0.0

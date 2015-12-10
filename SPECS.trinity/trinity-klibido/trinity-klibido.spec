#
# spec file for package klibido (version R14)
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

# Default version for this component
%define tde_pkg klibido
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif

%define tde_prefix /opt/trinity
# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

# TDE specific building variables
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_appdir %{tde_datadir}/applications

%define tde_tdeappdir %{tde_appdir}/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}

Name:			trinity-%{tde_pkg}
Summary:		A TDE usenet news grabber for Linux.
Summary(zh_CN.UTF-8): TDE 下的新闻组抓取器
Version:		0.2.5
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.3

License:		GPL
Group:			Applications/Network
Group(zh_CN.UTF-8): 应用程序/互联网

Vendor:			Trinity Project
Packager:		Francois Andriot <francois.andriot@free.fr>
URL:			http://klibido.sourceforge.net/

Prefix:			%{tde_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{tde_pkg}-%{version}.tar.gz
Patch0:		klibido-0.2.5-uulib.patch
Patch1:		%{name}-14.0.1-tqt.patch

BuildRequires:	trinity-tqtinterface-devel >= %{tde_version}
BuildRequires:	trinity-arts-devel >= 1:1.5.10
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	uulib-devel


%description
KLibido is a TDE program to download encoded articles from the usenet news
service, using the nntp protocol. It supports multiple servers, multiple
download threads per server, automatic joining and decoding of articles.

KLibido is not a NewsReader. It doesn't let you easily display the articles -
only their subject, and it discards all non-binary posts. If you want a nice
newsreader for TDE, try KNode.

%description -l zh_CN.UTF-8
TDE 下的新闻组抓取器。

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README RELEASE TODO
%{tde_bindir}/klibido
%{tde_datadir}/applnk/Utilities/klibido.desktop
%{tde_datadir}/apps/klibido/
%{tde_datadir}/doc/tde/HTML/en/klibido/
%{tde_datadir}/icons/hicolor/*/apps/klibido.png

##########

%prep
%setup -q -n %{tde_pkg}-%{version}
%patch0 -p1
%patch1 -p1

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

if [ -r /usr/include/db53/db_cxx.h ]; then
  EXTRA_INCLUDES="/usr/include/db53"
fi

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-final \
  --enable-new-ldflags \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility \
  \
  --with-extra-includes=%{_includedir}/uulib:${EXTRA_INCLUDES}

%__make %{?_smp_mflags} || %__make


%install
%__rm -rf $RPM_BUILD_ROOT
%__make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 0.2.5-1.opt.3
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.2.5-1.opt.2
- 为 Magic 3.0 重建

* Sun Oct 11 2015 Liu Di <liudidi@gmail.com> - 0.2.5-1.opt.1
- 为 Magic 3.0 重建

* Mon Dec 30 2013 François Andriot <francois.andriot@free.fr> - 0.25-1
- Initial release

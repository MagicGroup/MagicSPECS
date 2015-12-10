#
# spec file for package klamav (version R14)
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
%define tde_pkg klamav
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
Summary:        Frontend for clamav
Summary(zh_CN.UTF-8): clamav 的图形前端
Version:		0.46
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.3

License:		GPLv2+
Group:			Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具

Vendor:			Trinity Project
Packager:		Francois Andriot <francois.andriot@free.fr>
#URL:			http://www.trinitydesktop.org/
Url:            http://klamav.sourceforge.net/

Prefix:			%{_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{tde_pkg}-14.0.0.tar.gz

Patch1:		%{name}-14.0.1-tqt.patch

BuildRequires:	trinity-tqtinterface-devel >= %{tde_version}
BuildRequires:	trinity-arts-devel >= 1:1.5.10
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	gettext
BuildRequires:	curl-devel
BuildRequires:	gmp-devel
BuildRequires:	sqlite-devel
#BuildRequires:	unsermake
BuildRequires:  fdupes

BuildRequires:  clamav
Requires:		clamav

BuildRequires:  clamav-devel


%description
A TDE front-end for the Clam AntiVirus antivirus toolkit.

%description -l zh_CN.UTF-8
杀毒软件 clamav 的图形前端。

%prep
%setup -q -n %{tde_pkg}-%{version}
%patch1 -p1

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

# Warning: --enable-final causes FTBFS
%configure \
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
  --disable-gcc-hidden-visibility \
  \
  --without-included-sqlite \
  --with-extra-includes=%{_includedir}/tqt

find . -name "*.cpp" | while read f; do
  mf="${f%.cpp}.moc"
  if grep -qw "${mf##*/}" "${f}" && [ ! -f "${mf}" ]; then
    tqmoc "${f%.cpp}.h" -o "${mf}"
  fi
done

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}
magic_rpm_clean.sh
%find_lang %{tde_pkg} || :


%clean
%__rm -rf %{buildroot}
	

%post
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
/sbin/ldconfig


%postun
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
/sbin/ldconfig


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%{tde_bindir}/ScanWithKlamAV
%{tde_bindir}/klamarkollon
%{tde_bindir}/klamav
%{tde_bindir}/klammail
%{tde_tdeappdir}/klamav.desktop
%{tde_datadir}/apps/klamav/
%{tde_datadir}/apps/konqueror/servicemenus/klamav-dropdown.desktop
%{tde_datadir}/config.kcfg/klamavconfig.kcfg
%{tde_tdedocdir}/HTML/en/klamav02/
%{tde_datadir}/icons/hicolor/32x32/apps/klamav.png
%{tde_datadir}/icons/hicolor/48x48/apps/klamav.png


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 0.46-1.opt.3
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.46-1.opt.2
- 为 Magic 3.0 重建

* Sun Oct 11 2015 Liu Di <liudidi@gmail.com> - 0.46-1.opt.1
- 为 Magic 3.0 重建

* Sat Sep 20 2014 Francois Andriot <francois.andriot@free.fr> - 0.46-1
- Initial release for TDE 14.0.0

#
# spec file for package tdeio-umountwrapper (version R14)
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
%define tde_pkg tdeio-umountwrapper
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


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.2
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}.2
Summary:	Progress dialog for safely removing devices in Trinity
Summary(zh_CN.UTF-8): TDE 下安全移除设备的进度对话框
Group:		Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具
URL:		http://frode.kde.no/misc/tdeio_umountwrapper/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz
Source1:		media_safelyremove.desktop_tdeio

Patch1:		%{name}-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

Obsoletes:		trinity-kio-umountwrapper < %{version}-%{release}
Provides:		trinity-kio-umountwrapper = %{version}-%{release}

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	fdupes


%description
Wrapper around tdeio_media_mountwrapper.
Provides a progress dialog for Safely Removing of devices in Trinity.

%description -l zh_CN.UTF-8
TDE 下安全移除设备的进度对话框.

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%patch1 -p1

%__cp "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-final \
  --enable-new-ldflags \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

%__install -D -m 644 "%{SOURCE1}" %{?buildroot}%{tde_datadir}/apps/konqueror/servicemenus/media_safelyremove.desktop_tdeio-umountwrapper
%__install -D -m 644 "%{SOURCE1}" %{?buildroot}%{tde_datadir}/apps/d3lphin/servicemenus/media_safelyremove.desktop_tdeio-umountwrapper


%clean
%__rm -rf %{buildroot}

%post
for f in konqueror d3lphin; do
  update-alternatives --install \
    %{tde_datadir}/apps/${f}/servicemenus/media_safelyremove.desktop \
    media_safelyremove.desktop_${f} \
    %{tde_datadir}/apps/${f}/servicemenus/media_safelyremove.desktop_tdeio-umountwrapper \
    20
done

%postun
if [ $1 -eq 0 ]; then
  for f in konqueror d3lphin; do
    update-alternatives --remove \
      media_safelyremove.desktop_${f} \
      %{tde_datadir}/apps/${f}/servicemenus/media_safelyremove.desktop_tdeio-umountwrapper || :
  done
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{tde_bindir}/tdeio_umountwrapper
%{tde_datadir}/apps/konqueror/servicemenus/media_safelyremove.desktop_tdeio-umountwrapper
%dir %{tde_datadir}/apps/d3lphin
%dir %{tde_datadir}/apps/d3lphin/servicemenus
%{tde_datadir}/apps/d3lphin/servicemenus/media_safelyremove.desktop_tdeio-umountwrapper


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 2:0.2-1.2
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:0.2-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.2-1
- Initial release for TDE 14.0.0

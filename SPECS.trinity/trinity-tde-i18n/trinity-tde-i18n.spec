#
# spec file for package tde-i18n (version R14)
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
%define tde_pkg tde-i18n
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


Name:			trinity-%{tde_pkg}
Version:		%{tde_version}
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}.1
Summary:		Internationalization support for Trinity
Summary(zh_CN.UTF-8):   Trinity 的国际化支持
Group:			User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
URL:			http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{tde_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:		noarch

# Speed build options
%define debug_package %{nil}
%define __spec_install_post %{nil}
AutoReq: no

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}

BuildRequires:	findutils
BuildRequires:	gettext
BuildRequires:	cmake
BuildRequires:	gcc-c++

%description
This package contains %{summary}.

##########

%package Chinese
Summary:		Chinese(zh_CN) (Simplified Chinese) language support for TDE
Summary(zh_CN.UTF-8): TDE 的简体中文语言包
Group:			User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Provides:		%{name}-zh_CN = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Chinese < %{version}-%{release}
Provides:		trinity-kde-i18n-Chinese = %{version}-%{release}

%description Chinese
This package contains %{summary}.

%description Chinese -l zh_CN.UTF-8
TDE 的简单中文语言包。

%files Chinese
%defattr(-,root,root,-)
%{tde_datadir}/locale/zh_CN/
%{tde_tdedocdir}/HTML/zh_CN/

##########

%package Chinese-Big5
Summary:		Chinese(zh_TW) (Big5) language support for TDE
Summary(zh_CN.UTF-8): TDE 的繁体中文语言包
Group:			User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Provides:		%{name}-tz_TW = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Chinese-Big5 < %{version}-%{release}
Provides:		trinity-kde-i18n-Chinese-Big5 = %{version}-%{release}

%description Chinese-Big5
This package contains %{summary}.

%description Chinese-Big5 -l zh_CN.UTF-8
TDE 的繁体中文语言包。

%files Chinese-Big5
%defattr(-,root,root,-)
%{tde_datadir}/locale/zh_TW/
%{tde_tdedocdir}/HTML/zh_TW/

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

(
for l in %{TDE_LANGS}; do
  for f in tde-i18n-${l}/; do
    if [ -d "${f}" ]; then 
      pushd ${f}
      if ! rpm -E %%cmake|grep -q "cd build"; then
        %__mkdir_p build
        cd build
      fi
      
      %cmake \
        -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
        -DCMAKE_VERBOSE_MAKEFILE=ON \
        \
        -DCMAKE_INSTALL_PREFIX="%{tde_prefix}" \
        -DBIN_INSTALL_DIR="%{tde_bindir}" \
        -DINCLUDE_INSTALL_DIR="%{tde_tdeincludedir}" \
        -DLIB_INSTALL_DIR="%{tde_libdir}" \
        -DPKGCONFIG_INSTALL_DIR="%{tde_libdir}/pkgconfig" \
        -DSHARE_INSTALL_PREFIX="%{tde_datadir}" \
        \
        -DBUILD_ALL=ON \
        -DBUILD_DOC=ON \
        -DBUILD_DATA=ON \
        -DBUILD_MESSAGES=ON \
      ..

      # Run the build process in background
      ( %__make -j4 || %__make || echo TDE_Error ) &
      
      # Do not build more than 4 languages at the same time
      while [ $(jobs | wc -l) -ge 4 ]; do sleep 3; done
      popd
    fi
  done
done
) 2>&1 | tee /tmp/rpmbuild.$$

if grep -qw TDE_Error /tmp/rpmbuild.$$; then
  echo "Error while building. See '/tmp/rpmbuild.$$'"
  exit 1
fi

wait
rm -f /tmp/rpmbuild.$$


%install
%__rm -rf %{?buildroot}
export PATH="%{tde_bindir}:${PATH}"

for l in %{TDE_LANGS}; do
  for f in tde-i18n-${l}/; do
    %__make install DESTDIR="%{?buildroot}" -C "${f}/build"
  done
done


# remove zero-length file
find "%{buildroot}%{tde_tdedocdir}/HTML" -size 0 -exec rm -f {} \;

# remove obsolete KDE 3 application data translations
%__rm -rf "%{buildroot}%{tde_datadir}/apps"


%clean
%__rm -rf %{buildroot}


%changelog
* Thu Oct 08 2015 Liu Di <liudidi@gmail.com> - 14.0.0-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 14.0.0-1
- Initial release for TDE 14.0.0

# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?_prefix}" != "/usr"
%define _variant .opt
%endif

%define tdeversion 3.5.13.2

# TDE 3.5.13 specific building variables
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_appdir %{tde_datadir}/applications

%define tde_tdeappdir %{tde_appdir}/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}


Name:		trinity-k3b-i18n
Summary:	Locale files for K3B
Version:	1.0.5
Release:	3%{?dist}%{?_variant}

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

BuildArch:	noarch

# Speed build options
%define debug_package %{nil}
%define __spec_install_post %{nil}
AutoReq: no

Prefix:    %{_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Group:   Applications/Archiving
License: GPLv2+

Source0: k3b-i18n-trinity-%{tdeversion}.tar.xz

BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

Requires(post): coreutils
Requires(postun): coreutils

Requires:	trinity-k3b


%description
K3b provides a comfortable user interface to perform most CD/DVD
burning tasks. While the experienced user can take influence in all
steps of the burning process the beginner may find comfort in the
automatic settings and the reasonable k3b defaults which allow a quick
start.

%package zh_CN
Group:   Applications/Archiving
Requires: trinity-k3b
Summary: Chinese (zh_CN) translations for K3B [Trinity]
%description zh_CN
This package contains the Swedish translations for K3B.

%package zh_TW
Group:   Applications/Archiving
Requires: trinity-k3b
Summary: Chinses (zh_TW) translations for K3B [Trinity]
%description zh_TW
This package contains the Ukrainian translations for K3B.


%prep
%setup -q -n k3b-i18n-trinity-%{tdeversion}


# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i "admin/acinclude.m4.in" \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR || : ; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"

./configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --docdir=%{tde_tdedocdir} \
  --includedir=%{tde_tdeincludedir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  --disable-rpath \
  --with-extra-includes=%{tde_includedir}/tqt \
  --enable-closure

%__make %{?_smp_mflags}

%install
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

%__rm -rf %{buildroot}%{tde_datadir}/locale/[a-y]*
%__rm -rf %{buildroot}%{tde_docdir}/tde/*

%clean
%__rm -rf %{buildroot}


%files zh_CN
%defattr(-,root,root,-)
%lang(zh_CN) %{tde_datadir}/locale/zh_CN/LC_MESSAGES/*.mo

%files zh_TW
%defattr(-,root,root,-)
%lang(zh_TW) %{tde_datadir}/locale/zh_TW/LC_MESSAGES/*.mo



%changelog
* Wed Jul 31 2013 Liu Di <liudidi@gmail.com> - 1.0.5-3
- 为 Magic 3.0 重建

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 1.0.5-2
- Initial build for TDE 3.5.13.1

* Thu May 10 2012 Francois Andriot <francois.andriot@free.fr> - 1.0.5-1
- Initial build for TDE 3.5.13

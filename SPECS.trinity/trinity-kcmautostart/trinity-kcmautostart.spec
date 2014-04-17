# Default version for this component
%define kdecomp kchmviewer

# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

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


Name:		trinity-kcmautostart
Summary:	Manage applications automatic startup.
Version:	1.0
Release:	2%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:    %{_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	kcmautostart-3.5.13.tar.gz

# [kcmautostart] Fix FTBFS with TDE 3.5.13
Patch1:		kcmautostart-3.5.13-ftbfs.patch
# [kcmautostart] Add French support
Patch2:		kcmautostart-3.5.13-add_french.patch

BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires:	trinity-arts-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-tdebase-devel >= 3.5.13.1
BuildRequires: desktop-file-utils
BuildRequires: gcc-c++

Requires:		trinity-kdebase

%description
%{summary}

%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -a 0 -n applications/kcmautostart
%patch1 -p1
%patch2 -p1

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i admin/acinclude.m4.in \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR || : ; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --libdir=%{tde_libdir} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  --disable-rpath \
  --with-extra-includes=%{tde_includedir}/tqt \
  --disable-static

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

%find_lang autostart

%clean
%__rm -rf %{buildroot}


%files -f autostart.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README TODO
%{tde_tdelibdir}/kcm_autostart.la
%{tde_tdelibdir}/kcm_autostart.so
%{tde_tdeappdir}/autostart.desktop
%{tde_tdedocdir}/HTML/en/autostart/


%changelog
* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 1.0-2
- Initial build for TDE 3.5.13.1

* Thu May 10 2012 Francois Andriot <francois.andriot@free.fr> - 1.0-1
- Initial build for TDE 3.5.13

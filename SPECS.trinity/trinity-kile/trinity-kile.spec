# Default version for this component
%define kdecomp kile
%define tdeversion 3.5.13.2

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


Name:		trinity-%{kdecomp}
Summary:	KDE Integrated LaTeX Environment [Trinity]
Version:	2.0.2
Release:	5%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Publishing

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:    %{tde_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{kdecomp}-trinity-%{tdeversion}.tar.xz

BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-tdebase-devel >= 3.5.13.1
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

Obsoletes: %{name}-i18n-ar
Obsoletes: %{name}-i18n-bg
Obsoletes: %{name}-i18n-br
Obsoletes: %{name}-i18n-ca
Obsoletes: %{name}-i18n-cs
Obsoletes: %{name}-i18n-cy
Obsoletes: %{name}-i18n-da
Obsoletes: %{name}-i18n-de
Obsoletes: %{name}-i18n-el
Obsoletes: %{name}-i18n-engb
Obsoletes: %{name}-i18n-es
Obsoletes: %{name}-i18n-et
Obsoletes: %{name}-i18n-eu
Obsoletes: %{name}-i18n-fi
Obsoletes: %{name}-i18n-fr
Obsoletes: %{name}-i18n-ga
Obsoletes: %{name}-i18n-gl
Obsoletes: %{name}-i18n-hi
Obsoletes: %{name}-i18n-hu
Obsoletes: %{name}-i18n-is
Obsoletes: %{name}-i18n-it
Obsoletes: %{name}-i18n-ja
Obsoletes: %{name}-i18n-lt
Obsoletes: %{name}-i18n-ms
Obsoletes: %{name}-i18n-mt
Obsoletes: %{name}-i18n-nb
Obsoletes: %{name}-i18n-nds
Obsoletes: %{name}-i18n-nl
Obsoletes: %{name}-i18n-nn
Obsoletes: %{name}-i18n-pa
Obsoletes: %{name}-i18n-pl
Obsoletes: %{name}-i18n-pt
Obsoletes: %{name}-i18n-ptbr
Obsoletes: %{name}-i18n-ro
Obsoletes: %{name}-i18n-ru
Obsoletes: %{name}-i18n-rw
Obsoletes: %{name}-i18n-sk
Obsoletes: %{name}-i18n-sr
Obsoletes: %{name}-i18n-srlatin
Obsoletes: %{name}-i18n-sv
Obsoletes: %{name}-i18n-ta
Obsoletes: %{name}-i18n-th
Obsoletes: %{name}-i18n-tr
Obsoletes: %{name}-i18n-uk
Obsoletes: %{name}-i18n-zhcn


%description
Kile is a user-friendly LaTeX source editor and TeX shell for TDE.

The source editor is a multi-document editor designed for .tex and .bib
files.  Menus, wizards and auto-completion are provided to assist with
tag insertion and code generation.  A structural view of the document
assists with navigation within source files.

The TeX shell integrates the various tools required for TeX processing.
It assists with LaTeX compilation, DVI and postscript document viewing,
generation of bibliographies and indices and other common tasks.

Kile can support large projects consisting of several smaller files.

%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n %{kdecomp}-trinity-%{tdeversion}

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i admin/acinclude.m4.in \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  --disable-rpath \
  --with-extra-includes=%{tde_includedir}/tqt

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

%__chmod +x %{buildroot}%{tde_datadir}/apps/kile/test/runTests.sh

# Unwanted files ...
%__rm -f %{?buildroot}%{tde_datadir}/apps/katepart/syntax/bibtex.xml
%__rm -f %{?buildroot}%{tde_datadir}/apps/katepart/syntax/latex.xml

%find_lang %{kdecomp}

%clean
%__rm -rf %{buildroot}


%post
update-desktop-database %{tde_appdir} > /dev/null
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :

%postun
update-desktop-database %{tde_appdir} > /dev/null
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :


%files -f %{kdecomp}.lang
%defattr(-,root,root,-)
%{tde_bindir}/kile
%{tde_tdeappdir}/kile.desktop
%{tde_datadir}/apps/kconf_update
%{tde_datadir}/apps/kile
%{tde_datadir}/config.kcfg/kile.kcfg
%{tde_datadir}/icons/hicolor/*/apps/kile.png
%{tde_datadir}/icons/hicolor/scalable/apps/kile.svgz
%{tde_tdedocdir}/HTML/en/kile
%{tde_datadir}/mimelnk/text/x-kilepr.desktop

%lang(da) %{tde_tdedocdir}/HTML/da/kile/
%lang(es) %{tde_tdedocdir}/HTML/es/kile/
%lang(et) %{tde_tdedocdir}/HTML/et/kile/
%lang(it) %{tde_tdedocdir}/HTML/it/kile/
%lang(nl) %{tde_tdedocdir}/HTML/nl/kile/
%lang(pt) %{tde_tdedocdir}/HTML/pt/kile/
%lang(sv) %{tde_tdedocdir}/HTML/sv/kile/



%changelog
* Fri Aug 02 2013 Liu Di <liudidi@gmail.com> - 2.0.2-5.opt
- 为 Magic 3.0 重建

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 2.0.2-4
- Initial build for TDE 3.5.13.1

* Tue May 01 2012 Francois Andriot <francois.andriot@free.fr> - 2.0.2-3
- Rebuilt for Fedora 17
- Removes the XPM icon

* Fri Apr 20 2012 Francois Andriot <francois.andriot@free.fr> - 2.0.2-2
- Fix file conflict with trinity-kdelibs

* Fri Nov 25 2011 Francois Andriot <francois.andriot@free.fr> - 2.0.2-1
- Initial build for RHEL 5, RHEL 6, Fedora 15, Fedora 16

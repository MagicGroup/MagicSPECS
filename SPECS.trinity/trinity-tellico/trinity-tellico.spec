# Default version for this component
%define kdecomp tellico
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

%define _docdir %{tde_tdedocdir}


Name:		trinity-%{kdecomp}
Summary:	Icollection manager for books, videos, music [Trinity]
Version:	1.3.2.1
Release:	5%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://periapsis.org/tellico/

Prefix:    %{tde_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{kdecomp}-trinity-%{tdeversion}.tar.xz


# [tellico] Fix "not a string literal" error
Patch2:		tellico-3.5.13-fix_not_a_string_literal_error.patch
# [tellico] Fix FTBFS
Patch3:		tellico-3.5.13.1-fix_ftbfs.patch


BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-tdebase-devel >= 3.5.13.1
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

Requires:	%{name}-data = %{version}-%{release}
Requires:	%{name}-scripts = %{version}-%{release}

%description
Tellico is a collection manager for TDE. It includes default collections for
books, bibliographies, comic books, videos, music, coins, stamps, trading
cards, and wines, and also allows custom collections; with unlimited
user-defined fields allowed. Automatically formatted names, sorting by any
property, filters, automatic ISBN validation and full customization for
printing or display through XSLT files are some of the features present. It
can import CSV, RIS, BibTeX, and BibTeXML files; and export CSV, HTML, BibTeX,
BibTeXML, and PilotDB. Tellico can also import data from Amazon, IMDb, CDDB,
or any US-MARC compliant z39.50 server.

The files are stored in XML format, avoiding the need for database server.
It also makes it easy for other softwares to use the Tellico data.


%package data
Group:		Applications/Utilities
Summary:	collection manager for books, videos, music [data] [Trinity]

%description data
Tellico is a collection manager for TDE. It includes default collections for
books, bibliographies, comic books, videos, music, coins, stamps, trading
cards, and wines, and also allows custom collections; with unlimited
user-defined fields allowed. Automatically formatted names, sorting by any
property, filters, automatic ISBN validation and full customization for
printing or display through XSLT files are some of the features present. It
can import CSV, RIS, BibTeX, and BibTeXML files; and export CSV, HTML, BibTeX,
BibTeXML, and PilotDB. Tellico can also import data from Amazon, IMDb, CDDB,
or any US-MARC compliant z39.50 server.

The files are stored in XML format, avoiding the need for database server.
It also makes it easy for other softwares to use the Tellico data.

This package contains the architecture independent files, such data files and
documentation.

%package scripts
Group:		Applications/Utilities
Summary:	collection manager for books, videos, music [scripts] [Trinity]

%description scripts
Tellico is a collection manager for TDE. It includes default collections for
books, bibliographies, comic books, videos, music, coins, stamps, trading
cards, and wines, and also allows custom collections; with unlimited
user-defined fields allowed. Automatically formatted names, sorting by any
property, filters, automatic ISBN validation and full customization for
printing or display through XSLT files are some of the features present. It
can import CSV, RIS, BibTeX, and BibTeXML files; and export CSV, HTML, BibTeX,
BibTeXML, and PilotDB. Tellico can also import data from Amazon, IMDb, CDDB,
or any US-MARC compliant z39.50 server.

The files are stored in XML format, avoiding the need for database server.
It also makes it easy for other softwares to use the Tellico data.

This package contains the scripts to import data from external sources, such
as websites. As the format of the data may change, these scripts are provided
as a separate package which can be updated through debian-volatile.


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
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  --includedir=%{tde_tdeincludedir} \
  --disable-rpath \
  --with-extra-includes=%{tde_includedir}/tqt

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

# Add svg icons to xdg directories
%__install -D -c -p -m 644 -T icons/tellico.svg %{?buildroot}%{tde_datadir}/icons/hicolor/scalable/apps/tellico.svg
%__install -D -c -p -m 644 -T icons/tellico_mime.svg %{?buildroot}%{tde_datadir}/icons/hicolor/scalable/mimetypes/application-x-tellico.svg

# Remove  dead symlink from French translation
%__rm %{?buildroot}%{tde_tdedocdir}/HTML/fr/tellico/common


%find_lang %{kdecomp}


%clean
%__rm -rf %{buildroot}


%post
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :

%postun
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :


%files -f %{kdecomp}.lang
%defattr(-,root,root,-)
%{tde_bindir}/tellico
#%{tde_datadir}/pixmaps
%{tde_datadir}/applications
%{tde_datadir}/config/tellicorc

%files data
%defattr(-,root,root,-)
%{tde_datadir}/apps/tellico/*.xsl
%{tde_datadir}/apps/tellico/*.xml
%{tde_datadir}/apps/tellico/*.png
%{tde_datadir}/apps/tellico/entry-templates
%{tde_datadir}/apps/tellico/*.py*
%{tde_datadir}/apps/tellico/pics
%{tde_datadir}/apps/tellico/report-templates
%{tde_datadir}/apps/tellico/tellico.dtd
%{tde_datadir}/apps/tellico/tellico.tips
%{tde_datadir}/apps/tellico/tellico2html.js
%{tde_datadir}/apps/tellico/tellicoui.rc
%{tde_datadir}/apps/tellico/welcome.html
%{tde_datadir}/config.kcfg
%{tde_tdedocdir}/HTML/*/tellico/
%{tde_datadir}/icons
%{tde_datadir}/apps/mime
%{tde_datadir}/mimelnk
%{tde_datadir}/apps/kconf_update/tellico-1-3-update.pl
%{tde_datadir}/apps/kconf_update/tellico-rename.upd
%{tde_datadir}/apps/kconf_update/tellico.upd

%files scripts
%defattr(-,root,root,-)
%{tde_datadir}/apps/tellico/data-sources
%{tde_datadir}/apps/tellico/z3950-servers.cfg


%changelog
* Tue Aug 06 2013 Liu Di <liudidi@gmail.com> - 1.3.2.1-5.opt
- 为 Magic 3.0 重建

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 1.3.2.1-4
- Initial build for TDE 3.5.13.1

* Sat Dec 03 2011 Francois Andriot <francois.andriot@free.fr> - 1.3.2.1-3
- Fix compilation with GCC 4.7 [Bug #958]

* Fri Nov 25 2011 Francois Andriot <francois.andriot@free.fr> - 1.3.2.1-2
- Fix HTML directory location

* Thu Nov 24 2011 Francois Andriot <francois.andriot@free.fr> - 1.3.2.1-1
- Initial build for RHEL 5, RHEL 6, Fedora 15, Fedora 16

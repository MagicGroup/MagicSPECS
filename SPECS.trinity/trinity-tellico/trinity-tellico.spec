#
# spec file for package tellico (version R14)
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
%define tde_pkg tellico
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_confdir %{_sysconfdir}/trinity
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
Version:	1.3.2.1
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}.2
Summary:	Icollection manager for books, videos, music [Trinity]
Summary(zh_CN.UTF-8): 书箱、视频、音乐的管理工具
Group:		Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具
URL:		http://periapsis.org/tellico/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

Patch1:		%{name}-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	fdupes

# XML2 support
BuildRequires:  libxml2-devel

# XSLT support
BuildRequires:  libxslt-devel

# V4L support
BuildRequires:	libv4l-devel

Requires:		%{name}-data = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		%{name}-scripts = %{?epoch:%{epoch}:}%{version}-%{release}


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

%description -l zh_CN.UTF-8
书箱、视频、音乐的管理工具。

%post
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :

%postun
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :

%files 
%defattr(-,root,root,-)
%{tde_bindir}/tellico
#%{tde_datadir}/pixmaps
%{tde_datadir}/applications
%{tde_confdir}/tellicorc

##########

%package data
Group:			Applications/Utilities
Group(zh_CN.UTF-8): 	应用程序/工具
Summary:		collection manager for books, videos, music [data] [Trinity]
Summary(zh_CN.UTF-8):   %{name} 的数据文件。

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

%description data -l zh_CN.UTF-8
%{name} 的数据文件。

%files data
%defattr(-,root,root,-)
%dir %{tde_datadir}/apps/tellico
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
%{tde_datadir}/apps/tdeconf_update/tellico-1-3-update.pl
%{tde_datadir}/apps/tdeconf_update/tellico-rename.upd
%{tde_datadir}/apps/tdeconf_update/tellico.upd

##########

%package scripts
Group:			Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具
Summary:		collection manager for books, videos, music [scripts] [Trinity]
Summary(zh_CN.UTF-8): %{name} 的脚本

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

%description scripts -l zh_CN.UTF-8
%{name} 的脚本。

%files scripts
%defattr(-,root,root,-)
%{tde_datadir}/apps/tellico/data-sources
%{tde_datadir}/apps/tellico/z3950-servers.cfg

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%patch1 -p1

if [ -r /usr/include/libv4l1-videodev.h ]; then
%__sed -i "src/barcode/barcode_v4l.h" -e "s|linux/videodev.h|libv4l1.h|"
fi

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export kde_confdir="%{tde_confdir}"

# Warning, --enable-final causes FTBFS !
%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  --includedir=%{tde_tdeincludedir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --disable-final \
  --enable-new-ldflags \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility \
  \
  --enable-webcam

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

# Add svg icons to xdg directories
%__install -D -c -p -m 644 icons/tellico.svg %{?buildroot}%{tde_datadir}/icons/hicolor/scalable/apps/tellico.svg
%__install -D -c -p -m 644 icons/tellico_mime.svg %{?buildroot}%{tde_datadir}/icons/hicolor/scalable/mimetypes/application-x-tellico.svg
magic_rpm_clean.sh
%find_lang %{tde_pkg} || :


%clean
%__rm -rf %{buildroot}


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 2:1.3.2.1-1.2
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:1.3.2.1-1.1
- 为 Magic 3.0 重建

* Mon Jul 29 2013 Francois Andriot <francois.andriot@free.fr> - 2:1.3.2.1-1
- Initial release for TDE 14.0.0

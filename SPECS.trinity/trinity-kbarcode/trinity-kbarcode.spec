#
# spec file for package kbarcode (version R14)
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
%define tde_pkg kbarcode
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
Version:		2.0.7
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.1
Summary:		barcode and label printing application for Trinity
Summary(zh_CN.UTF-8): TDE 下的条码和标签打印程序
Group:			Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具
URL:			http://www.kbarcode.net

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

Patch1:			%{name}-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	gettext

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig

# PCRE support
BuildRequires:	pcre-devel

Requires:		%{name}-tdefile-plugin = %{?epoch:%{epoch}:}%{version}-%{release}


%description
KBarcode is a barcode and label printing application for Trinity. It can be used
to print everything from simple business cards up to complex labels with
several barcodes (e.g. article descriptions).

KBarcode comes with an easy to use WYSIWYG label designer, a setup wizard,
batch import of data for batch printing labels (directly from the delivery
note), thousands of predefined labels, database management tools and
translations in many languages. Even printing more than 10.000 labels in one
go is no problem for KBarcode. Data for printing can be imported from several
different data sources, including SQL databases, CSV files and the TDE address
book.

Additionally it is a simple barcode generator (similar to the old xbarcode you
might know). All major types of barcodes like EAN, UPC, CODE39 and ISBN are
supported. Even complex 2D barcodes are supported using third party tools. The
generated barcodes can be directly printed or you can export them into images
to use them in another application.

%description -l zh_CN.UTF-8
TDE 下的条码和标签打印程序。

%post
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
update-desktop-database %{tde_appdir} &> /dev/null

%postun
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
update-desktop-database %{tde_appdir} &> /dev/null

%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{tde_bindir}/kbarcode
%{tde_tdeappdir}/kbarcode-batch.desktop
%{tde_tdeappdir}/kbarcode-editor.desktop
%{tde_tdeappdir}/kbarcode-single.desktop
%{tde_tdeappdir}/kbarcode.desktop
%{tde_datadir}/mimelnk/application/kbarcode-label.desktop
%{tde_datadir}/apps/kbarcode/
%{tde_datadir}/icons/hicolor/*/actions/barcode.png
%{tde_datadir}/icons/hicolor/*/actions/kbarcodeellipse.png
%{tde_datadir}/icons/hicolor/*/actions/kbarcodegrid.png
%{tde_datadir}/icons/hicolor/*/actions/kbarcodelinetool.png
%{tde_datadir}/icons/hicolor/*/actions/kbarcoderect.png
%{tde_datadir}/icons/hicolor/*/apps/kbarcode.png
%{tde_tdedocdir}/HTML/en/kbarcode/

##########

%package tdefile-plugin
Summary:		tdefile-plugin for %{name}
Summary(zh_CN.UTF-8): %{name} 的 tdefile 插件
Group:			Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具
#Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description tdefile-plugin
%{summary}.
%description tdefile-plugin -l zh_CN.UTF-8
%{name} 的 tdefile 插件。

%files tdefile-plugin
%defattr(-,root,root,-)
%{tde_tdelibdir}/tdefile_kbarcode.la
%{tde_tdelibdir}/tdefile_kbarcode.so
%{tde_datadir}/services/tdefile_kbarcode.desktop

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
  --libdir=%{tde_libdir} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility \
  \
  --with-extra-includes=%{_includedir}/pcre

# SMP safe !
%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

%find_lang %{tde_pkg}

# Fix invalid icon path
%__sed -i "%{buildroot}%{tde_tdeappdir}/kbarcode.desktop" -e "s|Icon=.*|Icon=kbarcode|"

# Updates applications categories for openSUSE
%if 0%{?suse_version}
%suse_update_desktop_file -r kbarcode        Utility PrintingUtility
%suse_update_desktop_file -r kbarcode-batch  Utility PrintingUtility
%suse_update_desktop_file -r kbarcode-editor Utility PrintingUtility
%suse_update_desktop_file -r kbarcode-single Utility PrintingUtility
%endif


%clean
%__rm -rf %{buildroot}


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2:2.0.7-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:2.0.7-1
- Initial release for TDE 14.0.0

# Default version for this component
%define kdecomp kchmviewer
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
Summary:	CHM viewer for Trinity
Version:	3.1.2
Release:	4%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:    %{_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{kdecomp}-trinity-%{tdeversion}.tar.xz

# [kchmviewer] Missing LDFLAGS cause FTBFS on Mageia 2 / Mandriva 2011
Patch0:		kchmviewer-3.5.13-missing_ldflags.patch

BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-tdebase-devel >= 3.5.13.1
BuildRequires: desktop-file-utils

%description
KchmViewer is a chm (MS HTML help file format) viewer, written in C++.
Unlike most existing CHM viewers for Unix, it uses Trolltech Qt widget
library, and does not depend on KDE or GNOME. However, it may be compiled
with full Trinity support, including Trinity widgets and KIO/KHTML. 

The main advantage of KchmViewer is non-English language support. Unlike
others, KchmViewer in most cases correctly detects help file encoding,
correctly shows tables of context of Russian, Korean, Chinese and Japanese
help files, and correctly searches in non-English help files (search for
MBCS languages - ja/ko/ch is still in progress).

Completely safe and harmless. Does not support JavaScript in any way,
optionally warns you before opening an external web page, or switching to
another help file. Shows an appropriate image for every TOC entry. 

KchmViewer Has complete chm index support, including multiple index entries,
cross-links and parent/child entries in index as well as Persistent bookmarks
support. Correctly detects and shows encoding of any valid chm file.


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

%__cp "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR || : ; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{_includedir}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --libdir=%{tde_libdir} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  --disable-rpath \
  --with-x \
  --with-kde \
  --with-extra-includes=%{_includedir}/tqt \
  --enable-closure


%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

%find_lang %{kdecomp}

# Removes useless files
%__rm -f %{?buildroot}%{tde_libdir}/*.a

%clean
%__rm -rf %{buildroot}


%post
touch --no-create %{tde_datadir}/icons/crystalsvg || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/crystalsvg || :

%postun
touch --no-create %{tde_datadir}/icons/crystalsvg || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/crystalsvg || :


%files -f %{kdecomp}.lang
%defattr(-,root,root,-)
%doc ChangeLog COPYING FAQ README
%{tde_bindir}/kchmviewer
%{tde_tdelibdir}/kio_msits.la
%{tde_tdelibdir}/kio_msits.so
%{tde_datadir}/applnk/kchmviewer.desktop
%{tde_datadir}/icons/crystalsvg/*/apps/kchmviewer.png
%{tde_datadir}/services/msits.protocol


%changelog
* Wed Jul 31 2013 Liu Di <liudidi@gmail.com> - 3.1.2-4.opt
- 为 Magic 3.0 重建

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 3.1.2-3
- Initial build for TDE 3.5.13.1

* Tue May 01 2012 Francois Andriot <francois.andriot@free.fr> - 3.1.2-2
- Rebuilt for Fedora 17
- Fix post and postun
- Fix HTML directory location

* Sat Nov 19 2011 Francois Andriot <francois.andriot@free.fr> - 3.1.2-1
- Initial build for RHEL 5, RHEL 6, Fedora 15, Fedora 16

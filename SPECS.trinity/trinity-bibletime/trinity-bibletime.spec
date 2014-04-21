# Default version for this component
%define kdecomp bibletime
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

%define tde_tdeappdir %{tde_datadir}/applications/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}


Name:		trinity-%{kdecomp}
Summary:	A bible study tool for Trinity
Version:	1.6.6.0
Release:	3%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org

Prefix:    %{_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{kdecomp}-trinity-%{tdeversion}.tar.xz

# Fix detection of older versions of clucene in Fedora >= 16
Patch0:		bibletime-3.5.13-clucene_detection.patch
# [bibletime] Fix FTBFS on Mageia 2, error at linking with 'sword'
Patch2:		bibletime-3.5.13-fix_sword_linking.patch

BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-tdebase-devel >= 3.5.13.1
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

# Bibletime only works with clucene 0.9 ! Mageia 2 does not ship with that old version !
%if 0%{?fedora} >= 16 || 0%{?suse_version}
#BuildRequires:	clucene09-core-devel
%else
%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	clucene-devel < 1.0
%else
BuildRequires:	clucene-core-devel
%endif
%endif

BuildRequires:	sword-devel
Requires:		sword

%description
BibleTime is a free and easy to use bible study tool for UNIX systems.
It requires a working KDE environment and the SWORD library.
BibleTime provides easy handling of digitized texts (Bibles, commentaries
and lexicons) and powerful features to work with these texts (search in
texts, write own notes, save, print etc.).
 

%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n %{kdecomp}-trinity-%{tdeversion}
#%patch0 -p0 -b .clucene
#%patch2 -p1 -b .ftbfs

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
	--libdir=%{tde_libdir} \
	--datadir=%{tde_datadir} \
	--includedir=%{tde_tdeincludedir} \
	--disable-rpath \
	--with-extra-libs=%{_libdir}/clucene09 \
	--with-extra-includes=%{tde_includedir}/tqt

# Not SMP safe !
%__make -C bibletime/frontend

# SMP safe !
%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

%__chmod 644 %{buildroot}%{tde_datadir}/apps/bibletime/pics/*
%__chmod 644 %{buildroot}%{tde_datadir}/apps/bibletime/bibletimeui.rc
%__chmod 644 %{buildroot}%{tde_datadir}/apps/bibletime/tips




%clean
%__rm -rf %{buildroot}


%post
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
/sbin/ldconfig || :

%postun
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
/sbin/ldconfig || :


%files
%defattr(-,root,root,-)
%{tde_bindir}/bibletime
%{tde_tdeincludedir}/bibletimeinterface.h
%{tde_datadir}/applications/bibletime.desktop
%{tde_datadir}/apps/bibletime/
%{tde_datadir}/icons/hicolor/*/*/*.png
%{tde_tdedocdir}/HTML/en/bibletime/


%changelog
* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 1.6.6.0-3
- Initial build for TDE 3.5.13.1

* Tue May 01 2012 Francois Andriot <francois.andriot@free.fr> - 1.6.6.0-2
- Fix compilation on RHEL 5
- Fix compilation with GCC 4.7

* Tue Nov 29 2011 Francois Andriot <francois.andriot@free.fr> - 1.6.6.0-1
- Initial build for RHEL 5, RHEL 6, Fedora 15, Fedora 16

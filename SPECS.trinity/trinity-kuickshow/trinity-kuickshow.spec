# Default version for this component
%define kdecomp kuickshow
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
Summary:	Quick picture viewer for KDE 
Version:	0.8.13
Release:	6%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{kdecomp}-trinity-%{tdeversion}.tar.xz

BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-tdebase-devel >= 3.5.13.1
BuildRequires:	desktop-file-utils

%if 0%{?rhel} || 0%{?fedora} || 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	imlib-devel
%endif

%description
Kuickshow is a picture viewer for KDE. It displays the directory structure,
displaying images as thumbnails.
Clicking on an image shows the image in its normal size. 


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
  --with-extra-includes=%{tde_includedir}/tqt \
  --enable-closure

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{?buildroot}


%clean
%__rm -rf %{buildroot}


%post
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
/sbin/ldconfig

%postun
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{tde_bindir}/*
%{tde_datadir}/applications/*/*.desktop
%{tde_datadir}/apps/*/
%{tde_datadir}/icons/hicolor/*/*/*
%{tde_libdir}/lib[kt]deinit_%{kdecomp}.so
%{tde_libdir}/*.la
%{tde_tdelibdir}/*.so
%{tde_tdelibdir}/*.la
%{tde_tdedocdir}/HTML/en/*/


%changelog
* Tue Aug 06 2013 Liu Di <liudidi@gmail.com> - 0.8.13-6.opt
- 为 Magic 3.0 重建

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 0.8.13-5
- Initial build for TDE 3.5.13.1

* Mon Jul 09 2012 Francois Andriot <francois.andriot@free.fr> - 0.8.13-3
- Removes conflict with 'kdegraphics'

* Sat May 05 2012 Francois Andriot <francois.andriot@free.fr> - 0.8.13-3
- Rename old tq methods that no longer need a unique name [Commit #8712ab46]
- Remove additional unneeded tq method conversions [Commit #28d9c774]
- Rename obsolete tq methods to standard names [Commit #bdeb8b3a]
- Remove inadvertent renaming [Commit #d97e403f] [Bug #863]

* Tue Sep 14 2011 Francois Andriot <francois.andriot@free.fr> - 0.8.13-2
- Import to GIT

* Mon Aug 22 2011 Francois Andriot <francois.andriot@free.fr> - 0.8.13-1
- Correct macro to install under "/opt", if desired

* Sat Aug 13 2011 Francois Andriot <francois.andriot@free.fr> - 0.8.13-0
- Initial build for RHEL 6.0


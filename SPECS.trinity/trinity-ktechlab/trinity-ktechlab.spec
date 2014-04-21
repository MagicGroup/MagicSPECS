# Default version for this component
%define tdecomp ktechlab
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


Name:		trinity-%{tdecomp}
Summary:	circuit simulator for microcontrollers and electronics [Trinity]
Version:	0.3
Release:	6%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:    %{tde_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{tdecomp}-trinity-%{tdeversion}.tar.xz

BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.2
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.2
BuildRequires:	trinity-tdebase-devel >= 3.5.13.2
BuildRequires:	desktop-file-utils
BuildRequires:	gettext


%description
KTechlab is a circuit simulator with a nice, clickable and discoverable
interface. It supports many discrete components, logic circuits as well
as PIC programming in its own Basic dialect and some form of assembler. 

Homepage: http://ktechlab.org/


%if 0%{?suse_version} || 0%{?pclinuxos}
%debug_package
%endif


%prep
%setup -q -n %{tdecomp}-trinity-%{tdeversion}

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

%find_lang %{tdecomp}

%clean
%__rm -rf %{buildroot}


%post
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :

%postun
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :


%files -f %{tdecomp}.lang
%defattr(-,root,root,-)
%{tde_bindir}/ktechlab
%{tde_bindir}/microbe
%{tde_datadir}/applnk/Development/ktechlab.desktop
%{tde_datadir}/apps/katepart/syntax/microbe.xml
%{tde_datadir}/apps/ktechlab
%{tde_datadir}/config.kcfg/ktechlab.kcfg
%{tde_tdedocdir}/HTML/en/ktechlab/
%{tde_datadir}/icons/hicolor/*/*/*.png
%{tde_datadir}/mimelnk/application/x-circuit.desktop
%{tde_datadir}/mimelnk/application/x-flowcode.desktop
%{tde_datadir}/mimelnk/application/x-ktechlab.desktop
%{tde_datadir}/mimelnk/application/x-microbe.desktop


%changelog
* Fri Aug 09 2013 Liu Di <liudidi@gmail.com> - 0.3-6.opt
- 为 Magic 3.0 重建

* Fri Aug 09 2013 Liu Di <liudidi@gmail.com> - 0.3-5.opt
- 为 Magic 3.0 重建

* Mon Jun 03 2013 Francois Andriot <francois.andriot@free.fr> - 0.3-4
- Initial release for TDE 3.5.13.2

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 0.3-3
- Initial release for TDE 3.5.13.1

* Fri Nov 25 2011 Francois Andriot <francois.andriot@free.fr> - 0.3-2
- Fix HTML directory location

* Thu Nov 24 2011 Francois Andriot <francois.andriot@free.fr> - 0.3-1
- Initial release for RHEL 5, RHEL 6, Fedora 15, Fedora 16
- Fix list of icons to install [Bug #990]

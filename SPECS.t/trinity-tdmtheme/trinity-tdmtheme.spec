# Default version for this component
%define tdecomp kdmtheme
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


Name:		trinity-tdmtheme
Summary:	theme manager for TDM [Trinity]
Version:	1.2.2
Release:	6%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://beta.smileaf.org/projects

Prefix:    %{tde_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{tdecomp}-trinity-%{tdeversion}.tar.xz

# [tdmtheme] Fix tdmtheme crash. This resolves Bug 1544
Patch1:		tdmtheme-3.5.13.2-fix_segv.patch

BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.2
BuildRequires:	trinity-arts-devel >= 3.5.13.2
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.2
BuildRequires:	trinity-tdebase-devel >= 3.5.13.2
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

Obsoletes:		trinity-kdmtheme < %{version}-%{release}
Provides:		trinity-kdmtheme = %{version}-%{release}


%description
kdmtheme is a theme manager for KDM. It provides a TDE Control Module (KCM)
that allows you to easily install, remove and change your KDM themes.



%if 0%{?suse_version} || 0%{?pclinuxos}
%debug_package
%endif


%prep
%setup -q -n %{tdecomp}-trinity-%{tdeversion}
%patch1 -p1 -b .segv

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


%clean
%__rm -rf %{buildroot}



%files
%defattr(-,root,root,-)
%{tde_tdelibdir}/kcm_kdmtheme.la
%{tde_tdelibdir}/kcm_kdmtheme.so
%{tde_tdeappdir}/kdmtheme.desktop
%{tde_tdedocdir}/HTML/en/kdmtheme/


%post
update-desktop-database %{tde_appdir} &> /dev/null

%postun
update-desktop-database %{tde_appdir} &> /dev/null


%changelog
* Thu Aug 08 2013 Liu Di <liudidi@gmail.com> - 1.2.2-6.opt
- 为 Magic 3.0 重建

* Thu Jun 27 2013 Francois Andriot <francois.andriot@free.fr> - 1.2.2-5
- Fix tdmtheme crash. This resolves Bug 1544

* Mon Jun 03 2013 Francois Andriot <francois.andriot@free.fr> - 1.2.2-4
- Initial release for TDE 3.5.13.2

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 1.2.2-3
- Initial release for TDE 3.5.13.1

* Tue May 01 2012 Francois Andriot <francois.andriot@free.fr> - 1.2.2-2
- Rebuilt for Fedora 17
- Removes post and postun
- Removes the 'lintian' stuff from Debian

* Fri Nov 25 2011 Francois Andriot <francois.andriot@free.fr> - 1.2.2-1
- Initial release for RHEL 5, RHEL 6, Fedora 15, Fedora 16

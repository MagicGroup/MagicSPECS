# Default version for this component
%define tdecomp k9copy
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
Summary:	DVD backup tool for Trinity
Version:	1.2.3
Release:	4%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	k9copy-trinity-%{tdeversion}%{?preversion:~%{preversion}}.tar.xz

Patch1:		k9copy-3.5.13.2-fix_k3b_link.patch
Patch2:		k9copy-trinity-3.5.13.2-ffmpeg.patch

BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.2
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.2
BuildRequires:	trinity-tdebase-devel >= 3.5.13.2
BuildRequires:	trinity-arts-devel >= 3.5.13.2
BuildRequires:	desktop-file-utils
BuildRequires:	trinity-k3b-devel

# Warning: the target distribution must have ffmpeg !
BuildRequires: ffmpeg-devel
Requires:	ffmpeg

%description
k9copy is a tabbed tool that allows to copy of one or more titles from a DVD9
to a DVD5, in thesame way than DVDShrink for Microsoft Windows (R).
This is the Trinity version


%if 0%{?suse_version} || 0%{?pclinuxos}
%debug_package
%endif


%prep
%setup -q -n k9copy-trinity-%{tdeversion}%{?preversion:~%{preversion}}
%patch1 -p1 -b .ftbfs
%patch2 -p1 -b .ffmpeg

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

# FFMPEG ...
if [ -d /usr/include/ffmpeg ]; then
	export CXXFLAGS="${RPM_OPT_FLAGS} -I/usr/include/ffmpeg"
fi

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  --disable-rpath \
  --with-extra-includes=%{tde_includedir}/tqt \
  --enable-closure

%__make %{?_smp_mflags} || %__make


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
update-desktop-database %{tde_appdir} &> /dev/null

%postun
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
update-desktop-database %{tde_appdir} &> /dev/null


%files -f %{tdecomp}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{tde_bindir}/k9copy
%{tde_tdeappdir}/k9copy.desktop
%{tde_datadir}/apps/k9copy/
%{tde_datadir}/apps/konqueror/servicemenus/k9copy_open.desktop
%lang(en) %{tde_tdedocdir}/HTML/en/k9copy/
%{tde_datadir}/icons/hicolor/*/apps/k9copy.png


%changelog
* Mon Jun 03 2013 Francois Andriot <francois.andriot@free.fr> - 1.2.3-4
- Initial release for TDE 3.5.13.2

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 1.2.3-3
- Initial release for TDE 3.5.13.1

* Sat Aug 04 2012 Francois Andriot <francois.andriot@free.fr> - 1.2.3-2
- Add support for MGA2 and MDV2011
- Fix 'format not a string literal' error. Clean up warning. [Commit #3bfc84b0]
- Fix FTBFS [Commit #62acebb7]
- Fix 'format not a string literal' error [Commit #d9ed8b32]
- Fix remaining string format errors [Commit #a8e98ad9]
- Fix another string format error [Commit #b3bb8a8f]
- Fix FTBFS [Commit #ca864ede]
- Fix format string error [Commit #a016df82]

* Fri Nov 25 2011 Francois Andriot <francois.andriot@free.fr> - 1.2.3-2
- Fix HTML directory location

* Sat Nov 19 2011 Francois Andriot <francois.andriot@free.fr> - 1.2.3-1
- Initial release for RHEL 5, RHEL 6, Fedora 15, Fedora 16

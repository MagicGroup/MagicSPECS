# Default version for this component
%define kdecomp kio-umountwrapper
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
Summary:	progress dialog for safely removing devices in Trinity.
Version:	0.2
Release:	5%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://frode.kde.no/misc/kio_umountwrapper/

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{kdecomp}-trinity-%{tdeversion}.tar.xz
Source1:	media_safelyremove.desktop


BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-tdebase-devel >= 3.5.13.1
BuildRequires: desktop-file-utils


%description
Wrapper around kio_media_mountwrapper.
Provides a progress dialog for Safely Removing of devices in Trinity.



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
  --with-extra-includes=%{tde_includedir}/tqt \
  --enable-closure

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

%__install -D -m 644 %{SOURCE1} %{?buildroot}%{tde_datadir}/apps/konqueror/servicemenus/media_safelyremove.desktop_kio-umountwrapper
#%__install -D -m 644 %{SOURCE1} %{?buildroot}%{tde_datadir}/apps/dolphin/servicemenus/media_safelyremove.desktop_kio-umountwrapper
%__install -D -m 644 %{SOURCE1} %{?buildroot}%{tde_datadir}/apps/d3lphin/servicemenus/media_safelyremove.desktop_kio-umountwrapper


%clean
%__rm -rf %{buildroot}

%post
for f in konqueror d3lphin; do
%if 0%{?suse_version}
  update-alternatives --install \
%else
  alternatives --install \
%endif
    %{tde_datadir}/apps/${f}/servicemenus/media_safelyremove.desktop \
    media_safelyremove.desktop_${f} \
    %{tde_datadir}/apps/${f}/servicemenus/media_safelyremove.desktop_kio-umountwrapper \
    20
done

  
%postun
if [ $1 -eq 0 ]; then
  for f in konqueror d3lphin; do
%if 0%{?suse_version}
    update-alternatives --remove \
%else
    alternatives --remove \
%endif
      media_safelyremove.desktop_${f} \
      %{tde_datadir}/apps/${f}/servicemenus/media_safelyremove.desktop_kio-umountwrapper
  done
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{tde_bindir}/kio_umountwrapper
%{tde_datadir}/apps/konqueror/servicemenus/media_safelyremove.desktop_kio-umountwrapper
#%{tde_datadir}/apps/dolphin/servicemenus/media_safelyremove.desktop_kio-umountwrapper
%{tde_datadir}/apps/d3lphin/servicemenus/media_safelyremove.desktop_kio-umountwrapper

%changelog
* Mon Aug 05 2013 Liu Di <liudidi@gmail.com> - 0.2-5.opt
- 为 Magic 3.0 重建

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 0.2-4
- Initial build for TDE 3.5.13.1

* Sun Jul 08 2012 Francois Andriot <francois.andriot@free.fr> - 0.2-3
- Add 'desktop' file, to make this program useful :-)

* Wed May 02 2012 Francois Andriot <francois.andriot@free.fr> - 0.2-2
- Rebuilt for Fedora 17
- Removes post and postun

* Sat Dec 03 2011 Francois Andriot <francois.andriot@free.fr> - 0.2-1
- Initial build for RHEL 5, RHEL 6, Fedora 15, Fedora 16


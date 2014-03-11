# Default version for this component
%define kdecomp kaffeine-mozilla
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
Summary:	mozilla plugin that lanches kaffeine for supported media types [Trinity]
Version:	0.4.3.1
Release:	4%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Multimedia

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{kdecomp}-trinity-%{tdeversion}.tar.xz

# Fix 'nspr' includes location
Patch1:		kaffeine-mozilla-3.5.13-fix_nspr_include.patch

BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-tdebase-devel >= 3.5.13.1
BuildRequires:	desktop-file-utils

%if 0%{?suse_version}
BuildRequires:	mozilla-nspr-devel
%else
BuildRequires:	nspr-devel
%endif

%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	%{_lib}xaw-devel
%else
BuildRequires:	libXaw-devel
%endif

Requires:		trinity-kaffeine

%description
This mozilla plugin launches kaffeine, the xine-based media player for KDE,
when a page containing a supported media format is loaded.


%if 0%{?suse_version}
%debug_package
%endif


%prep
unset QTDIR; . /etc/profile.d/qt3.sh
%setup -q -n %{kdecomp}-trinity-%{tdeversion}
%patch1 -p1

%__cp -f "/usr/share/aclocal/libtool.m4" .
%__cp -f "/usr/share/libtool/config/ltmain.sh" . || %__cp "/usr/share/libtool/ltmain.sh" .

autoreconf -fiv


%build
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"

%configure \
	--disable-rpath \
    --with-extra-includes=%{tde_includedir}/tqt \
    --enable-closure \
    --prefix=%{_libdir}/mozilla

%__make %{?_smp_mflags}

%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

# Remove useless filess
%__rm -f %{?buildroot}%{_libdir}/mozilla/plugins/kaffeineplugin.a

%clean
%__rm -rf %{buildroot}


%post
/sbin/ldconfig || :

%postun
/sbin/ldconfig || :


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
# These files are installed outside TDE prefix
%{_libdir}/mozilla/plugins/kaffeineplugin.la
%{_libdir}/mozilla/plugins/kaffeineplugin.so


%changelog
* Wed Jul 31 2013 Liu Di <liudidi@gmail.com> - 0.4.3.1-4.opt
- 为 Magic 3.0 重建

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 0.4.3.1-3
- Initial build for TDE 3.5.13.1

* Thu Apr 26 2012 Francois Andriot <francois.andriot@free.fr> - 0.4.3.1-2
- Rebuild with nicer patch.

* Sat Dec 03 2011 Francois Andriot <francois.andriot@free.fr> - 0.4.3.1.dfsg-1
- Initial build for RHEL 5, RHEL 6, Fedora 15, Fedora 16


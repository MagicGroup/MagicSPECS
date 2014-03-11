Name:	mate-conf	
Version:	1.4.0
Release:	21%{?dist}
Summary:	MATE Desktop configuration tool
License:	GPLv2+	
URL:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz

# Copy schemas from old package for later uninstall on upgrade.
# Macro to remove schemas.  Not meant to be used publically.
# Remove schemas unconditionally.
# Remove schemas on package removal (not upgrade).
Source1:	macros.mateconf

BuildRequires:	desktop-file-utils polkit-devel libglade2-devel dbus-glib-devel gobject-introspection-devel libxml2-devel libxslt-devel mate-corba-devel glib2-devel gtk-doc openldap-devel gtk2-devel gobject-introspection-devel mate-common mate-doc-utils cairo-gobject-devel gtk3-devel
Requires:	dbus

# for patch0
Requires: /usr/bin/killall
# I removed this once, and it got re-added, please document why -- rex
Conflicts: mate-conf-dbus

Patch0: mate-conf-1.4.0-reload.patch
# http://bugzilla.gnome.org/show_bug.cgi?id=568845

%description
MATE Desktop configuration tool

%package devel
Summary:	Development files for mate-conf
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for mate-conf

%package gtk
Summary: Graphical mate-conf utilities
Group: System Environment/Base
Requires: %{name}%{?_isa} = %{version}-%{release}

%description gtk
The mate-conf-gtk package contains graphical mate-conf utilities
which require GTK+.


%prep
%setup -q -n mate-conf-%{version}
%patch0 -p1 -b .reload
NOCONFIGURE=1 ./autogen.sh


%build
%configure --disable-static --enable-gtk --with-openldap --enable-defaults-service --enable-gtk --enable-gsettings-backend=yes --enable-introspection --enable-gtk-doc

# drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' -e 's/    if test "$export_dynamic" = yes && test -n "$export_dynamic_flag_spec"; then/      func_append compile_command " -Wl,-O1,--as-needed"\n      func_append finalize_command " -Wl,-O1,--as-needed"\n\0/' libtool

make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}

# prep macros.mateconf
mkdir -p %{buildroot}%{_sysconfdir}/mateconf/schemas
mkdir -p %{buildroot}%{_sysconfdir}/mateconf/mateconf.xml.system
mkdir -p %{buildroot}%{_sysconfdir}/rpm/
mkdir -p %{buildroot}%{_localstatedir}/lib/rpm-state/mateconf
mkdir -p %{buildroot}%{_datadir}/MateConf/matesettings

install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm/

# unpackaged files
find %{buildroot} -name '*.la' -exec rm -rf {} ';'

mkdir -p %{buildroot}%{_datadir}/GConf/gsettings
magic_rpm_clean.sh
%find_lang %{name}


%post
/usr/sbin/ldconfig
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules || :
if [ $1 -gt 1 ]; then
    if ! fgrep -q mateconf.xml.system %{_sysconfdir}/mateconf/2/path; then
        sed -i -e 's@xml:readwrite:$(HOME)/.mateconf@&\n\n# Location for system-wide settings.\nxml:readonly:/etc/mateconf/mateconf.xml.system@' %{_sysconfdir}/mateconf/2/path
    fi
fi

%postun
/usr/sbin/ldconfig
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules || :

%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README
%config(noreplace) %{_sysconfdir}/mateconf/2/path
%dir %{_sysconfdir}/mateconf/
%dir %{_sysconfdir}/mateconf/2/
%dir %{_sysconfdir}/mateconf/mateconf.xml.defaults/
%dir %{_sysconfdir}/mateconf/mateconf.xml.mandatory/
%dir %{_sysconfdir}/mateconf/mateconf.xml.system/
%dir %{_sysconfdir}/mateconf/schemas/
%dir %{_localstatedir}/lib/rpm-state/mateconf/
%{_sysconfdir}/rpm/macros.mateconf
%{_sysconfdir}/mateconf/2/evoldap.conf
%{_sysconfdir}/xdg/autostart/mateconf-gsettings-data-convert.desktop
%{_mandir}/man1/*
%{_bindir}/mateconf-gsettings-data-convert
%{_bindir}/mateconf-gsettings-schema-convert
%{_bindir}/mateconf-merge-tree
%{_bindir}/mateconftool-2
%{_sysconfdir}/dbus-1/system.d/org.mate.MateConf.Defaults.conf
%dir %{_datadir}/sgml
%{_datadir}/sgml/mateconf/
%{_libexecdir}/mateconf-defaults-mechanism
%{_libexecdir}/mateconf-sanity-check-2
%{_libexecdir}/mateconfd-2
%{_libdir}/libmateconf-2.so.4*
%{_libdir}/MateConf/
%{_libdir}/gio/modules/libgsettingsmateconfbackend.so
%{_libdir}/girepository-1.0/MateConf-2.0.typelib
%{_datadir}/dbus-1/services/org.mate.MateConf.service
%{_datadir}/dbus-1/system-services/org.mate.MateConf.Defaults.service
%{_datadir}/polkit-1/actions/org.mate.mateconf.defaults.policy
%{_datadir}/MateConf/schema/evoldap.schema

%files gtk
%{_libexecdir}/mateconf-sanity-check-2

%files devel
%{_datadir}/gtk-doc/html/mateconf/
%{_libdir}/libmateconf-2.so
%{_includedir}/mateconf/
%{_datadir}/gir-1.0/MateConf-2.0.gir
%{_datadir}/aclocal/mateconf-2.m4
%{_libdir}/pkgconfig/mateconf-2.0.pc


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.4.0-21
- 为 Magic 3.0 重建

* Sat Oct 06 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4.0-20
- own %%{_localstatedir}/lib/rpm-state/mateconf/

* Wed Sep 26 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4.0-19
- fix macros.mateconf
- fix gio scriplets
- simplify some dir/file ownership
- drop Requires: desktop-file-utils

* Tue Sep 18 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-18
- Rebuild again.

* Thu Sep 06 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-17
- Rebuild entire spec from scratch

* Sun Sep 02 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-16
- Drop the useless gtk package, and specific version requirements for buildrequires field.
- Move mateconf-sanity-check-2 to the main package where it's needed

* Sun Aug 26 2012 Dan Mashal <dan.mashal@fedoraproject.org 1.4.0-15
- Bump release for repush

* Mon Aug 06 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4.0-14
- tighten subpkgs deps (isa)
- -devel: drop needless pkgconfig-related deps (they're autodetected)
- sort BR's
- omit needless Conflicts: mate-conf-dbus
- don't own /var/lib/rpm-state
- drop Group: tags
- files: track abi/abi items closer

* Tue Jul 31 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-11
- remove %%defattr(-, root, root)
- remove rm -rf $RPM_BUILD_ROOT from install section
- rename GConf-2.18.0.1-reload.patch to mate-conf-1.4.0-reload.patch

* Mon Jul 30 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-10
- remove double BuildRequires

* Sun Jul 29 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-9
- fix rpmlint error
- add %%doc COPYING NEWS README to mate-conf-gtk as rpmlint want this

* Sat Jul 28 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-8
- fix licence information
- add information to macro
- fix url
- update specific versions from dependencies from configure.in
- Change %%defines to %%global

* Sat Jul 28 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-7
- remove *.la files

* Sat Jul 28 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-6
- initial package for fedora

* Sun Dec 25 2011 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.1.0-1
- mate-conf.spec based on GConf2-2.32.4-1.fc16 spec

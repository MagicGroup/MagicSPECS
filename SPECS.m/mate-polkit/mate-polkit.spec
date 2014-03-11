Name:		mate-polkit
Version:	1.4.0
Release:	5%{?dist}
Summary:	Integrates polkit authentication for MATE desktop
License:	LGPLv2+
URL:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.4/%name-%version.tar.xz

BuildRequires:	gobject-introspection-devel gtk2-devel mate-common polkit-devel
# needed for gobject-introspection support somehow,
# https://bugzilla.redhat.com/show_bug.cgi?id=847419#c17 asserts this is a bug (elsewhere)
# but I'm not entirely sure -- rex
BuildRequires: 	cairo-gobject-devel

Provides:	PolicyKit-authentication-agent


%description
Integrates polkit with the MATE Desktop environment

%package devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary:	Integrates polkit with the MATE Desktop environment

%description devel
Development libraries for mate-polkit

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh --disable-static


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
magic_rpm_clean.sh
%find_lang %{name}

find %{buildroot} -name '*.la' -exec rm -fv {} ';'


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
# yes, license really is LGPLv2+, despite included COPYING is about GPL, poke upstreamo
# to include COPYING.LIB here instead  -- rex
%doc AUTHORS COPYING README
%{_sysconfdir}/xdg/autostart/polkit-mate-authentication-agent-1.desktop
%{_libdir}/libpolkit-gtk-mate-1.so.0
%{_libdir}/libpolkit-gtk-mate-1.so.0.0.0
%{_libdir}/girepository-1.0/PolkitGtkMate-1.0.typelib
%{_libexecdir}/polkit-mate-authentication-agent-1

%files devel
%{_libdir}/libpolkit-gtk-mate-1.so
%{_libdir}/pkgconfig/polkit-gtk-mate-1.pc
%{_includedir}/polkit-gtk-mate-1/
%{_datadir}/gir-1.0/PolkitGtkMate-1.0.gir


%changelog 
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.4.0-5
- 为 Magic 3.0 重建

* Mon Aug 27 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.4.0-4
- drop extraneous update-desktop-database scriptlet
- don't mark .desktop file %%config
- License: LGPLv2+

* Sun Aug 26 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Move PolkitGTKMate gir file to devel package

* Sat Aug 18 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Remove duplicate doc macro, add provides, fix post macro, have devel package own proper dir

* Wed Aug 08 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial build

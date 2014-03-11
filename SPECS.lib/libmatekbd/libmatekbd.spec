Name:		libmatekbd
Version:	1.4.0
Release:	7%{?dist}
Summary:	Libraries for mate kbd
License:	LGPLv2+
URL:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz

BuildRequires:	desktop-file-utils gtk2-devel libxklavier-devel mate-common mate-conf-devel
Requires(pre):	mate-conf
Requires(post):	mate-conf
Requires(preun):	mate-conf


%description
Libraries for matekbd

%package devel
Summary: Development libraries for libmatekbd
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries for libmatekbd

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh


%build
%configure --disable-static --disable-schemas-install
make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}

find %{buildroot} -name '*.la' -exec rm -fv {} ';'
magic_rpm_clean.sh
%find_lang %{name} --all-name

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/matekbd-indicator-plugins-capplet.desktop


%pre
/usr/sbin/ldconfig
%mateconf_schema_prepare desktop_mate_peripherals_keyboard_xkb

%preun
%mateconf_schema_remove desktop_mate_peripherals_keyboard_xkb

%post
/usr/sbin/ldconfig
%mateconf_schema_upgrade desktop_mate_peripherals_keyboard_xkb

%files -f %{name}.lang
%doc AUTHORS COPYING.LIB README
%config(noreplace) %{_sysconfdir}/mateconf/schemas/desktop_mate_peripherals_keyboard_xkb.schemas
%{_bindir}/matekbd-indicator-plugins-capplet
%{_datadir}/applications/matekbd-indicator-plugins-capplet.desktop
%{_datadir}/libmatekbd/
%{_libdir}/libmatekbd.so.4*
%{_libdir}/libmatekbdui.so.4*

%files devel
%{_includedir}/libmatekbd/
%{_libdir}/pkgconfig/libmatekbd.pc
%{_libdir}/pkgconfig/libmatekbdui.pc
%{_libdir}/libmatekbdui.so
%{_libdir}/libmatekbd.so

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.4.0-7
- 为 Magic 3.0 重建

* Wed Sep 26 2012 Dan Mashal <dan.mashal@fedoraproject.org>  1.4.0-6
- Remove onlyshowin from desktop-fileinstall  and mateconf_obsolete macro
- Fix date on previous changelog (I was tired, sorry).

* Mon Sep 24 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-5
- Update desktop-file-install and fix mate-conf scriptlets

* Mon Aug 27 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4.0-4
- License: LGPLv2+, %%doc COPYING.LIB
- dir ownership
- don't use undefined %%{po_package} macro
- s|MATE|X-MATE| only on < f18

* Sun Aug 26 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Remove obsolete scriptlet from pre macro, correct schema scriptlets for mateconf and bump release version

* Sat Aug 25 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Drop libs package add scriptlets for schemas

* Sun Aug 12 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial build

Name:	mate-session-manager
Version:	1.4.0
Release:	10%{?dist}
Summary:	MATE Desktop session manager
License:	GPLv2+
URL:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz

BuildRequires:	mate-conf-devel desktop-file-utils mate-conf-gtk mate-conf gtk2-devel dbus-glib-devel mate-common gstreamer-plugins-base-devel libSM-devel upower-devel mate-polkit-devel mate-icon-theme icon-naming-utils polkit-devel
Requires(pre):	mate-conf
Requires(post):	mate-conf
Requires(preun):	mate-conf

%description
MATE Desktop session manager

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build
%configure --disable-static --disable-schemas-install --enable-ipv6 --with-gtk=2.0 --with-gnu-ld --with-default-wm=marco --with-x
make %{?_smp_mflags} V=1


%install
export MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=%{buildroot}
unset MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
magic_rpm_clean.sh
%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/mate-session-properties.desktop

%pre
%mateconf_schema_prepare mate-session

%preun
%mateconf_schema_remove mate-session

%post
/usr/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
%mateconf_schema_upgrade mate-session


%postun
if [ $1 -eq 0 ] ; then
	/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
	/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_docdir}/mate-session/dbus/mate-session.html
%{_mandir}/man1/*
%{_bindir}/mate-session
%{_bindir}/mate-session-properties
%{_bindir}/mate-session-save
%{_bindir}/mate-wm
%{_sysconfdir}/mateconf/schemas/mate-session.schemas
%{_datadir}/applications/mate-session-properties.desktop
%{_datadir}/mate-session/
%{_datadir}/icons/hicolor/16x16/apps/*.png
%{_datadir}/icons/hicolor/22x22/apps/*.png
%{_datadir}/icons/hicolor/24x24/apps/*.png
%{_datadir}/icons/hicolor/32x32/apps/*.png
%{_datadir}/icons/hicolor/48x48/apps/*.png
%{_datadir}/icons/hicolor/scalable/apps/mate-session-properties.svg
%{_datadir}/xsessions/mate.desktop

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.4.0-10
- 为 Magic 3.0 重建

* Wed Oct 17 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-9
- Add mate.desktop to desktop-file-install

* Tue Oct 16 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-8
- Add MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 to install section

* Tue Oct 16 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-7
- Fix configure flags
- Remove no replace macro from schemas

* Sun Oct 07 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-6
- Remove kdm

* Sat Oct 06 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-5
- Add kdm to the requires field. mate-session-manager has no dm builtin yet

* Tue Oct 02 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-4
- Update post/postun/poststrans scriptlets to match files section for hicolor
- Update licensing to GPLv2+ only

* Sat Sep 29 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-3
- Fix buildrequires/requires field

* Mon Sep 26 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-2
- Fix mateconf scriptlets

* Thu Jul 12 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-1
-Initial build

Name:           libmatekbd
Version:        1.8.0
Release:        2%{?dist}
Summary:        Libraries for mate kbd
Summary(zh_CN.UTF-8): mate kbd 的库
License:        LGPLv2+
URL:            http://mate-desktop.org
Source0:        http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz

BuildRequires:  desktop-file-utils
BuildRequires:  gsettings-desktop-schemas-devel
BuildRequires:  gtk2-devel
BuildRequires:  libICE-devel
BuildRequires:  libxklavier-devel
BuildRequires:  mate-common

%description
Libraries for matekbd

%description -l zh_CN.UTF-8
matekbd 的库。

%package devel
Summary:  Development libraries for libmatekbd
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries for libmatekbd

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q


%build
# To work around rpath issue
autoreconf -fi

%configure                   \
   --disable-static          \
   --with-gtk=2.0            \
   --disable-schemas-compile \
   --with-x
  
make %{?_smp_mflags} V=1


%install
%{make_install}

find %{buildroot} -name '*.la' -exec rm -fv {} ';'

# remove needless gsettings convert file
rm -f  %{buildroot}%{_datadir}/MateConf/gsettings/matekbd.convert
magic_rpm_clean.sh
%find_lang %{name} --with-gnome --all-name


%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_datadir}/libmatekbd
%{_datadir}/glib-2.0/schemas/org.mate.peripherals-keyboard-xkb.gschema.xml
%{_libdir}/libmatekbd.so.4*
%{_libdir}/libmatekbdui.so.4*

%files devel
%{_includedir}/libmatekbd
%{_libdir}/pkgconfig/libmatekbd.pc
%{_libdir}/pkgconfig/libmatekbdui.pc
%{_libdir}/libmatekbdui.so
%{_libdir}/libmatekbd.so

%changelog
* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 1.8.0-2
- 为 Magic 3.0 重建

* Tue Mar 04 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Sun Feb 16 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90 release

* Thu Feb 13 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.2-2
- Add autoreconf to workaround rpath issue
- Sort BRs

* Sat Jan 18 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.2-1
- update to 1.7.2
- use modern 'make install' macro
- remove needless gsettings convert file
- use --with-gnome --all-name for find locale
- add BR libICE-devel
- fix ld scriptlets

* Wed Dec 04 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.1-1
- Update to 1.7.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-1
- Update to latest upstream release.

* Sat Jun 22 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-2
- Add upstream commits patch for various bugfixes

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Fri Feb 08 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-1
-Update to latest upstream release
-Update BR's
-Own dirs we are supposed to own
-Update configure flags

* Mon Dec 10 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.0-2
- Rebuild for ARM

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release
- change build requires style
- remove mateconf scriplets and replace with schema scriptlets
- add requires gsettings-desktop-schemas
- add build requires gsettings-desktop-schemas-devel

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

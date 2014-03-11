Name:		libmateweather
Version:	1.4.0
Release:	6%{?dist}
Summary:	Libraries to allow MATE Desktop to display weather information
License:	GPLv2+
URL:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz

BuildRequires:	gtk2-devel libsoup-devel mate-common mate-conf-devel pygobject2-codegen python-gudev pygtk2-devel
Requires(pre):	mate-conf
Requires(post):	mate-conf
Requires(preun):	mate-conf


%description
Libraries to allow MATE Desktop to display weather information


%package devel
Summary: Development files for libmateweather
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for libmateweather


%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh


%build
%configure --enable-python --disable-static --disable-schemas-install
make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}
magic_rpm_clean.sh
%find_lang %{name}

find %{buildroot} -name '*.la' -exec rm -fv {} ';'


%pre
%mateconf_schema_prepare mateweather

%post 
/usr/sbin/ldconfig
/usr/bin/touch --no-create %{_datadir}/icons/mate/status &>/dev/null || :
%mateconf_schema_upgrade mateweather

%postun
/usr/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /usr/bin/touch --no-create %{_datadir}/icons/mate &>/dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/mate/status/ &>/dev/null || :
fi
%mateconf_schema_remove mateweather

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/mate/status/ &>/dev/null || :

%files -f %{name}.lang
%doc AUTHORS COPYING README
%config(noreplace) %{_sysconfdir}/mateconf/schemas/mateweather.schemas
%{_datadir}/libmateweather/
%{_datadir}/icons/mate/*/status/*
%{_datadir}/gtk-doc/html/libmateweather/
%{python_sitearch}/mateweather/
%{_libdir}/libmateweather.so.1*

%files devel
%{_libdir}/libmateweather.so
%{_includedir}/libmateweather/
%{_libdir}/pkgconfig/mateweather.pc


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.4.0-6
- 为 Magic 3.0 重建

* Mon Aug 27 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4.0-5
- fix deps, a few cosmetics

* Sun Aug 25 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-4
- Fix mateconf scriptlets for schemas, bump release version

* Sat Aug 25 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Move python files to main package, drop libs subpackage, update mateconf scriptlets, move shared library to devel package

* Sat Aug 18 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Fix directory ownership

* Sun Aug 12 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial build

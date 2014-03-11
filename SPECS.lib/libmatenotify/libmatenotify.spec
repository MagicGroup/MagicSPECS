Name:		libmatenotify
Version:	1.4.1
Release:	9%{?dist}
Summary:	Libraries for mate notify
License:	LGPLv2+
URL:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz

BuildRequires:	mate-common dbus-glib-devel gtk2-devel pkgconfig

%description
Libraries for mate notify.

%package devel
Summary: Development libraries for libmatenotify
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries for libmatenotify


%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh


%build
%configure --disable-static
make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING README
%{_bindir}/mate-notify-send
%{_libdir}/libmatenotify.so.1*
%{_datadir}/gtk-doc/html/libmatenotify/

%files devel
%{_libdir}/libmatenotify.so
%{_libdir}/pkgconfig/libmatenotify.pc
%{_includedir}/libmatenotify/


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.4.1-9
- 为 Magic 3.0 重建

* Fri Aug 10 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.4.1-8
- drop BR: gtk+-devel
- drop explicit Requires: pkgconfig (-devel will autoreq this)
- %%files: glob on lib soname
- %%build: do verbose build
- License: LGPLv2+

* Thu Aug 09 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.1-7
- Fix typo in changelog, bump release number

* Thu Aug 09 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.1-6
- Update to libmatenotify 1.4.1 from upstream.

* Wed Aug 08 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-5
- Polish macros and build requires for Ankur as per package review.

* Wed Aug 08 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-4
- Update build requires for devel package

* Wed Aug 08 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Update build requires

* Wed Aug 08 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Updated spec file as per package review

* Wed Aug 08 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial build

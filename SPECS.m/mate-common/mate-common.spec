Name:	mate-common
Summary:	mate common build files
Version:	1.5.0
Release:	2%{?dist}

License:	GPLv3+
URL:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.5/mate-common-%{version}.tar.xz

BuildArch: noarch

BuildRequires:	automake autoconf
Requires: automake autoconf gettext intltool libtool glib2-devel gtk-doc 

%description
binaries for building all MATE desktop sub components

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build
%configure
make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}
magic_rpm_clean.sh

%files
%defattr(-,root,root,-)
%{_bindir}/mate-*
%{_datadir}/aclocal/mate-*.m4
%{_datadir}/mate-common/
%{_mandir}/man1/mate-*

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.5.0-2
- 为 Magic 3.0 重建

* Thu Oct 11 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.5.0-1
- New upstream release 1.5

* Thu Aug 2 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-8
- Re add requires with proper required packages for dependant packages.

* Thu Aug 2 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-7
- Remove requires field as it is not necessary.

* Tue Jul 24 2012 Dan Mashal <dan.mashal@gmail.com> 1.4.0-6
- Update requires/buildrequires field.

* Tue Jul 16 2012 Dan Mashal <dan.mashal@gmail.com> 1.4.0-5
- Update license, description and requires field.

* Mon Jul 16 2012 Dan Mashal <dan.mashal@gmail.com> 1.4.0-4
- Clean up requirements fields

* Sat Jul 14 2012 Dan Mashal <dan.mashal@gmail.com> 1.4.0-3
- incorporate Rex's changes, clean up spec file.

* Fri Jul 13 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4.0-2
- omit Group: tag
- fix URL, Source0
- use %%configure macro
- BuildArch: noarch

* Thu Jul 12 2012 Dan Mashal <dan.mashal@gmail.com> 1.4.0-1
- Initial build

Name:	mate-doc-utils
Summary:	MATE Desktop doc utils
Version:	1.4.0
Release:	14%{?dist}

License:	GPLv2+ and LGPLv2+
URL:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz

#For users upgrading from the unofficial MATE desktop Fedora repo
Obsoletes: mate-doc-utils-stylesheets < %{version}-%{release}
Provides: mate-doc-utils-stylesheets = %{version}-%{release}

# for /usr/share/aclocal
Requires: automake
# for the validation with xsltproc to use local dtds
Requires: docbook-dtds
# for /usr/share/pkgconfig
Requires: pkgconfig
# for /usr/share/xml
Requires: xml-common
# for /usr/share/xml/mallard
Requires: gnome-doc-utils-stylesheets

BuildArch:	noarch

BuildRequires:	mate-common intltool gettext libxslt-devel rarian-devel libxml2-devel scrollkeeper gnome-doc-utils
Requires:	mate-common gnome-doc-utils

%description
mate-doc-utils is a collection of documentation utilities for the Mate
project.  Notably, it contains utilities for building documentation and
all auxiliary files in your source tree, and it contains the DocBook
XSLT style sheets that were once distributed with Yelp.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build
%configure --disable-scrollkeeper
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
magic_rpm_clean.sh
%find_lang %{name}
#Remove unnecessary python sitepackages provided by gnome-doc-utils
rm -rf $RPM_BUILD_ROOT/%{python_sitelib}/*
rm -rf $RPM_BUILD_ROOT/%{python_sitelib}/xml2po/
rm -rf %{buildroot}/%{_mandir}/man1/*
rm -rf $RPM_BUILD_ROOT/%{_datadir}/xml/mallard
rm -rf $RPM_BUILD_ROOT/%{_bindir}/xml2po
rm -rf $RPM_BUILD_ROOT/%{_datadir}/pkgconfig/xml2po.pc
#Debian script not needed
rm -rf $RPM_BUILD_ROOT/%{_datadir}/mate-doc-utils/mate-debian.sh

%files -f %{name}.lang
%doc AUTHORS README NEWS COPYING COPYING.GPL COPYING.LGPL
%{_bindir}/mate-doc-prepare
%{_bindir}/mate-doc-tool
%{_datadir}/aclocal/mate-doc-utils.m4
%{_datadir}/mate/help/mate-doc-make
%{_datadir}/mate/help/mate-doc-xslt
%{_datadir}/omf/mate-doc-make
%{_datadir}/omf/mate-doc-xslt
%{_datadir}/mate-doc-utils
%{_datadir}/xml/mate
%{_datadir}/pkgconfig/mate-doc-utils.pc

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.4.0-14
- 为 Magic 3.0 重建

* Mon Jul 23 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-12
- Make changes per package review.

* Mon Jul 23 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-11
- Make changes per package review.

* Mon Jul 23 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-10
- Create devel package, fix license and requirements field per package review.

* Mon Jul 23 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-9
- Update spec file

* Sun Jul 22 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-8
- Fix python sitelib conflicts.

* Sun Jul 22 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-7
- Add language macros and add doc files

* Sat Jul 21 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-6
- Clean up spec file further.

* Tue Jul 16 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-5
- Update requires, licensing, remove unneeded python files

* Mon Jul 16 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-4
- Update licensing

* Sat Jul 14 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Incorporate Rex's changes, clean up spec file.

* Fri Jul 13 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4.0-2
- omit Group: tag
- fix URL, Source0
- use %%configure macro
- BuildArch: noarch

* Thu Jul 12 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial build

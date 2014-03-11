Summary: Tool for decoding raw image data from digital cameras
Name: dcraw
Version: 9.11
Release: 2%{?dist}
Group: Applications/Multimedia
License: GPLv2+
URL: http://cybercom.net/~dcoffin/dcraw
Source0: http://cybercom.net/~dcoffin/dcraw/archive/dcraw-%{version}.tar.gz
BuildRequires: gettext
BuildRequires: libjpeg-devel
BuildRequires: lcms-devel
BuildRequires: jasper-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%__id_u -n)

%description
This package contains dcraw, a command line tool to decode raw image data
downloaded from digital cameras.

%prep
%setup -q -n dcraw

%build
gcc %optflags -lm -ljpeg -llcms -ljasper -DLOCALEDIR="\"%{_datadir}/locale\"" -o dcraw dcraw.c
# build language catalogs
for catsrc in dcraw_*.po; do
    lang="${catsrc%.po}"
    lang="${lang#dcraw_}"
    msgfmt -o "dcraw_${lang}.mo" "$catsrc"
done

%install
rm -rf %buildroot
install -d -m 0755 %{buildroot}%{_bindir}
install -m 0755 dcraw %{buildroot}%{_bindir}

# install language catalogs
for catalog in dcraw_*.mo; do
    lang="${catalog%.mo}"
    lang="${lang#dcraw_}"
    install -d -m 0755 "%{buildroot}%{_datadir}/locale/${lang}/LC_MESSAGES"
    install -m 0644 "$catalog" "%{buildroot}%{_datadir}/locale/${lang}/LC_MESSAGES/dcraw.mo"
done

install -d -m 0755 %{buildroot}%{_bindir} %{buildroot}%{_mandir}/man1
install -m 0644 dcraw.1 %{buildroot}%{_mandir}/man1/dcraw.1
# localized manpages
rm -f %{name}-man-files
touch %{name}-man-files
for manpage in dcraw_*.1; do
    lang="${manpage%.1}"
    lang="${lang#dcraw_}"
    install -d -m 0755 "%{buildroot}%{_mandir}/${lang}/man1"
    install -m 0644 "${manpage}" "%{buildroot}%{_mandir}/${lang}/man1/dcraw.1"
    echo "%%lang($lang) %%{_mandir}/${lang}/man1/*" >> %{name}-man-files
done

%find_lang %{name}

%clean
rm -rf %buildroot

%files -f %{name}.lang -f %{name}-man-files
%defattr(-, root, root)
%{_bindir}/dcraw
%{_mandir}/man1/*

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 9.11-2
- 为 Magic 3.0 重建

* Wed Oct 12 2011 Nils Philippsen <nils@redhat.com> - 9.11-1
- version 9.11

* Mon Aug 01 2011 Nils Philippsen <nils@redhat.com> - 9.10-1
- version 9.10
- add BR: jasper-devel, link with jasper library

* Mon May 23 2011 Nils Philippsen <nils@redhat.com> - 9.08-1
- version 9.08

* Thu Apr 14 2011 Nils Philippsen <nils@redhat.com> - 9.07-1
- version 9.07

* Fri Mar 04 2011 Nils Philippsen <nils@redhat.com> - 9.06-1
- version 9.06

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 03 2010 Nils Philippsen <nils@redhat.com> - 9.04-1
- version 9.04

* Wed Jun 02 2010 Nils Philippsen <nils@redhat.com> - 9.01-1
- version 9.01
- color man page files with %%lang()

* Fri Feb 12 2010 Nils Philippsen <nils@redhat.com> - 8.99-1
- version 8.99

* Tue Aug 18 2009 Nils Philippsen <nils@redhat.com> - 8.96-1
- version 8.96

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 02 2009 Nils Philippsen <nils@redhat.com> - 8.91-1
- version 8.91

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.89-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 27 2008 Nils Philippsen <nphilipp@redhat.com> - 8.89-1
- version 8.89
- remove obsolete gps patch

* Mon Feb 25 2008 Nils Philippsen <nphilipp@redhat.com> - 8.82-1
- version 8.82

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 8.81-2
- Autorebuild for GCC 4.3

* Mon Jan 14 2008 Nils Philippsen <nphilipp@redhat.com> - 8.81-1
- version 8.81
- add support for GPS data (#428600, patch by Ulrich Drepper)

* Fri Nov 30 2007 Nils Philippsen <nphilipp@redhat.com> - 8.80-1
- version 8.80
- change license tag to GPLv2+

* Mon Feb 05 2007 Nils Philippsen <nphilipp@redhat.com> - 8.77-2
- rebuild with pristine source tarball

* Mon Feb 05 2007 Nils Philippsen <nphilipp@redhat.com> - 8.77-1
- version 8.77

* Mon Feb 05 2007 Nils Philippsen <nphilipp@redhat.com> - 8.53-2
- fix summary, use %%find_lang (#225678)

* Thu Feb 01 2007 Nils Philippsen <nphilipp@redhat.com> - 8.53-1
- upstream finally has a tarball, use that and its version (#209016)
- use dist tag

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.0.20060521-1.1
- rebuild

* Tue May 23 2006 Nils Philippsen <nphilipp@redhat.com> - 0.0.20060521-1
- program and manpage version of 2006-05-21
- use %%optflags
- change license tag to GPL
- use lcms

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.0.20051211-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.0.20051211-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Dec 14 2005 Nils Philippsen <nphilipp@redhat.com>
- version of 2005-12-11
- manpage of 2005-09-29

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 02 2005 Nils Philippsen <nphilipp@redhat.com>
- version of 2005-02-27
- manpage of 2005-01-19

* Wed Dec 01 2004 Nils Philippsen <nphilipp@redhat.com>
- version of 2004-11-28
- initial build

Summary: A tool for converting XML files to various formats
Name: xmlto
Version: 0.0.25
Release: 3%{?dist}
License: GPLv2+
Group: Applications/System
#Older versions up to xmlto-0.0.20
#URL: http://cyberelk.net/tim/xmlto/
#Source0: http://cyberelk.net/tim/data/xmlto/stable/%{name}-%{version}.tar.bz2
URL: https://fedorahosted.org/xmlto/
Source0: https://fedorahosted.org/releases/x/m/%{name}/%{name}-%{version}.tar.bz2

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: docbook-xsl >= 1.56.0
BuildRequires: libxslt
BuildRequires: util-linux, flex

# We rely heavily on the DocBook XSL stylesheets!
Requires: docbook-xsl >= 1.74.2
Requires: text-www-browser
Requires: libxslt
Requires: docbook-dtds
Requires: util-linux, flex

%description
This is a package for converting XML files to various formats using XSL
stylesheets.

%package tex
Group: Applications/System
License: GPLv2+
Summary: A set of xmlto backends with TeX requirements
# For full functionality, we need passivetex.
Requires: passivetex >= 1.11
# We require main package
Requires: xmlto = %{version}-%{release}
BuildArch: noarch


%description tex
This subpackage contains xmlto backend scripts which do require
PassiveTeX/TeX for functionality.

%package xhtml
Group: Applications/System
License: GPLv2+
Summary: A set of xmlto backends for xhtml1 source format
# For functionality we need stylesheets xhtml2fo-style-xsl
Requires: xhtml2fo-style-xsl
# We require main package
Requires: xmlto = %{version}-%{release}
BuildArch: noarch

%description xhtml
This subpackage contains xmlto backend scripts for processing
xhtml1 source format.

%prep
%setup -q

%build
%configure BASH=/bin/bash
make %{?_smp_mflags}

%check
make check

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog README AUTHORS NEWS
%{_bindir}/*
%{_mandir}/*/*
%{_datadir}/xmlto
%exclude %{_datadir}/xmlto/format/fo/dvi
%exclude %{_datadir}/xmlto/format/fo/ps
%exclude %{_datadir}/xmlto/format/fo/pdf
%exclude %dir %{_datadir}/xmlto/format/xhtml1/
%exclude %{_datadir}/xmlto/format/xhtml1


%files tex
%defattr(-,root,root,-)
%{_datadir}/xmlto/format/fo/dvi
%{_datadir}/xmlto/format/fo/ps
%{_datadir}/xmlto/format/fo/pdf

%files xhtml
%defattr(-,root,root,-)
%dir %{_datadir}/xmlto/format/xhtml1/
%{_datadir}/xmlto/format/xhtml1/*


%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.0.25-3
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 02 2011 Ondrej Vasik <ovasik@redhat.com> - 0.0.25-1
- fix handling of external data objects with fop
  (deb #568894)

* Tue Nov 29 2011 Ondrej Vasik <ovasik@redhat.com> - 0.0.24-2
- fix the functionality of fop.extensions (#757035)

* Thu Jul 14 2011 Ondrej Vasik <ovasik@redhat.com> - 0.0.24-1
- new release 0.0.24, basic support for docbook->epub
  conversion, use backend extensions by default
  (--noextensions) to disable it

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 13 2009 Ondrej Vasik <ovasik@redhat.com> - 0.0.23-3
- workaround passivetex limitation for chapter titles starting
  with L(#526273)

* Fri Sep 24 2009 Ondrej Vasik <ovasik@redhat.com> - 0.0.23-2
- ensure the default shell is /bin/bash instead of /bin/sh

* Mon Sep 21 2009 Ondrej Vasik <ovasik@redhat.com> - 0.0.23-1
- New version 0.0.23
- added autodetection for more common tools like
  gnu cp or tail
- added option --noautosize to prevent overriding
  of user-defined or system-default paper size
- use shell built-in 'type -t' instead of 'which'
  utility for detection of file availability

* Sat Aug 01 2009 Ondrej Vasik <ovasik@redhat.com> - 0.0.22-3
- make subpackages noarch, preserve timestamps - merge
  review (#226568)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 25 2009 Ondrej Vasik <ovasik@redhat.com> - 0.0.22-1
- New version 0.0.22
- autodetection for tools/program paths, consolidated
  error code handling, build warnings cleanup

* Mon Mar 16 2009 Ondrej Vasik <ovasik@redhat.com> - 0.0.21-9
- reenable noent switch - bug is on lcdproc side
- add xhtml support(subpackage) (#145140)

* Mon Mar 02 2009 Ondrej Vasik <ovasik@redhat.com> - 0.0.21-8
- temporarily disable noent switch - blocks lcdproc doc build
  (#488093)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Ondrej Vasik <ovasik@redhat.com> - 0.0.21-6
- fix cleaning up of temporary files with libpaper(Debian)
- fix xmllint postvalid (added noent option), use nonet
  switch

* Mon Jan 05 2009 Ondrej Vasik <ovasik@redhat.com> - 0.0.21-5
- fix stringparam option functionality

* Tue Dec 16 2008 Ondrej Vasik <ovasik@redhat.com> - 0.0.21-4
- merge review(#226568)
  correct doc filelist attributes, add License GPL+ for xmlif

* Fri Dec 12 2008 Ondrej Vasik <ovasik@redhat.com> - 0.0.21-3
- merge review(#226568):
  ship documentation files, fix license tag, use recommended
  parallel make, make install instead of macro, require libxslt
  instead of direct binary requirement

* Fri Jul 11 2008 Ondrej Vasik <ovasik@redhat.com> - 0.0.21-2
- xmlto-tex subpackage to prevent requirements for
  passivetex/tex for all backends(#454341)

* Mon Jun 20 2008 Ondrej Vasik <ovasik@redhat.com> - 0.0.21-1
- new version 0.0.21

* Tue May 13 2008 Ondrej Vasik <ovasik@redhat.com> - 0.0.20-3
- fixed errorneus handling of backend stylesheet(#446092)
- removed unused patches

* Mon Feb 11 2008 Ondrej Vasik <ovasik@redhat.com> - 0.0.20-2
- gcc4.3 rebuild

* Thu Jan 17 2008 Ondrej Vasik <ovasik@redhat.com> - 0.0.20-1
- new version 0.0.20
- added experimental fop support(additional output formats)
- possibility to read stylesheet from STDIN, using recursive
  cp in docbook formats, updated man pages

* Wed Nov 28 2007 Ondrej Vasik <ovasik@redhat.com> - 0.0.19-1
- new version 0.0.19
- added dist tag

* Fri Oct 12 2007 Ondrej Vasik <ovasik@redhat.com> - 0.0.18-17
- generalized text-www-browser requirements(#174566)

* Mon Oct  8 2007 Ondrej Vasik <ovasik@redhat.com> - 0.0.18-16
- fixed warning message from find in usage() display(#322121)

* Wed Sep 19 2007 Ondrej Vasik <ovasik@redhat.com> - 0.0.18-15
- fixed wrong source URL

* Thu Aug 23 2007 Ondrej Vasik <ovasik@redhat.com> - 0.0.18-14
- rebuilt for F8
- changed License tag to GPLv2

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.0.18-13.1
- rebuild

* Thu Jun  8 2006 Tim Waugh <twaugh@redhat.com> 0.0.18-13
- Removed debugging.

* Thu Jun  8 2006 Tim Waugh <twaugh@redhat.com> 0.0.18-12
- Debug build.

* Thu Jun  8 2006 Tim Waugh <twaugh@redhat.com> 0.0.18-11
- Rebuilt.

* Mon Jun  5 2006 Tim Waugh <twaugh@redhat.com> 0.0.18-10
- Rebuilt.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.0.18-9.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.0.18-9.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Aug  8 2005 Tim Waugh <twaugh@redhat.com> 0.0.18-9
- Fixed quoting in scripts (bug #165338).

* Mon Aug  1 2005 Tim Waugh <twaugh@redhat.com> 0.0.18-8
- Requires w3m (bug #164798).

* Mon Jul 25 2005 Tim Waugh <twaugh@redhat.com> 0.0.18-7
- Rebuild for new man-pages stylesheet.

* Mon Apr  4 2005 Tim Waugh <twaugh@redhat.com>
- Requires util-linux and flex, as does the build.

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 0.0.18-6
- Rebuild for new GCC.

* Wed Feb  9 2005 Tim Waugh <twaugh@redhat.com> 0.0.18-5
- Rebuilt.

* Thu Jul  1 2004 Tim Waugh <twaugh@redhat.com> 0.0.18-4
- Magic encoding is enabled again (bug #126921).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 21 2004 Tim Waugh <twaugh@redhat.com> 0.0.18-1
- 0.0.18.

* Mon Dec  1 2003 Tim Waugh <twaugh@redhat.com> 0.0.17-1
- 0.0.17.

* Tue Nov 18 2003 Tim Waugh <twaugh@redhat.com> 0.0.16-1
- 0.0.16.

* Tue Oct  7 2003 Tim Waugh <twaugh@redhat.com> 0.0.15-1
- 0.0.15.

* Tue Sep 23 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- allow compiling without tetex(passivetex) dependency

* Tue Jun 17 2003 Tim Waugh <twaugh@redhat.com> 0.0.14-3
- Rebuilt.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May 23 2003 Tim Waugh <twaugh@redhat.com> 0.0.14-1
- 0.0.14.

* Sun May 11 2003 Tim Waugh <twaugh@redhat.com> 0.0.13-1
- 0.0.13.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Jan  3 2003 Tim Waugh <twaugh@redhat.com> 0.0.12-2
- Disable magic encoding detection, since the stylesheets don't handle
  it well at all (bug #80732).

* Thu Dec 12 2002 Tim Waugh <twaugh@redhat.com> 0.0.12-1
- 0.0.12.

* Wed Oct 16 2002 Tim Waugh <twaugh@redhat.com> 0.0.11-1
- 0.0.11.
- xmlto.mak no longer needed.
- CVS patch no longer needed.
- Update docbook-xsl requirement.
- Ship xmlif.
- Run tests.
- No longer a noarch package.

* Tue Jul  9 2002 Tim Waugh <twaugh@redhat.com> 0.0.10-4
- Ship xmlto.mak.

* Thu Jun 27 2002 Tim Waugh <twaugh@redhat.com> 0.0.10-3
- Some db2man improvements from CVS.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 0.0.10-2
- automated rebuild

* Tue Jun 18 2002 Tim Waugh <twaugh@redhat.com> 0.0.10-1
- 0.0.10.
- No longer need texinputs patch.

* Tue Jun 18 2002 Tim Waugh <twaugh@redhat.com> 0.0.9-3
- Fix TEXINPUTS problem with ps and dvi backends.

* Thu May 23 2002 Tim Powers <timp@redhat.com> 0.0.9-2
- automated rebuild

* Wed May  1 2002 Tim Waugh <twaugh@redhat.com> 0.0.9-1
- 0.0.9.
- The nonet patch is no longer needed.

* Fri Apr 12 2002 Tim Waugh <twaugh@redhat.com> 0.0.8-3
- Don't fetch entities over the network.

* Thu Feb 21 2002 Tim Waugh <twaugh@redhat.com> 0.0.8-2
- Rebuild in new environment.

* Tue Feb 12 2002 Tim Waugh <twaugh@redhat.com> 0.0.8-1
- 0.0.8.

* Fri Jan 25 2002 Tim Waugh <twaugh@redhat.com> 0.0.7-2
- Require the DocBook DTDs.

* Mon Jan 21 2002 Tim Waugh <twaugh@redhat.com> 0.0.7-1
- 0.0.7 (bug #58624, bug #58625).

* Wed Jan 16 2002 Tim Waugh <twaugh@redhat.com> 0.0.6-1
- 0.0.6.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 0.0.5-4
- automated rebuild

* Wed Jan  9 2002 Tim Waugh <twaugh@redhat.com> 0.0.5-3
- 0.0.6pre2.

* Wed Jan  9 2002 Tim Waugh <twaugh@redhat.com> 0.0.5-2
- 0.0.6pre1.

* Tue Jan  8 2002 Tim Waugh <twaugh@redhat.com> 0.0.5-1
- 0.0.5.

* Mon Dec 17 2001 Tim Waugh <twaugh@redhat.com> 0.0.4-2
- 0.0.4.
- Apply patch from CVS to fix silly typos.

* Sat Dec  8 2001 Tim Waugh <twaugh@redhat.com> 0.0.3-1
- 0.0.3.

* Wed Dec  5 2001 Tim Waugh <twaugh@redhat.com>
- Built for Red Hat Linux.

* Fri Nov 23 2001 Tim Waugh <twaugh@redhat.com>
- Initial spec file.

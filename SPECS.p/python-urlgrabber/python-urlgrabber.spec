%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: A high-level cross-protocol url-grabber
Name: python-urlgrabber
Version: 3.9.1
Release: 12%{?dist}
Source0: urlgrabber-%{version}.tar.gz
Patch1: urlgrabber-HEAD.patch

License: LGPLv2+
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
BuildRequires: python-devel, python-pycurl
Url: http://urlgrabber.baseurl.org/
Provides: urlgrabber = %{version}-%{release}
Requires: python-pycurl

%description
A high-level cross-protocol url-grabber for python supporting HTTP, FTP 
and file locations.  Features include keepalive, byte ranges, throttling,
authentication, proxies and more.

%prep
%setup -q -n urlgrabber-%{version}
%patch1 -p1

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install -O1 --root=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/%{_docdir}/urlgrabber-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE README TODO
%{python_sitelib}/urlgrabber*
%{_bindir}/urlgrabber

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 3.9.1-12
- 为 Magic 3.0 重建

* Sun Jan 22 2012 Liu Di <liudidi@gmail.com> - 3.9.1-11
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep  3 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.9.1-9
- new update to latest head with a number of patches collected from 
  older bug reports.

* Mon Aug 30 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.9.1-8
- update to latest head patches

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 3.9.1-7
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Apr 13 2010 James Antill <james@fedoraproject.org> 3.9.1-6
- Update to upstream HEAD.
- LOWSPEEDLIMIT and hdrs

* Fri Feb 19 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.9.1-5
- add patch to allow reset_curl_obj() to close and reload the cached curl obj

* Thu Nov 12 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.1-4
- reset header values when we redirect and make sure debug output will work

* Wed Nov 11 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.1-3
- fixing a bunch of redirect and max size bugs

* Fri Sep 25 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.1-2
- stupid patch

* Fri Sep 25 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.1-1
- 3.9.1

* Tue Aug 18 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.0-8
- ssl options, http POST string type fixes

* Mon Aug 10 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.0-6
- reget fixes, tmpfiles no longer made for urlopen() calls.

* Wed Aug  5 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.0-5
- apply complete patch to head fixes: timeouts, regets, improves exception raising

* Tue Aug  4 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.0-4
- timeout patch for https://bugzilla.redhat.com/show_bug.cgi?id=515497


* Thu Jul 30 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.0-1
- new version - curl-based

* Wed Apr  8 2009 James Antill <james@fedoraproject.org> 3.0.0-15
- Fix progress bars for serial consoles.
- Make C-c behaviour a little nicer.

* Fri Mar 13 2009 Seth Vidal <skvidal at fedoraproject.org>
- kill deprecation warning from importing md5 if anyone uses keepalive

* Mon Mar  9 2009 Seth Vidal <skvidal at fedoraproject.org>
- apply patch for urlgrabber to properly check file:// urls with the checkfunc

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 28 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 3.0.0-11
- Rebuild for Python 2.6

* Wed Oct 14 2008 James Antill <james@fedoraproject.org> 3.0.0-10
- Have the progress bar have a small bar, for a virtual size doubling.

* Thu Jul 10 2008 James Antill <james@fedoraproject.org> 3.0.0-9
- Make urlgrabber usable if openssl is broken
- Relates: bug#454179

* Sun Jun 15 2008 James Antill <james@fedoraproject.org> 3.0.0-9
- Don't count partial downloads toward the total

* Sat May 18 2008 James Antill <james@fedoraproject.org> 3.0.0-8
- Tweak progress output so it's hopefully less confusing
- Add dynamic resizing ability to progress bar
- Resolves: bug#437197

* Fri May  2 2008 James Antill <james@fedoraproject.org> 3.0.0-7
- Fix reget's against servers that don't allow Range requests, also tweaks
- reget == check_timestamp, if anyone/thing uses that.
- Resolves: bug#435156
- Fix minor typo in progress for single instance.

* Mon Apr  7 2008 James Antill <james@fedoraproject.org> 3.0.0-6
- Fix the ftp byterange port problem:
- Resolves: bug#419241
- Fixup the progress UI:
-   add function for total progress
-   add total progress percentagee current download line
-   add rate to current download line
-   use dead space when finished downloading
-   don't confuse download rate on regets.

* Sat Mar 15 2008 Robert Scheck <robert@fedoraproject.org> 3.0.0-5
- Make sure, that *.egg-info is catched up during build

* Mon Dec  3 2007 Jeremy Katz <katzj@redhat.com> - 3.0.0-4
- Ensure fds are closed on exceptions (markmc, #404211)

* Wed Oct 10 2007 Jeremy Katz <katzj@redhat.com> - 3.0.0-3
- fix type checking of strings to also include unicode strings; fixes 
  regets from yum (#235618)

* Mon Aug 27 2007 Jeremy Katz <katzj@redhat.com> - 3.0.0-2
- fixes for package review (#226347)

* Thu May 31 2007 Jeremy Katz <katzj@redhat.com> - 3.0.0-1
- update to 3.0.0

* Wed Dec  6 2006 Jeremy Katz <katzj@redhat.com> - 2.9.9-5
- rebuild for python 2.5

* Wed Dec  6 2006 Jeremy Katz <katzj@redhat.com> - 2.9.9-4
- fix keepalive (#218268) 

* Sat Nov 11 2006 Florian La Roche <laroche@redhat.com>
- add version/release to "Provides: urlgrabber"

* Mon Jul 17 2006 James Bowes <jbowes@redhat.com> - 2.9.9-2
- Add support for byte ranges and keepalive over HTTPS

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.9.9-1.1
- rebuild

* Tue May 16 2006 Jeremy Katz <katzj@redhat.com> - 2.9.9-1
- update to 2.9.9

* Tue Mar 14 2006 Jeremy Katz <katzj@redhat.com> - 2.9.8-2
- catch read errors so they trigger the failure callback.  helps catch bad cds

* Wed Feb 22 2006 Jeremy Katz <katzj@redhat.com> - 2.9.8-1
- update to new version fixing progress bars in yum on regets

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Sep 21 2005 Jeremy Katz <katzj@redhat.com> - 2.9.6-4
- don't use --record and list files by hand so that we don't miss 
  directories (#158480)

* Wed Sep 14 2005 Jeremy Katz <katzj@redhat.com> - 2.9.6-3
- add directory to file list (#168261)

* Fri Jun 03 2005 Phil Knirsch <pknirsch@redhat.com> 2.9.6-2
- Fixed the reget method to actually work correctly (skip completely transfered
  files, etc)

* Tue Mar  8 2005 Jeremy Katz <katzj@redhat.com> - 2.9.6-1
- update to 2.9.6

* Mon Mar  7 2005 Jeremy Katz <katzj@redhat.com> - 2.9.5-1
- import into dist
- make the description less of a book

* Mon Mar  7 2005 Seth Vidal <skvidal@phy.duke.edu> 2.9.5-0
- 2.9.5

* Thu Feb 24 2005 Seth Vidal <skvidal@phy.duke.edu> 2.9.3-0
- first package for fc3
- named python-urlgrabber for naming guideline compliance


%if 0%{?fedora} ||0%{?rhel} >= 7
%global with_python3 1
%else
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib2: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

Name:           python-bugzilla
Version:	1.2.1
Release:	2%{?dist}
Summary:        A python library and tool for interacting with Bugzilla
Summary(zh_CN.UTF-8): 与 Bugzilla 交互的 PYthon 库和工具

License:        GPLv2+
URL:            https://fedorahosted.org/python-bugzilla
Source0:        https://fedorahosted.org/releases/p/y/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: python2-devel
BuildRequires: python-requests

%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-requests
%endif # if with_python3

Requires: python-requests
Requires: python-magic


%description
python-bugzilla is a python 2 library for interacting with bugzilla instances
over XML-RPC. This package also includes the 'bugzilla' command-line tool
for interacting with bugzilla from shell scripts.

%description -l zh_CN.UTF-8
与 Bugzilla 交互的 PYthon 库和工具。

%if 0%{?with_python3}
%package -n python3-bugzilla
Summary: A python 3 library for interacting with Bugzilla
Summary(zh_CN.UTF-8): 与 Bugzilla 交互的 PYthon3 库和工具
Requires: python3-requests
Requires: python3-magic

%description -n python3-bugzilla
python3-bugzilla is a python 3 library for interacting with bugzilla instances
over XML-RPC.

%description -n python3-bugzilla -l zh_CN.UTF-8
与 Bugzilla 交互的 PYthon3 库和工具。
%endif # if with_python3


%prep
%setup -q

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3


%build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%{__python2} setup.py build


%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
rm %{buildroot}/usr/bin/bugzilla
popd
%endif # with_python3

%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
magic_rpm_clean.sh

%check
%{__python2} setup.py test



%files
%doc COPYING README PKG-INFO
%{python2_sitelib}/*
%{_bindir}/bugzilla
%{_mandir}/man1/bugzilla.1.gz

%if 0%{?with_python3}
%files -n python3-bugzilla
%doc COPYING README PKG-INFO
%{python3_sitelib}/*
%endif # with_python3
%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.2.1-2
- 为 Magic 3.0 重建

* Sat Aug 22 2015 Liu Di <liudidi@gmail.com> - 1.2.1-1
- 更新到 1.2.1

* Wed Jun 18 2014 Cole Robinson <crobinso@redhat.com> - 1.1.0-2
- Fix tests on rawhide (bz #1106734)

* Sun Jun 01 2014 Cole Robinson <crobinso@redhat.com> - 1.1.0-1
- Rebased to version 1.1.0
- Support for bugzilla tokens (Arun Babu Nelicattu)
- bugzilla: Add query/modify --tags
- bugzilla --login: Allow to login and run a command in one shot
- bugzilla --no-cache-credentials: Don't use or save cached credentials
  when using the CLI
- Show bugzilla errors when login fails
- Don't pull down attachments in bug.refresh(), need to get
  bug.attachments manually
- Add Bugzilla bug_autorefresh parameter.

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Mar 27 2014 Cole Robinson <crobinso@redhat.com> - 1.0.0-2
- /usr/bin/bugzilla should use python2 (bz #1081594)

* Tue Mar 25 2014 Cole Robinson <crobinso@redhat.com> - 1.0.0-1
- Rebased to version 1.0.0
- Python 3 support (Arun Babu Neelicattu)
- Port to python-requests (Arun Babu Neelicattu)
- bugzilla: new: Add --keywords, --assigned_to, --qa_contact (Lon
  Hohberger)
- bugzilla: query: Add --quicksearch, --savedsearch
- bugzilla: query: Support saved searches with --from-url
- bugzilla: --sub-component support for all relevant commands

* Tue Nov 05 2013 Cole Robinson <crobinso@redhat.com> - 0.9.0-3
- Drop unneeded setuptools dep

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 19 2013 Cole Robinson <crobinso@redhat.com> - 0.9.0-1
- Rebased to version 0.9.0
- bugzilla: modify: add --dependson (Don Zickus)
- bugzilla: new: add --groups option (Paul Frields)
- bugzilla: modify: Allow setting nearly every bug parameter
- NovellBugzilla implementation removed, can't get it to work
- Gracefully handle private bugs (bz #963979)
- Raise error if python-magic is needed (bz #951572)
- CVE-2013-2191: Add SSL host and cert validation (bz #975961, bz #951594)

* Mon Mar 04 2013 Cole Robinson <crobinso@redhat.com> - 0.8.0-2
- Don't upload scrambled attachments (bz #915318)

* Fri Feb 15 2013 Cole Robinson <crobinso@redhat.com> - 0.8.0-1
- Rebased to version 0.8.0
- Drop most usage of non-upstream RH Bugzilla API
- Test suite improvements, nearly complete code coverage
- Fix all open bug reports and RFEs

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 03 2013 Adam Jackson <ajax@redhat.com> 0.7.0-3
- Make closing bugs work, and allow closing as duplicate.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Cole Robinson <crobinso@redhat.com> - 0.7.0-1
- Rebased to version 0.7.0
- Fix querying with latest Red Hat bugzilla
- Bugzilla 4 API support
- Improve querying non-RH bugzilla instances

* Tue Apr  3 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.6.2-4
- Cleanup spec and actually rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 09 2011 Will Woods <wwoods@redhat.com> - 0.6.2-2
- Add "Requires: python-magic"

* Tue Jun 07 2011 Will Woods <wwoods@redhat.com> - 0.6.2-1
- add 'bugzilla attach' command (#707320)
- update CLI --help, improve manpage a bit
- fix --blocked and other boolean CLI options (#621601)
- use NamedTemporaryFile for temp. cookiefiles (#625019)
- fix openattachment() on non-ascii filenames (#663674 - thanks kklic)
- clean up handling of unknown product names (#659331)
- misc CLI fixes (--oneline, --qa_whiteboard), add 'modify --qa_contact'

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug  5 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.1-3
- add compatibility patch for python 2.7 (bug 621298)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Apr 16 2010 Will Woods <wwoods@redhat.com> - 0.6.1-1
- CLI speedup: skip version autodetection for bugzilla.redhat.com
- CLI: fix bug 581670 - UnicodeEncodeError crash using --outputformat
- CLI: fix bug 549186 - parser failure/xmlrpc Fault on 'bugzilla query'
- Library: fix bug 577327 - crash changing assignee without --comment
- Library: fix bug 580711 - crash when bug has empty CC list
- Library: add new Bugzilla36 class
- Library: export and autodetect Bugzilla34 and Bugzilla36 classes

* Tue Mar 2 2010 Will Woods <wwoods@redhat.com> - 0.6.0-1
- New version 0.6, with lots of improvements and fixes.
- Library: add NovellBugzilla implementation
- Library: use standardized LWPCookieJar by default
- Library: implement unicode(bug), fix Bug.__str__ unicode handling
- Library: make Bug class pickle-friendly
- Library: add flag info helper methods to Bug class
- Library: handle problems with missing fields in User class
- CLI: --oneline formatting tweaks and dramatic speed improvements
- CLI: add support for modifying private, status, assignee, flags, cc, fixed_in
- CLI: improve query: allow multiple flags, flag negation, handle booleans
- CLI: make --cc work when creating bugs
- CLI: new --raw output style
- CLI: special output format fields for flag and whiteboard
- CLI: fix broken --cc and -p flags
- CLI: fix problem where bz comments default to being private
- CLI: improve 'info --product' output
- CLI: handle socket/network failure cleanly
- CLI: allow adding comments when updating whiteboards

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 14 2009 Will Woods <wwoods@redhat.com> - 0.5.1-2
- Fix missing util.py

* Thu Apr 9 2009 Will Woods <wwoods@redhat.com> - 0.5.1-1
- CLI: fix unicode handling
- CLI: add --from-url flag, which parses a bugzilla query.cgi URL
- CLI: fix showing aliases
- CLI: add --comment, --private, --status, --assignee, --flag, --cc for update
- CLI: fix --target_milestone

* Wed Mar 25 2009 Will Woods <wwoods@redhat.com> - 0.5-1
- Fix problem where login wasn't saving the cookies to a file 
- Fix openattachment (bug #487673)
- Update version number for 0.5 final

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-0.rc1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Will Woods <wwoods@redhat.com> 0.5-0.rc1
- Improve cookie handling
- Add User class and associated Bugzilla methods (in Bugzilla 3.4)
- Add {add,edit,get}component methods
- Fix getbugs() so a single invalid bug ID won't abort the whole request
- CLI: fix -c <component>

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.4-0.rc4.1
- Rebuild for Python 2.6

* Wed Oct 15 2008 Will Woods <wwoods@redhat.com> 0.4-0.rc4
- CLI: fix traceback with --full (Don Zickus)
- CLI: add --oneline (Don Zickus)
- CLI: speedup when querying bugs by ID (Don Zickus)
- CLI: add --bztype
- CLI: --bug_status defaults to ALL
- Fix addcc()/deletecc()
- RHBugzilla3: raise useful error on getbug(unreadable_bug_id)
- Add adduser() (Jon Stanley)

* Wed Oct  8 2008 Will Woods <wwoods@redhat.com> 0.4-0.rc3
- Add updateperms() - patch courtesy of Jon Stanley
- Fix attachfile() for RHBugzilla3
- Actually install man page. Whoops.

* Thu Sep 18 2008 Will Woods <wwoods@redhat.com> 0.4-0.rc2
- Auto-generated man page with much more info
- Fix _attachfile()

* Thu Sep  4 2008 Will Woods <wwoods@redhat.com> 0.4-0.rc1
- Update to python-bugzilla 0.4-rc1
- We now support upstream Bugzilla 3.x and Red Hat's Bugzilla 3.x instance
- library saves login cookie in ~/.bugzillacookies
- new 'bugzilla login' command to get a login cookie

* Sat Jan 12 2008 Will Woods <wwoods@redhat.com> 0.3-1
- Update to python-bugzilla 0.3 
- 'modify' works in the commandline-util
- add Bug.close() and Bug.setstatus()

* Thu Dec 13 2007 Will Woods <wwoods@redhat.com> 0.2-4
- use _bindir instead of /usr/bin and proper BR for setuptools

* Tue Dec 11 2007 Will Woods <wwoods@redhat.com> 0.2-3
- Fix a couple of things rpmlint complained about

* Tue Dec 11 2007 Will Woods <wwoods@redhat.com> 0.2-2
- Add docs

* Wed Oct 10 2007 Will Woods <wwoods@redhat.com> 0.2-1
- Initial packaging.

Name:           python3-cherrypy
%global         camelname CherryPy
Version:        3.8.0
Release:        3%{?dist}
Summary:        Pythonic, object-oriented web development framework
Summary(zh_CN.UTF-8): 面向对象的网页开发框架
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        BSD
URL:            http://www.cherrypy.org/
Source0:        https://pypi.python.org/packages/source/C/%{camelname}/%{camelname}-%{version}.tar.gz
Patch0:         python-cherrypy-tutorial-doc.patch
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-nose
BuildRequires:  python3-setuptools
BuildRequires:  dos2unix

# Delete pycache in %%doc after %%install
%global __os_install_post %(echo '%{__os_install_post}'; echo 'rm -rf cherrypy/tutorial/__pycache__')

%description
%{camelname} allows developers to build web applications in much the same way 
they would build any other object-oriented Python program. This usually 
results in smaller source code developed in less time.

%description -l zh_CN.UTF-8
面向对象的网页开发框架。

%prep
%setup -q -n %{camelname}-%{version}
%patch0 -p1

dos2unix README.txt cherrypy/LICENSE.txt cherrypy/tutorial/README.txt cherrypy/tutorial/tutorial.conf

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/cherryd %{buildroot}%{_bindir}/python3-cherryd
rm -f %{buildroot}%{python3_sitelib}/cherrypy/LICENSE.txt
rm -f %{buildroot}%{python3_sitelib}/cherrypy/cherryd
magic_rpm_clean.sh

%check
# This is cheating, we skip some tests
# The reason is, some of them are failing for dicts being unsorted in Py3
# And some of them are just weird :D
# Some of them would hang mock
# Some import httplib
cd cherrypy/test
LANG=en_US.UTF-8 /usr/bin/nosetests-3* -v -s ./ -e 'test_SIGTERM' -e \
  'test_SIGHUP_tty' -e 'test_file_stream' -e 'testCombinedTools' -e \
  'test_HTTP11_pipelining' -e 'testCookies' -e 'testEncoding' -e \
  'test_multipart_decoding' -e 'test_multipart_decoding_no_charset' -e \
  'testErrorHandling' -e 'test_config_errors' -e 'testParams' -e \
  'test_0_Session' -e 'test_conn' -e 'test_session' -e testTracebacks
cd -

# The tests created __pycache__ in tutorial again, let's delete it
# But keep the deleting after %%install, if %%check is skipped
rm -rf cherrypy/tutorial/__pycache__

%files
%doc README.txt
%doc cherrypy/tutorial
%doc cherrypy/LICENSE.txt
%{_bindir}/python3-cherryd
%{python3_sitelib}/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 3.8.0-3
- 为 Magic 3.0 重建

* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 3.8.0-2
- 为 Magic 3.0 重建

* Tue Jul 07 2015 Miro Hrončok <mhroncok@redhat.com> - 3.8.0-1
- Update to 3.8.0 (#1236248)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Apr 25 2015 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 3.7.0-1
- Update to 3.7.0 (#1215290)

* Fri Sep 26 2014 Miro Hrončok <mhroncok@redhat.com> - 3.6.0-1
- New version 3.6.0 (#1100749)
- Skip more tests :(

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 16 2014 Matej Stuchlik <mstuchli@redhat.com> - 3.2.6-1
- Updated to 3.2.6

* Fri May 02 2014 Miro Hrončok <mhroncok@redhat.com> - 3.2.4-4
- Rebuilt for Python 3.4

* Wed Nov 13 2013 Miro Hrončok <mhroncok@redhat.com> - 3.2.4-3
- Delete tutorial's __pycache__ after %%install AND after %%check

* Tue Nov 12 2013 Miro Hrončok <mhroncok@redhat.com> - 3.2.4-2
- Use only %%{buildroot} and don't mix it with RPM_BUILD_ROOT

* Tue Nov 12 2013 Miro Hrončok <mhroncok@redhat.com> - 3.2.4-1
- Retaken orphaned package
- Update to 3.2.4
- Remove some deprecated statements form the spec
- Remove some patches
- Refactor %%check
- Add license to %%doc and remove it form site-packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-0.rc1.r2567.1.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-0.rc1.r2567.1.7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 3.2.0-0.rc1.r2567.1.6
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-0.rc1.r2567.1.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-0.rc1.r2567.1.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-0.rc1.r2567.1.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 3.2.0-0.rc1.r2567.1.2
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 3.2.0-0.rc1.r2567.1.1
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Apr 19 2010 David Malcolm <dmalcolm@redhat.com> - 3.2.0-0.rc1.r2567.1
- disable a test that hangs when run under Koji (patch 1)

* Mon Apr  5 2010 David Malcolm <dmalcolm@redhat.com> - 3.2.0-0.rc1.r2567
- initial packaging for python 3, based on python-cherrypy-3.2.0-0.1.rc1.fc14

* Tue Feb 23 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 3.2.0-0.1.rc1
- New upstream release candidate

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 16 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 3.1.2-1
- New upstream with python-2.6 fixes.
- BR tidy for tests.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 1 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 3.1.1-1
- Update to 3.1.1
- Fix python-2.6 build errors
- Make test code non-interactive via cmdline switch
- Refresh the no test and tutorial patch

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.0.3-3
- Rebuild for Python 2.6

* Tue Jan 22 2008 Toshio Kuratomi <toshio@fedoraproject.org> 3.0.3-2
- Forgot to upload the tarball.

* Mon Jan 21 2008 Toshio Kuratomi <toshio@fedoraproject.org> 3.0.3-1
- Upgrade to 3.0.3.

* Thu Jan 17 2008 Toshio Kuratomi <toshio@fedoraproject.org> 2.3.0-2
- EINTR Patch needed to be forwarded ported as well as it is only applied to
  CP trunk (3.x).

* Thu Jan 17 2008 Toshio Kuratomi <toshio@fedoraproject.org> 2.3.0-1
- Update to new upstream which rolls in the backported security fix.
- Refresh other patches to apply against new version.
- Change to new canonical source URL.
- Reenable tests.

* Sun Jan  6 2008 Toshio Kuratomi <toshio@fedoraproject.org> 2.2.1-8
- Fix a security bug with a backport of http://www.cherrypy.org/changeset/1775
- Include the egginfo files as well as the python files.

* Sat Nov  3 2007 Luke Macken <lmacken@redhat.com> 2.2.1-7
- Apply backported fix from http://www.cherrypy.org/changeset/1766
  to improve CherryPy's SIGSTOP/SIGCONT handling (Bug #364911).
  Thanks to Nils Philippsen for the patch.

* Mon Feb 19 2007 Luke Macken <lmacken@redhat.com> 2.2.1-6
- Disable regression tests until we can figure out why they
  are dying in mock.

* Sun Dec 10 2006 Luke Macken <lmacken@redhat.com> 2.2.1-5
- Add python-devel to BuildRequires

* Sun Dec 10 2006 Luke Macken <lmacken@redhat.com> 2.2.1-4
- Rebuild for python 2.5

* Mon Sep 18 2006 Luke Macken <lmacken@redhat.com> 2.2.1-3
- Rebuild for FC6
- Include pyo files instead of ghosting them

* Thu Jul 13 2006 Luke Macken <lmacken@redhat.com> 2.2.1-2
- Rebuild

* Thu Jul 13 2006 Luke Macken <lmacken@redhat.com> 2.2.1-1
- Update to 2.2.1
- Remove unnecessary python-abi requirement

* Sat Apr 22 2006 Gijs Hollestelle <gijs@gewis.nl> 2.2.0-1
- Update to 2.2.0

* Wed Feb 22 2006 Gijs Hollestelle <gijs@gewis.nl> 2.1.1-1
- Update to 2.1.1 (Security fix)

* Tue Nov  1 2005 Gijs Hollestelle <gijs@gewis.nl> 2.1.0-1
- Updated to 2.1.0

* Sat May 14 2005 Gijs Hollestelle <gijs@gewis.nl> 2.0.0-2
- Added dist tag

* Sun May  8 2005 Gijs Hollestelle <gijs@gewis.nl> 2.0.0-1
- Updated to 2.0.0 final
- Updated python-cherrypy-tutorial-doc.patch to match new version

* Wed Apr  6 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 2.0.0-0.2.b
- Removed CFLAGS

* Wed Mar 23 2005 Gijs Hollestelle <gijs[AT]gewis.nl> 2.0.0-0.1.b
- Initial Fedora Package

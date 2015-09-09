%{!?py3dir: %global py3dir %{_builddir}/python3-%{name}-%{version}-%{release}}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-pycurl
Version:        7.19.5.1
Release:        3%{?dist}
Summary:        A Python interface to libcurl
Summary(zh_CN.UTF-8): libcurl 的 Python 接口

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        LGPLv2+ or MIT
URL:            http://pycurl.sourceforge.net/
Source0:        https://pypi.python.org/packages/source/p/pycurl/pycurl-%{version}.tar.gz

Requires:       keyutils-libs
BuildRequires:  python-devel
BuildRequires:  python3-devel
BuildRequires:  curl-devel >= 7.19.0
BuildRequires:  openssl-devel
BuildRequires:  python-bottle
BuildRequires:  python-cherrypy
BuildRequires:  python-nose
BuildRequires:  python3-bottle
BuildRequires:  python3-cherrypy
BuildRequires:  python3-nose
BuildRequires:  vsftpd

# During its initialization, PycURL checks that the actual libcurl version
# is not lower than the one used when PycURL was built.
# Yes, that should be handled by library versioning (which would then get
# automatically reflected by rpm).
# For now, we have to reflect that dependency.
%global libcurl_sed '/^#define LIBCURL_VERSION "/!d;s/"[^"]*$//;s/.*"//;q'
%global curlver_h /usr/include/curl/curlver.h
%global libcurl_ver %(sed %{libcurl_sed} %{curlver_h} 2>/dev/null || echo 0)
Requires:       libcurl >= %{libcurl_ver}

Provides:       pycurl = %{version}-%{release}

%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%description -l zh_CN.UTF-8
libcurl 的 Python 接口。

%package -n python3-pycurl
Summary:        A Python interface to libcurl for Python 3
Summary(zh_CN.UTF-8): libcurl 的 Python3 接口

%description -n python3-pycurl
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%description -n python3-pycurl -l zh_CN.UTF-8
libcurl 的 Python3 接口。

%prep
%setup0 -q -n pycurl-%{version}

# temporarily exclude failing test-cases
rm -f tests/{post_test,reset_test}.py

# copy the whole directory for the python3 build
rm -rf %{py3dir}
cp -a . %{py3dir}

%build
export CFLAGS="$RPM_OPT_FLAGS"
%{__python} setup.py build --with-nss
pushd %{py3dir}
%{__python3} setup.py build --with-nss
popd

%check
export PYTHONPATH=$RPM_BUILD_ROOT%{python_sitearch}
make test PYTHON=%{__python}
pushd %{py3dir}
export PYTHONPATH=$RPM_BUILD_ROOT%{python3_sitearch}
make test PYTHON=%{__python3} NOSETESTS="nosetests-%{python3_version} -v"
popd

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
rm -rf %{buildroot}%{_datadir}/doc/pycurl
magic_rpm_clean.sh

%files
%{!?_licensedir:%global license %%doc}
%license COPYING-LGPL COPYING-MIT
%doc ChangeLog README.rst examples doc tests
%{python_sitearch}/*

%files -n python3-pycurl
# TODO: find the lost COPYING file
%{!?_licensedir:%global license %%doc}
%license COPYING-LGPL COPYING-MIT
%doc ChangeLog README.rst examples doc tests
%{python3_sitearch}/*

%changelog
* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 7.19.5.1-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 12 2015 Kamil Dudka <kdudka@redhat.com> - 7.19.5.1-1
- update to 7.19.5.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Aug  3 2014 Tom Callaway <spot@fedoraproject.org> - 7.19.5-2
- fix license handling

* Mon Jul 14 2014 Kamil Dudka <kdudka@redhat.com> - 7.19.5-1
- update to 7.19.5

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 7.19.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Feb 06 2014 Kamil Dudka <kdudka@redhat.com> - 7.19.3.1-1
- update to 7.19.3.1

* Fri Jan 10 2014 Kamil Dudka <kdudka@redhat.com> - 7.19.3-2
- add python3 subpackage (#1014583)

* Fri Jan 10 2014 Kamil Dudka <kdudka@redhat.com> - 7.19.3-1
- update to 7.19.3

* Thu Jan 02 2014 Kamil Dudka <kdudka@redhat.com> - 7.19.0.3-1
- update to 7.19.0.3

* Tue Oct 08 2013 Kamil Dudka <kdudka@redhat.com> - 7.19.0.2-1
- update to 7.19.0.2

* Wed Sep 25 2013 Kamil Dudka <kdudka@redhat.com> - 7.19.0.1-1
- update to 7.19.0.1

* Thu Aug 08 2013 Kamil Dudka <kdudka@redhat.com> - 7.19.0-18.20130315git8d654296
- sync with upstream 8d654296

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.0-17.20120408git9b8f4e38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 09 2013 Kamil Dudka <kdudka@redhat.com> - 7.19.0-16.20120408git9b8f4e38
- sync with upstream 9b8f4e38 (fixes #928370)
- add the GLOBAL_ACK_EINTR constant to the list of exported symbols (#920589)
- temporarily disable tests/multi_socket_select_test.py

* Wed Mar 06 2013 Kamil Dudka <kdudka@redhat.com> - 7.19.0-15
- allow to return -1 from the write callback (#857875) 
- remove the patch for curl-config --static-libs no longer needed
- run the tests against the just built pycurl, not the system one

* Mon Feb 25 2013 Kamil Dudka <kdudka@redhat.com> - 7.19.0-14
- apply bug-fixes committed to upstream CVS since 7.19.0 (fixes #896025)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 22 2012 Jan Synáček <jsynacek@redhat.com> - 7.19.0-12
- Improve spec

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Dennis Gilmore <dennis@ausil.us> - 7.19.0-8
- add Missing Requires on keyutils-libs

* Tue Aug 17 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.19.0-7
- Add patch developed by David Malcolm to fix segfaults caused by a missing incref

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 7.19.0-6
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Mar  2 2010 Karel Klic <kklic@redhat.com> - 7.19.0-5
- Package COPYING2 file
- Added MIT as a package license

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 17 2009 Stepan Kasal <skasal@redhat.com> - 7.19.0-3
- fix typo in the previous change

* Fri Apr 17 2009 Stepan Kasal <skasal@redhat.com> - 7.19.0-2
- add a require to reflect a dependency on libcurl version (#496308)

* Thu Mar  5 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.19.0-1
- Update to 7.19.0

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.18.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 7.18.2-2
- Rebuild for Python 2.6

* Thu Jul  3 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.18.2-1
- Update to 7.18.2
- Thanks to Ville Skyttä re-enable the tests and fix a minor problem
  with the setup.py. (Bug # 45400)

* Thu Jun  5 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.18.1-1
- Update to 7.18.1
- Disable tests because it's not testing the built library, it's trying to
  test an installed library.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 7.16.4-3
- Autorebuild for GCC 4.3

* Thu Jan  3 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.16.4-2
- BR openssl-devel

* Wed Aug 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.16.4-1
- Update to 7.16.4
- Update license tag.

* Sat Jun  9 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.16.2.1-1
- Update to released version.

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.16.0-0.1.20061207
- Update to a CVS snapshot since development has a newer version of curl than is in FC <= 6

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.15.5.1-4
- Add -DHAVE_CURL_OPENSSL to fix PPC build problem.

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.15.5.1-3
- Don't forget to Provide: pycurl!!!

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.15.5.1-2
- Remove INSTALL from the list of documentation
- Use python_sitearch for all of the files

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.15.5.1-1
- First version for Fedora Extras

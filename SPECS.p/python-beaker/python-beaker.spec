%if 0%{?fedora}
%global with_python3 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

%if 0%{?fedora} <= 16
%{!?python3_version: %global python3_version %(%{__python3} -c 'import sys ; sys.stdout.write("%s.%s" % sys.version_info[:2])')}
%endif

Name: python-beaker
Version: 1.5.4
Release: 8%{?dist}
Summary: WSGI middleware layer to provide sessions

Group: Development/Languages
License: BSD and MIT
URL: http://beaker.groovie.org/
Source0: http://pypi.python.org/packages/source/B/Beaker/Beaker-%{version}.tar.gz
Patch0: beaker-use-system-paste.patch
Patch1: beaker-disable-badtest.patch
Patch2: beaker-anydbm.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: python2-devel
BuildRequires: python-setuptools
# Needed for the test suite
BuildRequires: python-nose
BuildRequires: python-webtest
Requires: python-paste
%if 0%{?fedora}
Requires: pycryptopp
%else
Requires: python-crypto
%endif

%if 0%{?with_python3}
BuildRequires: /usr/bin/2to3
BuildRequires: python3-devel
BuildRequires: python3-setuptools
# Needed for complete test suite
#BuildRequires: python3-webtest
%if 0%{?fedora} > 14
BuildRequires: python3-nose
%endif
%endif # if with_python3

%description
Beaker is a caching library that includes Session and Cache objects built on
Myghty's Container API used in MyghtyUtils. WSGI middleware is also included to
manage Session objects and signed cookies.

%if 0%{?with_python3}
%package -n python3-beaker
Summary: WSGI middleware layer to provide sessions
Group: Development/Languages
# Paste is not python3 compatible at the moment
#Requires: python3-paste
# Without one of these there's no aes implementation which means there's no way to
# have encrypted cookies.  This is a reduction in features over the python2 version.
# Currently there's no working python3 port for either:
# http://allmydata.org/trac/pycryptopp/ticket/35
# http://lists.dlitz.net/pipermail/pycrypto/2010q2/000253.html
#%if 0%{?fedora}
#Requires: python3-pycryptopp
#%else
#Requires: python3-crypto
#%endif

%description -n python3-beaker
Beaker is a caching library that includes Session and Cache objects built on
Myghty's Container API used in MyghtyUtils. WSGI middleware is also included to
manage Session objects and signed cookies.
%endif # with_python3


%prep
%setup -q -n Beaker-%{version}
%patch0 -p1 -b .system
%patch1 -p1 -b .badtest
%patch2 -p1 -b .anydbm

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3


%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3


%check
PYTHONPATH=$(pwd) nosetests

#%%if 0%{?with_python3} && 0%{?fedora} > 14
#pushd %{py3dir}
#PYTHONPATH=$(pwd) nosetests-%{python3_version}
#popd
#%%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE CHANGELOG
%{python_sitelib}/beaker/
%{python_sitelib}/Beaker*

%if 0%{?with_python3}
%files -n python3-beaker
%defattr(-,root,root,-)
%{python3_sitelib}/beaker/
%{python3_sitelib}/Beaker*
%endif


%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 1.5.4-6
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 1.5.4-5
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 09 2012 Luke Macken <lmacken@redhat.com> - 1.5.4-3
- Remove the python3-paste dependency.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 6 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5.4-1
- Update to 1.5.4
- Fix for python3 module and anydbm
- Tried enabling unittests on python3 -- still no joy

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 27 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5.3-8
- Remove explicit call to 2to3; setup.py handles this

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.5.3-7
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Thu Aug 12 2010 Kyle VanderBeek <kylev@kylev.com> - 1.5.3-6
- Disable broken test_dbm_container2 test.

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jun 28 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5.3-4
- Add Requires for crypto libs so we have encrypted cookies
- Add patch to unbundle file that comes from paste

* Sun Jun 27 2010 Kyle VanderBeek <kylev@kylev.com> - 1.5.3-3
- Add python3 conditionals

* Thu May 06 2010 Luke Macken <lmacken@redhat.com> - 1.5.3-2
- Add a python3 subpackage

* Mon Mar 22 2010 Luke Macken <lmacken@redhat.com> - 1.5.3-1
- Update to 1.5.3
- Remove the abspath patch, which was fixed upstream
- Run the test suite

* Fri Jan 22 2010 Luke Macken <lmacken@redhat.com> - 1.5.1-1
- Update to 1.5.1
- Remove beaker-hmac2.4.patch, which made it into 1.4 upstream
- Remove middleware-config.patch which is also upstream

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Kyle VanderBeek <kylev@kylev.com> - 1.3.1-5
- Add patch based on upstream hg 403ef7c82d32 for config overwriting that
  breaks Pylons unit tests

* Sat Jun 27 2009 Luke Macken <lmacken@redhat.com> - 1.3.1-4
- Add a patch to remove the use of __future__.absolute_import in the google
  backend

* Sat Jun 20 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3.1-3
- Different hmac patch suitable for upstream inclusion.

* Tue Jun 02 2009 Luke Macken <lmacken@redhat.com> - 1.3.1-2
- Add a patch to remove Beaker's use of hashlib on Python2.4,
  due to incompatiblities with Python's hmac module (#503772)

* Sun May 31 2009 Luke Macken <lmacken@redhat.com> - 1.3.1-1
- Update to 1.3.1

* Tue Apr 07 2009 Felix Schwarz <felix.schwarz@oss.schwarz.eu> - 1.3-1
- Update to 1.3
 
* Sun Apr 05 2009 Felix Schwarz <felix.schwarz@oss.schwarz.eu> - 1.2.3-1
- Update to 1.2.3
 
* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 06 2009 Luke Macken <lmacken@redhat.com> - 1.1.3-1
- Update to 1.1.3

* Sat Dec 20 2008 Felix Schwarz <felix.schwarz@oss.schwarz.eu> - 1.1.2-1
- Update to 1.1.2
 
* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.3-2
- Rebuild for Python 2.6

* Tue Jun 24 2008 Felix Schwarz <felix.schwarz@oss.schwarz.eu> - 1.0.3-1
- Update to 1.0.3.

* Tue Jun 24 2008 Kyle VanderBeek <kylev@kylev.com> - 0.9.5-1
- Update to 0.9.5.
- Remove license patch which is now corrected upstream.

* Mon May 12 2008 Kyle VanderBeek <kylev@kylev.com> - 0.9.4-4
- Fix files to not use wildcard, fixing dir ownership

* Mon May 12 2008 Kyle VanderBeek <kylev@kylev.com> - 0.9.4-3
- Corrected license

* Mon May 12 2008 Kyle VanderBeek <kylev@kylev.com> - 0.9.4-2
- More restrictive file includes for safety

* Sun May 11 2008 Kyle VanderBeek <kylev@kylev.com> - 0.9.4-1
- Update to 0.9.4 (security fix)
- Fix rpmlint complaints, add CHANGELOG and LICENSE

* Wed Apr  9 2008 Kyle VanderBeek <kylev@kylev.com> - 0.9.3-1
- Initial version.

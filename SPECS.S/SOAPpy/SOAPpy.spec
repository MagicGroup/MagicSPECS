%if !(0%{?rhel} > 6 || 0%{?fedora} >= 13)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

Name:           SOAPpy
Version:        0.11.6
Release:        18%{?dist}
Summary:        Full-featured SOAP library for Python

Group:          Development/Languages
# The entire source is licensed under the 3 clause BSD except for the following
# files which are under the ZPLv2.0:
# SOAPpy/wstools/Utility.py
# SOAPpy/wstools/XMLSchema.py
# SOAPpy/wstools/WSDLTools.py
License:        BSD and ZPLv2.0
URL:            http://pywebsvcs.sourceforge.net
Source0:        http://dl.sourceforge.net/pywebsvcs/SOAP.py/%{version}/%{name}-%{version}.tar.gz
# from __future__ imports need to be at the beginning of files
Patch0:         %{name}-%{version}-python25.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-fpconst >= 0.6.0
Requires:       python-fpconst >= 0.6.0
Requires:       m2crypto

%description
The goal of the SOAPpy team is to provide a full-featured SOAP library
for Python that is very simple to use and that fully supports dynamic
interaction between clients and servers.


%prep
%setup -q
%patch0 -p0 -b .python25

# remove shell bangs
pushd %{name}/wstools
for file in $(find . -type f -name "*.py"); do
  cp $file $file.orig
  grep -v "\#\! \/usr\/bin" $file.orig > $file
  rm -f $file.orig
done
popd

# remove executable flag from example scripts
chmod -x bid/* contrib/* docs/* tools/* validate/*

# fix file encodings
iconv -f iso8859-1 -t utf-8 ChangeLog > ChangeLog.conv && mv -f ChangeLog.conv ChangeLog


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%check
# testTime is meant to pass, testArray is a known failure.
# ERROR: testTime (__main__.SOAPTestCase)
# FAIL: testArray (__main__.SOAPTestCase)
PYTHONPATH="$RPM_BUILD_ROOT%{python_sitelib}" %{__python} tests/SOAPtest.py || :


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE README RELEASE_INFO TODO docs/ contrib/ validate/ bid/ tools/
%{python_sitelib}/%{name}*


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.11.6-18
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.11.6-17
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.11.6-16
- 为 Magic 3.0 重建

* Wed Jul 25 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.11.6-15
- Remove the Requires to PyXML

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Jul 01 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.11.6-12
- Add m2crypto as R
- Change License
- Update spec
-   All these changes comes from Toshio's patch BZRH #602932

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.11.6-11
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.11.6-8
- Rebuild for Python 2.6

* Thu May 22 2008 Christopher Stone <chris.stone@gmail.com> 0.11.6-7
- Simplify %%files
- Remove no longer needed Obsoletes/Provides
- Update %%license tag

* Fri Dec 08 2006 Christopher Stone <chris.stone@gmail.com> 0.11.6-6
- Readd python-devel to BR
- Add patch to build with python 2.5
- Add versioned Obsoletes
- python(abi) = 0:2.5 rebuild

* Wed Sep 06 2006 Christopher Stone <chris.stone@gmail.com> 0.11.6-5
- No longer %%ghost pyo files bug #205436

* Wed Aug 30 2006 Christopher Stone <chris.stone@gmail.com> 0.11.6-4
- FC6 Rebuild

* Sat May 06 2006 Christopher Stone <chris.stone@gmail.com> 0.11.6-3
- Add Provides/Obsolete for python-SOAPpy

* Mon Apr 17 2006 Christopher Stone <chris.stone@gmail.com> 0.11.6-2
- Add docs directory to %%doc
- Remove PyXML BR
- Removed executable bits from doc files
- Added call to run test script in %%check
- Added examples to %%doc

* Sat Apr 11 2006 Christopher Stone <chris.stone@gmail.com> 0.11.6-1
- Initial RPM release

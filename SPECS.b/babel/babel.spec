# only Fedora 20 has Babel >= 1.0 which is the first version supporting Python 3
%if 0%{?fedora} >= 20
%global with_python3 1
%endif

Name:           babel
Version:        1.3
Release:        3%{?dist}
Summary:        Tools for internationalizing Python applications
Summary(zh_CN.UTF-8): 国际化 Python 程序的工具

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        BSD
URL:            http://babel.pocoo.org/
Source0:        https://pypi.python.org/packages/source/B/Babel/Babel-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-setuptools-devel
BuildRequires:  pytz

# build the documentation
BuildRequires:  make
BuildRequires:  python-sphinx

Requires:       python-babel
Requires:       python-setuptools
Requires:       pytz

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytz
%endif

%description
Babel is composed of two major parts:

* tools to build and work with gettext message catalogs

* a Python interface to the CLDR (Common Locale Data Repository),
  providing access to various locale display names, localized number
  and date formatting, etc.

%description -l zh_CN.UTF-8
Babel 由两部分组成：

* 

%package -n python-babel
Summary:        Library for internationalizing Python applications
Group:          Development/Languages

%description -n python-babel
Babel is composed of two major parts:

* tools to build and work with gettext message catalogs

* a Python interface to the CLDR (Common Locale Data Repository),
  providing access to various locale display names, localized number
  and date formatting, etc.

%if 0%{?with_python3}
%package -n python3-babel
Summary:        Library for internationalizing Python applications
Group:          Development/Languages

Requires:       python3-babel
Requires:       python3-setuptools
Requires:       python3-pytz

%description -n python3-babel
Babel is composed of two major parts:

* tools to build and work with gettext message catalogs

* a Python interface to the CLDR (Common Locale Data Repository),
  providing access to various locale display names, localized number
  and date formatting, etc.
%endif

%package doc
Summary:        Documentation for Babel
Group:          Development/Languages
Provides:       python-babel-doc = %{version}-%{release}
%if 0%{?with_python3}
Provides:       python3-babel-doc = %{version}-%{release}
%endif

%description doc
Documentation for Babel

%prep
%setup0 -q -n Babel-%{version}
chmod a-x babel/messages/frontend.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -r . %{py3dir}
%endif

%build
%{__python} setup.py build

# build the docs and remove all source files (.rst, Makefile) afterwards
cd docs
make html
mv _build/html .
rm -rf _* api *.rst conf.py objects.inv Makefile make.bat
mv html/* .
rm -rf html

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
rm -rf %{buildroot}
# install python3 build before python2 build so executables from the former
# don't overwrite those from the latter
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --no-compile --root %{buildroot}
popd
%endif

%{__python} setup.py install --skip-build --no-compile --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE README AUTHORS
%{_bindir}/pybabel

%files -n python-babel
%defattr(-,root,root,-)
%{python_sitelib}/Babel-%{version}-py*.egg-info
%{python_sitelib}/babel

%if 0%{?with_python3}
%files -n python3-babel
%defattr(-,root,root,-)
%{python3_sitelib}/Babel-%{version}-py*.egg-info
%{python3_sitelib}/babel
%endif

%files doc
%doc docs/*

%changelog
* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 1.3-3
- 为 Magic 3.0 重建

* Sun Oct 06 2013 Felix Schwarz <fschwarz@fedoraproject.org> - 1.3-2
- enable python3 subpackage

* Wed Oct 02 2013 Felix Schwarz <fschwarz@fedoraproject.org> - 1.3-1
- update to Babel 1.3
- disabled %%check as it tries to download the CLDR

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 26 2013 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.6-8
- split documentation off to a separate subpackage

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 18 2012 Nils Philippsen <nils@redhat.com> - 0.9.6-6
- run tests in %%check
- add pytz build requirement for tests

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 0.9.6-5
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Wed Aug 01 2012 Felix Schwarz <felix.schwarz@oss.schwarz.eu> - 0.9.6-4
- disable building of non-functional python3 subpackage (#761583)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 07 2011 Nils Philippsen <nils@redhat.com> - 0.9.6-1
- version 0.9.6:
  * Backport r493-494: documentation typo fixes.
  * Make the CLDR import script work with Python 2.7.
  * Fix various typos.
  * Fixed Python 2.3 compatibility (ticket #146, #233).
  * Sort output of list-locales.
  * Make the POT-Creation-Date of the catalog being updated equal to
    POT-Creation-Date of the template used to update (ticket #148).
  * Use a more explicit error message if no option or argument (command) is
    passed to pybabel (ticket #81).
  * Keep the PO-Revision-Date if it is not the default value (ticket #148).
  * Make --no-wrap work by reworking --width's default and mimic xgettext's
    behaviour of always wrapping comments (ticket #145).
  * Fixed negative offset handling of Catalog._set_mime_headers (ticket #165).
  * Add --project and --version options for commandline (ticket #173).
  * Add a __ne__() method to the Local class.
  * Explicitly sort instead of using sorted() and don't assume ordering
    (Python 2.3 and Jython compatibility).
  * Removed ValueError raising for string formatting message checkers if the
    string does not contain any string formattings (ticket #150).
  * Fix Serbian plural forms (ticket #213).
  * Small speed improvement in format_date() (ticket #216).
  * Fix number formatting for locales where CLDR specifies alt or draft
    items (ticket #217)
  * Fix bad check in format_time (ticket #257, reported with patch and tests by
    jomae)
  * Fix so frontend.CommandLineInterface.run does not accumulate logging
    handlers (#227, reported with initial patch by dfraser)
  * Fix exception if environment contains an invalid locale setting (#200)
- install python2 rather than python3 executable (#710880)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug 26 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.5-3
- Add python3 subpackage

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Apr  7 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.5-1
- This release contains a small number of bugfixes over the 0.9.4
- release.
-
- What's New:
- -----------
- * Fixed the case where messages containing square brackets would break
-  with an unpack error
- * Fuzzy matching regarding plurals should *NOT* be checked against
-  len(message.id) because this is always 2, instead, it's should be
-  checked against catalog.num_plurals (ticket #212).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Mar 28 2009 Robert Scheck <robert@fedoraproject.org> - 0.9.4-4
- Added missing requires to python-setuptools for pkg_resources

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.9.4-2
- Rebuild for Python 2.6

* Mon Aug 25 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.4-1
- Update to 0.9.4

* Thu Jul 10 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.3-1
- Update to 0.9.3

* Sun Dec 16 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.1-1
- Update to 0.9.1

* Tue Aug 28 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9-2
- BR python-setuptools-devel

* Mon Aug 27 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9-1
- Update to 0.9

* Mon Jul  2 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8.1-1
- Update to 0.8.1
- Remove upstreamed patch.

* Fri Jun 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8-3
- Replace patch with one that actually applies.

* Fri Jun 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8-2
- Apply upstream patch to rename command line script to "pybabel" - BZ#246208

* Thu Jun 21 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8-1
- First version for Fedora


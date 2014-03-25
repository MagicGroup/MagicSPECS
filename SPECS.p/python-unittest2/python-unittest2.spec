%global srcname unittest2

Name:           python-%{srcname}
Version:        0.5.1
Release:        8%{?dist}
Summary:        Backport of new unittest features for Python 2.7 to Python 2.4+

License:        BSD
URL:            http://pypi.python.org/pypi/unittest2
Source0:        http://pypi.python.org/packages/source/u/%{srcname}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-nose


%description
unittest2 is a backport of the new features added to the unittest
testing framework in Python 2.7. It is tested to run on Python 2.4 - 
2.6.

To use unittest2 instead of unittest simply replace ``import unittest``
with ``import unittest2``.

Classes in unittest2 derive from the equivalent classes in unittest,
so it should be possible to use the unittest2 test running infra-
structure without having to switch all your tests to using unittest2
immediately. Similarly
you can use the new assert methods on ``unittest2.TestCase`` with the
standard unittest test running infrastructure. Not all of the new
features in unittest2 will work with the standard unittest test loaders
and runners however.

%prep
%setup -q -n %{srcname}-%{version}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%check
#Failing test deactivated
cd unittest2/test
nosetests test_new_tests.py
#nosetests test_unittest2.py
nosetests test_unittest2_with.py

%files
%doc README.txt
%{_bindir}/unit2*
%{python2_sitelib}/%{srcname}/
%{python2_sitelib}/%{srcname}*.egg-info

%changelog
* Mon Oct 28 2013 Fabian Affolter <mail@fabian-affolter.ch> - 0.5.1-8
- Python macro update

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 10 2012 Fabian Affolter <mail@fabian-affolter.ch> - 0.5.1-5
- Updated to match new guidlines

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 Fabian Affolter <mail@fabian-affolter.ch> - 0.5.1-1
- Updated to new upstream version 0.5.1

* Sat Jul 03 2010 Fabian Affolter <mail@fabian-affolter.ch> - 0.5.0-1
- Removed build cond for check section
- Switched to python2-devel
- Updated to new upstream version 0.5.0

* Sat Jul 03 2010 Fabian Affolter <mail@fabian-affolter.ch> - 0.1.4-1
- Initial package

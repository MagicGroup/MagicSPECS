%global srcname google-apputils
%global _docdir_fmt %{name}

Name:           python-%{srcname}
Version:        0.4.2
Release:        3%{?dist}
Summary:        Google Application Utilities for Python

License:        ASL 2.0
URL:            https://github.com/google/%{srcname}
Source0:        https://pypi.python.org/packages/source/g/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-dateutil
BuildRequires:  python-gflags
BuildRequires:  pytz
# For tests
BuildRequires:  python-mox
Requires:       python-dateutil
Requires:       python-gflags
Requires:       pytz

%description
This project is a small collection of utilities for building Python
applications. It includes some of the same set of utilities used to build and
run internal Python apps at Google.

Features:

* Simple application startup integrated with python-gflags.
* Subcommands for command-line applications.
* Option to drop into pdb on uncaught exceptions.
* Helper functions for dealing with files.
* High-level profiling tools.
* Timezone-aware wrappers for datetime.datetime classes.
* Improved TestCase with the same methods as unittest2, plus helpful flags for
  test startup.
* google_test setuptools command for running tests.
* Helper module for creating application stubs.

%package -n python3-%{srcname}
Summary:        Google Application Utilities for Python 3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python-tools
BuildRequires:  python3-dateutil
BuildRequires:  python3-gflags
BuildRequires:  python3-pytz
# For tests
# python-mox doesn't work with python3
# https://bugzilla.redhat.com/show_bug.cgi?id=1209203
#BuildRequires:  python3-mox
Requires:       python3-dateutil
Requires:       python3-gflags
Requires:       python3-pytz

%description -n python3-%{srcname}
This project is a small collection of utilities for building Python 3
applications. It includes some of the same set of utilities used to build and
run internal Python apps at Google.

Features:

* Simple application startup integrated with python-gflags.
* Subcommands for command-line applications.
* Option to drop into pdb on uncaught exceptions.
* Helper functions for dealing with files.
* High-level profiling tools.
* Timezone-aware wrappers for datetime.datetime classes.
* Improved TestCase with the same methods as unittest2, plus helpful flags for
  test startup.
* google_test setuptools command for running tests.
* Helper module for creating application stubs.


%prep
%setup -qc
mv %{srcname}-%{version} python2
# Strip shbang
find -name \*.py | xargs sed -i '/^#!\/usr\/bin\/.*python/d'
# setup cannot handle pytz versioning
sed -i -e 's/pytz>.*"/pytz"/' python2/setup.py
cp -a python2 python3
2to3 --write --nobackups python3


%build
pushd python2
%{__python2} setup.py build
popd
pushd python3
%{__python3} setup.py build
popd


%install
pushd python3
%{__python3} setup.py install --skip-build --root %{buildroot}
popd

pushd python2
%{__python2} setup.py install --skip-build --root %{buildroot}
popd


%check
pushd python2
%{__python2} setup.py test
popd
# python-mox doesn't work with python3 
#pushd python3
#%{__python3} setup.py test
#popd

 
%files
%license python2/LICENSE
%doc python2/README
%{python2_sitelib}/*

%files -n python3-%{srcname}
%license python3/LICENSE
%doc python3/README
%{python3_sitelib}/*


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 21 2015 Orion Poplawski <orion@cora.nwra.com> - 0.4.2-2
- Use _docdir_fmt macro
- Fix changelog
- Strip shbang from python library files

* Mon Apr  6 2015 Orion Poplawski <orion@cora.nwra.com> - 0.4.2-1
- Initial package

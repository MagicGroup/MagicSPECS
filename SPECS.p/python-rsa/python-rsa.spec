%global pkgname rsa

%if 0%{?fedora} > 12
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-rsa
Version:        3.1.1
Release:        7%{?dist}
Summary:        Pure-Python RSA implementation

License:        ASL 2.0
URL:            http://stuvel.eu/rsa
Source0:        https://pypi.python.org/packages/source/r/rsa/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pyasn1
BuildRequires:  python-unittest2
%if %with python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pyasn1
%endif

%description
Pure-Python RSA implementation.

%package -n python3-rsa
Summary:        Pure-Python RSA implementation

%description -n python3-rsa
Pure-Python RSA implementation for Python 3.

%prep
%setup -q -n %{pkgname}-%{version}
rm -rf %{pkgname}-*.egg-info
sed -i "/from distribute_setup import use_setuptools/d" setup.py
sed -i "/use_setuptools('0.6.10')/d" setup.py

%if %with python3
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%if %with python3
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%{__python2} setup.py build

%install
%if %with python3
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
for B in %{buildroot}%{_bindir}/pyrsa-*
        do mv $B $(echo $B |sed 's/pyrsa-/python3-pyrsa/'); done
popd
%endif

%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%check
%if %with python3
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif

%{__python2} setup.py test

%files
%doc LICENSE
%{_bindir}/pyrsa*
%{python2_sitelib}/rsa
%{python2_sitelib}/rsa-*.egg-info

%if %with python3
%files -n python3-rsa
%doc LICENSE
%{_bindir}/python3-pyrsa*
%{python3_sitelib}/rsa
%{python3_sitelib}/rsa-*.egg-info
%endif

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 3.1.1-6
- Add Python 3 subpackage

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 05 2013 Yohan Graterol <yohangraterol92@gmail.com> - 3.1.1-4
- Fix build in F20
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 26 2013 Yohan Graterol <yohangraterol92@gmail.com> - 3.1.1-2
- Change license name, remove MANIFEST.in
* Sun May 19 2013 Yohan Graterol <yohangraterol92@gmail.com> - 3.1.1-1
- Initial packaging 

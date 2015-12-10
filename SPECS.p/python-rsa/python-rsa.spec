%bcond_without python3

%define pkgname rsa

Name:           python-rsa
Version:	3.2
Release:	3%{?dist}
Summary:        Pure-Python RSA implementation
Summary(zh_CN.UTF-8): 纯 Python 的 RSA 实现

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

%description -l zh_CN.UTF-8
纯 Python 的 RSA 实现。

%package -n python3-rsa
Summary:        Pure-Python RSA implementation
Summary(zh_CN.UTF-8): 纯 Python 的 RSA 实现

%description -n python3-rsa
Pure-Python RSA implementation for Python 3.

%description -n python3-rsa -l zh_CN.UTF-8
纯 Python 的 RSA 实现

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
magic_rpm_clean.sh

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
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 3.2-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 3.2-2
- 为 Magic 3.0 重建

* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 3.2-1
- 更新到 3.2

* Wed Aug 19 2015 Liu Di <liudidi@gmail.com> - 3.1.1-8
- 为 Magic 3.0 重建

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

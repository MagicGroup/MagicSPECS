%global with_python3 1

Name:           python-service-identity
Version:        14.0.0
Release:        5%{?dist}
Summary:        Service identity verification for pyOpenSSL
Summary(zh_CN.UTF-8): pyOpenSSL 的服务名称校验

License:        MIT
URL:            https://github.com/pyca/service_identity
Source0:        https://pypi.python.org/packages/source/s/service_identity/service_identity-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
# Fedora 20 doesn't have a new enough version of pytest,
# so skip running the tests there.
# For tests
BuildRequires:  pytest >= 2.5
BuildRequires:  python-characteristic
BuildRequires:  python-pyasn1
BuildRequires:  python-pyasn1-modules
BuildRequires:  pyOpenSSL >= 0.12
BuildRequires:  python-idna

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# For tests
BuildRequires:  python3-pytest >= 2.5
BuildRequires:  python3-characteristic
BuildRequires:  python3-pyasn1
BuildRequires:  python3-pyasn1-modules
BuildRequires:  python3-pyOpenSSL >= 0.12
BuildRequires:  python3-idna
%endif # with_python3

Requires:       python-characteristic
Requires:       python-pyasn1
Requires:       python-pyasn1-modules
Requires:       pyOpenSSL >= 0.12
Requires:       python-idna

%if 0%{?with_python3}
%package -n python3-service-identity
Summary:        Logging as Storytelling
Summary(zh_CN.UTF-8):  pyOpenSSL 的服务名称校验
Requires:       python3-six
Requires:       python3-characteristic
Requires:       python3-pyasn1
Requires:       python3-pyasn1-modules
Requires:       python3-pyOpenSSL >= 0.12
Requires:       python3-idna
%endif # with_python3

%description
Service Identity Verification for pyOpenSSL

TL;DR: Use this package if you use pyOpenSSL and don’t want to be MITMed.

service_identity aspires to give you all the tools you need for verifying
whether a certificate is valid for the intended purposes.

In the simplest case, this means host name verification. However,
service_identity implements RFC 6125 fully and plans to add other relevant RFCs
too.

%description -l zh_CN.UTF-8
pyOpenSSL 的服务名称校验。


%if 0%{?with_python3}
%description -n python3-service-identity
Service Identity Verification for pyOpenSSL

TL;DR: Use this package if you use pyOpenSSL and don’t want to be MITMed.

service_identity aspires to give you all the tools you need for verifying
whether a certificate is valid for the intended purposes.

In the simplest case, this means host name verification. However,
service_identity implements RFC 6125 fully and plans to add other relevant RFCs
too.
%description -n python3-service-identity -l zh_CN.UTF-8
pyOpenSSL 的服务名称校验。

%endif # with_python3

%prep
%setup -q -n service_identity-%{version}
# Remove bundled egg-info
rm -rf service_identity.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3


%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%check

# https://bitbucket.org/hpk42/pytest/issue/539/pytest-doctest-modules-fails-if-python
echo "collect_ignore = ['build']" >> conftest.py
py.test --doctest-modules --doctest-glob='*.rst'

%if 0%{?with_python3}
pushd %{py3dir}
# https://bitbucket.org/hpk42/pytest/issue/539/pytest-doctest-modules-fails-if-python
echo "collect_ignore = ['build']" >> conftest.py
py.test --doctest-modules --doctest-glob='*.rst'
popd
%endif # with_python3

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3

%{__python2} setup.py install --skip-build --root %{buildroot}
magic_rpm_clean.sh


%files
%doc README.rst LICENSE
%{python2_sitelib}/service_identity
%{python2_sitelib}/service_identity-%{version}-py%{python2_version}.egg-info

%if 0%{?with_python3}
%files -n python3-service-identity
%doc README.rst LICENSE
%{python3_sitelib}/service_identity
%{python3_sitelib}/service_identity-%{version}-py%{python3_version}.egg-info
%endif # with_python3

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 14.0.0-5
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 14.0.0-4
- 为 Magic 3.0 重建

* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 14.0.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 22 2015 robyduck@fedoraproject.org - 14.0.0-1
- Build new version

* Sat Jul 12 2014 tom.prince@twistedmatrix.com - 1.0.0-2
- Add python-idna dependency.

* Sat Jul 12 2014 tom.prince@twistedmatrix.com - 1.0.0-1
- Initial package.

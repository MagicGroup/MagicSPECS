%global with_python3 1

%global srcname ecdsa

Name:           python-%{srcname}
Version:	0.13
Release:	3%{?dist}
Summary:        ECDSA cryptographic signature library
Summary(zh_CN.UTF-8): ECDSA 加密签名库

License:        MIT
URL:            https://pypi.python.org/pypi/ecdsa
# Remove the prime192v1 and secp224r1 curves for now
# https://bugzilla.redhat.com/show_bug.cgi?id=1067697
#Source0:        %{srcname}-%{version}-clean.tar.gz
Source0:        https://pypi.python.org/packages/source/e/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-six
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
%endif
# For tests
BuildRequires:  openssl
Requires:       python-six

%description
This is an easy-to-use implementation of ECDSA cryptography (Elliptic Curve
Digital Signature Algorithm), implemented purely in Python, released under
the MIT license. With this library, you can quickly create keypairs (signing
key and verifying key), sign messages, and verify the signatures. The keys
and signatures are very short, making them easy to handle and incorporate
into other protocols.

NOTE: The prime192v1 and secp224r1 curves are currently disabled.

%description -l zh_CN.UTF-8
ECDSA 加密签名库。

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        ECDSA cryptographic signature library
Summary(zh_CN.UTF-8): ECDSA 加密签名库
Requires:       python3-six

%description -n python3-%{srcname}
This is an easy-to-use implementation of ECDSA cryptography (Elliptic Curve
Digital Signature Algorithm), implemented purely in Python, released under
the MIT license. With this library, you can quickly create keypairs (signing
key and verifying key), sign messages, and verify the signatures. The keys
and signatures are very short, making them easy to handle and incorporate
into other protocols.

NOTE: The prime192v1 and secp224r1 curves are currently disabled.
%description -n python3-%{srcname} -l zh_CN.UTF-8
ECDSA 加密签名库。
%endif # with_python3


%prep
%setup -q -n %{srcname}-%{version}
rm -rf %{srcname}.egg-info
# Remove extraneous #!
find ecdsa -name \*.py | xargs sed -ie '/\/usr\/bin\/env/d'
# Use system python-six
find -name \*.py | xargs sed -ie 's/from \(ecdsa\|\)\.six/from six/g'
rm ecdsa/six.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3


%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
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

%check
%{__python2} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif # with_python3

 
%files
%doc LICENSE NEWS PKG-INFO README.md
%{python2_sitelib}/*

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc LICENSE NEWS PKG-INFO README.md
%{python3_sitelib}/*
%endif # with_python3


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.13-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.13-2
- 为 Magic 3.0 重建

* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 0.13-1
- 更新到 0.13

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 10 2014 Orion Poplawski <orion@cora.nwra.com> - 0.11-2
- Rebuild for Python 3.4

* Sat May 10 2014 Orion Poplawski <orion@cora.nwra.com> - 0.11-1
- Update to 0.11

* Mon Feb 24 2014 Orion Poplawski <orion@cora.nwra.com> - 0.10-3
- Add python3 package

* Mon Feb 24 2014 Orion Poplawski <orion@cora.nwra.com> - 0.10-2
- Use system python-six
- Remove extraneous #!s

* Fri Feb 21 2014 Orion Poplawski <orion@cora.nwra.com> - 0.10-1
- Initial package

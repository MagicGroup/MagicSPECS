%global with_python3 1

%global modname cryptography-vectors
%global pymodname cryptography_vectors

Name:               python-%{modname}
Version:            1.0
Release:            3%{?dist}
Summary:            Test vectors for the cryptography package
Summary(zh_CN.UTF-8): 加密库包的测试向量

Group:              Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:            ASL 2.0 or BSD
URL:                http://pypi.python.org/pypi/cryptography-vectors
Source0:            https://pypi.python.org/packages/source/c/%{modname}/cryptography_vectors-%{version}.tar.gz

BuildArch:          noarch
BuildRequires:      python2-devel python-setuptools
%if 0%{?with_python3}
BuildRequires:      python3-devel python3-setuptools
%endif

%description
Test vectors for the cryptography package.

The only purpose of this package is to be a building requirement for
python-cryptography, otherwise it has no use. Don’t install it unless
you really know what you are doing.

%description -l zh_CN.UTF-8
加密库包的测试向量。

%if 0%{?with_python3}
%package -n  python3-%{modname}
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary:        Test vectors for the cryptography package
Summary(zh_CN.UTF-8): 加密库包的测试向量

%description -n python3-%{modname}
Test vectors for the cryptography package.

The only purpose of this package is to be a building requirement for
python-cryptography, otherwise it has no use. Don’t install it unless
you really know what you are doing.

%description -n python3-%{modname} -l zh_CN.UTF-8
加密库包的测试向量。
%endif

%prep
%setup -q -n %{pymodname}-%{version}

# Remove bundled egg-info in case it exists
rm -rf %{modname}.egg-info


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build
%if 0%{?with_python3}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
%endif

%install
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}
%if 0%{?with_python3}
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
%endif
magic_rpm_clean.sh

%check
%{__python2} setup.py test
%if 0%{?with_python3}
%{__python3} setup.py test
%endif

%files
%doc LICENSE
%{python2_sitelib}/%{pymodname}/
%{python2_sitelib}/%{pymodname}-%{version}*

%if 0%{?with_python3}
%files -n python3-%{modname}
%doc LICENSE
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}*
%endif


%changelog
* Sun Aug 23 2015 Liu Di <liudidi@gmail.com> - 1.0-3
- 为 Magic 3.0 重建

* Mon Aug 17 2015 Liu Di <liudidi@gmail.com> - 1.0-2
- 为 Magic 3.0 重建

* Wed Aug 12 2015 Nathaniel McCallum <npmccallum@redhat.com> - 1.0-1
- New upstream release

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.9-1
- New upstream release

* Fri Apr 17 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.8.2-1
- New upstream release

* Fri Mar 13 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.8-1
- New upstream release

* Wed Mar 04 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.7.2-2
- Add python3 subpackage

* Wed Mar 04 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.7.2-1
- New upstream release
- Now licensed under Apache 2.0 or BSD

* Thu Oct 16 2014 Matej Cepl <mcepl@redhat.com> - 0.6.1-1
- New upstream release (fixes among others #1153501)

* Wed Oct 01 2014 Matej Cepl <mcepl@redhat.com> - 0.5.4-3
- Add LICENSE file from the upstream repo.

* Mon Sep 29 2014 Matej Cepl <mcepl@redhat.com> - 0.5.4-2
- initial package for Fedora

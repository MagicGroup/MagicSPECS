# Created by pyp2rpm-1.1.1
%global pypi_name unittest2
%global with_python3 1

Name:           python-%{pypi_name}
Version:	1.1.0
Release:	3%{?dist}
Summary:        The new features in unittest backported to Python 2.4+
Summary(zh_CN.UTF-8): 单元测试模块

License:        BSD
URL:            http://pypi.python.org/pypi/unittest2
Source0:        https://pypi.python.org/packages/source/u/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-six
Requires:       python-setuptools
Requires:       python-six

%if %{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
%endif # if with_python3


%description
unittest2 is a backport of the new features added to the unittest testing
framework in Python 2.7 and onwards. It is tested to run on Python 2.6, 2.7,
3.2, 3.3, 3.4 and pypy.

%description -l zh_CN.UTF-8
单元测试模块。

%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        The new features in unittest backported to Python 2.4+
Summary(zh_CN.UTF-8): 单元测试模块
Requires:       python3-setuptools
Requires:       python3-six

%description -n python3-%{pypi_name}
unittest2 is a backport of the new features added to the unittest testing
framework in Python 2.7 and onwards. It is tested to run on Python 2.6, 2.7,
3.2, 3.3, 3.4 and pypy.
%description -n python3-%{pypi_name} -l zh_CN.UTF-8
单元测试模块。
%endif # with_python3

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

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
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/unit2 %{buildroot}/%{_bindir}/python3-unit2
popd
%endif # with_python3

%{__python2} setup.py install --skip-build --root %{buildroot}
magic_rpm_clean.sh

%check
%{__python2} -m unittest2

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} -m unittest2
popd
%endif # with_python3


%files
%doc README.txt
%{_bindir}/unit2
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.txt
%{_bindir}/python3-unit2
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif # with_python3

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.1.0-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.1.0-2
- 为 Magic 3.0 重建

* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 1.1.0-1
- 更新到 1.1.0

* Wed Aug 19 2015 Liu Di <liudidi@gmail.com> - 0.8.0-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Nov 14 2014 Slavek Kabrda <bkabrda@redhat.com> - 0.8.0-2
- Bump to avoid collision with previously blocked 0.8.0-1

* Mon Nov 10 2014 Slavek Kabrda <bkabrda@redhat.com> - 0.8.0-1
- Unretire the package, create a fresh specfile

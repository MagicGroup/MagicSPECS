%bcond_without python3

%global srcname pretend

Name:           python-pretend
Version:        1.0.8
Release:        5%{?dist}
Summary:        A library for stubbing in Python
Summary(zh_CN.UTF-8): Python 的存根库

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        BSD
URL:            https://github.com/alex/pretend
Source0:        https://pypi.python.org/packages/source/p/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-setuptools
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif


%description
Pretend is a library to make stubbing with Python easier.

%description -l zh_CN.UTF-8
Python 的存根库。

%if %{with python3}
%package -n python3-pretend
Summary:        A library for stubbing in Python
Summary(zh_CN.UTF-8): Python 的存根库
License:        BSD


%description -n python3-pretend
Pretend is a library to make stubbing with Python easier.
%description -n python3-pretend -l zh_CN.UTF-8
Python 的存根库。
%endif


%prep
%setup -q -n %{srcname}-%{version}

# Delete upstream supplied egg-info
rm -rf *.egg-info

%if %{with python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
%{__python2} setup.py build

%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif


%install
%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif

%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
magic_rpm_clean.sh

%files
%doc PKG-INFO README.rst LICENSE.rst
%{python2_sitelib}/pretend.py*
%{python2_sitelib}/pretend-%{version}-py2.?.egg-info

%if %{with python3}
%files -n python3-pretend
%doc PKG-INFO README.rst LICENSE.rst
%{python3_sitelib}/pretend.py
%{python3_sitelib}/__pycache__/pretend.cpython-3?.py*
%{python3_sitelib}/pretend-%{version}-py3.?.egg-info
%endif


%changelog
* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 1.0.8-5
- 为 Magic 3.0 重建

* Mon Aug 17 2015 Liu Di <liudidi@gmail.com> - 1.0.8-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Nov 22 2014 Piotr Popieluch <piotr1212@gmail.com> - 1.0.8-2
- Added epel support

* Mon Oct 20 2014 Piotr Popieluch <piotr1212@gmail.com> - 1.0.8-1
- Initial package

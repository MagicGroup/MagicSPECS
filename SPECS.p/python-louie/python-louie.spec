%define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")

Summary: Dispatches signals between Python objects in a wide variety of contexts
Summary(zh_CN.UTF-8): 分派各种 Python 环境之间的信号
Name: python-louie
Version: 1.1
Release: 10%{?dist}
License: BSD
Group: Development/Languages
Group(zh_CN.UTF-8): 开发/语言
URL: http://pylouie.org/
Source: http://cheeseshop.python.org/packages/source/L/Louie/Louie-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: python-setuptools
# From the egg requires.txt
Requires: python-nose >= 0.8.3
BuildRequires: python-devel
# Must have setuptools to build the package
# The build portions moved to a subpackage in F-8
BuildRequires: python-setuptools
BuildArch: noarch

%description
Louie provides Python programmers with a straightforward way to dispatch
signals between objects in a wide variety of contexts. It is based on
PyDispatcher, which in turn was based on a highly-rated recipe in the
Python Cookbook.

%description -l zh_CN.UTF-8
分派各种 Python 环境之间的信号。

%prep
%setup -q -n Louie-%{version}


%build
%{__python} setup.py build


%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}
magic_rpm_clean.sh

%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc doc/*
%{python_sitelib}/Louie-*.egg-info/
%{python_sitelib}/louie/


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.1-10
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.1-9
- 为 Magic 3.0 重建

* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 1.1-8
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.1-7
- 为 Magic 3.0 重建



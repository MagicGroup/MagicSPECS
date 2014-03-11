%define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")

Summary: Dispatches signals between Python objects in a wide variety of contexts
Name: python-louie
Version: 1.1
Release: 7%{?dist}
License: BSD
Group: Development/Languages
URL: http://pylouie.org/
Source: http://cheeseshop.python.org/packages/source/L/Louie/Louie-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: python-setuptools
# From the egg requires.txt
Requires: python-nose >= 0.8.3
BuildRequires: python-devel
# Must have setuptools to build the package
# The build portions moved to a subpackage in F-8
BuildRequires: python-setuptools-devel
BuildArch: noarch

%description
Louie provides Python programmers with a straightforward way to dispatch
signals between objects in a wide variety of contexts. It is based on
PyDispatcher, which in turn was based on a highly-rated recipe in the
Python Cookbook.


%prep
%setup -q -n Louie-%{version}


%build
%{__python} setup.py build


%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc doc/*
%{python_sitelib}/Louie-*.egg-info/
%{python_sitelib}/louie/


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.1-7
- 为 Magic 3.0 重建



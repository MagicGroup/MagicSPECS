%if 0%{?fedora}
%global with_python3 1
%endif

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%global srcname iso8601

Name:           python-%{srcname}
Version:        0.1.10
Release:        5%{?dist}
Summary:        Simple module to parse ISO 8601 dates

Group:          Development/Languages
License:        MIT
URL:            http://pypi.python.org/pypi/%{srcname}/
Source0:        http://pypi.python.org/packages/source/i/%{srcname}/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python2-devel python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel python3-setuptools
%endif

%description
This module parses the most common forms of ISO 8601 date strings
(e.g. 2007-01-14T20:34:22+00:00) into datetime objects.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        Simple module to parse ISO 8601 dates
Group:          Development/Languages

%description -n python3-%{srcname}
This module parses the most common forms of ISO 8601 date strings
(e.g. 2007-01-14T20:34:22+00:00) into datetime objects.
%endif

%prep
%setup -qn %{srcname}-%{version}

%if 0%{?with_python3}
cp -a . %{py3dir}
%endif


%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

%files
%defattr(-,root,root,-)
%doc LICENSE README.rst
%{python2_sitelib}/*

%if 0%{?with_python3}
%files -n python3-%{srcname}
%defattr(-,root,root,-)
%doc LICENSE README.rst
%{python3_sitelib}/*
%endif

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Apr 23 2014 Pádraig Brady <pbrady@redhat.com> - 0.1.10-2
- Add python3 package

* Thu Mar 27 2014 Pádraig Brady <pbrady@redhat.com> - 0.1.10-1
- Latest upstream

* Tue Nov 12 2013 Pádraig Brady <pbrady@redhat.com> - 0.1.8-1
- Latest upstream

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul  9 2010 Ian Weller <iweller@redhat.com> - 0.1.4-2
- Correct python_sitelib macro

* Mon Jun 28 2010 Ian Weller <iweller@redhat.com> - 0.1.4-1
- Initial package build

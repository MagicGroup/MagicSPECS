%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%if 0%{?fedora} > 12 || 0%{?rhel} > 7
%global with_python3 1

%global __python3 python3

%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:           python-six
Version:        1.4.1
Release:        1%{?dist}
Summary:        Python 2 and 3 compatibility utilities

Group:          Development/Languages
License:        MIT
URL:            http://pypi.python.org/pypi/six/
Source0:        http://pypi.python.org/packages/source/s/six/six-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
# For use by selftests:
BuildRequires:  pytest
BuildRequires:  tkinter
%if 0%{?with_python3}
BuildRequires:  python3-devel
# For use by selftests:
BuildRequires:  python3-pytest
BuildRequires:  python3-tkinter
%endif

%description
python-six provides simple utilities for wrapping over differences between
Python 2 and Python 3.

This is the Python 2 build of the module.

%if 0%{?with_python3}
%package -n python3-six
Summary:        Python 2 and 3 compatibility utilities
Group:          Development/Languages

%description -n python3-six
python-six provides simple utilities for wrapping over differences between
Python 2 and Python 3.

This is the Python 3 build of the module.
%endif

%prep
%setup -q -n six-%{version}
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
%{__python} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%check
py.test -rfsxX test_six.py
%if 0%{?with_python3}
pushd %{py3dir}
py.test-%{python3_version} -rfsxX test_six.py
popd
%endif


%files
%defattr(-,root,root,-)
%doc LICENSE README documentation/index.rst
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-six
%defattr(-,root,root,-)
%doc LICENSE README documentation/index.rst
%{python3_sitelib}/*
%endif


%changelog
* Mon Sep 16 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.4.1-1
- 1.4.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 21 2013 David Malcolm <dmalcolm@redhat.com> - 1.3.0-1
- 1.3.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 29 2012 David Malcolm <dmalcolm@redhat.com> - 1.2.0-1
- 1.2.0 (rhbz#852658)
- add %%check section

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 1.1.0-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Ralph Bean <rbean@redhat.com> - 1.1.0-2
- Conditionalized python3-six, allowing an el6 build.

* Tue Feb  7 2012 David Malcolm <dmalcolm@redhat.com> - 1.1.0-1
- 1.1.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Mar 24 2011 David Malcolm <dmalcolm@redhat.com> - 1.0.0-1
- initial packaging



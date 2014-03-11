%if 0%{?fedora} > 12
%global with_python3 1
%endif

# %%global betaver b1

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# tracer.so is a private object, don't include it in the provides
%global _use_internal_dependency_generator 0
%global __find_provides /bin/sh -c "%{_rpmconfigdir}/find-provides | grep -v -E '(tracer.so)' || /bin/true"
%global __find_requires /bin/sh -c "%{_rpmconfigdir}/find-requires | grep -v -E '(tracer.so)' || /bin/true"

Name:           python-coverage
Summary:        Code coverage testing module for Python
Version:        3.5.3
Release:        3%{?dist}
License:        BSD and (MIT or GPLv2)
Group:          System Environment/Libraries
URL:            http://nedbatchelder.com/code/modules/coverage.html
Source0:        http://pypi.python.org/packages/source/c/coverage/coverage-%{version}.tar.gz
Patch0:         python-coverage-3.5.3-pickle.patch
BuildRequires:  python-setuptools, python-devel
Requires:       python-setuptools
%if 0%{?with_python3}
BuildRequires:  /usr/bin/2to3
BuildRequires:  python3-setuptools, python3-devel
%endif # with_python3

%description
Coverage.py is a Python module that measures code coverage during Python 
execution. It uses the code analysis tools and tracing hooks provided in the 
Python standard library to determine which lines are executable, and which 
have been executed.

%if 0%{?with_python3}
%package -n python3-coverage
Summary:        Code coverage testing module for Python 3
Group:          System Environment/Libraries
# As the "coverage" executable requires the setuptools at runtime (#556290),
# so the "python3-coverage" executable requires python3-setuptools:
Requires:       python3-setuptools

%description -n python3-coverage
Coverage.py is a Python 3 module that measures code coverage during Python
execution. It uses the code analysis tools and tracing hooks provided in the 
Python standard library to determine which lines are executable, and which 
have been executed.
%endif # with_python3

%prep
%setup -q -n coverage-%{version}

%patch0 -p1

find . -type f -exec chmod 0644 \{\} \;
sed -i 's/\r//g' README.txt

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
pushd %{py3dir}
2to3 --nobackups --write .
popd
%endif # if with_python3

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # if with_python3

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}/%{_bindir}/coverage %{buildroot}/%{_bindir}/python3-coverage
popd
%endif # if with_python3

%{__python} setup.py install --skip-build --root %{buildroot}
magic_rpm_clean.sh

%files
%doc README.txt
%{_bindir}/coverage
%{python_sitearch}/coverage/
%{python_sitearch}/coverage*.egg-info/

%if 0%{?with_python3}
%files -n python3-coverage
%{_bindir}/python3-coverage
%{python3_sitearch}/coverage/
%{python3_sitearch}/coverage*.egg-info/
%endif # if with_python3


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 3.5.3-3
- 为 Magic 3.0 重建

* Wed Oct 10 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 3.5.3-2
- Patch from upstream for traceback when people use this with python2 and
  python3 in the same directory

* Mon Oct  1 2012 Tom Callaway <spot@fedoraproject.org> - 3.5.3-1
- update to 3.5.3

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 3.5.2-0.4.b1
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 3.5.2-0.3.b1
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.2-0.2.b1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May  2 2012 Tom Callaway <spot@fedoraproject.org> - 3.5.2-0.1.b1
- update to 3.5.2b1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.1-0.2.b1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep  2 2011 Tom Callaway <spot@fedoraproject.org> - 3.5.1-0.1.b1
- update to 3.5.1b1

* Mon Jun  6 2011 Tom Callaway <spot@fedoraproject.org> - 3.5-0.1.b1
- update to 3.5b1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010  <David Malcolm <dmalcolm@redhat.com>> - 3.4-2
- rebuild for newer python3

* Thu Oct 21 2010 Luke Macken <lmacken@redhat.com> - 3.4-1
- Update to 3.4 (#631751)

* Fri Sep 03 2010 Luke Macken <lmacken@redhat.com> - 3.3.1-4
- Rebuild against Python 3.2

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed May 9 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 3.3.1-2
- Fix license tag, permissions, and filtering extraneous provides

* Wed May 9 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 3.3.1-1
- Update to 3.3.1

* Fri Feb  5 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-3
- add python 3 subpackage (#536948)

* Sun Jan 17 2010 Luke Macken <lmacken@redhat.com> - 3.2-2
- Require python-setuptools (#556290)

* Wed Dec  9 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2-1
- update to 3.2

* Fri Oct 16 2009 Luke Macken <lmacken@redhat.com> - 3.1-1
- Update to 3.1

* Wed Aug 10 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.0.1-1
- update to 3.0.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.85-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 15 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.85-2
- fix install invocation

* Wed May 6 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.85-1
- Initial package for Fedora

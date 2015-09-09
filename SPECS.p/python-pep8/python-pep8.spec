%bcond_without python3

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global module_name pep8

Name:           python-%{module_name}
Version:	1.6.2
Release:	1%{?dist}
Summary:        Python style guide checker
Summary(zh_CN.UTF-8): Python 风格向导检查器

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
# License is held in the comments of pep8.py
# setup.py claims license is Expat license, which is the same as MIT
License:        MIT
URL:            http://pypi.python.org/pypi/%{module_name}
Source0:        http://pypi.python.org/packages/source/p/%{module_name}/%{module_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
Requires:       python-setuptools

%description
pep8 is a tool to check your Python code against some of the style conventions
in PEP 8. It has a plugin architecture, making new checks easy, and its output
is parseable, making it easy to jump to an error location in your editor.

%description -l zh_CN.UTF-8
Python 风格向导检查器。

%if %{with python3}
%package -n python3-pep8
Summary:    Python style guide checker
Summary(zh_CN.UTF-8): Python 风格向导检查器

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx
 
Requires:  python3-setuptools
%description -n python3-pep8
pep8 is a tool to check your Python code against some of the style
conventions in PEP 8. It has a plugin architecture, making new checks
easy, and its output is parseable, making it easy to jump to an error
location in your editor.

This is a version for Python 3.

%description -n python3-pep8 -l zh_CN.UTF-8
Python 风格向导检查器。
%endif


%prep
%setup -qn %{module_name}-%{version}
# Remove #! from pep8.py
sed --in-place "s:#!\s*/usr.*::" pep8.py

%if %{with python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
%{__python} setup.py build build_sphinx

%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
rm -rf %{buildroot}
%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/pep8 %{buildroot}%{_bindir}/python3-pep8
popd
%endif

%{__python} setup.py install -O1 --skip-build --root %{buildroot}
magic_rpm_clean.sh
 

%check
python pep8.py --testsuite testsuite
python pep8.py --doctest

%if %{with python3}
pushd %{py3dir}
PYTHONPATH="%{buildroot}%{python3_sitelib}:$PYTHONPATH" %{__python3} pep8.py --testsuite testsuite
popd
%endif


%files
%defattr(-,root,root,-)
%doc CHANGES.txt README.rst build/sphinx/html/*
%{_bindir}/pep8
%{python_sitelib}/%{module_name}.py*
%{python_sitelib}/%{module_name}-%{version}-*.egg-info

%if %{with python3}
%files -n python3-pep8
%doc README.rst CHANGES.txt build/sphinx/html/*
%{_bindir}/python3-pep8
%{python3_sitelib}/%{module_name}.py*
%{python3_sitelib}/%{module_name}-%{version}-*.egg-info/
%{python3_sitelib}/__pycache__/%{module_name}*
%endif

%changelog
* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 1.6.2-1
- 更新到 1.6.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Oct 20 2014 Matthias Runge <mrunge@redhat.com> - 1.5.7-1
- update to 1.5.7

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed May 14 2014 Matthias Runge <mrunge@redhat.com> - 1.5.6-1
- update to 1.5.6 (rhbz#1087351)

* Tue Apr 08 2014 Matthias Runge <mrunge@redhat.com> - 1.5.4-1
- require python3-setuptools (rhbz#1084756)
- update to 1.5.4 (rhbz#1081516)

* Wed Feb 26 2014 Matthias Runge <mrunge@redhat.com> -1.4.6-2
- rename py3 version of pep8 to python3-pep8 (rhbz#1060408)

* Tue Aug 13 2013 Ian Weller <iweller@redhat.com> - 1.4.6-1
- update to 1.4.6

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 14 2013 Matthias Runge <mrunge@redhat.com> - 1.4.5-1
- update to 1.4.5 (rhbz#918924)
- introduce py3 package (rhbz#971941)

* Tue Feb 26 2013 Ian Weller <iweller@redhat.com> - 1.4.4-1
- Update to 1.4.4

* Mon Feb 11 2013 Ian Weller <iweller@redhat.com> - 1.4.2-1
- Update to 1.4.2

* Tue Jan 29 2013 Ian Weller <iweller@redhat.com> - 1.4.1-1
- Update to 1.4.1
- Add Sphinx docs

* Fri Sep 07 2012 Ian Weller <iweller@redhat.com> - 1.3.3-3
- Run test suite using the pep8.py that has been installed

* Fri Sep 07 2012 Ian Weller <iweller@redhat.com> - 1.3.3-2
- Add test suite

* Thu Sep 06 2012 Ian Weller <iweller@redhat.com> - 1.3.3-1
- Update to 1.3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Ian Weller <iweller@redhat.com> - 1.3-1
- Update to 1.3

* Sat Apr 07 2012 Ian Weller <iweller@redhat.com> - 1.0.1-1
- Update to 1.0.1

* Fri Jan 27 2012 Ian Weller <iweller@redhat.com> - 0.6.1-1
- Update to 0.6.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Ian Weller <iweller@redhat.com> - 0.6.0-2
- RHBZ 633102: Requires: python-setuptools

* Tue Nov 16 2010 Ian Weller <iweller@redhat.com> - 0.6.0-1
- Changed upstream (same code, new maintainer, new URL)
- New release

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Nov  9 2009 Ian Weller <ian@ianweller.org> - 0.4.2-2
- Add BR: python-setuptools
- Change URL to the correct upstream

* Sun Nov  8 2009 Ian Weller <ian@ianweller.org> - 0.4.2-1
- Initial package build

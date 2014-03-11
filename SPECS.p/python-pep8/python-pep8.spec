%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global module_name pep8

Name:           python-%{module_name}
Version:        1.3.3
Release:        3%{?dist}
Summary:        Python style guide checker

Group:          Development/Languages
# License is held in the comments of pep8.py
# setup.py claims license is Expat license, which is the same as MIT
License:        MIT
URL:            http://pypi.python.org/pypi/%{module_name}
Source0:        http://pypi.python.org/packages/source/p/%{module_name}/%{module_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-setuptools

%description
pep8 is a tool to check your Python code against some of the style conventions
in PEP 8. It has a plugin architecture, making new checks easy, and its output
is parseable, making it easy to jump to an error location in your editor.


%prep
%setup -qn %{module_name}-%{version}
# Remove #! from pep8.py
sed --in-place "s:#!\s*/usr.*::" pep8.py


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
python setup.py install -O1 --skip-build --root %{buildroot}

 
%clean
rm -rf %{buildroot}


%check
python %{buildroot}%{python_sitelib}/pep8.py --testsuite testsuite


%files
%defattr(-,root,root,-)
%doc CHANGES.txt README.rst
%{_bindir}/pep8
%{python_sitelib}/*


%changelog
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

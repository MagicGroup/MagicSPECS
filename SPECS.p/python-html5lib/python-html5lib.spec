%global modulename html5lib
%global with_python3 1

Name:		python-%{modulename}
Summary:	A python based HTML parser/tokenizer
Summary(zh_CN.UTF-8): Python 的 HTML 解析器
Version:	0.9999999
Release:	3%{?dist}
Epoch:		1
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:	MIT
URL:		https://pypi.python.org/pypi/%{modulename}

Source0:	https://pypi.python.org/packages/source/h/%{modulename}/%{modulename}-%{version}.tar.gz	

BuildArch:	noarch
Requires:	python-six
BuildRequires:	python-setuptools
BuildRequires:	python2-devel
BuildRequires:	python-nose
BuildRequires:	python-six

%description
A python based HTML parser/tokenizer based on the WHATWG HTML5 
specification for maximum compatibility with major desktop web browsers.

%description -l zh_CN.UTF-8
Python 的 HTML 解析器。

%if 0%{?with_python3}
%package -n python3-%{modulename}
Summary:	A python based HTML parser/tokenizer 
Summary(zh_CN.UTF-8): Python3 的 HTML 解析器
Group:		Development/Libraries 
Group(zh_CN.UTF-8): 开发/库

Requires:	python3-six
BuildRequires:	python3-devel
BuildRequires:	python-tools
BuildRequires:	python3-nose
BuildRequires:	python3-six
BuildRequires:	python3-setuptools

%description -n python3-%{modulename}
A python based HTML parser/tokenizer based on the WHATWG HTML5 
specification for maximum compatibility with major desktop web browsers.
%description -n python3-%{modulename} -l zh_CN.UTF-8
Python3 的 HTML 解析器。
%endif


%prep
%setup -q -n %{modulename}-%{version} 

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

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif

%{__python} setup.py install -O1 --skip-build --root %{buildroot}
magic_rpm_clean.sh

%check
nosetests

%if 0%{?with_python3}
pushd %{py3dir}
nosetests-%{python3_version}
popd
%endif

%files
%doc CHANGES.rst README.rst LICENSE 
%{python_sitelib}/%{modulename}-*.egg-info
%{python_sitelib}/%{modulename}

%if 0%{?with_python3}
%files -n python3-%{modulename}
%doc CHANGES.rst LICENSE README.rst
%{python3_sitelib}/%{modulename}-*.egg-info
%{python3_sitelib}/%{modulename}
%endif 


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1:0.9999999-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1:0.9999999-2
- 更新到 0.9999999

* Sun Sep 06 2015 Liu Di <liudidi@gmail.com> - 1:0.999999-1
- 更新到 0.999999

* Wed Aug 19 2015 Liu Di <liudidi@gmail.com> - 1:0.999-7
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.999-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.999-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1:0.999-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri May 09 2014 Dennis Gilmore <dennis@ausil.us> - 0.999-3
- move python3 Requires and BuildRequires into the python3 sub-package

* Wed Mar 12 2014 Dan Scott <dan@coffeecode.net> - 0.999-2
- "six" module is a runtime requirement

* Sat Mar 01 2014 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 0.999-1
- Added epoch information

* Wed Feb 26 2014 Dan Scott <dan@coffeecode.net> - 0.999-1
- Updated for new version
- Fixed bogus dates in changelog

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0b2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 8 2013 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 1.0b2-2
- Updated python3 support which accidently removed from previous revision.

* Mon Jul 8 2013 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 1.0b2-1
- Updated new source

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 0.95-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 21 2012 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 0.95-1
- Added python3 spec and updated new source

* Mon Jul 18 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 0.90-1
- Initial spec

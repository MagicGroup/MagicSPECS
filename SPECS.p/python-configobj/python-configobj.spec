%if !(0%{?rhel} >= 6 || 0%{?fedora} >= 13)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-configobj
Version:	5.0.6
Release:	2%{?dist}
Summary:        Config file reading, writing, and validation
Summary(zh_CN.UTF-8): 配置文件读取、写入和校验

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        BSD
URL:            http://configobj.readthedocs.org/
Source0:        https://pypi.python.org/packages/source/c/configobj/configobj-%{version}.tar.gz
# to get tests
# git clone https://github.com/DiffSK/configobj.git && cd configobj
# git checkout v5.0.5
# tar -czf configobj-5.0.5-tests.tar.gz tests/ test_configobj.py
Source1:        configobj-%{version}-tests.tar.gz
# Generated from source code on 2014-07-31
Source2:        configobj-bsd-license.txt
Patch0:         configobj-import-all-fix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-six
BuildRequires:  pytest

Requires:       python-six

%description
ConfigObj is a simple but powerful config file reader and writer: an ini file
round tripper. Its main feature is that it is very easy to use, with a
straightforward programmer's interface and a simple syntax for config files. 
It has lots of other features though:
    * Nested sections (subsections), to any level
    * List values
    * Multiple line values
    * String interpolation (substitution)
    * Integrated with a powerful validation system
          o including automatic type checking/conversion
          o repeated sections
          o and allowing default values
    * All comments in the file are preserved
    * The order of keys/sections is preserved
    * No external dependencies
    * Full Unicode support
    * A powerful unrepr mode for storing basic datatypes

%description -l zh_CN.UTF-8
配置文件读取、写入和校验。

%if 0%{?with_python3}
%package -n python3-configobj
Summary:        Config file reading, writing, and validation for Python 3
Summary(zh_CN.UTF-8): 配置文件读取、写入和校验（Python3）
BuildRequires:  python3-devel
BuildRequires:  python3-six
BuildRequires:  python3-pytest

Requires:       python3-six

%description -n python3-configobj
ConfigObj is a simple but powerful config file reader and writer: an ini file
round tripper. Its main feature is that it is very easy to use, with a
straightforward programmer's interface and a simple syntax for config files. 
It has lots of other features though:
    * Nested sections (subsections), to any level
    * List values
    * Multiple line values
    * String interpolation (substitution)
    * Integrated with a powerful validation system
          o including automatic type checking/conversion
          o repeated sections
          o and allowing default values
    * All comments in the file are preserved
    * The order of keys/sections is preserved
    * No external dependencies
    * Full Unicode support
    * A powerful unrepr mode for storing basic datatypes

This package ships Python 3 build of configobj.

%description -n python3-configobj -l zh_CN.UTF-8
配置文件读取、写入和校验，这是 Python3 版本。
%endif


%prep
%setup -q -n configobj-%{version}
%patch0 -p1 -b .all

cp %{SOURCE2} .

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
%{__python} setup.py install --skip-build --root=$RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

%check
# this needs to be set for tests.test_configobj.test_options_deprecation
export PYTHONWARNINGS=always

tar -xzf %{SOURCE1}
%{__python} test_configobj.py
py.test tests

%if 0%{?with_python3}
pushd %{py3dir}
tar -xzf %{SOURCE1}
%{__python3} test_configobj.py
py.test-%{python3_version} tests
popd
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
# no docs untile upstream puts them in sdist again:
#  https://github.com/DiffSK/configobj/issues/63
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license configobj-bsd-license.txt
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-configobj
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license configobj-bsd-license.txt
%{python3_sitelib}/*
%endif


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 5.0.6-2
- 为 Magic 3.0 重建

* Sun Aug 23 2015 Liu Di <liudidi@gmail.com> - 5.0.6-1
- 更新到 5.0.6

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jul 31 2014 Tom Callaway <spot@fedoraproject.org> - 5.0.5-2
- fix license handling

* Thu Jun 26 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 5.0.5-1
- Updated to 5.0.5 (new upstream "with the blessing of original creator")
- Introduced python3-configobj subpackage
- Changed upstream url to documentation written by new upstream

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 4.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jun 17 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 4.7.2-1
- Fix traceback when doing from validate import *
- Upstream bugfix release

* Wed Jan 20 2010 Luke Macken <lmacken@redhat.com> - 4.7.0-2
- Merge a bunch of changes from Gareth Armstrong <gareth.armstrong@hp.com>
    - The src zip file should come either from http://www.voidspace.org.uk/
      downloads/ or http://code.google.com/p/configobj/ as the PyPI tarball is
      not complete.  No docs and no test code.
    - Added docs
    - Remove BR on python-setuptools-devel

* Sun Jan 10 2010 Luke Macken <lmacken@redhat.com> - 4.7.0-1
- Update to 4.7.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May  7 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 4.6.0-1
- updated to latest upstream

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 09 2009 Luke Macken <lmacken@redhat.com> - 4.5.3-4
- Conditionally include the egg-info, when available (#478417)

* Mon Dec 1 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 4.5.3-3
- Upload Source file so this actually builds.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 4.5.3-2
- Rebuild for Python 2.6

* Sat Jun 28 2008 Luke Macken <lmacken@redhat.com> - 4.5.3-1
- Update to 4.5.3

* Thu Feb 28 2008 Luke Macken <lmacken@redhat.com> - 4.5.2-1
- Update to 4.5.2

* Sun Sep  2 2007 Luke Macken <lmacken@redhat.com> - 4.4.0-2
- Update for python-setuptools changes in rawhide

* Sat Mar  3 2007 Luke Macken <lmacken@redhat.com> - 4.4.0-1
- 4.4.0

* Sat Dec  9 2006 Luke Macken <lmacken@redhat.com> - 4.3.2-6
- Rebuild for python 2.5

* Sun Sep  3 2006 Luke Macken <lmacken@redhat.com> - 4.3.2-5
- Fix dist tag

* Sun Sep  3 2006 Luke Macken <lmacken@redhat.com> - 4.3.2-4
- Rebuild for FC6

* Mon Aug 14 2006 Luke Macken <lmacken@redhat.com> - 4.3.2-3
- Include pyo files

* Tue Jul 18 2006 Luke Macken <lmacken@redhat.com> - 4.3.2-2
- Fix typo in the url

* Mon Jul 10 2006 Luke Macken <lmacken@redhat.com> - 4.3.2-1
- Initial package

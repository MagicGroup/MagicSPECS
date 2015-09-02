%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global with_python3 1

Name:           python-dtopt
Summary:        Add options to doctest examples while they are running
Summary(zh_CN.UTF-8): 给 doctest 样例运行的时候添加选项
Version:        0.1
Release:        15%{?dist}
License:        MIT
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            http://pypi.python.org/pypi/dtopt/
Source0:        http://pypi.python.org/packages/source/d/dtopt/dtopt-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-setuptools-devel

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif


%description
dtopts adds options to doctest examples while they are running. When
using the doctest module it is often convenient to use the ELLIPSIS
option, which allows you to use ... as a wildcard. But you either have
to setup the test runner to use this option, or you must put #doctest:
+ELLIPSIS on every example that uses this feature. dtopt lets you enable
this option globally from within a doctest, by doing:
>>> from dtopt import ELLIPSIS

%description -l zh_CN.UTF-8
给 doctest 样例运行的时候添加选项。

%if 0%{?with_python3}
%package -n python3-dtopt
Summary:        Add options to doctest examples while they are running
Summary(zh_CN.UTF-8): 给 doctest 样例运行的时候添加选项
Version:        0.1

%description -n python3-dtopt
dtopts adds options to doctest examples while they are running. When
using the doctest module it is often convenient to use the ELLIPSIS
option, which allows you to use ... as a wildcard. But you either have
to setup the test runner to use this option, or you must put #doctest:
+ELLIPSIS on every example that uses this feature. dtopt lets you enable
this option globally from within a doctest, by doing:
>>> from dtopt import ELLIPSIS
%description -n python3-dtopt -l zh_CN.UTF-8
给 doctest 样例运行的时候添加选项。
%endif

%prep
%setup -q -n dtopt-%{version}

# Remove bundled egg info if it exists.
rm -rf *.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
pushd %{py3dir}
# There is a print statement in the test that is not python3 compatible.
rm dtopt/tests.py*
popd
%endif


%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif
magic_rpm_clean.sh

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc docs/*
%{python_sitelib}/dtopt/
%{python_sitelib}/dtopt*.egg-info/

%if 0%{?with_python3}
%files -n python3-dtopt
%doc docs/*
%{python3_sitelib}/dtopt/
%{python3_sitelib}/dtopt*.egg-info/
%endif

%changelog
* Wed Sep 02 2015 Liu Di <liudidi@gmail.com> - 0.1-15
- 为 Magic 3.0 重建

* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 0.1-14
- 为 Magic 3.0 重建

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Feb 19 2013 Ralph Bean <rbean@redhat.com> - 0.1-12
- Added python3 subpackage.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 14 2009 Ricky Zhou <ricky@fedoraproject.org> - 0.1-5
- Change define to global.
- Remove unnecessary BuildRequires on python-devel.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.1-3
- Rebuild for Python 2.6

* Fri Jun 27 2008 Ricky Zhou <ricky@fedoraproject.org> 0.1-2
- Initial package for Fedora

* Sat Mar 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.1-1
- Initial package for Fedora

%if 0%{?fedora} > 12 || 0%{?rhel} > 6
%global with_python3 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

Name:           python-straight-plugin
Version:        1.4.0
Release:        4%{?dist}
Summary:        Python plugin loader

License:        BSD
URL:            https://github.com/ironfroggy/straight.plugin/

Source0:        http://pypi.python.org/packages/source/s/straight.plugin/straight.plugin-1.4.0-post-1.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python-tools
BuildRequires:  python3-setuptools
%endif

%if (0%{?rhel} && 0%{?rhel} <= 6)  || ( 0%{?fedora} && 0%{?fedora} <= 13 )
BuildRequires:  python-importlib
Requires:       python-importlib
%endif


%description
straight.plugin is a Python plugin loader inspired by twisted.plugin with two
important distinctions:

 - Fewer dependencies
 - Python 3 compatible

The system is used to allow multiple Python packages to provide plugins within
a namespace package, where other packages will locate and utilize. The plugins
themselves are modules in a namespace package where the namespace identifies
the plugins in it for some particular purpose or intent.


%if 0%{?with_python3}
%package -n     python3-straight-plugin
Summary:        Python plugin loader

%description -n python3-straight-plugin
straight.plugin is a Python plugin loader inspired by twisted.plugin with two
important distinctions:

 - Fewer dependencies
 - Python 3 compatible

The system is used to allow multiple Python packages to provide plugins within
a namespace package, where other packages will locate and utilize. The plugins
themselves are modules in a namespace package where the namespace identifies
the plugins in it for some particular purpose or intent.
%endif

%prep
%setup -q -c -n straight.plugin-1.4.0-post-1

%if 0%{?with_python3}
cp -r straight.plugin-%{version}-post-1/ py3-straight.plugin-%{version}-post-1
2to3 --write --nobackups py3-straight.plugin-%{version}-post-1
%endif

%build
pushd straight.plugin-%{version}-post-1
%{__python} setup.py build
popd

%if 0%{?with_python3}
pushd py3-straight.plugin-%{version}-post-1
%{__python3} setup.py build
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
pushd straight.plugin-%{version}-post-1
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd

%if 0%{?with_python3}
pushd py3-straight.plugin-%{version}-post-1
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif

#%check
#pushd straight.plugin-%{version}-post-1
#%{__python} tests.py
#popd
#
#%if 0%{?with_python3}
#pushd py3-straight.plugin-%{version}-post-1
#%{__python3} tests.py
#popd
#%endif

%files
# For noarch packages: sitelib
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-straight-plugin
# For noarch packages: sitelib
%{python3_sitelib}/*
%endif

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jan 25 2013 Pierre-Yves Chibon - 1.4.0-1
- Update to 1.4.0
- Remove doc as they are not part of the sources anymore (reported upstream)
- Comment out the tests as they are apparently also not in the sources anymore
- Add python{,3}-setuptools as BR

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 1.1.1-0.10.20111110.git57ef11c
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-0.9.20111110.git57ef11c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-0.8.20111110.git57ef11c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 11 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.1.1-0.7.20111110git57ef11c
- Fix the import of python-importlib (Finally!!)

* Fri Nov 11 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.1.1-0.6.20111110git57ef11c
- Fix typo in the use if for python-importlib

* Fri Nov 11 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.1.1-0.5.20111110git57ef11c
- Add python-importlib as BR and R on EL6

* Fri Nov 11 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.1.1-0.4.20111110git57ef11c
- EL6 has no python3 /me should get glasses...
- Fix comment on how to generate the tarball properly (previous method didn't keep the timestamp)

* Thu Nov 10 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.1.1-0.3.20111110git57ef11c
- Fix the use of __python3 for the tests and the build
- Change python-devel to python2-devel on the BR

* Thu Nov 10 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.1.1-0.2.20111110git57ef11c
- Rename the package to remove the dot

* Thu Nov 10 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.1.1-0.1.20111110git57ef11c
- Initial packaging work for Fedora

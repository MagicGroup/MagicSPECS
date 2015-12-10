%global srcname bottle

Name:           python-%{srcname}
Version:	0.12.9
Release:	3%{?dist}
Summary:        Fast and simple WSGI-framework for small web-applications
Summary(zh_CN.UTF-8): 小网页程序使用的快速简单 WSGI 框架

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        MIT
URL:            http://bottlepy.org
Source0:        http://pypi.python.org/packages/source/b/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description
Bottle is a fast and simple micro-framework for small web-applications. 
It offers request dispatching (Routes) with URL parameter support, Templates, 
a built-in HTTP Server and adapters for many third party WSGI/HTTP-server and 
template engines. All in a single file and with no dependencies other than the 
Python Standard Library.

%description -l zh_CN.UTF-8
小网页程序使用的快速简单 WSGI 框架。

%package -n python3-%{srcname}
Summary:        Fast and simple WSGI-framework for small web-applications
Summary(zh_CN.UTF-8): 小网页程序使用的快速简单 WSGI 框架

%description -n python3-%{srcname}
Bottle is a fast and simple micro-framework for small web-applications. 
It offers request dispatching (Routes) with URL parameter support, Templates, 
a built-in HTTP Server and adapters for many third party WSGI/HTTP-server and 
template engines. All in a single file and with no dependencies other than the 
Python Standard Library.

%description -n python3-%{srcname} -l zh_CN.UTF-8
小网页程序使用的快速简单 WSGI 框架。

%prep
%setup -q -n %{srcname}-%{version}
sed -i '/^#!/d' bottle.py

rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

%build
%{__python} setup.py build

pushd %{py3dir}
%{__python3} setup.py build
popd

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
rm %{buildroot}%{_bindir}/bottle.py

pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
rm %{buildroot}%{_bindir}/bottle.py
popd
magic_rpm_clean.sh

%files
%doc README.rst PKG-INFO
%{python_sitelib}/*

%files -n python3-%{srcname}
%doc README.rst PKG-INFO
%{python3_sitelib}/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.12.9-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.12.9-2
- 更新到 0.12.9

* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 0.12.8-1
- 更新到 0.12.8

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jul 12 2014 Rahul Sundaram <sundaram@fedoraproject.org> - 0.12.6-1
- resolves rhbz#1093257 - JSON content type not restrictive enough

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.11.6-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 23 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 0.11.6-1
- upstream release 0.11.6
- add python3 subpackage. resolves rhbz#949240
- spec file patch from Haïkel Guémar <hguemar@fedoraproject.org>

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 01 2012 Ian Weller <iweller@redhat.com> - 0.10.7-1
- Update to 0.10.7 (required by python-mwlib)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 18 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.9.5-1
- Initial spec

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global with_python3 1

Name:           python-webtest
Version:	2.0.18
Release:	2%{?dist}
Summary:        Helper to test WSGI applications
Summary(zh_CN.UTF-8): 测试 WSGI 应用的辅助程序

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        MIT
URL:            http://pythonpaste.org/webtest/
Source0:        http://pypi.python.org/packages/source/W/WebTest/WebTest-%{version}.zip
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:      noarch
BuildRequires:  python-setuptools
BuildRequires:  python-nose
BuildRequires:  python-webob
BuildRequires:  python-dtopt

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-nose
BuildRequires:  python3-webob
BuildRequires:  python3-dtopt
Requires:       python3-webob
%endif

Requires:       python-webob

%description
WebTest wraps any WSGI application and makes it easy to send test
requests to that application, without starting up an HTTP server.

This provides convenient full-stack testing of applications written
with any WSGI-compatible framework.

%description -l zh_CN.UTF-8
测试 WSGI 应用的辅助程序。

%if 0%{?with_python3}
%package -n python3-webtest
Summary:        Helper to test WSGI applications
Summary(zh_CN.UTF-8): 测试 WSGI 应用的辅助程序
Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言

Requires:       python3-webtest

%description -n python3-webtest
WebTest wraps any WSGI application and makes it easy to send test
requests to that application, without starting up an HTTP server.

This provides convenient full-stack testing of applications written
with any WSGI-compatible framework.
%description -n python3-webtest -l zh_CN.UTF-8
测试 WSGI 应用的辅助程序。
%endif


%prep
%setup -q -n WebTest-%{version}

# Remove bundled egg info if it exists.
rm -rf *.egg-info

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
%{__rm} -rf %{buildroot}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif

%{__python} setup.py install -O1 --skip-build --root %{buildroot}
magic_rpm_clean.sh

%clean
%{__rm} -rf %{buildroot}

%check
PYTHONPATH=$(pwd) %{__python} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
PYTHONPATH=$(pwd) %{__python3} setup.py test
popd
%endif

%files
%doc docs/*
%{python_sitelib}/webtest
%{python_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-webtest
%doc docs/*
%{python3_sitelib}/webtest
%{python3_sitelib}/*.egg-info
%endif

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.0.18-2
- 更新到

* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 2.0.18-1
- 更新到 2.0.18

* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 1.3.4-7
- 为 Magic 3.0 重建

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr  5 2013 Luke Macken <lmacken@redhat.com> - 1.3.4-5
- Made the python3 subpackage require python-webob instead of python-webob1.2

* Tue Feb 19 2013 Ralph Bean <rbean@redhat.com> - 1.3.4-4
- Added python3 subpackage

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 24 2012 Ricky Zhou <ricky@fedoraproject.org> - 1.3.4-1
- Update to 1.3.4.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 14 2011 Luke Macken <lmacken@redhat.com> - 1.3.3-1
- Update to 1.3.3

* Fri Jul 15 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 05 2010 Luke Macken <lmacken@redhat.com> - 1.2.2-1
- Update to 1.2.2
- Add python-dtopt to the BuildRequires
- Include the docs again

* Sun Jul 25 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot[com> - 1.2.1-3
- Disable tests and docs for now. They are not included in this tarball

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jun 09 2010 Luke Macken <lmacken@redhat.com> - 1.2.1-1
- Update to 1.2.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 31 2009 Luke Macken <lmacken@redhat.com> - 1.2-1
- Update to 1.2

* Tue Apr 14 2009 Ricky Zhou <ricky@fedoraproject.org> - 1.1-3
- Change define to global.
- Remove old >= 8 conditional.
- Remove unnecessary BuildRequires on python-devel.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 06 2008 Ricky Zhou <ricky@fedoraproject.org> - 1.1-1
- Upstream released new version.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0-4
- Rebuild for Python 2.6

* Thu Jul 17 2008 Ricky Zhou <ricky@fedoraproject.org> - 1.0-3
- Update Requires for python-webob rename.
- Add BuildRequires on python-webob for tests.

* Sat Jul 07 2008 Ricky Zhou <ricky@fedoraproject.org> - 1.0-2
- Add %%check section.

* Sat Jun 14 2008 Ricky Zhou <ricky@fedoraproject.org> - 1.0-1
- Initial RPM Package.

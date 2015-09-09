%global with_python3 1

%global pkgname tornado

Name:           python-%{pkgname}
Version:	4.2.1
Release:	1%{?dist}
Summary:        Scalable, non-blocking web server and tools
Summary(zh_CN.UTF-8): 可扩展，无阻塞的网络服务器和工具

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        ASL 2.0
URL:            http://www.tornadoweb.org
Source0:        https://pypi.python.org/packages/source/t/tornado/tornado-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
BuildRequires:  python-backports-ssl_match_hostname
Requires:       python-backports-ssl_match_hostname
Requires:       python-pycurl
Requires:       python-simplejson
%if 0%{?with_python3}
BuildRequires:  python-tools
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
%endif

%description
Tornado is an open source version of the scalable, non-blocking web
server and tools.

The framework is distinct from most mainstream web server frameworks
(and certainly most Python frameworks) because it is non-blocking and
reasonably fast. Because it is non-blocking and uses epoll, it can
handle thousands of simultaneous standing connections, which means it is
ideal for real-time web services.

%description -l zh_CN.UTF-8
可扩展，无阻塞的网络服务器和工具。

%package doc
Summary:        Examples for python-tornado
Summary(zh_CN.UTF-8): %{name} 的文档
Group:          Documentation
Group(zh_CN.UTF-8): 文档
Requires:       python-tornado = %{version}-%{release}

%description doc
Tornado is an open source version of the scalable, non-blocking web
server and and tools. This package contains some example applications.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%if 0%{?with_python3}
%package -n python3-tornado
Summary:        Scalable, non-blocking web server and tools
Summary(zh_CN.UTF-8): 可扩展，无阻塞的网络服务器和工具
%description -n python3-tornado
Tornado is an open source version of the scalable, non-blocking web
server and tools.

The framework is distinct from most mainstream web server frameworks
(and certainly most Python frameworks) because it is non-blocking and
reasonably fast. Because it is non-blocking and uses epoll, it can
handle thousands of simultaneous standing connections, which means it is
ideal for real-time web services.
%description -n python3-tornado -l zh_CN.UTF-8
可扩展，无阻塞的网络服务器和工具。

%package -n python3-tornado-doc
Summary:        Examples for python-tornado
Summary(zh_CN.UTF-8): python3-tornado 的文档
Group:          Documentation
Group(zh_CN.UTF-8): 文档
Requires:       python3-tornado = %{version}-%{release}

%description -n python3-tornado-doc
Tornado is an open source version of the scalable, non-blocking web
server and and tools. This package contains some example applications.
%description -n python3-tornado-doc -l zh_CN.UTF-8
python3-tornado 的文档。

%endif # with_python3

%prep 
%setup -q -n %{pkgname}-%{version}

# remove shebang from files
%{__sed} -i.orig -e '/^#!\//, 1d' *py tornado/*.py tornado/*/*.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
2to3 --write --nobackups %{py3dir}
pushd %{py3dir}
    # add __future__.division/print_function to testfile as 2to3 strips it off
    mv tornado/test/template_test.py tornado/test/template_test.py.orig
    echo "from __future__ import division" > tornado/test/template_test.py
    cat tornado/test/template_test.py.orig >> tornado/test/template_test.py
    touch -r tornado/test/template_test.py.orig tornado/test/template_test.py
    mv tornado/test/util_test.py tornado/test/util_test.py.orig
    echo "from __future__ import print_function" > tornado/test/util_test.py
    cat tornado/test/util_test.py.orig >> tornado/test/util_test.py
    touch -r tornado/test/util_test.py.orig tornado/test/util_test.py
popd
%endif # with_python3

%build
%if 0%{?with_python3}
pushd %{py3dir}
    python3 setup.py build
popd
%endif # with_python3

python setup.py build


%install
rm -rf %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
    PATH=$PATH:%{buildroot}%{python3_sitearch}/%{pkgname}
    python3 setup.py install --root=%{buildroot}
popd
%endif # with_python3

PATH=$PATH:%{buildroot}%{python_sitearch}/%{pkgname}
python setup.py install --root=%{buildroot}
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%check
%if "%{dist}" != ".el6"
    %if 0%{?with_python3}
    pushd %{py3dir}
        PYTHONPATH=%{python3_sitearch} \
        python3 -m tornado.test.runtests --verbose || :
    popd
    %endif # with_python3
    PYTHONPATH=%{python_sitearch} \
    python -m tornado.test.runtests --verbose
%endif

%files
%doc README.rst PKG-INFO

%{python_sitearch}/%{pkgname}/
%{python_sitearch}/%{pkgname}-%{version}-*.egg-info

%files doc
%doc demos

%if 0%{?with_python3}
%files -n python3-tornado
%doc README.rst PKG-INFO

%{python3_sitearch}/%{pkgname}/
%{python3_sitearch}/%{pkgname}-%{version}-*.egg-info

%files -n python3-tornado-doc
%doc demos
%endif


%changelog
* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 4.2.1-1
- 更新到 4.2.1

* Tue Jul 01 2014 Liu Di <liudidi@gmail.com> - 3.2.1-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Thomas Spura <tomspur@fedoraproject.org> - 3.2.1-1
- update to 3.2.1
- no noarch anymore
- remove defattr

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 2.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 14 2013 Thomas Spura <tomspur@fedoraproject.org> - 2.2.1-5
- remove rhel conditional for with_python3:
  https://fedorahosted.org/fpc/ticket/200

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 2.2.1-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 20 2012 Thomas Spura <tomspur@fedoraproject.org> - 2.2.1-1
- update to upstream release 2.2.1 (fixes CVE-2012-2374)
- fix typo for epel6 macro bug #822972 (Florian La Roche)

* Thu Feb 9 2012 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 2.2-1
- upgrade to upstream release 2.2

* Thu Feb 9 2012 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 2.1.1-4
- remove python3-simplejson dependency

* Fri Jan 27 2012 Thomas Spura <tomspur@fedoraproject.org> - 2.1.1-3
- build python3 package

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 25 2011 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 2.1.1-1
- new upstream version 2.1.1
- remove double word in description and rearrange it (#715272)
- fixed removal of shebangs
- added %%check section to run unittests during package build

* Tue Mar 29 2011 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.2.1-1
- new upstream version 1.2.1

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep  8 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.1-1
- new upstream release 1.1

* Tue Aug 17 2010 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 1.0.1-1
- new upstream bugfix release: 1.0.1

* Wed Aug  4 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.0-2
- changed upstream source url

* Wed Aug  4 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.0-1
- new upstream release 1.0
- there's no longer a problem with spurious permissions, so remove that fix

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Oct 21 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 0.2-3
- changed -doc package group to Documentation
- use global instead of define

* Tue Oct 20 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 0.2-2
- create -doc package for examples
- altered description to not include references to FriendFeed
- rename to python-tornado

* Fri Sep 25 2009 Ionuț Arțăriși <mapleoin@lavabit.com> - 0.2-1
- New upstream version
- Fixed macro usage and directory ownership in spec

* Thu Sep 10 2009 Ionuț Arțăriși <mapleoin@lavabit.com> - 0.1-1
- Initial release


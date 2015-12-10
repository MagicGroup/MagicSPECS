%global with_python3 1
# paste is not python3 compatible at this time

Name:           python-paste
Version:	2.0.2
Release:	3%{?dist}
Summary:        Tools for using a Web Server Gateway Interface stack
Summary(zh_CN.UTF-8): 使用网页服务器网关接口的工具
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
# Most of the code is MIT
# paste/exceptions/collector.py is ZPLv2.0
# paste/evalexception/mochikit/MochiKit.js AFL or MIT
# paste/lint.py MIT or Apache v2
# subproccess24.py PySourceColor.py, Python
# doctest24.py, Public Domain
License: MIT and ZPLv2.0 and Python and Public Domain and (AFL or MIT) and (MIT or ASL 2.0)
URL:            http://pythonpaste.org
# All files arent included in the 0.7.5.1 release.  Take a snapshot to get
# unittests working and pick up three bugfixes as well
# hg clone -r 1498 https://bitbucket.org/ianb/paste
# cd paste
# patch -p1 < ../paste-manifest.patch
# python setup.py sdist
# Source is in dist/Paste-1.7.5.1.tar.gz
# Source0:        Paste-%{version}.tar.gz
Source0:        https://pypi.python.org/packages/source/P/Paste/Paste-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires: python-nose
BuildRequires: python-tempita
BuildRequires: pyOpenSSL
Requires: python-tempita
Requires: pyOpenSSL
Requires:  python-setuptools

%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-nose
BuildRequires: python3-tempita
BuildRequires: /usr/bin/2to3
%endif # if with_python3

%description
These provide several pieces of "middleware" (or filters) that can be nested
to build web applications.  Each piece of middleware uses the WSGI (PEP 333)
interface, and should be compatible with other middleware based on those
interfaces.

%description -l zh_CN.UTF-8
使用网页服务器网关接口的工具。

%if 0%{?with_python3}
%package -n python3-paste
Summary:        Tools for using a Web Server Gateway Interface stack
Summary(zh_CN.UTF-8): 使用网页服务器网关接口的工具
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: python3-tempita
Requires: python3-setuptools
# TODO is there a pyOpenSSL for python3

%description -n python3-paste
These provide several pieces of "middleware" (or filters) that can be nested
to build web applications.  Each piece of middleware uses the WSGI (PEP 333)
interface, and should be compatible with other middleware based on those
interfaces.
%description -n python3-paste -l zh_CN.UTF-8
使用网页服务器网关接口的工具。
%endif # with_python3


%prep
%setup -q -n Paste-%{version}
# Strip #! lines that make these seem like scripts
%{__sed} -i -e '/^#!.*/,1 d' paste/util/scgiserver.py paste/debug/doctest_webapp.py

# clean docs directory
pushd docs
rm StyleGuide.txt
popd

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
2to3 --write --nobackups %{py3dir}
%endif # with_python3

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3
magic_rpm_clean.sh

%check
export PYTHONPATH=$(pwd)
# We don't have access to the wider internet in the buildsystem
nosetests -e '.*test_paste_website'

%if 0%{?with_python3}
pushd %{py3dir}
export PYTHONPATH=$(pwd)
nosetests-%{python3_version}
popd
%endif # with_python3

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc docs/*
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-paste
%defattr(-,root,root,-)
%{python3_sitelib}/*
%endif


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 2.0.2-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.0.2-2
- 为 Magic 3.0 重建

* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 2.0.2-1
- 更新到 2.0.2

* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 1.7.5.1-10.20111221hg1498
- 为 Magic 3.0 重建

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5.1-9.20111221hg1498
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5.1-8.20111221hg1498
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5.1-7.20111221hg1498
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 23 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 1.7.5.1-6.20111221hg1498
- Disable python3 subpackage as paste is not python3 compatible at this time

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5.1-5.20111221hg1498
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.7.5.1-4.20111221hg1498
- Tarball is missing files, use a snapshot to get those files and also pick up
  several bug fixes (one related to serving CGI scripts, another for http
  Continue requests, and a third regarding digest authentication and internet
  explorer)

* Tue Dec 20 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.7.5.1-3
- Ugh.  Enable unittests and make a note that the python3 module is totally
  non-functional.  Open a bug for that for the actual package maintainers to
  make a decision on.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 22 2010 Luke Macken <lmacken@redhat.com> - 1.7.5.1-1
- 1.7.5.1 upstream release

* Wed Sep 15 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 1.7.5-1
- New upstream bugfix

* Mon Aug 23 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 1.7.4-8
- Rebuild for python3-3.2

* Mon Aug  2 2010 Kyle VanderBeek <kylev@kylev.com> - 1.7.4-7
- Add python3 version.
- Fix python 2.7/3 incompatible lambda syntax.
- Unbundle stdlib (2.4+) subprocess module (removed because it isn't even 3.x legal).

* Fri Jul 30 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 1.7.4-6
- Include another function from tempita that is used by paste-script.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.7.4-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 9 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 1.7.4-4
- Actually apply the patches :-(

* Fri Jul 2 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 1.7.4-3
- Require pyOpenSSL so that we get SSL capabilities

* Thu Jul 1 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 1.7.4-2
- Unbundle tempita and don't rely on utils.string24

* Thu Jun 24 2010 Luke Macken <lmacken@redhat.com> - 1.7.4-1
- 1.7.4 security release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Kyle VanderBeek <kylev@kylev.com> - 1.7.2-3
- Package formerly ghost'ed .pyo files
- Update to current python package methods

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 06 2009 Luke Macken <lmacken@redhat.com> - 1.7.2-1
- Update to 1.7.2

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.7.1-2
- Rebuild for Python 2.6

* Sat Jun 14 2008 Luke Macken <lmacken@redhat.com> - 1.7.1-1
- Update to Paste 1.7.1

* Thu Feb 28 2008 Luke Macken <lmacken@redhat.com> - 1.6-1
- Update to 1.6

* Wed Oct  3 2007 Luke Macken <lmacken@redhat.com> - 1.4.2-1
- 1.4.2

* Sun Sep  2 2007 Luke Macken <lmacken@redhat.com> - 1.4-2
- Update for python-setuptools changes in rawhide

* Sat Jul  8 2007 Luke Macken <lmacken@redhat.com> - 1.4-1
- 1.4

* Sat Mar  3 2007 Luke Macken <lmacken@redhat.com> - 1.2.1-1
- 1.2.1

* Sat Dec  9 2006 Luke Macken <lmacken@redhat.com> - 1.0-2
- Add python-devel to BuildRequires
- 1.0

* Sun Sep 17 2006 Luke Macken <lmacken@redhat.com> - 0.9.8.1-1
- 0.9.8.1

* Sun Sep  3 2006 Luke Macken <lmacken@redhat.com> - 0.9.3-5
- Rebuild for FC6

* Wed Jul 19 2006 Luke Macken <lmacken@redhat.com> - 0.9.3-4
- Use a smarter shebang removal expression

* Wed Jul 19 2006 Luke Macken <lmacken@redhat.com> - 0.9.3-3
- Fix doc inclusion

* Sat Jul 15 2006 Luke Macken <lmacken@redhat.com> - 0.9.3-2
- Clean up docs directory
- Remove shebang from from non-executable scripts
- Use consistent build root variables

* Mon Jul 10 2006 Luke Macken <lmacken@redhat.com> - 0.9.3-1
- Initial package

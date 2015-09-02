%global with_python3 1

Name:           python-decorator
Version:	4.0.2
Release:	1%{?dist}
Summary:        Module to simplify usage of decorators
Summary(zh_CN.UTF-8): 简化修饰器使用的模块

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        BSD
URL:            http://pypi.python.org/pypi/decorator/
Source0:        http://pypi.python.org/packages/source/d/decorator/decorator-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-nose

%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
%endif

%description
The aim of the decorator module is to simplify the usage of decorators for
the average programmer, and to popularize decorators usage giving examples
of useful decorators, such as memoize, tracing, redirecting_stdout, locked,
etc.  The core of this module is a decorator factory called decorator.

%description -l zh_CN.UTF-8
简化修饰器使用的模块。

%if 0%{?with_python3}
%package -n python3-decorator
Summary:        Module to simplify usage of decorators in python3
Summary(zh_CN.UTF-8): 简化修饰器使用的模块（Python3）
Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言

%description -n python3-decorator
The aim of the decorator module is to simplify the usage of decorators for
the average programmer, and to popularize decorators usage giving examples
of useful decorators, such as memoize, tracing, redirecting_stdout, locked,
etc.  The core of this module is a decorator factory called decorator.
%description -n python3-decorator -l zh_CN.UTF-8
简化修饰器使用的模块。
%endif # if with_python3

%prep
%setup -q -n decorator-%{version}

chmod a-x *.txt *.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3


%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%check
# Until we get the python-multiprocessing backport packaged
%if 0%{?fedora} || 0%{?rhel} > 5
nosetests --with-doctest -e documentation3
%endif

# nose is not Python3 ready yet
%if 0%{?with_python3}
pushd %{py3dir}
PYTHONPATH=$(pwd)/build/lib python3 documentation3.py
popd
%endif # with_python3

%files
%defattr(-,root,root,-)
%doc *.txt 
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-decorator
%defattr(-,root,root,-)
%doc *.txt
%{python3_sitelib}/*
%endif # with_python3


%changelog
* Wed Sep 02 2015 Liu Di <liudidi@gmail.com> - 4.0.2-1
- 更新到 4.0.2

* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 3.3.3-6
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 3.3.3-5
- 为 Magic 3.0 重建

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.3-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.3-3
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 24 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 3.3.3-1
- New upstream release

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 2 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 3.3.2-1
- New upstream release

* Thu Apr 28 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 3.3.1-1
- Upstream update 3.3.1 that deprecates the .decorated attribute name in
  favor of .__wrapped__

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 1 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 3.3.0-1
- Upstream update 3.3.0 that adds function annotation support for python3 code

* Wed Dec 1 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 3.2.1-1
- Upstream bugfix 3.2.1
- Enable unittests for python3

* Mon Aug 23 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 3.2.0-4
- Rebuild for python-3.2.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 7 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 3.2.0-2
- Add documentation.py files to both subpackages (this contains a brief license
  assertion among other things).
* Wed Jun 30 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 3.2.0-1
- Minor cleanups
- Upgrade to 3.2.0
- Add python3 subpackage

* Tue Oct 6 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 3.1.2-2
- Really include the new source tarball

* Tue Oct 6 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 3.1.2-1
- Update to upstream release 3.1.2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 31 2009 Luke Macken <lmacken@redhat.com> - 3.0.1-2
- Only run the test suite on Fedora 11, which has Py2.6 and the multiprocessing
  module.  We can disable this once the compat module is packaged for F10 and
  below.

* Thu May 21 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 3.0.1-1
- Update to upstream release 3.0.1.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 21 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 2.3.2-1
- Update to 2.3.2
- Enable tests via nose

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.2.0-2
- Rebuild for Python 2.6

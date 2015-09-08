%global with_python3 1

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%{!?python3_version: %global python3_version %(%{__python3} -c 'import sys ; sys.stdout.write("%s.%s" % sys.version_info[:2])')}

Name: python-mako
Version:	1.0.2
Release:	1%{?dist}
Summary: Mako template library for Python
Summary(zh_CN.UTF-8): Python 的 Mako 模板库

Group: Development/Languages
Group(zh_CN.UTF-8): 开发/语言
# Mostly MIT, but _ast_util.py is Python licensed.
# The documentation contains javascript for search licensed BSD or GPLv2
License: (MIT and Python) and (BSD or GPLv2)
URL: http://www.makotemplates.org/
Source0: https://pypi.python.org/packages/source/M/Mako/Mako-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-markupsafe
BuildRequires: python-beaker
BuildRequires: python-nose
Requires: python-markupsafe
Requires: python-beaker

%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-markupsafe
BuildRequires: python3-beaker
%if 0%{?fedora} > 14
BuildRequires: python3-nose
%endif
BuildRequires: /usr/bin/2to3
%endif # if with_python3

%description
Mako is a template library written in Python. It provides a familiar, non-XML
syntax which compiles into Python modules for maximum performance. Mako's
syntax and API borrows from the best ideas of many others, including Django
templates, Cheetah, Myghty, and Genshi. Conceptually, Mako is an embedded
Python (i.e. Python Server Page) language, which refines the familiar ideas of
componentized layout and inheritance to produce one of the most straightforward
and flexible models available, while also maintaining close ties to Python
calling and scoping semantics.
%description -l zh_CN.UTF-8
Python 的 Mako 模板库。

%if 0%{?with_python3}
%package -n python3-mako
Summary: Mako template library for Python 3
Summary(zh_CN.UTF-8): Python3 的 Mako 模板库
Group: Development/Languages
Group(zh_CN.UTF-8): 开发/语言
Requires: python3-beaker
Requires: python3-markupsafe

%description -n python3-mako
Mako is a template library written in Python. It provides a familiar, non-XML
syntax which compiles into Python modules for maximum performance. Mako's
syntax and API borrows from the best ideas of many others, including Django
templates, Cheetah, Myghty, and Genshi. Conceptually, Mako is an embedded
Python (i.e. Python Server Page) language, which refines the familiar ideas of
componentized layout and inheritance to produce one of the most straightforward
and flexible models available, while also maintaining close ties to Python
calling and scoping semantics.

This package contains the mako module built for use with python3.
%description -n python3-mako -l zh_CN.UTF-8
Python3 的 Mako 模板库。
%endif # with_python3

%prep
%setup -q -n Mako-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
2to3 --no-diffs -w mako test
%{__python3} setup.py build
popd
%endif # with_python3


%install
rm -rf %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}/%{_bindir}/mako-render %{buildroot}/%{_bindir}/python3-mako-render
popd
%endif # with_python3

%{__python} setup.py install --skip-build --root %{buildroot}

# These are supporting files for building the docs.  No need to ship
rm -rf doc/build

%check
PYTHONPATH=$(pwd) nosetests

%if 0%{?with_python3} && 0%{?fedora} > 14
pushd %{py3dir}
PYTHONPATH=$(pwd) nosetests-%{python3_version}
popd
%endif

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE README.rst doc examples
%{_bindir}/mako-render
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-mako
%defattr(-,root,root,-)
%doc CHANGES LICENSE README.rst doc examples
%{_bindir}/python3-mako-render
%{python3_sitelib}/*
%endif

%changelog
* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 1.0.2-1
- 更新到 1.0.2

* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 0.7.3-3
- 为 Magic 3.0 重建

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr  9 2013 Luke Macken <lmacken@redhat.com> - 0.7.3-1
- Update to 0.7.3 (#784257)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 0.5.0-5
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 0.5.0-4
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 Luke Macken <lmacken@redhat.com> - 0.5.0-1
- Update to 0.5.0

* Mon Sep 5 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.4.2-2
- Require beaker to run unittests since its required at runtime
- Fix license tag

* Mon Sep 5 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.4.2-1
- Update to 0.4.2
- Run unit tests on python3

* Thu Feb 24 2011 Luke Macken <lmacken@redhat.com> - 0.4.0-1
- Update to 0.4.0 (#654779)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Luke Macken <lmacken@redhat.com> - 0.3.6-1
- Update to 0.3.6
- Remove 2to3 patch

* Wed Oct 27 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.3.5-2
- Use a patch from Debian submitted upstream to convert to python3 syntax

* Thu Oct 21 2010 Luke Macken <lmacken@redhat.com> - 0.3.5-1
- Update to 0.3.5 (#645063)

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.3.4-3
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jun 27 2010 Kyle VanderBeek <kylev@kylev.com> - 0.3.4-1
- Update to 0.3.4 security fix release
- Fix missing python3-beaker dependency

* Sat Jun  5 2010 Kyle VanderBeek <kylev@kylev.com> - 0.3.3-1
- Update to upstream 0.3.3

* Tue May  4 2010 David Malcolm <dmalcolm@redhat.com> - 0.3.2-2
- add python3 subpackage

* Tue May 04 2010 Luke Macken <lmacken@redhat.com> - 0.3.2-1
- Update to 0.3.2
- Run the test suite in %%check

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 06 2009 Luke Macken <lmacken@redhat.com> - 0.2.4-1
- Update to 0.2.4

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.1.10-3
- Rebuild for Python 2.6

* Sun May 11 2008 Kyle VanderBeek <kylev@kylev.com> - 0.1.10-2
- Fix rpmlint warnings.
- Add docs and examples.

* Wed Apr  9 2008 Kyle VanderBeek <kylev@kylev.com> - 0.1.10-1
- Initial version.

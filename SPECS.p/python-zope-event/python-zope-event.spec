%global with_python3 1

Name:           python-zope-event
Version:	4.1.0
Release:	2%{?dist}
Summary:        Zope Event Publication
Summary(zh_CN.UTF-8): Zope 事件
Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        ZPLv2.1
URL:            http://pypi.python.org/pypi/zope.event/
# Upstream accidentally used strange version
Source0:        http://pypi.python.org/packages/source/z/zope.event/zope.event-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-setuptools

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

BuildRequires:  python-sphinx

%description
The zope.event package provides a simple event system. It provides
an event publishing system and a very simple event-dispatching system
on which more sophisticated event dispatching systems can be built.
(For example, a type-based event dispatching system that builds on
zope.event can be found in zope.component.)

This package contains the version for Python 2.

%description -l zh_CN.UTF-8
Zope 事件。

%if 0%{?with_python3}
%package -n python3-zope-event
Summary:        Zope Event Publication (Python 3)
Summary(zh_CN.UTF-8): Zope 事件

%description -n python3-zope-event
The zope.event package provides a simple event system. It provides
an event publishing system and a very simple event-dispatching system
on which more sophisticated event dispatching systems can be built.
(For example, a type-based event dispatching system that builds on
zope.event can be found in zope.component.)

This package contains the version for Python 3.
%description -n python3-zope-event -l zh_CN.UTF-8
Zope 事件。
%endif

%prep
%setup -q -n zope.event-%{version}
rm -rf %{modname}.egg-info

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

# build the sphinx documents
pushd docs
PYTHONPATH=../src make html
rm -f _build/html/.buildinfo
popd


%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
magic_rpm_clean.sh

%check
%{__python} setup.py test
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif
 
%files
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%doc docs/_build/html/
%{python_sitelib}/zope/event/
%exclude %{python_sitelib}/zope/event/tests.py*
%dir %{python_sitelib}/zope/
%{python_sitelib}/zope/__init__*
%{python_sitelib}/zope.event-*.egg-info
%{python_sitelib}/zope.event-*-nspkg.pth

%if 0%{?with_python3}
%files -n python3-zope-event
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%doc docs/_build/html/
%{python3_sitelib}/zope/event/
%exclude %{python3_sitelib}/zope/event/tests.py*
%exclude %{python3_sitelib}/zope/event/__pycache__/tests*
%dir %{python3_sitelib}/zope/
%{python3_sitelib}/zope/__init__*
%{python3_sitelib}/zope.event-*.egg-info
%{python3_sitelib}/zope.event-*-nspkg.pth
%endif

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 4.1.0-2
- 更新到 4.1.0

* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 4.0.3-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Oct 15 2014 Ralph Bean <rbean@redhat.com> - 4.0.3-2
- Fix a python3 conditional block.

* Mon Jul 21 2014 Ralph Bean <rbean@redhat.com> - 4.0.3-1
- Latest upstream.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 4.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Ralph Bean <rbean@redhat.com> - 4.0.2-1
- Latest upstream.
- Conditionalized python3 subpackage for el6.

* Thu Oct 18 2012 Robin Lee <cheeselee@fedoraproject.org> - 3.5.2-1
- Update to 3.5.2 (ZTK 1.1.5)

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 3.5.1-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep  1 2011 Robin Lee <cheeselee@fedoraproject.org> - 3.5.1-1
- Update to 3.5.1 (#728489)
- Build subpackage for Python 3.
- Include the sphinx documents
- Exclude the module for tests.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 31 2010 Robin Lee <robinlee.sysu@gmail.com> - 3.5.0.1-4
- Add a missed percent character

* Tue Aug 31 2010 Robin Lee <robinlee.sysu@gmail.com> - 3.5.0.1-3
- Remove python-zope-filesystem from requirements
- Own %%{python_sitelib}/zope/
- Spec cleaned up

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 3.5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jun 17 2010 Robin Lee <robinlee.sysu@gmail.com> - 3.5.0.1-1
- Update to 3.5.0-1
- Include more documents

* Sun Jul 5 2009 Conrad Meyer <konrad@tylerc.org> - 3.4.1-1
- Add missing BR on python-setuptools.
- Enable testing stuff as zope-testing is in devel.

* Sun Dec 14 2008 Conrad Meyer <konrad@tylerc.org> - 3.4.0-1
- Initial package.

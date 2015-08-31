Name:           python-dateutil
Version:        2.4.2
Release:        4%{?dist}
Epoch:          1
Summary:        Powerful extensions to the standard datetime module
Summary(zh_CN.UTF-8): 标准日期时间模块的强力扩展

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        Python
URL:            https://github.com/dateutil/dateutil
Source0:        https://github.com/dateutil/dateutil/archive/%{version}.tar.gz
# https://github.com/dateutil/dateutil/issues/11
Patch0:         python-dateutil-system-zoneinfo.patch
Patch1:         python-dateutil-timelex-string.patch

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-six
Requires:       tzdata
Requires:       python-six
Conflicts:      python-vobject <= 0.8.1c-10

# Use the same directory of the main package for subpackage licence and docs
%global _docdir_fmt %{name}

%description
The dateutil module provides powerful extensions to the standard datetime
module available in Python 2.3+.

This is the version for Python 2.

%description -l zh_CN.UTF-8
标准日期时间模块的强力扩展。这是 Python2 版本。

%package -n python3-dateutil
Summary:        Powerful extensions to the standard datetime module
Summary(zh_CN.UTF-8): 标准日期时间模块的强力扩展
BuildRequires:  python3-devel
BuildRequires:  python3-six
Requires:       tzdata
Requires:       python3-six

%description -n python3-dateutil
The dateutil module provides powerful extensions to the standard datetime
module available in Python 2.3+.

This is the version for Python 3.

%description -n python3-dateutil -l zh_CN.UTF-8
标准日期时间模块的强力扩展，这是 Python3 版本。

%package doc
Summary: API documentation for python-dateutil
Summary(zh_CN.UTF-8): %{name} 的文档
%description doc
This package contains %{summary}.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%autosetup -p0 -n dateutil-%{version}
iconv --from=ISO-8859-1 --to=UTF-8 NEWS > NEWS.new
mv NEWS.new NEWS

%build
%{__python2} setup.py build
%{__python3} setup.py build
make -C docs html

%install
%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
magic_rpm_clean.sh

%check
%{__python2} setup.py test
%{__python3} setup.py test

%files
%license LICENSE
%doc NEWS README.rst
%{python2_sitelib}/dateutil/
%{python2_sitelib}/*.egg-info

%files -n python3-dateutil
%license LICENSE
%doc NEWS README.rst
%{python3_sitelib}/dateutil/
%{python3_sitelib}/*.egg-info

%files doc
%license LICENSE
%doc docs/_build/html

%changelog
* Tue Aug 25 2015 Liu Di <liudidi@gmail.com> - 1:2.4.2-4
- 为 Magic 3.0 重建

* Thu Aug 06 2015 Liu Di <liudidi@gmail.com> - 1:2.4.2-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr  6 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:2.4.2-1
- Update to latest upstream release.

* Tue Mar  3 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:2.4.0-3
- Add patch for string handling in dateutil.tz.tzstr (#1197791)

* Wed Jan 21 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:2.4.0-2
- Add python3 subpackage.
- Conflict with python-vobject <= 0.8.1c-10 (workaround until #1183377
  is fixed one way or another).

* Wed Jan 21 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:2.4.0-1
- Change to new upstream, update to 2.4 (#1126521)
- Build documentation.

* Tue Aug 05 2014 Jon Ciesla <limburgher@gmail.com> - 1:1.5-9
- Reverting to 1.5 pre user feedback and upstream.

* Mon Aug 04 2014 Jon Ciesla <limburgher@gmail.com> - 2.2-1
- Update to 2.2, BZ 1126521.
- Fix bad dates.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 15 2011 Jef Spaleta <jspaleta@fedoraproject.org> - 1.5-3
- Adjust patch to respect systemwide tzdata. Ref bug 729786

* Thu Sep 15 2011 Jef Spaleta <jspaleta@fedoraproject.org> - 1.5-2
- Added a patch to respect systemwide tzdata. Ref bug 729786

* Wed Jul 13 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 1.5-1
- New upstream release
- Fix UTF8 encoding correctly
- Drop buildroot, clean, defattr and use macro for Source

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 1.4.1-2
- small specfile fix

* Fri Feb 20 2009 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 1.4.1-2
- New upstream version

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.4-3
- Rebuild for Python 2.6

* Fri Aug 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.4-2
- fix license tag

* Tue Jul 01 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> 1.4-1
- Latest upstream release

* Fri Jan 04 2008 Jef Spaleta <jspaleta@fedoraproject.org> 1.2-2
- Fix for egg-info file creation

* Thu Jun 28 2007 Orion Poplawski <orion@cora.nwra.com> 1.2-1
- Update to 1.2

* Mon Dec 11 2006 Jef Spaleta <jspaleta@gmail.com> 1.1-5
- Fix python-devel BR, as per discussion in maintainers-list

* Mon Dec 11 2006 Jef Spaleta <jspaleta@gmail.com> 1.1-4
- Release bump for rebuild against python 2.5 in devel tree

* Wed Jul 26 2006 Orion Poplawski <orion@cora.nwra.com> 1.1-3
- Add patch to fix building on x86_64

* Wed Feb 15 2006 Orion Poplawski <orion@cora.nwra.com> 1.1-2
- Rebuild for gcc/glibc changes

* Thu Dec 22 2005 Orion Poplawski <orion@cora.nwra.com> 1.1-1
- Update to 1.1

* Thu Jul 28 2005 Orion Poplawski <orion@cora.nwra.com> 1.0-1
- Update to 1.0

* Tue Jul 05 2005 Orion Poplawski <orion@cora.nwra.com> 0.9-1
- Initial Fedora Extras package

Name:           python-dateutil
Version:        1.5
Release:        6%{?dist}
Summary:        Powerful extensions to the standard datetime module

Group:          Development/Languages
License:        Python
URL:            http://labix.org/python-dateutil
Source0:        http://labix.org/download/%{name}/%{name}-%{version}.tar.gz
Patch0:		python-dateutil-1.5-system-zoneinfo.patch

BuildArch:      noarch
BuildRequires:  python-devel,python-setuptools
Requires:	tzdata
%description
The dateutil module provides powerful extensions to the standard datetime
module available in Python 2.3+.

%prep
%setup -q
%patch0 -p1

iconv --from=ISO-8859-1 --to=UTF-8 NEWS > NEWS.new
mv NEWS.new NEWS

%build
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%files
%doc example.py LICENSE NEWS README
%{python_sitelib}/dateutil/
%exclude %{python_sitelib}/dateutil/zoneinfo/zoneinfo-2010g.tar.gz
%{python_sitelib}/*.egg-info

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.5-6
- 为 Magic 3.0 重建

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 15 2011 Jef Spaleta <jspaleta@fedoraproject.org> - 1.5-3
- Adjust patch to respect systemwide tzdata. Ref bug 729786

* Wed Sep 15 2011 Jef Spaleta <jspaleta@fedoraproject.org> - 1.5-2
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

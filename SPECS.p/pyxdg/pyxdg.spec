%global with_python3 1

Name:           pyxdg
Version:        0.25
Release:        9%{?dist}
Summary:        Python library to access freedesktop.org standards
Summary(zh_CN.UTF-8): 访问 freedesktop.org 标准的 Python 库
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        LGPLv2
URL:            http://freedesktop.org/Software/pyxdg
Source0:        http://people.freedesktop.org/~takluyver/%{name}-%{version}.tar.gz
# https://bugs.freedesktop.org/show_bug.cgi?id=61817
Patch0:		pyxdg-0.25-find-first-mimetype-match.patch
# https://bugs.freedesktop.org/show_bug.cgi?id=73878
Patch1:		pyxdg-0.25-CVE-2014-1624.patch
BuildArch:      noarch
# These are needed for the nose tests.
BuildRequires:	python-nose, hicolor-icon-theme
BuildRequires:  python2-devel
%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif # if with_python3

%description
PyXDG is a python library to access freedesktop.org standards 

%description -l zh_CN.UTF-8
访问 freedesktop.org 标准的 Python 库。

%if 0%{?with_python3}
%package -n python3-pyxdg
Summary:	Python3 library to access freedesktop.org standards
Summary(zh_CN.UTF-8): 访问 freedesktop.org 标准的 Python3 库
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description -n python3-pyxdg
PyXDG is a python library to access freedesktop.org standards. This
package contains a Python 3 version of PyXDG.
%description -n python3-pyxdg -l zh_CN.UTF-8
访问 freedesktop.org 标准的 Python3 库。
%endif # with_python3

%prep
%setup -q
%patch0 -p1 -b .pngfix
%patch1 -p1 -b .CVE-2014-1624

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf $RPM_BUILD_ROOT 

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root=$RPM_BUILD_ROOT
popd
%endif # with_python3

%{__python} setup.py install --skip-build --root=$RPM_BUILD_ROOT 
magic_rpm_clean.sh

%check
nosetests

%if 0%{?with_python3}
pushd %{py3dir}
nosetests
popd
%endif # with_python3

%clean
rm -rf $RPM_BUILD_ROOT 

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README TODO
%{python_sitelib}/xdg
%{python_sitelib}/pyxdg-*.egg-info

%if 0%{?with_python3}
%files -n python3-pyxdg
%doc AUTHORS COPYING ChangeLog README TODO
%{python3_sitelib}/xdg
%{python3_sitelib}/pyxdg-*.egg-info
%endif #with_python3

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.25-9
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.25-8
- 为 Magic 3.0 重建

* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 0.25-7
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Dec  4 2014 Tom Callaway <spot@fedoraproject.org> - 0.25-5
- fix CVE-2014-1624

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 28 2013 Tom Callaway <spot@fedoraproject.org> - 0.25-1
- update to 0.25

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov  7 2012 Tomas Bzatek <tbzatek@redhat.com> - 0.24-1
- update to 0.24

* Fri Oct 26 2012 Tom Callaway <spot@fedoraproject.org> - 0.23-2
- gracefully handle kde-config fails

* Mon Oct  8 2012 Tom Callaway <spot@fedoraproject.org> - 0.23-1
- update to 0.23
- enable python3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Apr 28 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.19-1
- update to 0.19

* Wed Aug 19 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.17-1
- update to 0.17

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.16-2
- Rebuild for Python 2.6

* Thu Oct 30 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.16-1
- update to 0.16
- fix indent bug in DesktopEntry.py (bz 469229)

* Sat Apr  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.15-6
- add egg-info (fixes FTBFS bz 440813)

* Wed Jan  3 2007 Patrice Dumas <pertusus@free.fr> - 0.15-5
- remove requires for python-abi (automatic now) and python directory
- remove package name from summary
- change tabs to spaces

* Thu Dec 21 2006 Patrice Dumas <pertusus@free.fr> - 0.15-4
- rebuild for python 2.5

* Sat Sep 23 2006 Tom "spot" Callaway <tcallawa@redhat.com> - 0.15-3
- rebuild for fc6

* Wed Feb 15 2006 John Mahowald <jpmahowald@gmail.com> - 0.15.2
- Rebuild for Fedora Extras 5

* Fri Oct 14 2005 John Mahowald <jpmahowald@gmail.com> - 0.15-1
- Rebuilt for 0.15

* Sun Jul 03 2005 Sindre Pedersen Bjordal <foolish[AT]fedoraforum.org> - 0.14-2
- Added %%{?dist} tag to release
- BuildArch: noarch
- Removed unneccesary CLFAGS

* Sun Jun 05 2005 Sindre Pedersen Bjordal <foolish[AT]fedoraforum.org> - 0.14-1
- Rebuilt for 0.14

* Wed Jun 01 2005 Sindre Pedersen Bjordal <foolish[AT]fedoraforum.org> - 0.13-1
- Rebuilt for 0.13

* Tue May 31 2005 Sindre Pedersen Bjordal <foolish[AT]fedoraforum.org> - 0.12-1
- Rebuilt for 0.12

* Sat May 28 2005 Sindre Pedersen Bjordal <foolish[AT]fedoraforum.org> - 0.11-1
- Rebuilt for 0.11

* Mon May 23 2005 Sindre Pedersen Bjordal <foolish[AT]fedoraforum.org> - 0.10-1
- Adapt to Fedora Extras template, based on spec from NewRPMs

* Tue Dec 14 2004 Che
- initial rpm release



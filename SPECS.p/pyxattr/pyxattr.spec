%global with_python3 1
Name:		pyxattr
Summary:	Extended attributes library wrapper for Python
Summary(zh_CN.UTF-8): Python 的扩展属性库
Version:	0.5.5
Release:	2%{?dist}
License:	LGPLv2+
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:		http://pyxattr.k1024.org/
Source:		https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
BuildRequires:	libattr-devel
BuildRequires:	python2-devel, python-setuptools
%if %{?with_python3}
BuildRequires:	python3-devel, python3-setuptools
%endif # with_python3

%description
Python extension module wrapper for libattr. It allows to query, list,
add and remove extended attributes from files and directories.

%description -l zh_CN.UTF-8
Python 的扩展属性库，是 libattr 的接口。

%if %{?with_python3}
%package -n python3-%{name}
Summary:	Extended attributes library wrapper for Python 3
Summary(zh_CN.UTF-8): Python3 的扩展属性库

%description -n python3-%{name}
Python extension module wrapper for libattr. It allows to query, list,
add and remove extended attributes from files and directories.

Python 3 version.
%description -n python3-%{name} -l zh_CN.UTF-8
Python3 的扩展属性库，是 libattr 的接口。
%endif # with_python3

%prep
%setup -q

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
CFLAGS="%{optflags}" %{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
popd
%endif # with_python3

%install
%{__python2} setup.py install --root="%{buildroot}" --prefix="%{_prefix}"

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --root="%{buildroot}" --prefix="%{_prefix}"
popd
%endif # with_python3
magic_rpm_clean.sh

%check
# selinux in koji produces unexpected xattrs for tests
export TEST_IGNORE_XATTRS=security.selinux

%{__python2} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif # with_python3

%files
%defattr(0644,root,root,0755)
%{python2_sitearch}/xattr.so
%{python2_sitearch}/*egg-info
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS 

%if %{?with_python3}
%files -n python3-%{name}
%defattr(0644,root,root,0755)
%{python3_sitearch}/xattr.cpython-??m.so
%{python3_sitearch}/*egg-info
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS
%endif # with_python3

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.5.5-2
- 为 Magic 3.0 重建

* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 0.5.5-1
- 更新到 0.5.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug  7 2014 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.5.3-3
- add Mark Hamzy's patch to fix issue with PPC builds (bug 1127310)

* Mon Aug  4 2014 Tom Callaway <spot@fedoraproject.org> - 0.5.3-2
- fix license handling

* Sat Jun 28 2014 Miro Hrončok <mhroncok@redhat.com> - 0.5.3-1
- Updated to 0.5.3
- Updated the website
- Updated download URL to PyPI
- Removed useless Require of python >= 2.2
- Use %%{pythonX_sitearch} macros
- Removed BuildRoot definition, %%clean section and rm -rf at the beginning of %%install
- Introduced Python 3 subpackage
- Introduced %%check and run the test suite

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.5.1-1
- updated to 0.5.1
- fix bugs found with cpychecker (bug 809974)

* Mon Feb 27 2012 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.5.0-5
- remove prodive/obsolete of python-xattr (bug 781838)
- fix problem with mixed use of tabs and spaces

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Dec 27 2009 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.5.0-1
- updated to 0.5.0
- added support for unicode filenames (bug 479417)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 6 2008 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.4.0-2
- added python-setuptools in BuildRequires which is needed in build process
since version 0.4.0 (thanks to Kevin Fenzi)

* Fri Dec 5 2008 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.4.0-1
- updated to 0.4.0
- License Tag adjusted to current licensing LGPLv2+
- modified Python Eggs support due to its usage in source distribution 

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.2.2-4
- Rebuild for Python 2.6

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.2-3
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.2-2
- added compatibility with Python Eggs forced in F9 

* Mon Aug 27 2007 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.2-1
- upgraded to 0.2.2

* Sun Aug 26 2007 Kevin Fenzi <kevin@tummy.com> - 0.2.1-5
 - Updated License tag

* Wed Apr 25 2007 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.1-4
 - added Provides/Obsoletes tags

* Sat Apr 21 2007 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.1-3
 - removed redundant after name change "exclude" tag
 - comments cleanup

* Wed Apr 18 2007 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.1-2
 - applied suggestions from Kevin Fenzi
 - name changed from python-xattr to pyxattr
 - corrected path to the source file

* Thu Apr 5 2007 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.1-1
 - updated to 0.2.1
 - added python-devel in BuildRequires
 - added more doc files
 - added Provides section
 - modified to Fedora Extras requirements

* Sun Sep 11 2005 Dag Wieers <dag@wieers.com> - 0.2-1 - +/
- Initial package. (using DAR)

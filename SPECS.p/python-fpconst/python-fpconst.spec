%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-fpconst
Version:        0.7.3
Release:        11%{?dist}
Summary:        Python module for handling IEEE 754 floating point special values

Group:          Development/Languages
License:        ASL 2.0
URL:            http://research.warnes.net/statcomp/projects/RStatServer/fpconst
Source0:        http://downloads.sourceforge.net/rsoap/fpconst-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel

%description
This python module implements constants and functions for working with
IEEE754 double-precision special values.  It provides constants for
Not-a-Number (NaN), Positive Infinity (PosInf), and Negative Infinity
(NegInf), as well as functions to test for these values.


%prep
%setup -qn fpconst-%{version}
chmod -x README pep-0754.txt


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CHANGELOG COPYING README pep-0754.txt
%{python_sitelib}/*.py
%{python_sitelib}/*.pyc
%{python_sitelib}/*.pyo
%{python_sitelib}/*.egg-info


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.7.3-11
- 为 Magic 3.0 重建

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.3-7
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.7.3-4
- Rebuild for Python 2.6

* Sat Mar 08 2008 Christopher Stone <chris.stone@gmail.com> 0.7.3-3
- Add egg-info to %%files

* Sat Mar 08 2008 Christopher Stone <chris.stone@gmail.com> 0.7.3-2
- Fix %%Source0 URL

* Sun Sep 30 2007 Christopher Stone <chris.stone@gmail.com> 0.7.3-1
- Upstream sync
- Update source URL
- Some spec file cleanups

* Fri Dec 08 2006 Christopher Stone <chris.stone@gmail.com> 0.7.2-3.2
- Add python-devel to BR

* Fri Dec 08 2006 Christopher Stone <chris.stone@gmail.com> 0.7.2-3.1
- python(abi) = 0:2.5

* Wed Sep 06 2006 Christopher Stone <chris.stone@gmail.com> 0.7.2-3
- No longer %%ghost pyo files.  Bug #205414

* Wed Aug 30 2006 Christopher Stone <chris.stone@gmail.com> 0.7.2-2
- Shorten summary
- Remove unnecessary requires

* Sat Mar 18 2006 Christopher Stone <chris.stone@gmail.com> 0.7.2-1
- Initial Release of python-fpconst, changes from fpconst include:
- Renamed package from fpconst to python-fpconst
- Removed macros in URL
- Removed python-devel from BR
- Droped the second paragraph in %%description
- Droped PKG-INFO from %%doc
- Added pep-0754.txt to %%doc

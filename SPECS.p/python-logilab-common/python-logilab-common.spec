%if 0%{?fedora} > 12
%global with_python3 0
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

Name:           python-logilab-common
Version:        0.58.3
Release:        2%{?dist}
Summary:        Common libraries for Logilab projects
Group:          Development/Libraries
License:        GPLv2+
URL:            http://www.logilab.org/projects/common
Source0:        ftp://ftp.logilab.org/pub/common/logilab-common-%{version}.tar.gz
BuildArch:      noarch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  python-devel python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel python3-setuptools
%endif # if with_python3

%description
This package contains several modules providing low level functionality
shared among some python projects developed by logilab.

%if 0%{?with_python3}
%package -n python3-logilab-common
Summary:        Common libraries for Logilab projects
Group:          Development/Libraries

%description -n python3-logilab-common
This package contains several modules providing low level functionality
shared among some python projects developed by logilab.
%endif # if with_python3

%prep
%setup -q -n logilab-common-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
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

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{python3_sitelib}/logilab/common/test
# Add python3- to the binaries
for FILE in %{buildroot}%{_bindir}/*; do
    NAME=$(basename $FILE)
    mv $FILE %{buildroot}%{_bindir}/python3-$NAME
done
popd
%endif # with_python3

%{__python} setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{python_sitelib}/logilab/common/test

%check
%{__python} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif # with_python3

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README ChangeLog COPYING
%{python_sitelib}/logilab*
%{_bindir}/pytest

%if 0%{?with_python3}
%files -n python3-logilab-common
%defattr(-,root,root,-)
%doc README ChangeLog COPYING
%{python3_sitelib}/logilab*
%{_bindir}/python3-pytest
%endif # with_python3

%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.58.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 10 2013 Brian C. Lane <bcl@redhat.com> 0.58.3-1
- Upstream 0.58.3
- Add python3-logilab-common subpackage to spec. Not ready to turn it on yet
  due to this upstream bug: http://www.logilab.org/ticket/110213

* Fri Aug 03 2012 Brian C. Lane <bcl@redhat.com> 0.58.2-1
- Upstream 0.58.2

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.57.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.57.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Brian C. Lane <bcl@redhat.com> - 0.57.1-1
- Upstream 0.57.1

* Fri Jul 29 2011 Brian C. Lane <bcl@redhat.com> - 0.56.0-1
- Upstream 0.56.0

* Mon Mar 28 2011 Brian C. Lane <bcl@redhat.com> - 0.55.1-1
- Upstream 0.55.1
- Add unit tests to spec

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.53.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 29 2010 Brian C. Lane <bcl@redhat.com> - 0.53.0-1
- Upstream 0.53.0

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.50.3-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 08 2010 Brian C. Lane <bcl@brdhat.com> - 0.50.3-1
- Upstream 0.50.3

* Fri Mar 26 2010 Brian C. Lane <bcl@redhat.com> - 0.49.0-2
- Add python-setuptools to BuildRequires

* Thu Mar 25 2010 Brian C. Lane <bcl@redhat.com> - 0.49.0-1
- Upstream 0.49.0

* Sun Aug 30 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.45.0-1
- Upstream 0.45.0 (small enhancements and bugfixes)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.41.0-2
- Upstream 0.41.0
- Bugfixes and a few minor new features

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.38.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.38.0-1
- Upstream 0.38.0

* Tue Dec 30 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.37.0-1
- Upstream 0.37.0

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.32.0-2
- Rebuild for Python 2.6

* Mon Jun 30 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.32.0-1
- Upstream 0.32.0

* Sun Feb 17 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.28.0-1
- Upstream 0.28.0

* Thu Jan 17 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.26.1-1
- Upstream 0.26.1
- Package egg-info and other files.

* Mon Dec 24 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.25.2-1
- Upstream 0.25.2

* Sun Nov 18 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.24.0-1
- Upstream 0.24.0
- Adjust license to the new standard

* Sun Apr 01 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.21.2-1
- Upstream 0.21.2

* Sun Dec 17 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.21.0-1
- Upstream 0.21.0
- Include COPYING with docs

* Tue Sep 26 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.19.2-1
- Upstream 0.19.2
- Ghostbusting
- Require mx

* Mon May 01 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.15.0-1
- Version 0.15.0

* Sun Mar 12 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.14.1-2
- Also handle __init__.pyc and __init__.pyo

* Sun Mar 12 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.14.1-1
- Version 0.14.1

* Thu Jan 12 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.13.0-1
- Version 0.13.0
- astng no longer part of the package

* Thu Nov 17 2005 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.12.0-1
- Version 0.12.0

* Mon Jun 13 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.10.0-1
- Version 0.10.0.
- Disttagging.

* Thu May 05 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.9.3-3
- Fix paths.

* Tue Apr 26 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.9.3-2
- Ghost .pyo files.
- Get rid of test, which doesn't do anything.

* Fri Apr 22 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.9.3-1
- Initial packaging.

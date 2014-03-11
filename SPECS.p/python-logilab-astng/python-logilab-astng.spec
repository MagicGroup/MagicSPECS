%if 0%{?fedora} > 12
%global with_python3 0
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

Name:           python-logilab-astng
Version:        0.24.1
Release:        2%{?dist}
Summary:        Python Abstract Syntax Tree New Generation
Group:          Development/Languages
License:        GPLv2+
URL:            http://www.logilab.org/projects/astng/
Source0:        ftp://ftp.logilab.org/pub/astng/logilab-astng-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:       python-astng = %{version}-%{release}
Obsoletes:      python-astng <= 0.16.0

BuildArch:      noarch
BuildRequires:  python-devel python-setuptools
BuildRequires:  python-logilab-common >= 0.56.0
Requires:       python-logilab-common >= 0.56.0
%if 0%{?with_python3}
BuildRequires:  python3-devel python3-setuptools
BuildRequires:  python3-logilab-common >= 0.56.0
%endif # if with_python3

%description
The aim of this module is to provide a common base representation of
python source code for projects such as pychecker, pyreverse,
pylint, and others. It extends the class defined in the compiler.ast
python module with some additional methods and attributes.

%if 0%{?with_python3}
%package -n python3-logilab-astng
Summary:        Python Abstract Syntax Tree New Generation
Group:          Development/Languages
Requires:       python3-logilab-common >= 0.56.0

%description -n python3-logilab-astng
The aim of this module is to provide a common base representation of
python source code for projects such as pychecker, pyreverse,
pylint, and others. It extends the class defined in the compiler.ast
python module with some additional methods and attributes.
%endif # if with_python3

%prep
%setup -q -n logilab-astng-%{version}

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
rm -rf %{buildroot}%{python3_sitelib}/logilab/astng/test
# Provided by the python3-logilab-common package
rm -f %{buildroot}%{python3_sitelib}/logilab/__init__.*
# Fix encoding in readme
for FILE in README; do
    iconv -f iso-8859-15 -t utf-8 $FILE > $FILE.utf8
    mv -f $FILE.utf8 $FILE
done
popd
%endif # with_python3

%{__python} setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{python_sitelib}/logilab/astng/test
# Provided by the python-logilab-common package
rm -f %{buildroot}%{python_sitelib}/logilab/__init__.*
# Fix encoding in readme
for FILE in README; do
    iconv -f iso-8859-15 -t utf-8 $FILE > $FILE.utf8
    mv -f $FILE.utf8 $FILE
done

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
%doc README COPYING
%{python_sitelib}/logilab/astng
%{python_sitelib}/logilab_astng*.egg-info
%{python_sitelib}/logilab_astng*.pth

%if 0%{?with_python3}
%files -n python3-logilab-astng
%defattr(-,root,root,-)
%doc README COPYING
%{python3_sitelib}/logilab/astng
%{python3_sitelib}/logilab_astng*.egg-info
%{python3_sitelib}/logilab_astng*.pth
%endif # with_python3

%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 10 2013 Brian C. Lane <bcl@redhat.com> 0.24.1-1
- Upstream v0.24.1
- Add python3-logilab-astng subpackage to spec. Not ready to turn it on yet
  due to this upstream bug: http://www.logilab.org/ticket/110213

* Fri Aug 03 2012 Brian C. Lane <bcl@redhat.com> 0.24.0-1
- Upstream v0.24.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 14 2012 Brian C. Lane <bcl@redhat.com> 0.23.1-1
- Upstream v0.23.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Brian C. Lane <bcl@redhat.com> - 0.23.0-1
- Upstream v0.23.0

* Fri Jul 29 2011 Brian C. Lane <bcl@redhat.com> - 0.22.0-1
- Upstream v0.22.0

* Mon Mar 28 2011 Brian C. Lane <bcl@redhat.com> - 0.21.1-1
- Upstream 0.21.1
- Add unit tests to spec

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 06 2010 Brian C. Lane <bcl@redhat.com> - 0.21.0-2
- Add version to requirement for python-logilab-common so that updates will
  work correctly.

* Mon Nov 29 2010 Brian C. Lane <bcl@redhat.com> - 0.21.0-1
- Upstream 0.21.0

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 08 2010 Brian C. Lane <bcl@redhat.com> - 0.20.1-1
- Upstream 0.20.1

* Thu Mar 25 2010 Brian C. Lane <bcl@redhat.com> - 0.20.0-2
- Added python-setuptools to BuildRequires

* Thu Mar 25 2010 Brian C. Lane <bcl@redhat.com> - 0.20.0-1
- Upstream 0.20.0

* Sun Aug 30 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.19.1-1
- Upstream 0.19.1 (bugfixes)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.19.0-1
- Upstream 0.19.0
- Fixes for better support of python 2.5 and 2.6

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 27 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.17.4-1
- Upstream 0.17.4

* Thu Jan 17 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.17.2-1
- Upstream 0.17.2
- Package .egg-info file

* Mon Dec 24 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.17.1-1
- Upstream 0.17.1
- Adjust license to a more specific GPLv2+
- Fix docs to be valid utf-8

* Sun Apr 01 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.17.0-1
- Upstream 0.17.0

* Sun Dec 17 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.16.3-1
- Upstream 0.16.3

* Tue Sep 26 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.16.1-2
- Setting Provides/Obsoletes as per guidelines.

* Tue Sep 26 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.16.1-1
- Renaming package python-logilab-astng from python-astng. Should have done
  a while ago.
- Upstream version 0.16.1

* Mon May 01 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.16.0-0
- Version 0.16.0

* Sun Mar 12 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.15.1-1
- Version 0.15.1

* Thu Jan 12 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.14.0-1
- Version 0.14.0
- Drop the modname patch

* Tue Nov 15 2005 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.13.1-2
- Patch for the modname traceback

* Sat Nov 12 2005 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.13.1-1
- Fedora Extras import
- Disttagging

* Mon Nov 07 2005 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.13.1-0.1
- Version 0.13.1
- Remove our own GPL license text, since it's now included.

* Sun Nov 06 2005 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.13.0-0.1
- Initial packaging.

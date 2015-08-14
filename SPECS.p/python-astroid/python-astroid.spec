%if 0%{?fedora} > 12
%global with_python3 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

# This needs to be pulled from the source tarball
%global commit cda2deee65e3


Name:           python-astroid
Version:        1.3.7
Release:        1%{?dist}
Summary:        Python Abstract Syntax Tree New Generation
Group:          Development/Languages
License:        GPLv2+
URL:            http://www.astroid.org
Source0:        https://bitbucket.org/logilab/astroid/get/astroid-%{version}.tar.bz2

Patch1:         0001-Fix-multiprocessing-on-py3.4.patch
Patch2:         0001-brain-py2gi-Silence-pygi-deprecation-warnings.patch
Patch3:         0003-Duplicate-calls-to-gi.require_version.patch
Patch4:         0004-Ignore-exceptions-raised-by-gi.require_version.patch
Patch5:         0005-Subprocess-communicate-has-a-different-signature-for.patch
Patch6:         0006-logilab-common-requirement-should-be-1.0.0.patch

Provides:       python-astroid = %{version}-%{release}
Obsoletes:      python-logilab-astng <= 0.24.1

BuildArch:      noarch
BuildRequires:  python-devel python-setuptools python-tools
BuildRequires:  python-six
BuildRequires:  python-logilab-common >= 0.63.2
Requires:       python-logilab-common >= 0.63.2
%if 0%{?with_python3}
BuildRequires:  python3-devel python3-setuptools python3-tools
BuildRequires:  python3-six
BuildRequires:  python3-logilab-common >= 0.63.2
%endif # if with_python3

%description
The aim of this module is to provide a common base representation of
python source code for projects such as pychecker, pyreverse,
pylint, and others. It extends the class defined in the compiler.ast
python module with some additional methods and attributes.

%if 0%{?with_python3}
%package -n python3-astroid
Summary:        Python Abstract Syntax Tree New Generation
Group:          Development/Languages
Requires:       python3-logilab-common >= 0.63.2

%description -n python3-astroid
The aim of this module is to provide a common base representation of
python source code for projects such as pychecker, pyreverse,
pylint, and others. It extends the class defined in the compiler.ast
python module with some additional methods and attributes.
%endif # if with_python3

%prep
%setup -q -n logilab-astroid-%{commit}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

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
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{python3_sitelib}/astroid/tests
# Fix encoding in readme
for FILE in README; do
    iconv -f iso-8859-15 -t utf-8 $FILE > $FILE.utf8
    mv -f $FILE.utf8 $FILE
done
popd
%endif # with_python3

%{__python} setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{python_sitelib}/astroid/tests
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

%files
%doc README COPYING
%{python_sitelib}/astroid
%{python_sitelib}/astroid*.egg-info

%if 0%{?with_python3}
%files -n python3-astroid
%doc README COPYING
%{python3_sitelib}/astroid
%{python3_sitelib}/astroid*.egg-info
%endif # with_python3

%changelog
* Thu Jul 30 2015 Brian C. Lane <bcl@redhat.com> 1.3.7-1
- Upstream 1.3.7
- Fix for subprocess communicate() timeout argument
  https://bitbucket.org/logilab/astroid/pull-requests/83
- Fix for logilab-common required version in astroid

* Tue Jul 14 2015 Brian C. Lane <bcl@redhat.com> 1.3.6-5
- Fixes for gi.require_version from dshea
  https://bitbucket.org/logilab/astroid/pull-request/78

* Tue Jul 07 2015 Brian C. Lane <bcl@redhat.com> 1.3.6-4
- Helps if you actually APPLY the patch in question.

* Tue Jul 07 2015 Brian C. Lane <bcl@redhat.com> 1.3.6-3
- Fix for pygi deprecation warnings
  https://bitbucket.org/logilab/astroid/issue/86

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 28 2015 Brian C. Lane <bcl@redhat.com> 1.3.6-1
- Upstream v1.3.6
- Fix for python3.4 multiprocessing
  https://bitbucket.org/logilab/pylint/issue/265/

* Thu Jan 29 2015 Brian C. Lane <bcl@redhat.com> 1.3.4-2
- Adjust paths for tests

* Wed Jan 28 2015 Brian C. Lane <bcl@redhat.com> 1.3.4-1
- Upstream v1.3.4
  Drop patches now included in upstream

* Fri Oct 17 2014 Brian C. Lane <bcl@redhat.com> 1.2.1-2
- Add patch to fix GLib detection (#1141440)
  https://bitbucket.org/logilab/astroid/issue/49

* Fri Oct 03 2014 Brian C. Lane <bcl@redhat.com> 1.2.1-1
- Upstream v1.2.1
  Drop patches now included in upstream

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Apr 23 2014 Brian C. Lane <bcl@redhat.com> 1.1-3
- Add patch to fix metaclass recursion (upstream bug #25)
  https://bitbucket.org/logilab/astroid/issue/25/runtimeerror-maximum-recursion-depth

* Tue Apr 22 2014 Brian C. Lane <bcl@redhat.com> 1.1-2
- Add missing source file

* Tue Apr 22 2014 Brian C. Lane <bcl@redhat.com> 1.1-1
- Upstream v1.1
  Drop patches now included in upstream

* Tue Apr 01 2014 Cole Robinson <crobinso@redhat.com> - 1.0.1-3
- Fix some gobject introspection false positives (bz #1079643)

* Fri Feb 28 2014 Brian C. Lane <bcl@redhat.com> 1.0.1-2
- Add patch to fix gobject introspection of illegal symbol names (dshea)

* Thu Feb 27 2014 Brian C. Lane <bcl@redhat.com> 1.0.1-1
- Upstream v1.0.1
  Drop patch included in upstream

* Thu Oct 24 2013 Brian C. Lane <bcl@redhat.com> 1.0.0-6
- Switching on python3 support

* Tue Sep 17 2013 Brian C. Lane <bcl@redhat.com> 1.0.0-5
- Switch to versioned obsolete. (#996780)

* Fri Sep 13 2013 Brian C. Lane <bcl@redhat.com> 1.0.0-4
- Fix wrong obsoletes. Should be python-logilab-astng (#1007916)

* Tue Sep 03 2013 Brian C. Lane <bcl@redhat.com> 1.0.0-3
- Add upstream patch for TypeError bug

* Fri Aug 16 2013 Brian C. Lane <bcl@redhat.com> 1.0.0-2
- Removed BuildRoot from spec

* Tue Aug 13 2013 Brian C. Lane <bcl@redhat.com> 1.0.0-1
- Rename package to python-astroid
- Upstream v1.0.0 

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

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

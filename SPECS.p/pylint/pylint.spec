%if 0%{?fedora} > 12
%global with_python3 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

# This needs to be pulled from the source tarball
%global commit 4e17fe0c44f9


Name:           pylint
Version:	1.4.4
Release:	2%{?dist}
Summary:        Analyzes Python code looking for bugs and signs of poor quality
Group:          Development/Debuggers
License:        GPLv2+
URL:            http://www.pylint.org/
Source0:        https://bitbucket.org/logilab/pylint/get/pylint-%{version}.tar.bz2

BuildArch:      noarch
BuildRequires:  python-devel python-setuptools python-tools
BuildRequires:  python-six
BuildRequires:  python-astroid >= 1.3.6
Requires:       python-astroid >= 1.3.6
Requires:       python-setuptools
Requires:       python-six

%description
Pylint is a python tool that checks if a module satisfy a coding standard.
Pylint can be seen as another PyChecker since nearly all tests you can do
with PyChecker can also be done with Pylint. But Pylint offers some more
features, like checking line-code's length, checking if variable names are
well-formed according to your coding standard, or checking if declared
interfaces are truly implemented, and much more. The big advantage with
Pylint is that it is highly configurable, customizable, and you can easily
write a small plugin to add a personal feature.

%if 0%{?with_python3}
%package -n python3-pylint
Summary:        Analyzes Python code looking for bugs and signs of poor quality
Group:          Development/Debuggers
BuildRequires:  python3-devel python3-setuptools python3-tools
BuildRequires:  python3-six
BuildRequires:  python3-astroid >= 1.3.6
Requires:       python3-astroid >= 1.3.6
Requires:       python3-setuptools
Requires:       python3-six

%description -n python3-pylint
Pylint is a python tool that checks if a module satisfy a coding standard.
Pylint can be seen as another PyChecker since nearly all tests you can do
with PyChecker can also be done with Pylint. But Pylint offers some more
features, like checking line-code's length, checking if variable names are
well-formed according to your coding standard, or checking if declared
interfaces are truly implemented, and much more. The big advantage with
Pylint is that it is highly configurable, customizable, and you can easily
write a small plugin to add a personal feature.
%endif # with_python3

%package gui
Summary:        Graphical Interface tool for Pylint
Group:          Development/Debuggers
Requires:       %{name} = %{version}-%{release}
Requires:       tkinter

%description gui
This package provides a gui tool for pylint written in tkinter.

%if 0%{?with_python3}
%package -n python3-pylint-gui
Summary:        Graphical Interface tool for Pylint
Group:          Development/Debuggers
Requires:       python3-pylint = %{version}-%{release}
Requires:       python3-tkinter

%description -n python3-pylint-gui
This package provides a gui tool for pylint written in tkinter.
%endif # with_python3

%prep
%setup -q -n logilab-pylint-%{commit}

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
rm -rf %{buildroot}%{python3_sitelib}/pylint/test
mkdir -pm 755 %{buildroot}%{_mandir}/man1
install -pm 644 man/*.1 %{buildroot}%{_mandir}/man1/
# Add python3- to the binaries
for FILE in %{buildroot}%{_bindir}/*; do
    NAME=$(basename $FILE)
    mv $FILE %{buildroot}%{_bindir}/python3-$NAME
done
# Add python3- to the manpages
for FILE in %{buildroot}%{_mandir}/man1/*; do
    NAME=$(basename $FILE)
    mv $FILE %{buildroot}%{_mandir}/man1/python3-$NAME
done
popd
%endif # with_python3

%{__python} setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{python_sitelib}/pylint/test
mkdir -pm 755 %{buildroot}%{_mandir}/man1
install -pm 644 man/*.1 %{buildroot}%{_mandir}/man1/

%check
%{__python} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif # with_python3

%files
%defattr(-,root,root,-)
%doc README ChangeLog examples elisp COPYING
%{python_sitelib}/pylint*
%{_bindir}/*
%{_mandir}/man?/*
%exclude %{python_sitelib}/pylint/gui.py*
%exclude %{_bindir}/pylint-gui
%exclude %{_bindir}/python3-*
%exclude %{_mandir}/man?/python3-*

%files gui
%defattr(-,root,root,-)
%doc COPYING
%{python_sitelib}/pylint/gui.py*
%{_bindir}/pylint-gui

%if 0%{?with_python3}
%files -n python3-pylint
%defattr(-,root,root,-)
%doc README ChangeLog examples elisp COPYING
%{python3_sitelib}/pylint*
%{_bindir}/python3-*
%{_mandir}/man?/python3-*
%exclude %{python3_sitelib}/pylint/gui.py*
%exclude %{_bindir}/python3-pylint-gui

%files -n python3-pylint-gui
%defattr(-,root,root,-)
%doc COPYING
%{python3_sitelib}/pylint/gui.py*
%{_bindir}/python3-pylint-gui
%endif # with_python3

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.4.4-2
- 为 Magic 3.0 重建

* Fri Aug 14 2015 Liu Di <liudidi@gmail.com> - 1.4.4-1
- 更新到 1.4.4

* Fri Aug 14 2015 Liu Di <liudidi@gmail.com> - 1.4.3-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Mathieu Bridon <bochecha@daitauha.fr> - 1.4.3-2
- Drop python3 requirements from the python2 package.
- Add missing requirement on six.

* Tue Apr 28 2015 Brian C. Lane <bcl@redhat.com> 1.4.3-1
- Upstream v1.4.3

* Fri Jan 30 2015 Brian C. Lane <bcl@redhat.com> 1.4.1-3
- Exclude the python3-* files from the python2 package

* Thu Jan 29 2015 Brian C. Lane <bcl@redhat.com> 1.4.1-2
- Add python-six requirement

* Wed Jan 28 2015 Brian C. Lane <bcl@redhat.com> 1.4.1-1
- Upstream v1.4.1

* Mon Oct 27 2014 Brian C. Lane <bcl@redhat.com> 1.3.1-2
- python3-pylint-gui needs python3-tkinter

* Fri Oct 03 2014 Brian C. Lane <bcl@redhat.com> 1.3.1-1
- Upstream v1.3.1
  Dropped patches included in upstream

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Brian C. Lane <bcl@redhat.com> 1.2-6
- Add python3-astroid and python3-setuptools as Requires (#1103479)

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri May 09 2014 Brian C. Lane <bcl@redhat.com> 1.2-4
- Fix a potential AttributeError when checking for `reversed` arguments.
  https://bitbucket.org/logilab/pylint/commits/93babaf6bffc59a49c75319d9850086b4935edbc

* Thu May 08 2014 Brian C. Lane <bcl@redhat.com> 1.2-3
- fix explicit check of python script
  https://bitbucket.org/logilab/pylint/issue/219/

* Thu Apr 24 2014 Brian C. Lane <bcl@redhat.com> 1.2-2
- Patch to Fix --init-hook typo (dshea)
  https://bitbucket.org/logilab/pylint/issue/211/init-hook-no-longer-works

* Tue Apr 22 2014 Brian C. Lane <bcl@redhat.com> 1.2-1
- Upstream v1.2

* Thu Feb 27 2014 Brian C. Lane <bcl@redhat.com> 1.1.0-1
- Upstream v1.1.0
  Drop patch included in upstream

* Thu Oct 24 2013 Brian C. Lane <bcl@redhat.com> 1.0.0-3
- Switching on python3 support

* Tue Sep 03 2013 Brian C. Lane <bcl@redhat.com> 1.0.0-2
- Add upstream patch for epylint input validation (#981859)

* Tue Aug 13 2013 Brian C. Lane <bcl@redhat.com> 1.0.0-1
- Upstream 1.0.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 10 2013 Brian C. Lane <bcl@redhat.com> 0.26.0-1
- Upstream 0.26.0
- Add python3-pylint and python3-pylint-gui subpackages. Not ready to turn it
  on yet due to this upstream bug: http://www.logilab.org/ticket/110213

* Fri Aug 03 2012 Brian C. Lane <bcl@redhat.com> 0.25.2-1
- Upstream 0.25.2

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 14 2012 Brian C. Lane <bcl@redhat.com> 0.25.1-1
- Upstream 0.25.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Brian C. Lane <bcl@redhat.com> - 0.25.0-1
- Upstream 0.25.0

* Fri Jul 29 2011 Brian C. Lane <bcl@redhat.com> - 0.24.0-1
- Upstream 0.24.0

* Mon Mar 28 2011 Brian C. Lane <bcl@redhat.com> - 0.23-0.1
- Upstream 0.23.0
- Add unit tests to spec

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 06 2010 Brian C. Lane <bcl@redhat.com> - 0.22.0-2
- Add version to requirement for python-logilab-astng so that updates will
  work correctly.

* Mon Nov 29 2010 Brian C. Lane <bcl@redhat.com> - 0.22.0-1
- Upstream 0.22.0

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.21.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 08 2010 Brian C. Lane <bcl@redhat.com> - 0.21.1-1
- Upstream 0.21.1
- Removed patch for 500272, fixed upstream - http://www.logilab.org/ticket/22962

* Mon Apr 05 2010 Brian C. Lane <bcl@redhat.com> - 0.20.0-2
- Added patch for bug 500272 (exception with --disable-msg-cat)

* Fri Mar 26 2010 Brian C.Lane <bcl@redhat.com> - 0.20.0-1
- Upstream 0.20.0
- Added python-setuptools to BuildRequires

* Sun Aug 30 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.18.1-1
- Upstream 0.18.1 (bugfixes and small enhancements)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.18.0-1
- Upstream 0.18.0 (bugfixes and minor feature updates)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.16.0-1
- Upstream 0.16.0

* Tue Dec 30 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.15.2-1
- Upstream 0.15.2

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.14.0-2
- Rebuild for Python 2.6

* Thu Jan 17 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.14.0-1
- Upstream 0.14.0
- Package the .egg-info files.

* Mon Dec 24 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.13.2-1
- Upstream 0.13.2
- Adjust license to a more precise version
- Fix docs to be valid utf-8

* Sun Apr 01 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.13.1-1
- Upstream 0.13.1

* Sun Dec 17 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.12.2-1
- Upstream 0.12.2
- Add COPYING to -gui

* Tue Sep 26 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.12.1-1
- Upstream 0.12.1
- Require the renamed python-logilab-astng

* Mon May 01 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.11.0-0
- Version 0.11.0

* Sun Mar 12 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.10.0-1
- Version 0.10.0

* Thu Jan 12 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.9.0-1
- Version 0.9.0
- Add COPYING to docs

* Sun Nov 13 2005 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.8.1-1
- Version 0.8.1
- Add dependency on python-astng
- Drop artificial version requirement on python-logilab-common

* Mon Jun 13 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.7.0-1
- Version 0.7.0
- No longer in the logilab subdir
- Disttagging

* Mon May 09 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.6.4-4
- Install the pylint.1 manfile.
- Add examples and elisp dirs to docs.

* Thu May 05 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.6.4-3
- Only doc the .txt files.
- Don't buildrequire python-logilab-common
- Fix paths.

* Tue Apr 26 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.6.4-2
- Ghost .pyo files.
- Remove the test dir, as it doesn't do anything.
- Separate the gui package, which depends on tkinter.
- Don't own site-packages/logilab, which is owned by
  python-logilab-common.

* Fri Apr 22 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.6.4-1
- Initial packaging.

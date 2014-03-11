%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:       python-reportlab
Version:    2.5
Release:    6%{?dist}
Summary:    Python PDF generation library

Group:      Development/Libraries
License:    BSD
URL:        http://www.reportlab.org/
Source0:    http://www.reportlab.org/ftp/reportlab-%{version}.tar.gz
Patch0:     reportlab-%{version}-font-locations.patch

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: python-devel, python-imaging, freetype-devel
Requires:   dejavu-sans-fonts


%description
Python PDF generation library.


%package docs
Summary:    Documentation files for %{name}
Group:        Documentation
Requires:    %{name} = %{version}-%{release}


%description docs
Contains the documentation for ReportLab.


%prep
%setup -q -n reportlab-%{version}
%patch0 -p1 -b .fonts
# clean up hashbangs from libraries
find src -name '*.py' | xargs sed -i -e '/^#!\//d'


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
# a bit of a horrible hack due to a chicken-and-egg problem. The docs
# require reportlab, which isn't yet installed, but is at least built.
PYTHONPATH="`pwd`/`ls -d build/lib*`" %{__python} docs/genAll.py


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
# Remove bundled fonts
rm -rf $RPM_BUILD_ROOT%{python_sitearch}/reportlab/fonts


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.txt CHANGES.txt LICENSE.txt
%{python_sitearch}/reportlab
%{python_sitearch}/reportlab*.egg-info
%{python_sitearch}/*.so


%files docs
%defattr(-,root,root,-)
%doc docs/*.pdf demos tools LICENSE.txt


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.5-6
- 为 Magic 3.0 重建

* Wed Jan 25 2012 Liu Di <liudidi@gmail.com> - 2.5-5
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.5-2
- Update to version 2.5 of reportlab.
- Remove tabs in specfile.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Nov 23 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.3-2
- Do not bundle fonts
- Point the config to Fedora's font locations

* Thu Nov 12 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.3-1
- Updated to 2.3
- New version is no longer noarch.

* Fri Apr 17 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 2.1-6
- Rebuild for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.1-4
- Fix locations for Python 2.6

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.1-3
- Rebuild for Python 2.6

* Mon Jan  7 2008 Brian Pepple <bpepple@fedoraproject.org> - 2.1-2
- Remove luxi font. (#427845)
- Add patch to not search for the luxi font.

* Sat May 26 2007 Brian Pepple <bpepple@fedoraproject.org> - 2.1-1
- Update to 2.1.

* Wed Dec 27 2006 Brian Pepple <bpepple@fedoraproject.org> - 2.0-2
- Make docs subpackage.

* Wed Dec 27 2006 Brian Pepple <bpepple@fedoraproject.org> - 2.0-1
- Update to 2.0.

* Fri Dec  8 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.21.1-2
- Rebuild against new python.

* Thu Sep  7 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.21.1-1
- Update to 1.20.1.

* Tue Feb 14 2006 Brian Pepple <bdpepple@ameritech.net> - 1.20-5
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Dec 26 2005 Brian Pepple <bdpepple@ameritech.net> - 1.20-4
- Add dist tag. (#176479)

* Mon May  9 2005 Brian Pepple <bdpepple@ameritech.net> - 1.20-3.fc4
- Switchback to sitelib patch.
- Make package noarch.

* Thu Apr  7 2005 Brian Pepple <bdpepple@ameritech.net> - 1.20-2.fc4
- Use python_sitearch to fix x86_64 build.

* Wed Mar 30 2005 Brian Pepple <bdpepple@ameritech.net> - 1.20-1.fc4
- Rebuild for Python 2.4.
- Update to 1.20.
- Switch to the new python macros for python-abi
- Add dist tag.

* Sat Apr 24 2004 Brian Pepple <bdpepple@ameritech.net> 0:1.19-0.fdr.2
- Removed ghosts.

* Sat Mar 20 2004 Brian Pepple <bdpepple@ameritech.net> 0:1.19-0.fdr.1
- Initial Fedora RPM build.


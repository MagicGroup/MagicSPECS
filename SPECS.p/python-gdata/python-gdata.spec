%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:           python-gdata
Version:        2.0.14
Release:        3%{?dist}
Summary:        A Python module for accessing online Google services

Group:          Development/Languages
License:        ASL 2.0
URL:            http://code.google.com/p/gdata-python-client/
Source0:        http://gdata-python-client.googlecode.com/files/gdata-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
Requires:       python >= 2.5


%description
This is a Python module for accessing online Google services such as:
- Base
- Blogger
- Calendar
- Health
- Picasa Web Albums
- Spreadsheets
- Documents List
- Contacts
- YouTube
- Google Apps Provisioning
- Code Search
- Notebook
- Webmaster Tools API
- Google Analytics Data Export API
- Google Book Search Data API
- Google Finance Portfolio Data API
- Google Maps Data API
- Sites Data API
- Issue Tracker Data API


%prep
%setup -q -n gdata-%{version}
find samples src -type f -print0 | xargs -0 chmod a-x
find src -type f -print0 |  xargs -0 sed -i -e '/^#!\//, 1d' *.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README.txt RELEASE_NOTES.txt samples/
%{python_sitelib}/atom
%{python_sitelib}/gdata
%{python_sitelib}/gdata-%{version}-py*.egg-info

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.0.14-3
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Mar 28 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 2.0.14-1
- New upstream release
- Drop clean section
- Fix relevant rpmlint errors and warnings
- 
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct  9 2010 Richard Fearn <richardfearn@gmail.com> - 2.0.12-1
- Update to 2.0.12 (rhbz#635717)

* Sat Jul 31 2010 Adam Goode <adam@spicenitz.org> - 2.0.11-1
- Update to 2.0.11
- Clean up the specfile a little

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jun 16 2010 Richard Fearn <richardfearn@gmail.com> - 2.0.10-1
- Update to 2.0.10

* Thu Apr 15 2010 Roshan Kumar Singh <singh.roshan08@gmail.com> - 2.0.9-2
- Update to 2.0.9 with fixed permission issue

* Thu Mar 18 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 2.0.9-1
- Update to 2.0.9

* Sat Oct 10 2009 Bastien Nocera <bnocera@redhat.com> 2.0.3-1
- Update to 2.0.3

* Tue Sep 01 2009 Bastien Nocera <bnocera@redhat.com> 2.0.2-1
- Update to 2.0.2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 24 2009 Bastien Nocera <bnocera@redhat.com> 2.0.1-1
- Update to 2.0.1

* Tue Jun 30 2009 Bastien Nocera <bnocera@redhat.com> 2.0.0-1
- Update to 2.0.0

* Mon Jun 08 2009 Bastien Nocera <bnocera@redhat.com> 1.3.3-1
- Update to 1.3.3

* Wed Apr 29 2009 Bastien Nocera <bnocera@redhat.com> 1.3.1-2
- Fix deprecation warning (#492641)

* Fri Apr 24 2009 Bastien Nocera <bnocera@redhat.com> 1.3.1-1
- Update to 1.3.1

* Sun Mar 22 2009 - Bastien Nocera <bnocera@redhat.com> - 1.3.0-1
- Update to 1.3.0

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 - Bastien Nocera <bnocera@redhat.com> - 1.2.4-1
- Update to 1.2.4

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.2.3-2
- Rebuild for Python 2.6

* Thu Dec 04 2008 - Bastien Nocera <bnocera@redhat.com> - 1.2.3-1
- Update to 1.2.3

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.2.2-2
- Rebuild for Python 2.6

* Wed Oct 22 2008 - Bastien Nocera <bnocera@redhat.com> - 1.2.2-1
- Update to 1.2.2 (#467563)

* Mon May 12 2008 - Bastien Nocera <bnocera@redhat.com> - 1.0.13-1
- Update to 1.0.13 (#446000)

* Tue Nov 13 2007 - Bastien Nocera <bnocera@redhat.com> - 1.0.9-1
- Update to 1.0.9

* Sun Oct 21 2007 - Bastien Nocera <bnocera@redhat.com> - 1.0.8-3
- Remove CFLAGS from the make part,as there's no native compilation,
  spotted by Parag AN <panemade@gmail.com>

* Tue Oct 16 2007 - Bastien Nocera <bnocera@redhat.com> - 1.0.8-2
- Remove python-elementtree dep,it's builtin to Python 2.5
- Add samples to the docs,for documentation purposes
- Remove unneeded macro

* Fri Oct 12 2007 - Bastien Nocera <bnocera@redhat.com> - 1.0.8-1
- Initial RPM release

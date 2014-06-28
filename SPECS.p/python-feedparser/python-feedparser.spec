%if 0%{?fedora} > 12 || 0%{?rhel} > 6
%global with_python3 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

%global srcname feedparser

Name:           python-feedparser
Version:        5.1
Release:        3%{?dist}
Summary:        Parse RSS and Atom feeds in Python

Group:          Development/Languages
License:        BSD
URL:            http://feedparser.org/
Source0:        http://feedparser.googlecode.com/files/feedparser-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
Universal Feed Parser is a Python module for downloading and parsing 
syndicated feeds. It can handle RSS 0.90, Netscape RSS 0.91, 
Userland RSS 0.91, RSS 0.92, RSS 0.93, RSS 0.94, RSS 1.0, RSS 2.0, 
Atom 0.3, Atom 1.0, and CDF feeds. It also parses several popular extension 
modules, including Dublin Core and Apple's iTunes extensions.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        Parse RSS and Atom feeds in Python
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%description -n python3-%{srcname}
Universal Feed Parser is a Python module for downloading and parsing 
syndicated feeds. It can handle RSS 0.90, Netscape RSS 0.91, 
Userland RSS 0.91, RSS 0.92, RSS 0.93, RSS 0.94, RSS 1.0, RSS 2.0, 
Atom 0.3, Atom 1.0, and CDF feeds. It also parses several popular extension 
modules, including Dublin Core and Apple's iTunes extensions.
%endif


%prep
%setup -q -n %{srcname}-%{version}
find -type f -exec sed -i 's/\r//' {} ';'
find -type f -exec chmod 0644 {} ';'
%if 0%{?with_python3}
cp -a . %{py3dir}
%endif


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd
%endif


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif


#%check
#%{__python} feedparser/feedparsertest.py
#%if 0%{?with_python3}
#pushd %{py3dir}
#%{__python3} feedparser/feedparsertest.py
#popd
#%endif

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc LICENSE README
%{python3_sitelib}/*
%endif

%changelog
* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 5.1-3
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 5.1-2
- 为 Magic 3.0 重建

* Sat Feb  4 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 5.1-1
- upstream 5.1 (#787401)
- spec cleanup
- tests disabled
- python3 support

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Apr 05 2011 Luke Macken <lmacken@redhat.com> - 5.0.1-1
- Latest upstream release
- Remove feedparser_utf8_decoding.patch
- Remove democracynow_feedparser_fix.patch
- Run the test suite

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 4.1-12
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Dec 14 2009 Haïkel Guémar <karlthered@gmail.com> - 4.1-11
- rebuild for Fedora 13

* Fri Aug 07 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.1-10
- Apply patch for title munging issue (#491373)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 04 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.1-8
- Fix source URL (moved to googlecode).

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 27 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.1-6
- Patch for a utf8 decoding issue (#477024)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 4.1-5
- Rebuild for Python 2.6

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4.1-4
- fix license tag

* Thu Jun 28 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.1-3
- Ghostbusting (#205413).
- Remove manual python-abi Requires.
- Appease rpmlint.

* Sat Dec 23 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 4.1-2
- Rebuild for new Python.

* Wed Jan 11 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.1-1
- Version 4.1

* Sat Jan 07 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.0.2-2
- Set sane permissions on doc files.

* Wed Jan 04 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.0.2-1
- Initial build.

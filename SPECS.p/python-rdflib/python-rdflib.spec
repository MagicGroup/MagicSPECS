%define run_tests 0

Name:           python-rdflib
Version:        3.2.0
Release:        6%{?dist}
Summary:        Python library for working with RDF

Group:          Development/Languages
License:        BSD
URL:            http://code.google.com/p/rdflib/
Source0:        http://rdflib.googlecode.com/files/rdflib-%{version}.tar.gz
# Upstreamed: http://code.google.com/p/rdflib/issues/detail?id=206
Patch0:         0001-Skip-test-if-it-can-not-join-the-network.patch
BuildArch:      noarch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires:       python-isodate

BuildRequires:  python-isodate
BuildRequires:  python-devel
BuildRequires: python-setuptools-devel

%if %{run_tests}
BuildRequires:  python-nose >= 0.9.2
%endif

%description
RDFLib is a Python library for working with RDF, a simple yet powerful
language for representing information.

The library contains parsers and serializers for RDF/XML, N3, NTriples,
Turtle, TriX and RDFa. The library presents a Graph interface which can
be backed by any one of a number of store implementations, including
memory, MySQL, Redland, SQLite, Sleepycat, ZODB and SQLObject.

%prep
%setup -q -n rdflib-%{version}

%patch0 -p0 -b .test

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
cp LICENSE $RPM_BUILD_ROOT/%{python_sitelib}/rdflib/LICENSE

# Various .py files within site-packages have a shebang line but aren't
# flagged as executable.
# I've gone through them and either removed the shebang or made them
# executable as appropriate:

# __main__ parses URI as N-Triples:
chmod +x $RPM_BUILD_ROOT/%{python_sitelib}/rdflib/plugins/parsers/ntriples.py

# __main__ parses the file given on the command line:
chmod +x $RPM_BUILD_ROOT/%{python_sitelib}/rdflib/plugins/parsers/notation3.py

magic_rpm_clean.sh

%check
%if %{run_tests}
sed -i -e "s|'--with-doctest'|#'--with-doctest'|" run_tests.py
%{__python} run_tests.py
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE
%{python_sitelib}/*

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 3.2.0-6
- 为 Magic 3.0 重建

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 3.2.0-4
- Re-add the unittests, for that, patch one and disable the run of
the tests in the documentation of the code.

* Mon Jan 23 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 3.2.0-3
- Add python-isodate as R (RHBZ#784027)

* Fri Jan 20 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 3.2.0-2
- Found the official sources of the 3.2.0 release

* Fri Jan 20 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 3.2.0-1
- Update to 3.2.0-RC which seem to be same as 3.2.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 28 2011 David Malcolm <dmalcolm@redhat.com> - 3.1.0-1
- 3.1.0; converting from arch-specific to noarch (sitearch -> sitelib);
removing rdfpipe and various other extensions

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jan  6 2010 David Malcolm <dmalcolm@redhat.com> - 2.4.2-1
- bump to 2.4.2 (#552909)
- fix source URL to use version macro

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 10 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.4.0-8
- Rebuild for Python 2.6

* Wed Oct  1 2008 David Malcolm <dmalcolm@redhat.com> - 2.4.0-7
- fix tab/space issue in specfile

* Tue Sep 30 2008 David Malcolm <dmalcolm@redhat.com> - 2.4.0-6
- override autogeneration of provides info to eliminate unwanted provision
of SPARQLParserc.so

* Mon Sep 29 2008 David Malcolm <dmalcolm@redhat.com> - 2.4.0-5
- make various scripts executable, or remove shebang, as appropriate

* Tue Feb 19 2008 David Malcolm <dmalcolm@redhat.com> - 2.4.0-4
- delete test subdir

* Thu Jan 24 2008 David Malcolm <dmalcolm@redhat.com> - 2.4.0-3
- introduce macro to disable running the test suite, in the hope of eventually
patching it so it passes

* Mon Nov 19 2007 David Malcolm <dmalcolm@redhat.com> - 2.4.0-2
- add python-setuptools(-devel) build requirement; move testing to correct stanza

* Wed Aug  1 2007 David Malcolm <dmalcolm@redhat.com> - 2.4.0-1
- initial version


%global with_python3 1

%{!?__python2:%global __python2 %{__python}}
%{!?python2_sitelib:   %global python2_sitelib         %{python_sitelib}}
%{!?python2_sitearch:  %global python2_sitearch        %{python_sitearch}}
%{!?python2_version:   %global python2_version         %{python_version}}

%global pypi_name rdflib

%global run_tests 1

Name:           python-rdflib
Version:	4.2.1
Release:	3%{?dist}
Summary:        Python library for working with RDF
Summary(zh_CN.UTF-8): RDF 的 Python 库

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        BSD
URL:            https://github.com/RDFLib/rdflib
Source0:        http://pypi.python.org/packages/source/r/rdflib/rdflib-%{version}.tar.gz
Patch1:         python-rdflib-SPARQLWrapper-optional.patch
BuildArch:      noarch

Requires:       python-html5lib >= 1:
Requires:       python-isodate
Requires:       pyparsing

BuildRequires:  python-html5lib >= 1:
BuildRequires:  python-isodate
BuildRequires:  pyparsing
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%if %{run_tests}
BuildRequires:  python-nose >= 0.9.2
%endif

Obsoletes:      python-rdfextras <= 0.1-7


%description
RDFLib is a Python library for working with RDF, a simple yet powerful
language for representing information.

The library contains parsers and serializers for RDF/XML, N3,
NTriples, Turtle, TriX, RDFa and Microdata. The library presents
a Graph interface which can be backed by any one of a number of
Store implementations. The core rdflib includes store
implementations for in memory storage, persistent storage on top
of the Berkeley DB, and a wrapper for remote SPARQL endpoints.

A SPARQL 1.1 engine is also included.
%description -l zh_CN.UTF-8
RDF 的 Python 库。

%if %{with_python3}
%package -n python3-%{pypi_name}
Summary:        Python library for working with RDF
Summary(zh_CN.UTF-8): RDF 的 Python 库
BuildRequires:  python3-html5lib >= 1:
BuildRequires:  python3-isodate
BuildRequires:  python3-pyparsing
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%if %{run_tests}
BuildRequires:  python3-nose >= 0.9.2
%endif


%description -n python3-%{pypi_name}
RDFLib is a Python library for working with RDF, a simple yet powerful
language for representing information.

The library contains parsers and serializers for RDF/XML, N3,
NTriples, Turtle, TriX, RDFa and Microdata. The library presents
a Graph interface which can be backed by any one of a number of
Store implementations. The core rdflib includes store
implementations for in memory storage, persistent storage on top
of the Berkeley DB, and a wrapper for remote SPARQL endpoints.

A SPARQL 1.1 engine is also included.
%description -n python3-%{pypi_name} -l zh_CN.UTF-8
RDF 的 Python 库。
%endif

%prep
%setup -q -n rdflib-%{version}
%patch1 -p1

# remove bundled egg-info
rm -rf %{pypi_name}.egg-info

find -name "*.pyc" -delete

sed -i -e 's|_sn_gen=bnode_uuid()|_sn_gen=bnode_uuid|' test/test_bnode_ncname.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%{__python2} setup.py build

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd

# rename binaries
for i in csv2rdf rdf2dot rdfgraphisomorphism rdfpipe rdfs2dot; do
    mv %{buildroot}%{_bindir}/$i %{buildroot}%{_bindir}/python3-$i
done

%endif

%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
cp LICENSE $RPM_BUILD_ROOT/%{python_sitelib}/rdflib/LICENSE

# Various .py files within site-packages have a shebang line but aren't
# flagged as executable.
# I've gone through them and either removed the shebang or made them
# executable as appropriate:

# __main__ parses URI as N-Triples:
chmod +x $RPM_BUILD_ROOT/%{python_sitelib}/rdflib/plugins/parsers/ntriples.py

# __main__ parses the file given on the command line:
chmod +x $RPM_BUILD_ROOT/%{python_sitelib}/rdflib/plugins/parsers/notation3.py

# __main__ parses the file or URI given on the command line:
chmod +x $RPM_BUILD_ROOT/%{python_sitelib}/rdflib/tools/rdfpipe.py

# __main__ runs a test (well, it's something)
chmod +x $RPM_BUILD_ROOT/%{python_sitelib}/rdflib/extras/infixowl.py

# sed these headers out as they include no __main__
for lib in $RPM_BUILD_ROOT/%{python_sitelib}/rdflib/extras/describer.py \
    $RPM_BUILD_ROOT/%{python_sitelib}/rdflib/plugins/parsers/pyRdfa/extras/httpheader.py \
    $RPM_BUILD_ROOT/%{python_sitelib}/rdflib/plugins/parsers/structureddata.py; do
 sed '1{\@^#!/usr/bin/env python@d}' $lib > $lib.new &&
 touch -r $lib $lib.new &&
 mv $lib.new $lib
done
magic_rpm_clean.sh

%check
%if %{run_tests}
sed -i -e "s|'--with-doctest'|#'--with-doctest'|" run_tests.py
sed -i -e "s|'--doctest-tests'|#'--doctest-tests'|" run_tests.py
sed -i -e "s|with-doctest = 1|#with-doctest = 1|" setup.cfg
PYTHONPATH=./build/lib %{__python} run_tests.py --verbose
%endif

%files
%doc LICENSE
%{python_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py%{python2_version}.egg-info
%{_bindir}/csv2rdf
%{_bindir}/rdf2dot
%{_bindir}/rdfgraphisomorphism
%{_bindir}/rdfpipe
%{_bindir}/rdfs2dot

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info
%{_bindir}/python3-csv2rdf
%{_bindir}/python3-rdf2dot
%{_bindir}/python3-rdfgraphisomorphism
%{_bindir}/python3-rdfpipe
%{_bindir}/python3-rdfs2dot
%endif

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 4.2.1-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 4.2.1-2
- 为 Magic 3.0 重建

* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 4.2.1-1
- 更新到 4.2.1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 05 2015 Matthias Runge <mrunge@redhat.com> - 4.1.2-3
- add python3 subpackage (rhbz#1086844)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 18 2014 Dan Scott <dan@coffeecode.net> - 4.1.2-1
- Update for 4.1.2 release
- Add PYTHONPATH awareness for running tests

* Tue Mar 04 2014 Dan Scott <dan@coffeecode.net> - 4.1.1-1
- Update for 4.1.1 release
- Support for RDF 1.1 and HTML5
- Support for RDFa, TRiG, microdata parsers, and HTML structured data
- Patch to make SPARQLWrapper an extras_require until it is packaged

* Thu Dec 12 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 3.2.3-6
- Remove BR of python-setuptools-devel

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 David Malcolm <dmalcolm@redhat.com> - 3.2.3-4
- disable doctests (rhbz#914414)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 10 2012  Pierre-Yves Chibon <pingou@pingoured.fr> - 3.2.3-2
- Re-enable tests
- Backport using sed unit-tests fix from upstream
   (commit 26d25faa90483ed1ba7675d159d10e955dbaf442)

* Wed Oct 10 2012  Pierre-Yves Chibon <pingou@pingoured.fr> - 3.2.3-1
- Update to 3.2.3
- One test is failing, so disabling them for now

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


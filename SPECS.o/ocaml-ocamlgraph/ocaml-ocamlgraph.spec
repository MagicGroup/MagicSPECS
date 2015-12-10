%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%global ocaml_destdir %{_libdir}/ocaml
%if !%{opt}
%global debug_package %{nil}
%endif

# Disable documentation.  In ocamldoc 4.02 we get the error
#   analyse_module: parsetree and typedtree don't match.
%global documentation 0

Name:           ocaml-ocamlgraph
Version:        1.8.5
Release:        7%{?dist}
Summary:        OCaml library for arc and node graphs
Summary(zh_CN.UTF-8): arc 和 node 图形的 OCaml 库

License:        LGPLv2 with exceptions
URL:            http://ocamlgraph.lri.fr/
Source0:        http://ocamlgraph.lri.fr/download/ocamlgraph-%{version}.tar.gz
Source1:        ocamlgraph-test.result
# When building the byte variant, do not try to install artifacts that were
# not built.
Patch0:         ocamlgraph-1.8.5-byte-install.patch

BuildRequires:  libart_lgpl-devel
BuildRequires:  libgnomecanvas-devel
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-lablgtk-devel
BuildRequires:  ocaml-ocamldoc

%global __requires_exclude ocaml\\\(Sig\\\)
%global libname %(sed -e 's/^ocaml-//' <<< %{name})

%description
Ocamlgraph provides several different implementations of graph data
structures. It also provides implementations for a number of classical
graph algorithms like Kruskal's algorithm for MSTs, topological
ordering of DAGs, Dijkstra's shortest paths algorithm, and
Ford-Fulkerson's maximal-flow algorithm to name a few. The algorithms
and data structures are written functorially for maximal
reusability. Also has input and output capability for Graph Modeling
Language file format and Dot and Neato graphviz (graph visualization)
tools.

%description -l zh_CN.UTF-8
arc 和 node 图形的 OCaml 库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        tools
Summary:        Graph editing tools for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    tools
The %{name}-tools package contains graph editing tools for use with
%{name}.


%prep
%setup -q -n %{libname}-%{version}
%if ! %opt
%patch0
%endif

cp -p %{SOURCE1} .

# Remove spurious executable bits
find . -name '*.ml*' -perm /0111 | xargs chmod a-x

# Fix encoding
for fil in CHANGES COPYING CREDITS; do
  iconv -f latin1 -t utf-8 $fil > $fil.utf8
  touch -r $fil $fil.utf8
  mv -f $fil.utf8 $fil
done


%build
%configure

%if %opt
%global opt_option OCAMLBEST=opt OCAMLOPT='ocamlopt.opt -g'
%else
%global opt_option OCAMLBEST=byte OCAMLC=ocamlc
%endif
make depend
make %{opt_option}
%if %documentation
make doc
%endif

%check
make --no-print-directory check >& test
diff -u test ocamlgraph-test.result


%install
mkdir -p %{buildroot}%{ocaml_destdir}
make OCAMLFIND_DESTDIR=%{buildroot}%{ocaml_destdir} install-findlib
%if %opt
install -m 0755 -p graph.cmxs %{buildroot}%{ocaml_destdir}/%{libname}
%endif

# Include all code and examples in the docs
mkdir -p dox-devel/examples
mkdir -p dox-devel/API
cp -p examples/*.ml dox-devel/examples
%if %documentation
cp -p doc/* dox-devel/API
%endif

# Install the graph editing tools
mkdir -p %{buildroot}%{_bindir}
%if %opt
install -m 0755 -p editor/editor.opt %{buildroot}/%{_bindir}/ocaml-graph-editor
install -m 0755 -p dgraph/dgraph.opt %{buildroot}%{_bindir}/ocaml-graph-viewer
install -m 0755 -p view_graph/viewgraph.opt \
    %{buildroot}%{_bindir}/ocaml-viewgraph
%else
install -m 0755 -p editor/editor.byte %{buildroot}/%{_bindir}/ocaml-graph-editor
install -m 0755 -p dgraph/dgraph.byte %{buildroot}%{_bindir}/ocaml-graph-viewer
install -m 0755 -p view_graph/viewgraph.byte \
     %{buildroot}%{_bindir}/ocaml-viewgraph
%endif
magic_rpm_clean.sh

%files
%doc COPYING CREDITS FAQ LICENSE
%{ocaml_destdir}/%{libname}/
%if %opt
%exclude %{ocaml_destdir}/*/*.a
%exclude %{ocaml_destdir}/*/*.cmxa
%exclude %{ocaml_destdir}/*/*.cmx
%exclude %{ocaml_destdir}/*/*.o
%endif
%exclude %{ocaml_destdir}/*/*.mli


%files devel
%doc CHANGES README dox-devel/*
%if %opt
%{ocaml_destdir}/*/*.a
%{ocaml_destdir}/*/*.cmxa
%{ocaml_destdir}/*/*.cmx
%{ocaml_destdir}/*/*.o
%endif
%{ocaml_destdir}/*/*.mli


%files tools
%{_bindir}/*


%changelog
* Wed Nov 25 2015 Liu Di <liudidi@gmail.com> - 1.8.5-7
- 为 Magic 3.0 重建

* Wed Nov 11 2015 Liu Di <liudidi@gmail.com> - 1.8.5-6
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.8.5-5
- 为 Magic 3.0 重建

* Mon Mar 09 2015 Liu Di <liudidi@gmail.com> - 1.8.5-4
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 1.8.5-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 21 2014 Jerry James <loganjerry@gmail.com> - 1.8.5-1
- New upstream release

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 1.8.4-2
- Remove ocaml_arches macro (RHBZ#1087794).

* Wed Feb 26 2014 Jerry James <loganjerry@gmail.com> - 1.8.4-1
- New upstream release, 1.8.4+dev, where the "+dev" refers to a bug fix
  that was applied immediately after the 1.8.4 release
- Drop upstreamed patch
- Install graph.cmxs and enable the -debuginfo subpackage
- Update expected test results
- BR ocaml-findlib only, not ocaml-findlib-devel
- Install graph editing tools into -tools subpackage
- Fix the bytecode build

* Wed Oct 02 2013 Richard W.M. Jones <rjones@redhat.com> - 1.8.3-5
- Rebuild for ocaml-lablgtk 2.18.

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1.8.3-4
- Rebuild for OCaml 4.01.0.

* Tue Aug  6 2013 Jerry James <loganjerry@gmail.com> - 1.8.3-3
- Adapt to Rawhide unversioned docdir change (bz 994002)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 14 2013 Jerry James <loganjerry@gmail.com> - 1.8.3-1
- New upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Jerry James <loganjerry@gmail.com> - 1.8.2-2
- Rebuild for OCaml 4.00.1.

* Mon Jul 30 2012 Jerry James <loganjerry@gmail.com> - 1.8.2-1
- New upstream release

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-3
- Rebuild for OCaml 4.00.0.

* Sat Jan  7 2012 Jerry James <loganjerry@gmail.com> - 1.8.1-2
- Rebuild for OCaml 3.12.1

* Tue Oct 25 2011 Jerry James <loganjerry@gmail.com> - 1.8.1-1
- New upstream release

* Mon Jul 11 2011 Jerry James <loganjerry@gmail.com> - 1.7-1
- New upstream release
- Drop unnecessary spec file elements (BuildRoot, etc.)
- Drop dependency generation workaround for Fedora 12 and earlier
- Remove spurious executable bits on source files
- Replace the definition of __ocaml_requires_opts to "-i Sig", which removes
  the legitimate Requires: ocaml(GtkSignal), with __requires_exclude.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Richard W.M. Jones <rjones@redhat.com> - 1.6-2
- Ignore ocaml(Sig) symbol.

* Mon Jan 10 2011 Richard W.M. Jones <rjones@redhat.com> - 1.6-1
- New upstream version 1.6.
- Rebuild for OCaml 3.12.
- Remove obsolete patches and add patch to fix install-findlib rule.

* Wed Feb 10 2010 Alan Dunn <amdunn@gmail.com> - 1.3-3
- Include files (including .cmo files) and install more files that are
  needed by other applications (eg: Frama-C) that depend on
  ocaml-ocamlgraph
- define -> global
- Update for new dependency generator in F13

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.3-2
- Rebuild for OCaml 3.11.2.

* Thu Oct  8 2009 Richard W.M. Jones <rjones@redhat.com> - 1.3-1
- New upstream release 1.3.
- A slightly different viewGraph-related patch is required for this release.

* Fri Aug 07 2009 Alan Dunn <amdunn@gmail.com> - 1.1-1
- New upstream release 1.1.
- Makefile patch updated (still not incorporated upstream).

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0-5
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec  5 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0-3
- Rebuild for OCaml 3.11.0.
- Requires lablgtk2.
- Pull in gtk / libgnomecanvas too.

* Thu Nov 20 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0-1
- New upstream release 1.0.
- Patch0 removed - now upstream.
- Added a patch to fix documentation problem.
- Run tests with 'make --no-print-directory'.

* Wed Aug 13 2008 Alan Dunn <amdunn@gmail.com> 0.99c-2
- Incorporates changes suggested during review:
- License information was incorrect
- rpmlint error now properly justified

* Thu Aug 07 2008 Alan Dunn <amdunn@gmail.com> 0.99c-1
- Initial Fedora RPM release.

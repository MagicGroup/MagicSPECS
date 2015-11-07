%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-p3l
Version:        2.03
Release:        19%{?dist}
Summary:        OCaml compiler for parallel programs
Summary(zh_CN.UTF-8): 并行程序的 OCaml 编译器
License:        LGPLv2+ with exceptions

ExcludeArch:    sparc64 s390 s390x

URL:            http://ocamlp3l.inria.fr/
Source0:        http://ocamlp3l.inria.fr/ocamlp3l-2.03.tgz
Source1:        README.Fedora

# These patches come from Debian:
Patch0:         debian-01-correct-href-to-gz-doc.patch
Patch1:         debian-02-install-mli.patch

# Fix for new OCaml Marshal flags in OCaml 4.01.0.
Patch2:         ocamlp3l-2.03-fix-ocaml-marshal.patch

# Fix for warning about immutable strings, OCaml 4.02.
Patch3:         ocamlp3l-2.03-fix-warn-error.patch

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-ocamldoc


%description
OCamlP3l is a compiler for Caml parallel programs.

The OCamlP3l programming paradigm is skeleton programming. The
skeletons encapsulate basic parallel programming patterns in a well
understood and structured approach. Based on P3L, the Pisa Parallel
Programming Language, OCamlP3l skeleton algebra is embedded in a
full-fledged functional programming language, namely Objective Caml.

The skeleton programming approach used in OCamlP3l allows three
different operational interpretations of the same source program:

* the sequential interpretation which is deterministic, hence easy
  to understand and debug,
* the parallel interpretation using a network of computing nodes
  run in parallel to speed up the computation,
* the graphical interpretation, which is run to obtain a drawing
  of the parallel computing network deployed at run-time by the
  parallel interpretation. 

%description -l zh_CN.UTF-8
并行程序的 OCaml 编译器。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        doc
Summary:        User manual and other documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的文档
Requires:       %{name} = %{version}-%{release}


%description    doc
The %{name}-doc package contains the user manual and other
documentation for %{name}.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q -n ocamlp3l-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
# Parallel builds don't work:
unset MAKEFLAGS
make configure
make CAMLCBIN="ocamlopt.opt -g"


%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $RPM_BUILD_ROOT%{_bindir}

make install \
  CAMLLIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml \
  PREFIX=$RPM_BUILD_ROOT%{_prefix}

# Zero-length file - remove it.
rm doc/favicon.ico

cp %{SOURCE1} README.Fedora
magic_rpm_clean.sh

%files
%doc doc/LICENSE
%{_libdir}/ocaml/ocamlp3l
%if %opt
%exclude %{_libdir}/ocaml/ocamlp3l/vprocess/*.cmx
%exclude %{_libdir}/ocaml/ocamlp3l/vthread/*.cmx
%endif
%exclude %{_libdir}/ocaml/ocamlp3l/vprocess/*.mli
%exclude %{_libdir}/ocaml/ocamlp3l/vthread/*.mli
%{_bindir}/ocamlp3lc
%{_bindir}/ocamlp3lopt
%{_bindir}/ocamlp3ltop


%files devel
%doc README.Fedora
%if %opt
%{_libdir}/ocaml/ocamlp3l/vprocess/*.cmx
%{_libdir}/ocaml/ocamlp3l/vthread/*.cmx
%endif
%{_libdir}/ocaml/ocamlp3l/vprocess/*.mli
%{_libdir}/ocaml/ocamlp3l/vthread/*.mli


%files doc
%defattr(-,root,root,-)
%doc doc/*


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 2.03-19
- 为 Magic 3.0 重建

* Tue Mar 10 2015 Liu Di <liudidi@gmail.com> - 2.03-18
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 2.03-17
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 2.03-15
- OCaml 4.01.0 rebuild.
- Enable debuginfo.
- Modernize spec file.
- Patch for new OCaml Marshal flags in OCaml 4.01.0.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 Bruno Wolff III <bruno@wolff.to> 2.03-12
- Rebuild for ocaml 4.0.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 2.03-10
- Rebuild for OCaml 4.00.0.

* Sat Jan 07 2012 Richard W.M. Jones <rjones@redhat.com> - 2.03-9
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 07 2011 Richard W.M. Jones <rjones@redhat.com> - 2.03-7
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Tue Jan 12 2010 Richard W.M. Jones <rjones@redhat.com> - 2.03-6
- Fix URL & Source URL.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 2.03-5
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 2.03-3
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Mon Mar 16 2009 Richard W.M. Jones <rjones@redhat.com> - 2.03-2
- Don't duplicate the LICENSE and README.Fedora files.

* Sat Dec 20 2008 Richard W.M. Jones <rjones@redhat.com> - 2.03-1
- Initial RPM release.

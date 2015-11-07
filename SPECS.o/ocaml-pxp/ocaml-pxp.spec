%global debug_package %{nil}

Name:           ocaml-pxp
Version:	1.2.7
Release:	2%{?dist}
Summary:        Validating XML parser
Summary(zh_CN.UTF-8): 检验 XML 解析器
License:        BSD

URL:            http://projects.camlcity.org/projects/pxp.html
Source0:        http://download.camlcity.org/download/pxp-%{version}.tar.gz

ExcludeArch:    sparc64 s390 s390x
ExcludeArch:    ppc64

BuildRequires:  ocaml >= 3.10.2
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamlnet-devel
BuildRequires:  ocaml-ulex-devel
BuildRequires:  ocaml-pcre-devel, pcre-devel
BuildRequires:  ocaml-camlp4-devel

%global __ocaml_requires_opts -i Asttypes -i Outcometree -i Parsetree -i Pxp_rea


%description
PXP is a validating XML parser for O'Caml. It represents the parsed
document either as tree or as stream of events. In tree mode, it is
possible to validate the XML document against a DTD.

The acronym PXP means Polymorphic XML Parser. This name reflects the
ability to create XML trees with polymorphic type parameters.

%description -l zh_CN.UTF-8
检验 XML 解析器。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n pxp-%{version}
./configure \
  -without-wlex \
  -without-wlex-compat \
  -lexlist all


%build
# Parallel builds don't work:
unset MAKEFLAGS

make all
make opt


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
make install
magic_rpm_clean.sh

%files
%doc LICENSE
%{_libdir}/ocaml/pxp-engine/*.cma
%{_libdir}/ocaml/pxp-engine/*.cmi
%{_libdir}/ocaml/pxp-engine/*.cmo
%{_libdir}/ocaml/pxp-lex-*/*.cma
%{_libdir}/ocaml/pxp-lex-*/*.cmi
%{_libdir}/ocaml/pxp-lex-*/*.cmo
%{_libdir}/ocaml/pxp-ulex-utf8/*.cma
%{_libdir}/ocaml/pxp-ulex-utf8/*.cmi
%{_libdir}/ocaml/pxp-ulex-utf8/*.cmo
%{_libdir}/ocaml/pxp-pp/pxp_pp.cma


%files devel
%doc LICENSE
%{_libdir}/ocaml/pxp-engine/META
%{_libdir}/ocaml/pxp-engine/*.a
%{_libdir}/ocaml/pxp-engine/*.cmxa
%{_libdir}/ocaml/pxp-engine/*.mli
%{_libdir}/ocaml/pxp-lex-*/META
%{_libdir}/ocaml/pxp-lex-*/*.a
%{_libdir}/ocaml/pxp-lex-*/*.cmxa
%{_libdir}/ocaml/pxp-lex-*/*.cmx
%{_libdir}/ocaml/pxp-lex-*/*.o
%{_libdir}/ocaml/pxp-ulex-utf8/META
%{_libdir}/ocaml/pxp-ulex-utf8/*.a
%{_libdir}/ocaml/pxp-ulex-utf8/*.cmxa
%{_libdir}/ocaml/pxp-ulex-utf8/*.cmx
%{_libdir}/ocaml/pxp-ulex-utf8/*.o
%{_libdir}/ocaml/pxp-pp/META
%{_libdir}/ocaml/pxp/META


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.2.7-2
- 为 Magic 3.0 重建

* Wed Mar 11 2015 Liu Di <liudidi@gmail.com> - 1.2.7-1
- 更新到 1.2.7

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 1.2.4-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 1.2.4-1
- New upstream version 1.2.4.
- OCaml 4.01.0 rebuild.
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-5
- Rebuild for OCaml 4.00.1.

* Mon Jul 30 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-4
- Rebuild for OCaml 4.00.0 official.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul  3 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-2
- Ignore Pxp_rea symbol when generating requires.

* Mon Jul  2 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-1
- New upstream version 1.2.3.
- Includes fixes upstream for OCaml 4.00.0 so remove patch.

* Sat Jun  9 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2.2-3
- Rebuild for OCaml 4.00.0.
- Patch for new ocamldoc library.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2.2-2
- Rebuild for OCaml 3.12.1.

* Wed Sep 21 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.2-1
- New upstream version 1.2.2.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-4
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-3
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-1
- New upstream version 1.2.1.
- Rebuild for OCaml 3.11.1.

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0test2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0test2-5
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0test2-4
- Rebuild for OCaml 3.11.0

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0test2-3
- ExcludeArch ppc64 (bz #443899).

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0test2-2
- Rebuild for OCaml 3.10.2

* Mon Apr  2 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0test2-1
- New upstream version 1.2.0test2.
- New upstream URL.
- Re-enabled camlp4 extension.

* Sun Mar  2 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0test1-6
- Rebuild for ppc64.

* Fri Feb 15 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0test1-5
- Added BR ocaml-camlp4-devel

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0test1-4
- Added BR ocaml-pcre-devel, pcre-devel

* Thu Sep 13 2007 Richard W.M. Jones <rjones@redhat.com> - 1.2.0test1-3
- ExcludeArch ppc64

* Thu Sep 13 2007 Richard W.M. Jones <rjones@redhat.com> - 1.2.0test1-2
- Build on OCaml 3.10
- Disable building the preprocessor (requires old camlp4 or camlp5).
- License is BSD.
- Ignore Parsetree.

* Sat May 26 2007 Richard W.M. Jones <rjones@redhat.com> - 1.2.0test1-1
- Initial RPM release.

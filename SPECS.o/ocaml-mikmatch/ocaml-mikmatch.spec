%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%global debug_package %{nil}

Name:           ocaml-mikmatch
Version:	1.0.7
Release:	1%{?dist}
Summary:        OCaml extension for pattern matching with regexps
Summary(zh_CN.UTF-8): 使用正则表达式模式匹配的 OCaml 扩展
License:        BSD

URL:            http://mjambon.com/micmatch.html
Source0:        http://mjambon.com/releases/mikmatch/mikmatch-%{version}.tar.gz

# Upstream patches that fix the build with new ocaml-pcre.
Patch1:         0001-minor-fix-to-str-ocamlfind-requirements.patch
Patch2:         0002-fix-for-pcre-7.10.patch

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.12.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-camlp4-devel
BuildRequires:  ocaml-pcre-devel
BuildRequires:  pcre-devel

%global __ocaml_provides_opts -i Charset -i Constants -i Global_def -i Match -i Messages -i Mm_util -i Pa_mikmatch_pcre -i Pa_mikmatch_str -i Pcre_lib -i Regexp_ast -i Select_lib -i Str_lib -i Syntax_common -i Syntax_pcre -i Syntax_str


%description
Mikmatch (with a 'k') is the OCaml >= 3.10 version of Micmatch, an
extension for adding pattern matching with regular expressions to the
language.

The goal of Micmatch/Mikmatch is to make text-oriented programs even
easier to write, read and run without losing the unique and powerful
features of Objective Caml (OCaml).

Micmatch/Mikmatch provides a concise and highly readable syntax for
regular expressions, and integrates it into the syntax of OCaml thanks
to Camlp4.

%description -l zh_CN.UTF-8
使用正则表达式模式匹配的 OCaml 扩展。


%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name} = %{version}-%{release}
Requires:       ocaml-pcre-devel


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n mikmatch-%{version}
%patch1 -p1
%patch2 -p1

%build
# Parallel builds don't work:
unset MAKEFLAGS
make all str pcre OCAMLFLAGS=-g
%if %opt
make opt
%endif


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
make install-str install-pcre
magic_rpm_clean.sh

%files
%doc LICENSE
%{_libdir}/ocaml/mikmatch_str
%{_libdir}/ocaml/mikmatch_pcre
%if %opt
%exclude %{_libdir}/ocaml/mikmatch_str/*.a
%exclude %{_libdir}/ocaml/mikmatch_str/*.cmxa
%exclude %{_libdir}/ocaml/mikmatch_str/*.cmx
%exclude %{_libdir}/ocaml/mikmatch_pcre/*.a
%exclude %{_libdir}/ocaml/mikmatch_pcre/*.cmxa
%exclude %{_libdir}/ocaml/mikmatch_pcre/*.cmx
%endif
%exclude %{_libdir}/ocaml/mikmatch_str/*.mli
%exclude %{_libdir}/ocaml/mikmatch_pcre/*.mli


%files devel
%doc LICENSE README.md Changes VERSION
%if %opt
%{_libdir}/ocaml/mikmatch_str/*.a
%{_libdir}/ocaml/mikmatch_str/*.cmxa
%{_libdir}/ocaml/mikmatch_str/*.cmx
%{_libdir}/ocaml/mikmatch_pcre/*.a
%{_libdir}/ocaml/mikmatch_pcre/*.cmxa
%{_libdir}/ocaml/mikmatch_pcre/*.cmx
%endif
%{_libdir}/ocaml/mikmatch_str/*.mli
%{_libdir}/ocaml/mikmatch_pcre/*.mli


%changelog
* Mon Mar 09 2015 Liu Di <liudidi@gmail.com> - 1.0.7-1
- 更新到 1.0.7

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 1.0.6-7
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan  9 2014 Richard W.M. Jones <rjones@redhat.com> - 1.0.6-5
- Fix Source URL.

* Wed Sep 18 2013 Richard W.M. Jones <rjones@redhat.com> - 1.0.6-4
- OCaml 4.01.0 rebuild.
- Modernize the specfile.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov  6 2012 Michael Ekstrand <michael@elehack.net> - 1.0.6-1
- New upstream version 1.0.6

* Sun Nov  4 2012 Michael Ekstrand <michael@elehack.net> - 1.0.5-1
- New upstream version 1.0.5.
- Add BR on ocaml-pcre-devel to -devel package

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-2
- Rebuild for OCaml 4.00.0.

* Sun Jan  8 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-1
- New upstream version 1.0.4.
- Rebuild for OCaml 3.12.1.

* Tue Jun  7 2011 Michael Ekstrand <michael@elehack.net> - 1.0.3-4
- Bump for rebuild with proper changelog entry

* Tue Jun  7 2011 Michael Ekstrand <michael@elehack.net> - 1.0.3-3
- Patch META file to drop tophide dependency (#603249)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan  7 2011 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-1
- New upstream version 1.0.3 (support for OCaml 3.12).
- Rebuild for OCaml 3.12.0.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-2
- Rebuild for OCaml 3.11.2.

* Thu Oct  8 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-1
- New upstream version 1.0.2.
- Removed dynlink patch (now upstream).

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.0-6
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec  5 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.0-4
- Patch for dynlink.cma dependency for camlp4.
- Rebuild for OCaml 3.11.0.

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.0-3
- Rebuild for OCaml 3.11.0+rc1.

* Sun Aug 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.0-2
- +BR pcre-devel

* Mon Jul 28 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.0-1
- Initial RPM release.

%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-pcre
Version: 7.1.6
Release: 4%{?dist}
Summary:        Perl compatibility regular expressions (PCRE) for OCaml
Summary(zh_CN.UTF-8): OCaml 的 Perl 兼容正则表达式库

License:        LGPLv2
URL:            https://github.com/mmottl/pcre-ocaml
Source0:        https://github.com/mmottl/pcre-ocaml/releases/download/v%{version}/pcre-ocaml-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.12.1-3
BuildRequires:  ocaml-findlib-devel
BuildRequires:  pcre-devel
BuildRequires:  gawk
BuildRequires:  ocaml-ocamldoc


%description
Perl compatibility regular expressions (PCRE) for OCaml.

%description -l zh_CN.UTF-8
OCaml 的 Perl 兼容正则表达式库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name} = %{version}-%{release}
# This isn't quite right - we need to specify same architecture of pcre-devel
Requires:       pcre-devel


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n pcre-ocaml-%{version}
./configure \
  --prefix %{_prefix} \
  --docdir %{_docdir} \
  --destdir $RPM_BUILD_ROOT


%build
%if %opt
make all
%else
make -C lib byte-code-library
%endif


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
%if %opt
make NATIVE=true install
%else
make LIBINSTALL_FILES="pcre.mli pcre.cmi pcre.cma libpcre_stubs.a dllpcre_stubs.so" install
%endif

# Installs API docs in %{_docdir}/api.  Install this using %doc instead.
mv $RPM_BUILD_ROOT%{_docdir}/api .
magic_rpm_clean.sh

%files
%doc COPYING.txt
%{_libdir}/ocaml/pcre
%if %opt
%exclude %{_libdir}/ocaml/pcre/*.a
%exclude %{_libdir}/ocaml/pcre/*.cmxa
%endif
%exclude %{_libdir}/ocaml/pcre/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%doc COPYING.txt README.md api
%if %opt
%{_libdir}/ocaml/pcre/*.a
%{_libdir}/ocaml/pcre/*.cmxa
%endif
%{_libdir}/ocaml/pcre/*.mli


%changelog
* Wed Nov 25 2015 Liu Di <liudidi@gmail.com> - 7.1.6-4
- 为 Magic 3.0 重建

* Wed Nov 11 2015 Liu Di <liudidi@gmail.com> - 7.1.6-3
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 7.1.6-2
- 更新到 7.1.6

* Fri Mar 06 2015 Liu Di <liudidi@gmail.com> - 7.1.5-1
- 更新到 7.1.5

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 7.0.2-7
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 7.0.2-5
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 7.0.2-2
- New upstream version 7.0.2.
- Rebuild for OCaml 4.00.1.
- Fix homepage and source.
- Clean up the spec file.
- Add dependency on ocamldoc.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 6.2.5-3
- Rebuild for OCaml 4.00.0.

* Sat Apr 28 2012 Richard W.M. Jones <rjones@redhat.com> - 6.2.5-2
- Bump and rebuild against new OCaml compiler in ARM.

* Fri Jan  6 2012 Richard W.M. Jones <rjones@redhat.com> - 6.2.5-1
- New upstream version 6.2.5.
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 6.1.1-1
- New upstream version 6.1.1.
- Rebuild for OCaml 3.12.0.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 6.0.1-2
- Rebuild for OCaml 3.11.2.

* Sun Oct  4 2009 Richard W.M. Jones <rjones@redhat.com> - 6.0.1-1
- New upstream version 6.0.1.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.15.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 5.15.0-3
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 5.15.0-2
- Rebuild for OCaml 3.11.0

* Sun Aug 31 2008 Richard W.M. Jones <rjones@redhat.com> - 5.15.0-1
- New upstream release 5.15.0.

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 5.14.0-2
- Rebuild for OCaml 3.10.2

* Mon Apr 21 2008 Richard W.M. Jones <rjones@redhat.com> - 5.14.0-1
- New upstream release 5.14.0.
- -devel subpackage should depend on pcre-devel.
- Fixed upstream URL.
- Changed to use .bz2 package.

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 5.13.0-2
- Rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 5.13.0-1
- New upstream version 5.13.0.
- Rebuild for OCaml 3.10.1.

* Tue Sep 18 2007 Richard W.M. Jones <rjones@redhat.com> - 5.12.2-1
- New upstream version 5.12.2.
- Clarified license is LGPLv2.
- Strip .so file.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 5.11.4-9
- Force rebuild because of updated requires/provides scripts in OCaml.

* Mon Sep  3 2007 Richard W.M. Jones <rjones@redhat.com> - 5.11.4-8
- Force rebuild because of base OCaml.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 5.11.4-7
- Force rebuild because of changed BRs in base OCaml.

* Wed Aug  1 2007 Richard W.M. Jones <rjones@redhat.com> - 5.11.4-6
- ExcludeArch ppc64

* Mon Jun 11 2007 Richard W.M. Jones <rjones@redhat.com> - 5.11.4-5
- Updated to latest packaging guidelines.

* Sat Jun  2 2007 Richard W.M. Jones <rjones@redhat.com> - 5.11.4-4
- Handle bytecode-only architectures.

* Sat May 26 2007 Richard W.M. Jones <rjones@redhat.com> - 5.11.4-3
- Put the stubs in stublibs subdirectory.

* Fri May 25 2007 Richard W.M. Jones <rjones@redhat.com> - 5.11.4-2
- Use ocaml find-requires, find-provides

* Sat May 19 2007 Richard W.M. Jones <rjones@redhat.com> - 5.11.4-1
- Initial RPM release.

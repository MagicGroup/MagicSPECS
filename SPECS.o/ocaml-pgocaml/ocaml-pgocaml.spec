%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

# Note new upstream versions of this require 'batteries' (it is, or
# was, actually just an optional dependency).  Since this is not yet
# packaged for Fedora, we're sticking with 1.6.

Name:           ocaml-pgocaml
Version:        1.6
Release:        9%{?dist}
Summary:        OCaml library for type-safe access to PostgreSQL databases
Summary(zh_CN.UTF-8): 类型安全的访问 PostgreSQL 数据库的 OCaml 库
License:        LGPLv2+ with exceptions

URL:            http://pgocaml.forge.ocamlcore.org/
# Old tarball is not on the website any longer.  When we package batteries
# (see comment above) we can go back to a website link here.
Source0:        pgocaml-%{version}.tgz

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib-devel, ocaml-ocamldoc
BuildRequires:  ocaml-extlib-devel
BuildRequires:  ocaml-pcre-devel, pcre-devel
BuildRequires:  ocaml-calendar-devel >= 2.01.1-2
BuildRequires:  ocaml-csv-devel
BuildRequires:  ocaml-camlp4-devel

# The find-requires/provides scripts don't understand the packed
# CalendarLib module well.  Ignore the packed submodules.
%global __ocaml_requires_opts /usr/lib/rpm/ocaml-find-requires.sh -i Asttypes -i Calendar_builder -i Calendar_sig -i Date -i Date_sig -i Fcalendar -i Ftime -i Parsetree -i Period -i Printer -i Time -i Time_sig -i Time_Zone -i Utils -i Version
%global __ocaml_provides_opts /usr/lib/rpm/ocaml-find-provides.sh


%description
PG'OCaml is a type-safe, simple interface to PostgreSQL from OCaml. It
lets you embed SQL statements directly into OCaml code.

%description -l zh_CN.UTF-8
类型安全的访问 PostgreSQL 数据库的 OCaml 库。

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
%setup -q -n pgocaml-%{version}


%build
make depend
make all OCAMLOPTFLAGS=-g
make doc


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
ocamlfind install pgocaml META *.mli *.cmi *.cmx *.cma *.cmxa *.a pa_*.cmo

mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 0755 pgocaml_prof $RPM_BUILD_ROOT%{_bindir}
magic_rpm_clean.sh

%files
%doc COPYING.LIB
%{_libdir}/ocaml/pgocaml
%if %opt
%exclude %{_libdir}/ocaml/pgocaml/*.a
%exclude %{_libdir}/ocaml/pgocaml/*.cmxa
%exclude %{_libdir}/ocaml/pgocaml/*.cmx
%endif
%exclude %{_libdir}/ocaml/pgocaml/*.mli
%{_bindir}/pgocaml_prof


%files devel
%doc README.txt README.profiling BUGS.txt CONTRIBUTORS.txt COPYING.LIB HOW_IT_WORKS.txt html/*
%if %opt
%{_libdir}/ocaml/pgocaml/*.a
%{_libdir}/ocaml/pgocaml/*.cmxa
%{_libdir}/ocaml/pgocaml/*.cmx
%endif
%{_libdir}/ocaml/pgocaml/*.mli


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.6-9
- 为 Magic 3.0 重建

* Wed Mar 11 2015 Liu Di <liudidi@gmail.com> - 1.6-8
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 1.6-7
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 1.6-5
- OCaml 4.01.0 rebuild.
- Enable debuginfo.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 Bruno Wolff III <bruno@wolff.to> - 1.6-2
- Rebuild for ocaml 4.0.1.

* Tue Oct 30 2012 Richard W.M. Jones <rjones@redhat.com> - 1.6-1
- New upstream version 1.6.
- Remove patch for OCaml 4, now upstream.
- Clean up spec file.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1.5-1
- New upstream version 1.5.
- Upstream site moved to ocamlforge.
- Patch camlp4 code to use _loc instead of loc.

* Mon Jun 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1.4-4
- Rebuild for OCaml 4.00.0.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 1.4-3
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 1.4-1
- New upstream version 1.4.
- Rebuild for OCaml 3.12.0.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.3-2
- Rebuild for OCaml 3.11.2.

* Thu Oct  8 2009 Richard W.M. Jones <rjones@redhat.com> - 1.3-1
- New upstream version 1.3.
- Simplify build system.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.1-9
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec  5 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1-7
- Rebuild for OCaml 3.11.0.

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1-6
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1-5
- Rebuild for OCaml 3.11.0

* Thu Jul 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1-4
- Rebuild against ocaml-calendar 2.0.4

* Tue Jul  1 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1-3
- Ignore Parsetree dep.
- Bump release to -3 to solve EVR problems with F-9.

* Tue Mar  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1-1
- New upstream release 1.1.
- Clarify license is LGPLv2+ with exceptions.
- New home page and download URL.

* Mon Mar  3 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9-5
- Ignore modules which are really submodules of CalendarLib.

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9-4
- Add missing BR for ocaml-camlp4-devel.
- Add missing BR for pcre-devel.
- Check it builds in mock.

* Sat Feb 23 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9-3
- Check it builds with OCaml 3.10.1
- Only keep license file in main package.
- Clarify license is LGPLv2 with exceptions.

* Mon Sep  3 2007 Richard W.M. Jones <rjones@redhat.com> - 0.9-2
- Added the syntax extension.

* Mon Sep  3 2007 Richard W.M. Jones <rjones@redhat.com> - 0.9-1
- Initial RPM release.

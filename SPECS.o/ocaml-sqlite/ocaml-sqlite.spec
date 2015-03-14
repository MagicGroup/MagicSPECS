%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%if !%{opt}
%global debug_package %{nil}
%endif

Name:           ocaml-sqlite
Version:	2.0.9
Release:	1%{?dist}
Summary:        OCaml library for accessing SQLite3 databases
Summary(zh_CN.UTF-8): 访问 SQLite3 数据库的 OCaml 库
License:        BSD

URL:            https://github.com/mmottl/sqlite3-ocaml
Source0:        https://github.com/mmottl/sqlite3-ocaml/releases/download/v%{version}/sqlite3-ocaml-%{version}.tar.gz
BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-camlp4-devel
BuildRequires:  sqlite-devel >= 3


%description
SQLite 3 database library wrapper for OCaml.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       sqlite-devel%{?_isa} >= 3


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n sqlite3-ocaml-%{version}


%build
./configure --prefix=%{_prefix} --libdir=%{_libdir} --docdir=%{_pkgdocdir} \
  --destdir $RPM_BUILD_ROOT
make all


%check
./configure --prefix=%{_prefix} --libdir=%{_libdir} --docdir=%{_pkgdocdir} \
  --destdir $RPM_BUILD_ROOT --enable-tests
make test


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
make install


%files
%doc COPYING.txt
%{_libdir}/ocaml/sqlite3
%if %opt
%exclude %{_libdir}/ocaml/sqlite3/*.a
%exclude %{_libdir}/ocaml/sqlite3/*.cmxa
%exclude %{_libdir}/ocaml/sqlite3/*.cmx
%endif
%exclude %{_libdir}/ocaml/sqlite3/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%doc CHANGES.txt README.md TODO.md 
%if %opt
%{_libdir}/ocaml/sqlite3/*.a
%{_libdir}/ocaml/sqlite3/*.cmxa
%{_libdir}/ocaml/sqlite3/*.cmx
%endif
%{_libdir}/ocaml/sqlite3/*.mli
%{_docdir}/*

%changelog
* Sat Mar 14 2015 Liu Di <liudidi@gmail.com> - 2.0.9-1
- 更新到 2.0.9

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 2.0.5-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 21 2014 Jerry James <loganjerry@gmail.com> - 2.0.5-1
- New upstream version 2.0.5
- Enable debuginfo for non-bytecode builds only
- BR ocaml-findlib instead of ocaml-findlib-devel
- Drop chrpath BR, no longer needed

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 2.0.4-3
- Remove ocaml_arches macro (RHBZ#1087794).

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 2.0.4-2
- Remove 'Group' line.

* Tue Sep 17 2013 Jerry James <loganjerry@gmail.com> - 2.0.4-1
- New upstream release
- Build for OCaml 4.01.0
- Enable debuginfo
- Modernize spec file
- Drop all patches, none are needed

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 Bruno Wolff III <bruno@wolff.to> - 1.6.3-3
- Rebuild for ocaml 4.0.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul  3 2012 Richard W.M. Jones <rjones@redhat.com> - 1.6.3-1
- New upstream version 1.6.3.
- Change download URLs.

* Mon Jun 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1.6.1-2
- Rebuild for OCaml 4.00.0.

* Fri Jan  6 2012 Richard W.M. Jones <rjones@redhat.com> - 1.6.1-1
- New upstream version 1.6.1.
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 1.5.9-1
- New upstream version 1.5.9.
- Rebuild for OCaml 3.12.0.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.5.6-3
- Rebuild for OCaml 3.11.2.

* Sun Oct  4 2009 Richard W.M. Jones <rjones@redhat.com> - 1.5.6-2
- New upstream version 1.5.6.
- Upstream tests should be fixed now, so reenable all of them.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.5.0-1
- Rebuild for OCaml 3.11.1
- New upstream version 1.5.0.
- Fix tests.
- Fix documentation.

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-4
- Rebuild for OCaml 3.11.0.

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-3
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-2
- Rebuild for OCaml 3.11.0

* Sun Aug 31 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-1
- New upstream version 1.2.0.

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-2
- Rebuild for OCaml 3.10.2

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-1
- Jump in upstream version to 1.0.3.
- New upstream URL.

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 0.23.0-3
- Build for ppc64.

* Fri Feb 29 2008 Richard W.M. Jones <rjones@redhat.com> - 0.23.0-2
- Added BR ocaml-camlp4-devel.

* Sun Feb 24 2008 Richard W.M. Jones <rjones@redhat.com> - 0.23.0-1
- Initial RPM release.

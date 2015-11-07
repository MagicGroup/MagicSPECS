%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-postgresql
Version:	3.2.1
Release:	2%{?dist}
Summary:        OCaml library for accessing PostgreSQL databases
Summary(zh_CN.UTF-8): 访问 PostgreSQL 数据库的 OCaml 库

License:        LGPLv2+ with exceptions
URL:            https://github.com/mmottl/postgresql-ocaml
Source0:        https://github.com/mmottl/postgresql-ocaml/releases/download/v%{version}/postgresql-ocaml-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  postgresql-devel
BuildRequires:  chrpath
BuildRequires:  rpm >= 4.4.2.3-2

%global __ocaml_provides_opts -i Condition -i Event -i Mutex -i Thread -i ThreadUnix


%description
This OCaml-library provides an interface to PostgreSQL, an efficient
and reliable, open source, relational database.  Almost all
functionality available through the C-API (libpq) is replicated in a
type-safe way.  This library uses objects for representing database
connections and results of queries.

%description -l zh_CN.UTF-8
访问 PostgreSQL 数据库的 OCaml 库。

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
%setup -q -n postgresql-ocaml-%{version}
ocaml setup.ml -configure --prefix %{_prefix} --destdir $RPM_BUILD_ROOT


%build
make

chrpath --delete _build/lib/dll*.so


%install
# These rules work if the library uses 'ocamlfind install' to install itself.
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
make install
magic_rpm_clean.sh

%files
%doc COPYING.txt
%{_libdir}/ocaml/postgresql
%if %opt
%exclude %{_libdir}/ocaml/postgresql/*.a
%exclude %{_libdir}/ocaml/postgresql/*.cmxa
%endif
%exclude %{_libdir}/ocaml/postgresql/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%doc COPYING.txt AUTHORS.txt CHANGES.txt README.md examples
%if %opt
%{_libdir}/ocaml/postgresql/*.a
%{_libdir}/ocaml/postgresql/*.cmxa
%endif
%{_libdir}/ocaml/postgresql/*.mli


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 3.2.1-2
- 更新到 3.2.1

* Wed Mar 11 2015 Liu Di <liudidi@gmail.com> - 3.0.0-1
- 更新到 3.0.0

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 2.0.4-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 2.0.4-1
- New upstream version 2.0.4.
- OCaml 4.01.0 rebuild.
- Enable debuginfo.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Richard W.M. Jones <rjones@redhat.com> - 2.0.2-1
- New upstream version 2.0.2.
- Fix home page and source URL.
- Clean up spec file.
- Fix build.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1.18.0-2
- Rebuild for OCaml 4.00.0.

* Thu Jan 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1.18.0-1
- New upstream version 1.18.0.
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 1.14.0-1
- New upstream version 1.14.0.

* Mon Jan 11 2010 Richard W.M. Jones <rjones@redhat.com> - 1.12.3-3
- Ignore bogus thread module Provides which the automatic dependency
  generator was giving us.
- Replace %%define with %%global.
- Use upstream RPM 4.8 OCaml internal dependency generator.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.12.3-2
- Rebuild for OCaml 3.11.2.

* Fri Oct 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.12.3-1
- New upstream version 1.12.3.
- This contains a SECURITY fix for:
  https://bugzilla.redhat.com/show_bug.cgi?id=529325
  CVE-2009-2943 ocaml-postgresql: Missing escape function (DSA-1909-1)
  HOWEVER you are not protected until you change your code to
  use the new connection#escape_string method.

* Sun Oct  4 2009 Richard W.M. Jones <rjones@redhat.com> - 1.12.1-1
- New upstream version 1.12.1.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.11.1-2
- Rebuild for OCaml 3.11.1
- New upstream version 1.11.1.

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Tue Mar 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.10.3-1
- New upstream version 1.10.3.
- Fix URL.
- Upstream Source URLs have all changed.

* Mon Mar  9 2009 Richard W.M. Jones <rjones@redhat.com> - 1.9.2-6
- Fix typo in summary (rhbz#487632).

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.9.2-3
- Rebuild for OCaml 3.11.0+rc1.

* Mon Nov 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.9.2-2
- Rebuild.

* Thu Nov 20 2008 Richard W.M. Jones <rjones@redhat.com> - 1.9.2-1
- New upstream release 1.9.2.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.8.2-5
- Rebuild for OCaml 3.11.0

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.8.2-4
- Rebuild for OCaml 3.10.2

* Fri Apr 18 2008 Richard W.M. Jones <rjones@redhat.com> - 1.8.2-3
- Can't spell.  prm -> rpm.

* Fri Apr 18 2008 Richard W.M. Jones <rjones@redhat.com> - 1.8.2-2
- Rebuild against updated RPM (see bug 443114).

* Fri Apr  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.8.2-1
- New upstream version 1.8.2.

* Tue Mar  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.7.0-3
- Rebuild for ppc64.

* Mon Mar  3 2008 Richard W.M. Jones <rjones@redhat.com> - 1.7.0-2
- Only include LICENSE doc in main package.
- Include extra documentation and examples in devel package.
- Check it builds in mock.

* Sun Feb 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.7.0-1
- Initial RPM release.

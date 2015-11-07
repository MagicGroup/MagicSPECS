%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-mysql
Version:	1.2.0
Release:	2%{?dist}
Summary:        OCaml library for accessing MySQL databases
Summary(zh_CN.UTF-8): 访问 MySQL 数据库的 OCaml 库
License:        LGPLv2+ with exceptions

URL:            http://forge.ocamlcore.org/projects/ocaml-mysql/
Source0:        https://forge.ocamlcore.org/frs/download.php/1472/ocaml-mysql-%{version}.tar.gz

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-camlp4-devel
BuildRequires:  mysql-devel
BuildRequires:  chrpath

# See: https://bugzilla.redhat.com/show_bug.cgi?id=916822
Patch1:         ocaml-mysql-1.1.3-int64.patch


%description
ocaml-mysql is a package for ocaml that provides access to mysql
databases. It consists of low level functions implemented in C and a
module Mysql intended for application development.

%description -l zh_CN.UTF-8
访问 MySQL 数据库的 OCaml 库。

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
%setup -q
%patch1 -p1


%build
LDFLAGS="-L%{_libdir}/mysql" \
%configure
make
%if %opt
make opt
%endif

chrpath --delete dll*.so


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
make install
magic_rpm_clean.sh

%files
%doc COPYING
%{_libdir}/ocaml/mysql
%if %opt
%exclude %{_libdir}/ocaml/mysql/*.a
%exclude %{_libdir}/ocaml/mysql/*.cmxa
%exclude %{_libdir}/ocaml/mysql/*.cmx
%endif
%exclude %{_libdir}/ocaml/mysql/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%doc COPYING CHANGES README VERSION
%if %opt
%{_libdir}/ocaml/mysql/*.a
%{_libdir}/ocaml/mysql/*.cmxa
%{_libdir}/ocaml/mysql/*.cmx
%endif
%{_libdir}/ocaml/mysql/*.mli


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.2.0-2
- 更新到 1.2.0

* Mon Mar 09 2015 Liu Di <liudidi@gmail.com> - 1.1.3-1
- 更新到 1.1.3

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 1.1.1-8
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 1.1.1-6
- OCaml 4.01.0 rebuild.
- Enable debuginfo.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1.1.1-4
- Remove direct dependency of mysql-libs, since RPM picks up the
  correct dependency implicitly (RHBZ#962742).

* Fri Mar  1 2013 Richard W.M. Jones <rjones@redhat.com> - 1.1.1-3
- Ensure we link to mysql client shared library (RHBZ#916822, thanks Sato Ichi).
- Move configure into build section, and replace with RPM macro.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.1-1
- New upstream version 1.1.1.
- Clean up the spec file.
- Rebuild for OCaml 4.00.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-2
- Rebuild for OCaml 4.00.0.

* Wed Jan 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-1
- New upstream version 1.1.0.
- It is now hosted on OCaml Forge.
- Rebuild for OCaml 3.12.1.
- Remove patch, now upstream.
- HTML docs are not built, so don't include them in the package.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-13
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-12
- Rebuild for OCaml 3.11.2.

* Fri Oct 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-11
- Patch for CVE 2009-2942 Missing escape function (RHBZ#529321).

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-9
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-7
- Force another rebuild to try to get updated MySQL client deps.

* Sat Jan 17 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-6
- Requires mysql-libs, not automatically found.

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-5
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-4
- Rebuild for OCaml 3.11.0

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-3
- Rebuild for OCaml 3.10.2

* Mon Mar  3 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-2
- Don't need 'ExcludeArch: ppc64' any more.
- Add missing BR for ocaml-camlp4-devel.
- Test build in mock.

* Sun Feb 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-1
- Initial RPM release.

%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-lacaml
Version: 7.2.6
Release: 2%{?dist}
Summary:        BLAS/LAPACK-interface for OCaml
Summary(zh_CN.UTF-8): OCaml 的 BLAS/LAPACK 接口

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        LGPLv2 with exceptions
URL:            https://github.com/mmottl/lacaml
Source0:        https://github.com/mmottl/lacaml/releases/download/v%{version}/lacaml-%{version}.tar.gz

BuildRequires:  ocaml
BuildRequires:  ocaml-camlp4-devel
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-compiler-libs
BuildRequires:  lapack-devel
BuildRequires:  blas-devel

%global __ocaml_requires_opts -i Asttypes -i Parsetree -i Common -i Utils
%global __ocaml_provides_opts -i Common -i Install_printers -i Io -i Utils


%description
This OCaml-library interfaces the BLAS-library (Basic Linear Algebra
Subroutines) and LAPACK-library (Linear Algebra routines), which are
written in FORTRAN.

This allows people to write high-performance numerical code for
applications that need linear algebra.

%description -l zh_CN.UTF-8
OCaml 的 BLAS/LAPACK 接口。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n lacaml-%{version}
./configure --prefix %{_prefix} --destdir $RPM_BUILD_ROOT


%build
make
make examples


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
make install

# By installing the *.cmx files, the compiler can do cross-module inlining.
install -m 0644 _build/lib/*.cmx $RPM_BUILD_ROOT%{_libdir}/ocaml/lacaml
magic_rpm_clean.sh

%files
%doc COPYING.txt
%{_libdir}/ocaml/lacaml
%if %opt
%exclude %{_libdir}/ocaml/lacaml/*.a
%exclude %{_libdir}/ocaml/lacaml/*.cmxa
%exclude %{_libdir}/ocaml/lacaml/*.cmx
%endif
%exclude %{_libdir}/ocaml/lacaml/*.mli
%exclude %{_libdir}/ocaml/lacaml/*.ml
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%doc COPYING.txt AUTHORS.txt CHANGES.txt README.md TODO.md
%if %opt
%{_libdir}/ocaml/lacaml/*.a
%{_libdir}/ocaml/lacaml/*.cmxa
%{_libdir}/ocaml/lacaml/*.cmx
%endif
%{_libdir}/ocaml/lacaml/*.mli
%{_libdir}/ocaml/lacaml/*.ml


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 7.2.6-2
- 更新到 7.2.6

* Fri Mar 06 2015 Liu Di <liudidi@gmail.com> - 7.1.5-1
- 更新到 7.1.5

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 7.0.9-5
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 7.0.9-3
- Remove ocaml_arches macro (RHBZ#1087794).

* Sat Sep 21 2013 Richard W.M. Jones <rjones@redhat.com> - 7.0.9-2
- Ignore Common and Utils when calculating requires.

* Wed Sep 18 2013 Jerry James <loganjerry@gmail.com> - 7.0.9-1
- New upstream version 7.0.9
- Rebuild for OCaml 4.01.0
- Enable debuginfo
- Minor spec file cleanups

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 7.0.3-1
- New upstream version 7.0.3.
- Clean up the spec file.
- Rebuild for OCaml 4.00.1.
- +BR ocamldoc.

* Mon Jul 30 2012 Richard W.M. Jones <rjones@redhat.com> - 5.5.2-4
- Rebuild for OCaml 4.00.0 official.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 5.5.2-2
- Rebuild for OCaml 4.00.0.
- Patch Makefile to disable warn-error and to include +compiler-libs.

* Wed Jan 11 2012 Richard W.M. Jones <rjones@redhat.com> - 5.5.2-1
- New upstream version 5.5.2.
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 5.4.8-1
- New upstream version 5.4.8.
- Rebuild for OCaml 3.12.0.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 5.4.7-2
- Rebuild for OCaml 3.11.2.

* Sun Oct  4 2009 Richard W.M. Jones <rjones@redhat.com> - 5.4.7-1
- New upstream release 5.4.7.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 5.1.0-1
- Rebuild for OCaml 3.11.1.
- New upstream release 5.1.0.

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Tue Mar 10 2009 Richard W.M. Jones <rjones@redhat.com> - 4.7.6-1
- New upstream version 4.7.6.
- Name of documentation files has changed slightly.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 4.6.8-2
- Rebuild.

* Thu Nov 20 2008 Richard W.M. Jones <rjones@redhat.com> - 4.6.8-1
- New upstream version 4.6.8.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.3-2
- Rebuild for OCaml 3.11.0

* Sun Aug 31 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.3-1
- New upstream version 4.3.3.

* Fri May  2 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-1
- New upstream version 4.3.2.

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.1-2
- Rebuild for OCaml 3.10.2

* Mon Apr 21 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.1-1
- New upstream release 4.3.1.
- Fix upstream URL.

* Tue Mar  4 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.0-2
- Rebuild for ppc64.

* Wed Feb 20 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.0-1
- Initial RPM release.

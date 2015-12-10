%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%global debug_package %{nil}

Name:           ocaml-reins
Version:        0.1a
Release:        23%{?dist}
Summary:        Library of OCaml persistent data structures
Summary(zh_CN.UTF-8): 持续性数据结构的 OCaml 库
License:        LGPLv2 with exceptions

URL:            http://ocaml-reins.sourceforge.net/
Source0:        http://garr.dl.sourceforge.net/sourceforge/ocaml-reins/ocaml-reins-%{version}.tar.gz

ExcludeArch:    sparc64 s390 s390x

Patch0:         reins-destdir-debian.patch
Patch1:         reins-install-cmi-debian.patch
Patch2:         reins-ocamldep-fix.patch

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-omake
BuildRequires:  ocaml-ounit-devel


%description
Reins is a collection of persistent data structures for OCaml.

In addition to providing a large collection of data structures, the
O'Caml Reins project also includes several features that I hope will
make developing O'Caml applications easier such as a random testing
framework and a collection of "standard" modules.

Current features:

* List data types:
   o Single linked lists (compatible with the standard library type)
   o O(1) catenable lists
   o Acyclic double linked lists
   o Random access lists with O(1) hd/cons/tl and O(log i) lookup/update
     for i'th element
* Double ended queues
* Sets/Maps:
   o AVL
   o Red/Black
   o Big-endian Patricia
   o Splay
* Heaps:
   o Binomial
   o Skew Binomial
* Zipper style cursor interfaces
* Persistent, bi-directional cursor based iterators (currently only
  for lists and sets)
* All standard types hoisted into the module level (Int, Bool, etc...)
* A collection of functor combinators to minimize boilerplate (e.g.,
  constructing compare or to_string functions)
* Quickcheck testing framework
   o Each structure provides a gen function that can generate a random
     instance of itself
* Completely safe code. No -unsafe or references to Obj.*
* Consistent function signatures. For instance, all fold functions take
  the accumulator in the same position.
* All operations use no more than O(log n) stack space (except for a
  few operations on splay trees which currently have O(log n) expected
  time, but O(n) worst case)

%description -l zh_CN.UTF-8
持续性数据结构的 OCaml 库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1


%build
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
omake --config
omake doc


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
omake install
magic_rpm_clean.sh

%files
%doc COPYING LGPL-2.1
%{_libdir}/ocaml/reins
%if %opt
%exclude %{_libdir}/ocaml/reins/*.a
%exclude %{_libdir}/ocaml/reins/*.cmxa
%exclude %{_libdir}/ocaml/reins/*.cmx
%endif
%exclude %{_libdir}/ocaml/reins/*.mli


%files devel
%doc AUTHORS COPYING LGPL-2.1 doc/html
%if %opt
%{_libdir}/ocaml/reins/*.a
%{_libdir}/ocaml/reins/*.cmxa
%{_libdir}/ocaml/reins/*.cmx
%endif
%{_libdir}/ocaml/reins/*.mli


%changelog
* Wed Nov 25 2015 Liu Di <liudidi@gmail.com> - 0.1a-23
- 为 Magic 3.0 重建

* Wed Nov 11 2015 Liu Di <liudidi@gmail.com> - 0.1a-22
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0.1a-21
- 为 Magic 3.0 重建

* Fri Mar 13 2015 Liu Di <liudidi@gmail.com> - 0.1a-20
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 0.1a-19
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1a-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 0.1a-17
- OCaml 4.01.0 rebuild.
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1a-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1a-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 Bruno Wolff III <bruno@wolff.to> - 0.1a-14
- Rebuild for ocaml 4.0.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1a-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  2 2012 Richard W.M. Jones <rjones@redhat.com> - 0.1a-12
- Rebuild for OCaml 4.00.0.

* Thu Jan 12 2012 Richard W.M. Jones <rjones@redhat.com> - 0.1a-11
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1a-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Richard W.M. Jones <rjones@redhat.com> - 0.1a-9
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).
- Add patch for missing OCAMLDEP_MODULES in config.omake.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.1a-7
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1a-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.1a-5
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1a-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1a-3
- Rebuild for OCaml 3.11.0+rc1.

* Wed Sep  3 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1a-2
- Use normal versioning scheme.

* Sat Aug 30 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1-0.1.a
- Initial RPM release.

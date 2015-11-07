%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

%define ocamllibdir %{_libdir}/ocaml

Name:           ocaml-ancient
Version:        0.9.0
Release:        17%{?dist}
Summary:        OCaml library for large memory structures and sharing
Summary(zh_CN.UTF-8): 大内存结构和共享的 Ocaml 库
License:        LGPLv2+ with exceptions

# Upstream website is dead, but the code is maintained at
# http://git.annexia.org/?p=ocaml-ancient.git;a=summary.  The current
# tarball is based on the last one released upstream.
URL:            http://git.annexia.org/?p=ocaml-ancient.git;a=summary
Source0:        ancient-%{version}.tar.gz

Patch1:         ancient-0.9.0-use-ocamlopt-g.patch

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  chrpath
ExcludeArch:    sparc64 s390 s390x


%description
Ancient is an OCaml module that allows you to use in-memory data
structures which are larger than available memory and so are kept in
swap. If you try this in normal OCaml code, you'll find that the
machine quickly descends into thrashing as the garbage collector
repeatedly iterates over swapped memory structures. This module lets
you break that limitation. Of course the module doesn't work by magic.
If your program tries to access these large structures, they still
need to be swapped back in, but it is suitable for large, sparsely
accessed structures.

Secondly, this module allows you to share those structures between
processes. In this mode, the structures are backed by a disk file, and
any process that has read/write access to that disk file can map that
file in and see the structures.

Developers should read the README.txt file included with the
ocaml-ancient-devel package carefully.

%description -l zh_CN.UTF-8
大内存结构和共享的 Ocaml 库。

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
%setup -q -n ancient-%{version}

%patch1 -p1


%build
pushd mmalloc
%configure
make
popd

make CFLAGS='-g -fPIC -Wall -Werror -I%{ocamllibdir} -DOCAML_VERSION_MAJOR=$(OCAML_VERSION_MAJOR) -DOCAML_VERSION_MINOR=$(OCAML_VERSION_MINOR) %{optflags}'

make doc ||:


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
ocamlfind install ancient ancient.cmi *.mli *.cma ancient.cmx *.cmxa *.a *.so \
  mmalloc/*.a META

chrpath --delete $OCAMLFIND_DESTDIR/stublibs/dll*.so
magic_rpm_clean.sh

%files
%doc mmalloc/COPYING.LIB
%{_libdir}/ocaml/ancient
%if %opt
%exclude %{_libdir}/ocaml/ancient/*.a
%exclude %{_libdir}/ocaml/ancient/*.cmxa
%exclude %{_libdir}/ocaml/ancient/*.cmx
%endif
%exclude %{_libdir}/ocaml/ancient/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%doc README.txt html/*
%if %opt
%{_libdir}/ocaml/ancient/*.a
%{_libdir}/ocaml/ancient/*.cmxa
%{_libdir}/ocaml/ancient/*.cmx
%endif
%{_libdir}/ocaml/ancient/*.mli


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0.9.0-17
- 为 Magic 3.0 重建

* Tue Mar 03 2015 Liu Di <liudidi@gmail.com> - 0.9.0-16
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 0.9.0-15
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 0.9.0-13
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.
- Fix URL and Source.
- Modernize spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.0-10
- Rebuild for OCaml 4.00.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.0-8
- Rebuild for OCaml 4.00.0.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.0-7
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Richard W.M. Jones <rjones@redhat.com> - 0.9.0-5
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9.0-4
- Rebuild for OCaml 3.11.2.

* Tue Sep 22 2009 Dennis Gilmore <dennis@ausil.us> - 0.9.0-3
- ExcludeArch sparc64 s390 s390x  no ocaml

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 26 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9.0-1
- Initial RPM release.

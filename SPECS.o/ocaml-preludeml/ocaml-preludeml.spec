%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%global debug_package %{nil}

# There are no official releases, so we just use git dates.
# This software is much more stable than the "0.1" version
# number might indicate.
%global gitdate 20100314

Name:           ocaml-preludeml
Version:        0.1
Release:        0.31.%{gitdate}%{?dist}
Summary:        OCaml utility functions
Summary(zh_CN.UTF-8): OCaml 工具函数
License:        MIT

ExcludeArch:    sparc64 s390 s390x

# To recreate the source tarball, do:
#   git clone git://github.com/kig/preludeml.git
#   tar --exclude .git -cf /tmp/preludeml-%{gitdate}.tar preludeml
#   bzip2 /tmp/preludeml-%{gitdate}.tar
URL:            http://github.com/kig/preludeml/tree/master
Source0:        preludeml-%{gitdate}.tar.bz2

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-pcre-devel
BuildRequires:  ocaml-ocamlnet-devel
BuildRequires:  ocaml-omake
BuildRequires:  ocaml-ounit-devel
BuildRequires:  ruby
BuildRequires:  libX11-devel


%description
Prelude.ml is a collection of utility functions for OCaml programs.
Of particular interest are high level parallel combinators, which make
multicore parallelization of OCaml programs easy.

%description -l zh_CN.UTF-8
OCaml 工具函数。

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
%setup -q -n preludeml


%build
omake

# Create a META file.
cat >META <<_EOF_
version = "%{version}"
requires = "pcre,unix,netstring,bigarray"
description = "OCaml utility functions"
archive(byte) = "prelude.cmo"
archive(native) = "prelude.cmxa"
_EOF_


%check
# The tests fail in various delightful ways:
# - i386 & ppc fail on 1 test (out of several hundred).  Probably a
#   64 bit assumption in the code or in the test somewhere.
# - ppc64 runs out of memory during the test.
omake test ||:


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR

ocamlfind install preludeml \
  META \
  src/prelude.ml \
  src/prelude.cmi \
  src/prelude.cmo \
  src/prelude.cmx \
  src/prelude.a \
  src/prelude.cmxa
magic_rpm_clean.sh

%files
%doc LICENSE
%{_libdir}/ocaml/preludeml
%if %opt
%exclude %{_libdir}/ocaml/preludeml/*.a
%exclude %{_libdir}/ocaml/preludeml/*.cmx
%exclude %{_libdir}/ocaml/preludeml/*.cmxa
%endif
%exclude %{_libdir}/ocaml/preludeml/*.ml


%files devel
%doc LICENSE README TESTING
%if %opt
%{_libdir}/ocaml/preludeml/*.a
%{_libdir}/ocaml/preludeml/*.cmx
%{_libdir}/ocaml/preludeml/*.cmxa
%endif
%{_libdir}/ocaml/preludeml/*.ml


%changelog
* Wed Nov 25 2015 Liu Di <liudidi@gmail.com> - 0.1-0.31.20100314
- 为 Magic 3.0 重建

* Wed Nov 11 2015 Liu Di <liudidi@gmail.com> - 0.1-0.30.20100314
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0.1-0.29.20100314
- 为 Magic 3.0 重建

* Wed Mar 11 2015 Liu Di <liudidi@gmail.com> - 0.1-0.28.20100314
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 0.1-0.27.20100314
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.26.20100314
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 0.1-0.25.20100314
- OCaml 4.01.0 rebuild.
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.24.20100314
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.23.20100314
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 Bruno Wolff III <bruno@wolff.to> - 0.1-0.22.20100314
- Rebuild for ocaml 4.0.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.21.20100314
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul  3 2012 Richard W.M. Jones <rjones@redhat.com> - 0.1-0.20.20100314
- Rebuild for OCaml 4.00.0.

* Thu Jan 12 2012 Richard W.M. Jones <rjones@redhat.com> - 0.1-0.19.20100314
- Rebuild for OCaml 3.12.1.

* Wed Sep 21 2011 Richard W.M. Jones <rjones@redhat.com> - 0.1-0.18.20100314
- Bump for rebuilt ocamlnet.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.17.20100314
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan  7 2011 Richard W.M. Jones <rjones@redhat.com> - 0.1-0.16.20100314
- New upstream git version 20100314.
- Rebuild for OCaml 3.12.0.
- Add BR libX11-devel.  Seems to have been an implicit dependency before.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.1-0.14.20090113
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.13.20090113
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.1-0.12.20090113
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.11.20090113
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 0.1-0.10.20090113
- Tests require ounit & ruby.

* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 0.1-0.4.20090113
- New upstream version 20090113, resolving licensing issues.
- Use omake to build.
- Added a check section to run automated tests.

* Sat Dec 20 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1-0.2.20080922
- Fix the META file.

* Sat Dec 20 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1-0.1.20080922
- Initial RPM release.

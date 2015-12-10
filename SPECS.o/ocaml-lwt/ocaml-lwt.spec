%global commit 75b1dc1aefae75dc4ac6455f5a2688b3a52adabd
%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-lwt
Version: 2.4.5
Release: 4%{?dist}
Summary:        OCaml lightweight thread library
Summary(zh_CN.UTF-8): OCaml 的轻量级线程库

# The openssl linking exception is granted.
License:        LGPLv2+ with exceptions
URL:            http://ocsigen.org/lwt
Source0:        https://github.com/ocsigen/lwt/archive/%{commit}/lwt-%{commit}.tar.gz
#Source0:        https://github.com/ocsigen/lwt/archive/%{version}.tar.gz

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-camlp4-devel
BuildRequires:  ocaml-ssl-devel >= 0.4.0
BuildRequires:  ocaml-react-devel >= 0.9.0
BuildRequires:  chrpath
BuildRequires:  glib2-devel
BuildRequires:  libev-devel


%description
Lwt is a lightweight thread library for Objective Caml.  This library
is part of the Ocsigen project.

%description -l zh_CN.UTF-8
OCaml 的轻量级线程库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n lwt-%{commit}

%build
./configure --enable-ssl --enable-glib --disable-react --prefix=%{_prefix}
make


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
make install

chrpath --delete $OCAMLFIND_DESTDIR/stublibs/dll*.so
magic_rpm_clean.sh

%check
./configure --enable-ssl --enable-glib --disable-react --enable-tests \
  --prefix=%{_prefix}
make test

# Check lwt.react support is enabled (RHBZ#1048367).
OCAMLPATH=$RPM_BUILD_ROOT%{_libdir}/ocaml ocamlfind query lwt.react


%files
%doc LICENSE COPYING
%{_libdir}/ocaml/lwt
%if %opt
%exclude %{_libdir}/ocaml/lwt/*.a
%exclude %{_libdir}/ocaml/lwt/*.cmxa
#%exclude %{_libdir}/ocaml/lwt/*.cmx
%endif
%exclude %{_libdir}/ocaml/lwt/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%doc CHANGES
%if %opt
%{_libdir}/ocaml/lwt/*.a
%{_libdir}/ocaml/lwt/*.cmxa
#%{_libdir}/ocaml/lwt/*.cmx
%endif
%{_libdir}/ocaml/lwt/*.mli


%changelog
* Wed Nov 25 2015 Liu Di <liudidi@gmail.com> - 2.4.5-4
- 为 Magic 3.0 重建

* Wed Nov 11 2015 Liu Di <liudidi@gmail.com> - 2.4.5-3
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 2.4.5-2
- 为 Magic 3.0 重建

* Fri Mar 06 2015 Liu Di <liudidi@gmail.com> - 2.4.5-1
- 更新到 2.4.5

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 2.4.3-9
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 2.4.3-7
- Remove ocaml_arches macro (RHBZ#1087794).

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 2.4.3-6
- Remove ocaml_arches macro (RHBZ#1087794).

* Fri Jan  3 2014 Richard W.M. Jones <rjones@redhat.com> - 2.4.3-5
- Enable lwt.react support, and check it gets enabled (RHBZ#1048367).
- Remove libev patch since headers are back to normal location
  in libev >= 4.15-3.

* Wed Sep 18 2013 Jerry James <loganjerry@gmail.com> - 2.4.3-4
- Rebuild for OCaml 4.01.0, and add -ocaml41 patch to adapt to changes
- Enable debuginfo
- Enable glib integration
- Add check script
- Add manual to -devel subpackage
- Minor spec file cleanups

* Sat Sep 14 2013 Scott Tsai <scottt.tw@gmail.com> - 2.4.3-3
- New upstream version 2.4.3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Richard W.M. Jones <rjones@redhat.com> - 2.4.2-1
- New upstream version 2.4.2.
- Rebuild for OCaml 4.00.1.
- Remove patches which are now upstream.
- Clean up spec file.

* Mon Jul 30 2012 Richard W.M. Jones <rjones@redhat.com> - 2.3.2-7
- Rebuild for OCaml 4.00.0 official.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Scott Tsai <scottt.tw@gmail.com> - 2.3.2-5
- Patch myocamlobuild.ml in lwt-2.3.2-ocaml-4.patch to
  add compiler-libs to search patch for "Toploop".
- Add oasis-common.patch to make setup.ml work on OCaml 4.00.0
- Both patches from https://sympa.inria.fr/sympa/arc/caml-list/2012-05/msg00223.html

* Mon Jun 11 2012 Richard W.M. Jones <rjones@redhat.com> - 2.3.2-4
- Patch for OCaml 4.00.0.

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 2.3.2-3
- Rebuild for OCaml 4.00.0.

* Sat Jan 07 2012 Richard W.M. Jones <rjones@redhat.com> - 2.3.2-2
- Rebuild for OCaml 3.12.1.

* Thu Dec 08 2011 Scott Tsai scottt.tw@gmail.com - 2.3.2-1
- New upstream version 2.3.2. 

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 2.2.0-1
- New upstream version 2.2.0.
- Rebuild for OCaml 3.12.0.
- Add BR libev-devel.
- Patch <ev.h> -> <libev/ev.h>
- *.cmx files are no longer being distributed.
- No VERSION file.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-0.3.rc1
- Rebuild for OCaml 3.11.2.

* Mon Oct 12 2009 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-0.2.rc1.fc13
- ocaml-react is now in Fedora, so build this package.
- Missing BR on camlp4.

* Thu Oct  8 2009 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-0.rc1.fc13
- New upstream version 2.0.0+rc1.
- NB. This cannot be built as it depends on new package ocaml-react
  (RHBZ#527971).

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-5
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-3
- Rebuild.

* Wed Sep  3 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-2
- Rebuild with higher EVR than F-9 branch.

* Mon Sep  1 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-1
- Initial RPM release.

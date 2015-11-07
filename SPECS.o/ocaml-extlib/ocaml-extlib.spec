Name:           ocaml-extlib
Version:        1.6.1
Release:        10%{?dist}
Summary:        OCaml ExtLib additions to the standard library
Summary(zh_CN.UTF-8): OCaml 标准库的附加组件
License:        LGPLv2+ with exceptions

URL:            http://code.google.com/p/ocaml-extlib/
Source0:        http://ocaml-extlib.googlecode.com/files/extlib-%{version}.tar.gz

ExcludeArch:    sparc64 s390 s390x

Patch0:         extlib-install.patch

# Omitted from source tarball, I think.  This is copied from 1.5.2.
Source1:        odoc_style.css

BuildRequires:  ocaml >= 4.00.1
BuildRequires:  ocaml-findlib-devel >= 1.3.3-3
BuildRequires:  ocaml-camlp4-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  gawk


%description
ExtLib is a project aiming at providing a complete - yet small -
standard library for the OCaml programming language. The purpose of
this library is to add new functions to OCaml Standard Library
modules, to modify some functions in order to get better performances
or more safety (tail-recursive) but also to provide new modules which
should be useful for the average OCaml programmer.

%description -l zh_CN.UTF-8
OCaml 标准库的附加组件。

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
%setup -q -n extlib-%{version}

cp %{SOURCE1} .

%patch0 -p1


%build
# You can't just build extlib!


%install
extlibdir=$RPM_BUILD_ROOT%{_libdir}/ocaml/extlib
mkdir -p $extlibdir

# This does the build and install.
ocaml install.ml -d $extlibdir -b -min -doc \
%ifarch %{ocaml_native_compiler}
  -n
%endif

# Copy the interface files, and extLib.ml which is really an interface.
cp extLib.ml *.mli $RPM_BUILD_ROOT%{_libdir}/ocaml/extlib

install -m 0644 META $RPM_BUILD_ROOT%{_libdir}/ocaml/extlib/

# Move the HTML documentation - we'll install it using a %doc rule.
mv $extlibdir/extlib-doc .
magic_rpm_clean.sh

%files
%doc README.txt LICENSE
%{_libdir}/ocaml/extlib
%ifarch %{ocaml_native_compiler}
%exclude %{_libdir}/ocaml/extlib/*.a
%exclude %{_libdir}/ocaml/extlib/*.cmxa
%exclude %{_libdir}/ocaml/extlib/*.cmx
%endif
%exclude %{_libdir}/ocaml/extlib/*.mli
%exclude %{_libdir}/ocaml/extlib/*.ml


%files devel
%doc extlib-doc/*
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/extlib/*.a
%{_libdir}/ocaml/extlib/*.cmxa
%{_libdir}/ocaml/extlib/*.cmx
%endif
%{_libdir}/ocaml/extlib/*.mli
%{_libdir}/ocaml/extlib/*.ml


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.6.1-10
- 为 Magic 3.0 重建

* Wed Mar 04 2015 Liu Di <liudidi@gmail.com> - 1.6.1-9
- 为 Magic 3.0 重建

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 1.6.1-8
- ocaml-4.02.1 rebuild.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 1.6.1-7
- ocaml-4.02.0 final rebuild.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 1.6.1-6
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 01 2014 Richard W.M. Jones <rjones@redhat.com> - 1.6.1-4
- ocaml-4.02.0-0.8.git10e45753.fc22 build.

* Mon Jul 21 2014 Richard W.M. Jones <rjones@redhat.com> - 1.6.1-3
- Bump release and rebuild.

* Thu Jul 17 2014 Richard W.M. Jones <rjones@redhat.com> - 1.6.1-2
- New upstream version 1.6.1.
- Rebuild for OCaml 4.02.0 beta.
- Remove enable debug patch which is now upstream.
- New version requires camlp4.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1.5.4-1
- New upstream version 1.5.4.
- Rebuild against OCaml 4.01.0.
- Enable debuginfo.
  Does not work yet because the dumbass build system removed object files.
- Small modernizations of the specfile.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Richard W.M. Jones <rjones@redhat.com> - 1.5.3-2
- BR >= OCaml 4.00.1 so we can't be built against the wrong OCaml.

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1.5.3-1
- New upstream version 1.5.3.
- Remove patch, now upstream.
- Clean up the spec file.
- Rebuild for OCaml 4.00.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1.5.2-3
- Rebuild for OCaml 4.00.0.

* Thu Jun  7 2012 Richard W.M. Jones <rjones@redhat.com> - 1.5.2-2
- Fix for OCaml 4.00.0.

* Fri Jan  6 2012 Richard W.M. Jones <rjones@redhat.com> - 1.5.2-1
- New upstream version 1.5.2.

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-10
- Rebuild for OCaml 3.12.0.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-9
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-7
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-5
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-4
- Rebuild for OCaml 3.11.0

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-3
- Rebuild for OCaml 3.10.2

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-2
- License is LGPLv2+ with exceptions.
- Rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-1
- New upstream version 1.5.1.
- New home page.
- Rebuild for OCaml 3.10.1.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-8
- Force rebuild because of updated requires/provides scripts in OCaml.

* Mon Sep  3 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-7
- Force rebuild because of base OCaml.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-6
- Force rebuild because of changed BRs in base OCaml.

* Wed Aug  1 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-5
- ExcludeArch ppc64
- Added BR on ocaml-ocamldoc
- Use %doc to install documentation.

* Mon Jun 11 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-4
- Updated to latest packaging guidelines.

* Sat Jun  2 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-3
- Support for bytecode-only architectures.
- *.cmx files are needed.

* Fri May 25 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-2
- Use OCaml find-requires and find-provides.

* Fri May 18 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-1
- Initial RPM release.


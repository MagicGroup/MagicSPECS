%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-dbus
Version:        0.29
Release:        11%{?dist}
Summary:        OCaml library for using D-Bus
License:        LGPLv2

URL:            http://projects.snarc.org/ocaml-dbus/
Source0:        http://projects.snarc.org/ocaml-dbus/download/ocaml_dbus-%{version}.tar.bz2

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.10.0-7, ocaml-findlib
BuildRequires:  dbus-devel
BuildRequires:  chrpath


%description
D-Bus is a project that permits programs to communicate with each
other, using a simple IPC protocol.  This is an OCaml binding for
D-Bus.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n ocaml_dbus-%{version}


%build
make \
%if %opt
OCAMLC="ocamlc.opt" OCAMLOPT="ocamlopt.opt" OCAMLOPTFLAGS="-g"
%endif

if ! test -f "README"; then
cat > README <<_EOF
OCaml D-BUS bindings version %{version}.

Please see the main website for documentation:
http://tab.snarc.org/projects/ocaml_dbus/
_EOF
fi


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
make OCAMLDESTDIR=$OCAMLFIND_DESTDIR install

chrpath --delete $OCAMLFIND_DESTDIR/stublibs/dlldbus_stubs.so


%files
%doc README
%{_libdir}/ocaml/dbus
%if %opt
%exclude %{_libdir}/ocaml/dbus/*.a
%exclude %{_libdir}/ocaml/dbus/*.cmxa
%exclude %{_libdir}/ocaml/dbus/*.cmx
%endif
%exclude %{_libdir}/ocaml/dbus/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%doc README THANKS example_avahi.ml
%if %opt
%{_libdir}/ocaml/dbus/*.a
%{_libdir}/ocaml/dbus/*.cmxa
%{_libdir}/ocaml/dbus/*.cmx
%endif
%{_libdir}/ocaml/dbus/*.mli


%changelog
* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 0.29-11
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 0.29-9
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 Bruno Wolff III <bruno@wolff.to> - 0.29-6
- Rebuild for ocaml 4.0.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 0.29-4
- Rebuild for OCaml 4.00.0.

* Thu Jan 12 2012 Richard W.M. Jones <rjones@redhat.com> - 0.29-3
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 0.29-1
- New upstream version 0.29.
- Project moved to new URL and Source0.
- Rebuild for OCaml 3.12.0.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.24-2
- Rebuild for OCaml 3.11.2.

* Thu Oct  8 2009 Richard W.M. Jones <rjones@redhat.com> - 0.24-1
- New upstream version 0.24.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.07-5
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.07-3
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.07-2
- Rebuild for OCaml 3.11.0

* Sun Aug 31 2008 Richard W.M. Jones <rjones@redhat.com> - 0.07-1
- New upstream release 0.07.
- Remove rpath from shared object.

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 0.06-2
- Rebuild for OCaml 3.10.2

* Tue Mar  4 2008 Richard W.M. Jones <rjones@redhat.com> - 0.06-1
- New upstream release 0.06.
- All patches are now upstream.

* Mon Mar  3 2008 Richard W.M. Jones <rjones@redhat.com> - 0.05-1
- New upstream release 0.05.
- Include 'THANKS' file in doc.

* Sat Mar  1 2008 Richard W.M. Jones <rones@redhat.com> - 0.04-2
- Rebuild for ppc64.

* Sat Feb 23 2008 Richard W.M. Jones <rjones@redhat.com> - 0.04-1
- New upstream release 0.04.
- Added patches which have gone upstream for Avahi support.
- Added demo Avahi program.

* Tue Jan  8 2008 Richard W.M. Jones <rjones@redhat.com> - 0.03-2
- BR dbus-devel.
- Fix a typo in the description.
- Initial RPM release.

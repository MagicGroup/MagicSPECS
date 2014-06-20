%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-ssl
Version:        0.4.6
Release:        10%{?dist}
Summary:        SSL bindings for OCaml

License:        LGPLv2+ with exceptions
URL:            http://savonet.sourceforge.net/
Source0:        http://downloads.sourceforge.net/savonet/ocaml-ssl-%{version}.tar.gz
ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.12.1-3
BuildRequires:  ocaml-findlib-devel
BuildRequires:  openssl-devel >= 0.9.8j-1
BuildRequires:  gawk
Requires:       openssl

%global __ocaml_provides_opts -i Unix -i UnixLabels

%description
SSL bindings for OCaml.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       openssl-devel


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --libdir=%{_libdir}
# Parallel builds don't work.
unset MAKEFLAGS
%if %opt
export OCAMLC="ocamlc.opt -g"
export OCAMLOPT="ocamlopt.opt -g"
%endif
make


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
mkdir -p $OCAMLFIND_DESTDIR/stublibs
make install

# Copy the examples to the docdir.
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-devel/examples
cp examples/*.ml $RPM_BUILD_ROOT%{_docdir}/%{name}-devel/examples


%files
%doc CHANGES COPYING README
%{_libdir}/ocaml/ssl
%if %opt
%exclude %{_libdir}/ocaml/ssl/*.a
%exclude %{_libdir}/ocaml/ssl/*.cmxa
%endif
%exclude %{_libdir}/ocaml/ssl/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%if %opt
%{_libdir}/ocaml/ssl/*.a
%{_libdir}/ocaml/ssl/*.cmxa
%endif
%{_libdir}/ocaml/ssl/*.mli
%doc %{_docdir}/%{name}-devel


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 0.4.6-9
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.

* Tue Aug  6 2013 Richard W.M. Jones <rjones@redhat.com> - 0.4.6-8
- Unversioned docdir for Fedora 20 (RHBZ#994001).
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 0.4.6-5
- Rebuild for OCaml 4.00.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 0.4.6-3
- Rebuild for OCaml 4.00.0.

* Sat Apr 28 2012 Richard W.M. Jones <rjones@redhat.com> - 0.4.6-2
- Bump and rebuild against new OCaml compiler in ARM.

* Fri Jan  6 2012 Richard W.M. Jones <rjones@redhat.com> - 0.4.6-1
- New upstream version 0.4.6.
- Rebuild for OCaml 3.12.1.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 0.4.4-1
- New upstream version 0.4.4.
- Rebuild for OCaml 3.12.0.

* Tue Jan  5 2010 Richard W.M. Jones <rjones@redhat.com> - 0.4.3-7
- -devel package should require openssl-devel.
- Use upstream RPM 4.8 OCaml dependency generator.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.4.3-6
- Rebuild for OCaml 3.11.2.

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.4.3-5
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.4.3-3
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Richard W.M. Jones <rjones@redhat.com> - 0.4.3-1
- New upstream version 0.4.3.
- Force rebuild against new OpenSSL 0.9.8j.

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.2-12
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.2-11
- Rebuild for OCaml 3.11.0

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.4.2-10
- fix license tag

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.2-9
- Rebuild for OCaml 3.10.2

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.2-8
- Rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.2-7
- Rebuild for OCaml 3.10.1.
- For some reason 'Unix' and 'UnixLabels' leak so ignore them.

* Wed Dec  5 2007 Richard W.M. Jones <rjones@redhat.com> - 0.4.2-6
- Force rebuild because of new libssl, libcrypto sonames.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 0.4.2-5
- Force rebuild because of updated requires/provides scripts in OCaml.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 0.4.2-4
- Force rebuild because of changed BRs in base OCaml.

* Wed Jul 25 2007 Richard W.M. Jones <rjones@redhat.com> - 0.4.2-3
- ExcludeArch ppc64

* Mon Jun 11 2007 Richard W.M. Jones <rjones@redhat.com> - 0.4.2-2
- Updated to latest packaging guidelines.

* Sat May 26 2007 Richard W.M. Jones <rjones@redhat.com> - 0.4.2-1
- Initial RPM.

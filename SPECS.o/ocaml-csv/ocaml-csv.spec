%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-csv
Version: 1.3.3
Release: 2%{?dist}
Summary:        OCaml library for reading and writing CSV files
Summary(zh_CN.UTF-8): 读写 CSV 文件的 OCaml 库
License:        LGPLv2+

URL:            https://forge.ocamlcore.org/projects/csv/
Source0:        https://forge.ocamlcore.org/frs/download.php/1376/csv-%{version}.tar.gz

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 4.00.1
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-findlib-devel >= 1.3.3-3
BuildRequires:  ocaml-extlib-devel >= 1.5.3-2
BuildRequires:  gawk


%description
This OCaml library can read and write CSV files, including all
extensions used by Excel - eg. quotes, newlines, 8 bit characters in
fields, quote-0 etc.

The library comes with a handy command line tool called csvtool for
handling CSV files from shell scripts.

%description -l zh_CN.UTF-8
读写 CSV 文件的 OCaml 库。

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
%setup -q -n csv-%{version}


%build
ocaml setup.ml -configure --prefix %{_prefix} --destdir $RPM_BUILD_ROOT
make


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR

make install

%if %opt
mkdir -p $DESTDIR%{_bindir}
install -m 0755 csvtool.native $DESTDIR%{_bindir}/csvtool
%endif
magic_rpm_clean.sh

%check
make test


%files
%doc LICENSE.txt
%{_libdir}/ocaml/csv
%if %opt
%exclude %{_libdir}/ocaml/csv/*.a
%exclude %{_libdir}/ocaml/csv/*.cmxa
%exclude %{_libdir}/ocaml/csv/*.cmx
%endif
%exclude %{_libdir}/ocaml/csv/*.mli
%if %opt
%{_bindir}/csvtool
%endif


%files devel
%doc AUTHORS.txt LICENSE.txt README.txt
%if %opt
%{_libdir}/ocaml/csv/*.a
%{_libdir}/ocaml/csv/*.cmxa
%{_libdir}/ocaml/csv/*.cmx
%endif
%{_libdir}/ocaml/csv/*.mli


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.3.3-2
- 为 Magic 3.0 重建

* Thu Mar 05 2015 Liu Di <liudidi@gmail.com> - 1.3.3-1
- 更新到 1.3.3

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 1.3.1-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-1
- New upstream version 1.3.1.
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.
- Modernize the spec file some more.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-3
- BR >= OCaml 4.00.1 so we can't be built against the wrong OCaml.

* Mon Nov 26 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-2
- New upstream version 1.2.3.
- New upstream location.
- Clean up the spec file.
- Remove patches since they are no longer relevant.
- New setup appears to require ocamldoc.

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-13
- Rebuild for OCaml 4.00.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun  7 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-11
- Rebuild for OCaml 4.00.0.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-10
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-8
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-7
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-5
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-3
- Rebuild.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-2
- Rebuild for OCaml 3.11.0

* Mon Oct 27 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-1
- New upstream version 1.1.7.

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-8
- Rebuild for OCaml 3.10.2

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-7
- Rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-6
- Force rebuild for OCaml 3.10.1.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-5
- Force rebuild because of base OCaml.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-4
- Force rebuild because of changed BRs in base OCaml.

* Fri Aug 24 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-3
- License clarified to LGPLv2+ (and fixed/clarified upstream).
- Added ExcludeArch ppc64

* Mon Jun 11 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-2
- Updated to latest packaging guidelines.

* Tue May 29 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-1
- Initial RPM release.

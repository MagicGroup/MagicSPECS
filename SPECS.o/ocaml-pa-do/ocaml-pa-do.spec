%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-pa-do
Version:        0.8.16
Release:        4%{?dist}
Summary:        OCaml syntax extension for delimited overloading
Summary(zh_CN.UTF-8): OCaml 的高效算术语法扩展
License:        LGPLv2+ with exceptions

URL:            http://forge.ocamlcore.org/projects/pa-do/
Source0:        https://forge.ocamlcore.org/frs/download.php/1063/pa_do-%{version}.tar.gz

Patch0:         ocaml-pa-do-0.8.9-pdfpagelabels-off.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.12.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-camlp4-devel

# This package requires graphics.cmxa for some reason.
BuildRequires:  ocaml-x11

# For pdflatex, used to build the documentation.
BuildRequires:  texlive-latex

%global __ocaml_requires_opts -i Asttypes -i Parsetree


%description
A syntax extension to ease the writing of efficient arithmetic
expressions in OCaml.

This package contains three syntax extensions.
- pa_infix
- pa_do (includes Delimited_overloading, Macros)
- pa_do_nums

%description -l zh_CN.UTF-8
OCaml 的高效算术语法扩展。

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
%setup -q -n pa_do-%{version}

%patch0 -p2

ocaml setup.ml -configure \
  --prefix %{_prefix} \
  --docdir %{_docdir} \
  --destdir $RPM_BUILD_ROOT


%build
make
make doc


%check
%ifnarch ppc64
make test
%endif


%install
# These rules work if the library uses 'ocamlfind install' to install itself.
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
make install

# Install API docs using %doc section.
mv $RPM_BUILD_ROOT%{_docdir}/api .
magic_rpm_clean.sh

%files
%doc LICENSE.txt
%{_libdir}/ocaml/pa_do
%exclude %{_libdir}/ocaml/pa_do/*.mli


%files devel
%doc AUTHORS.txt INSTALL.txt LICENSE.txt README.txt api
%{_libdir}/ocaml/pa_do/*.mli


%changelog
* Tue Mar 10 2015 Liu Di <liudidi@gmail.com> - 0.8.16-4
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 0.8.16-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 0.8.16-1
- New upstream version 0.8.16.
- OCaml 4.01.0 rebuild.
- Enable debuginfo.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 0.8.15-1
- New upstream version 0.8.15.
- Remove patches, now upstream.
- Rebuild for OCaml 4.00.1.
- Clean up the spec file.

* Mon Jul 30 2012 Richard W.M. Jones <rjones@redhat.com> - 0.8.13-3
- Rebuild for OCaml 4.00.0 official.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul  3 2012 Richard W.M. Jones <rjones@redhat.com> - 0.8.13-1
- New upstream version 0.8.13.
- Rebuild for OCaml 4.00.0.
- Send some patches for 4.00.0 upstream.
- No *.cmx files upstream.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 0.8.12-1
- New upstream version 0.8.12.
- Rebuild for OCaml 3.12.0.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.8.10-3
- Rebuild for OCaml 3.11.2.

* Thu Nov  5 2009 Richard W.M. Jones <rjones@redhat.com> - 0.8.10-2
- Correct Source0 URL.

* Thu Oct  8 2009 Richard W.M. Jones <rjones@redhat.com> - 0.8.10-1
- New upstream version 0.8.10.

* Thu Aug  6 2009 Richard W.M. Jones <rjones@redhat.com> - 0.8.9-7
- Force rebuild again to test FTBFS issue.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Richard W.M. Jones <rjones@redhat.com> - 0.8.9-5
- Force rebuild to test FTBFS issue (RHBZ#511603).
- Add ocaml-pa-do-0.8.9-pdfpagelabels-off.patch.

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.8.9-2
- New upstream version 0.8.9.
- Rebuild for OCaml 3.11.1.
- Remove upstreamed patches.

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Thu Mar 19 2009 Richard W.M. Jones <rjones@redhat.com> - 0.8.4-5
- Ignore Asttypes and Parsetree deps (mschwendt).

* Tue Mar 17 2009 Richard W.M. Jones <rjones@redhat.com> - 0.8.4-4
- Don't run the tests on ppc64, causes out of memory error.

* Tue Mar 17 2009 Richard W.M. Jones <rjones@redhat.com> - 0.8.4-3
- Patch module name which is illegal in OCaml 3.11.
- Patch complex tests.

* Mon Mar 16 2009 Richard W.M. Jones <rjones@redhat.com> - 0.8.4-2
- Add check section which runs the tests.
- Don't duplicate LICENSE file in the -devel subpackage as well.

* Mon Mar 16 2009 Richard W.M. Jones <rjones@redhat.com> - 0.8.4-1
- New upstream version 0.8.4.
- Use http URLs instead of https URLs.
- Min version of OCaml required is 3.10, not 3.11.  This will let us
  distribute on Fedora 10.

* Sun Feb  8 2009 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-2
- New upstream version 0.8.3.
- Missing BR pdflatex.

* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 0.8.2-1
- New upstream version 0.8.2.

* Sun Dec 21 2008 Richard W.M. Jones <rjones@redhat.com> - 0.8.1-2
- Correct the source URL.

* Sat Dec 20 2008 Richard W.M. Jones <rjones@redhat.com> - 0.8.1-1
- New upstream release 0.8.1.
- Run omake with the --verbose option to try to debug Koji failures.

* Tue Dec 16 2008 Richard W.M. Jones <rjones@redhat.com> - 0.8-1
- Initial RPM release, forward-ported to OCaml 3.11.0.

%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-res
Version: 4.0.7
Release: 4%{?dist}
Summary:        OCaml library for resizing arrays and strings
Summary(zh_CN.UTF-8): 调整数组和字符串大小的 OCaml 库
License:        LGPLv2+ with exceptions

URL:            https://github.com/mmottl/res
Source0:        https://github.com/mmottl/res/releases/download/v%{version}/res-%{version}.tar.gz

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ghostscript
BuildRequires:  texlive-collection-latexrecommended
BuildRequires:  texlive-preprint


%description
This OCaml-library consists of a set of modules which implement
automatically resizing (= reallocating) datastructures that consume a
contiguous part of memory. This allows appending and removing of
elements to/from arrays (both boxed and unboxed), strings (->
buffers), bit strings and weak arrays while still maintaining fast
constant-time access to elements.

There are also functors that allow the generation of similar modules
which use different reallocation strategies.

%description -l zh_CN.UTF-8
调整数组和字符串大小的 OCaml 库。

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
%setup -q -n res-%{version}


%build
./configure \
  --destdir $RPM_BUILD_ROOT \
  --prefix %{_prefix} \
  --sysconfdir %{_sysconfdir}
make

make doc


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
make install

# Remove installed documentation.  We'll add it with a %doc directive.
rm -r $RPM_BUILD_ROOT/usr/share/doc
magic_rpm_clean.sh

%files
%doc COPYING.txt
%{_libdir}/ocaml/res
%if %opt
%exclude %{_libdir}/ocaml/res/*.a
%exclude %{_libdir}/ocaml/res/*.cmxa
%endif
%exclude %{_libdir}/ocaml/res/*.mli


%files devel
%doc COPYING.txt AUTHORS.txt CHANGES.txt INSTALL.txt README.md TODO.md
%doc _build/API.docdir
%if %opt
%{_libdir}/ocaml/res/*.a
%{_libdir}/ocaml/res/*.cmxa
%endif
%{_libdir}/ocaml/res/*.mli


%changelog
* Wed Nov 25 2015 Liu Di <liudidi@gmail.com> - 4.0.7-4
- 为 Magic 3.0 重建

* Wed Nov 11 2015 Liu Di <liudidi@gmail.com> - 4.0.7-3
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 4.0.7-2
- 为 Magic 3.0 重建

* Sat Mar 14 2015 Liu Di <liudidi@gmail.com> - 4.0.7-1
- 更新到 4.0.7

* Sat Mar 14 2015 Liu Di <liudidi@gmail.com> - 4.0.3-3
- 更新到 4.0.7

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 4.0.3-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 4.0.3-16
- Update to 4.0.3.
- Fix upstream URL and source.
- Use ./configure script, and set -destdir parameter.
- DVI & PDF documentation is no longer build, so don't include it.
- OCaml 4.01.0 rebuild.
- Enable debuginfo.

* Thu Aug  8 2013 Richard W.M. Jones <rjones@redhat.com> - 3.2.0-15
- Re-enable latex/PDF doc generation.

* Mon Aug  5 2013 Richard W.M. Jones <rjones@redhat.com> - 3.2.0-14
- Disable latex/PDF doc generation as texlive is broken (RHBZ#919891).

* Sun Aug  4 2013 Richard W.M. Jones <rjones@redhat.com> - 3.2.0-13
- Modernize the spec file.
- +BR texlive-pdftex-bin to make latex work.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 Bruno Wolff III <bruno@wolff.to> - 3.2.0-10
- Rebuild for ocaml 4.0.1.
- Adjust build requirements for texlive packaging changes.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 3.2.0-8
- Rebuild for OCaml 4.00.0.

* Sat Jan 07 2012 Richard W.M. Jones <rjones@redhat.com> - 3.2.0-7
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Richard W.M. Jones <rjones@redhat.com> - 3.2.0-5
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 3.2.0-4
- Rebuild for OCaml 3.11.2.

* Sun Oct  4 2009 Richard W.M. Jones <rjones@redhat.com> - 3.2.0-3
- New upstream release 3.2.0.
- Changes file -> Changelog

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 3.1.1-3
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Tue Mar 10 2009 Richard W.M. Jones <rjones@redhat.com> - 3.1.1-1
- New upstream version 3.1.1.
- Fix URL.
- Fix Source URL.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 3.0.0-2
- Rebuild for OCaml 3.11.0+rc1.

* Thu Nov 20 2008 Richard W.M. Jones <rjones@redhat.com> - 3.0.0-1
- New upstream version 3.0.0.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.6-2
- Rebuild for OCaml 3.11.0

* Sun Aug 31 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.6-1
- New upstream version 2.2.6.

* Sat May  3 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.5-1
- Initial RPM release.

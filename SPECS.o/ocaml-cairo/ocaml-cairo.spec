%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

%define git 1
%define vcsdate 20151101

# Important note!  There are at least two quite separate OCaml cairo
# projects.  This one is: http://cairographics.org/cairo-ocaml/
# The other one is: http://forge.ocamlcore.org/projects/cairo/

# There are no source releases for ocaml-cairo > 1.0.0.  To get the
# source matching this you have to do:
#
# git clone git://anongit.freedesktop.org/cairo-ocaml
# cd cairo-ocaml
# git archive --prefix=ocaml-cairo-%{version}/ %{commit} | \
#   gzip > ../ocaml-cairo-1.2.0-git%{commit}.tar.gz
%global commit 872c9bc92e6

Name:           ocaml-cairo
Epoch:          1
Version:        1.2.0
Release:        0.26.git%{vcsdate}%{?dist}
Summary:        OCaml library for accessing cairo graphics

ExcludeArch:    sparc64 s390 s390x

License:        LGPLv2
URL:            http://cairographics.org/cairo-ocaml/

Source0:        ocaml-cairo-git%{vcsdate}.tar.xz
Source1:        ocaml-cairo-META
Source2:	make_ocaml-cairo_git_package.sh

Patch1:         ocaml-cairo-1.2.0-enable-ocamlopt-debug.patch

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-lablgtk-devel
BuildRequires:  cairo-devel >= 1.2.0
BuildRequires:  automake
BuildRequires:  gtk2-devel
BuildRequires:  chrpath


%description
Cairo is a multi-platform library providing anti-aliased vector-based
rendering for multiple target backends. Paths consist of line segments
and cubic splines and can be rendered at any width with various join
and cap styles. All colors may be specified with optional translucence
(opacity/alpha) and combined using the extended Porter/Duff
compositing algebra as found in the X Render Extension.

Cairo exports a stateful rendering API similar in spirit to the path
construction, text, and painting operators of PostScript, (with the
significant addition of translucence in the imaging model). When
complete, the API is intended to support the complete imaging model of
PDF 1.4.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       ocaml-lablgtk-devel


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}-git%{vcsdate}

%patch1 -p1

aclocal -I support
autoconf
./configure --libdir=%{_libdir}
cp %{SOURCE1} META


%build
make
make doc


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs

ocamlfind install cairo src/{*.mli,*.cmi,*.cma,*.a,*.cmxa,*.cmx,dll*.so} META

chrpath --delete $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs/dll*.so


%files
%doc COPYING
%{_libdir}/ocaml/cairo
%if %opt
%exclude %{_libdir}/ocaml/cairo/*.a
%exclude %{_libdir}/ocaml/cairo/*.cmxa
%exclude %{_libdir}/ocaml/cairo/*.cmx
%endif
%exclude %{_libdir}/ocaml/cairo/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%doc COPYING ChangeLog README doc/html
%if %opt
%{_libdir}/ocaml/cairo/*.a
%{_libdir}/ocaml/cairo/*.cmxa
%{_libdir}/ocaml/cairo/*.cmx
%endif
%{_libdir}/ocaml/cairo/*.mli


%changelog
* Wed Nov 25 2015 Liu Di <liudidi@gmail.com> - 1:1.2.0-0.26.git20151101
- 为 Magic 3.0 重建

* Wed Nov 11 2015 Liu Di <liudidi@gmail.com> - 1:1.2.0-0.25.git20151101
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1:1.2.0-0.24.git20151101
- 更新到 20151101 日期的仓库源码

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1:1.2.0-0.23.git20150305
- 为 Magic 3.0 重建

* Thu Mar 05 2015 Liu Di <liudidi@gmail.com> - 1:1.2.0-0.22.git20150305
- 为 Magic 3.0 重建

* Thu Mar 05 2015 Liu Di <liudidi@gmail.com> - 1:1.2.0-0.21.git20150305
- 更新到 20150305 日期的仓库源码

* Thu Mar 05 2015 Liu Di <liudidi@gmail.com> - 1:1.2.0-0.21.git20150303
- 为 Magic 3.0 重建

* Tue Feb 17 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.0-0.20.git872c9bc92e6
- ocaml-4.02.1 rebuild.

* Fri Oct 31 2014 Orion Poplawski <orion@cora.nwra.com> - 1:1.2.0-0.19.git872c9bc92e6
- Update to latest git

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.0-0.18.git08b40192975
- ocaml-4.02.0 final rebuild.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.0-0.17.git08b40192975
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.0-0.16.git08b40192975
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.0-0.15.git08b40192975
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Wed Jul 23 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.0-0.14.git08b40192975
- OCaml 4.02.0 beta rebuild.

* Mon Jul 14 2014 Orion Poplawski <orion@cora.nwra.com> - 1:1.2.0-0.13.git08b40192975
- Rebuild for OCaml 4.02

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.0-0.12.git08b40192975
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.0-0.11.git08b40192975
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.0-0.10.git08b40192975
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.0-0.9.git08b40192975
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Orion Poplawski <orion@cora.nwra.com> - 1:1.2.0-0.8.git08b40192975
- Rebuild for OCaml 4.00.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.0-0.7.git08b40192975
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 8 2012 Orion Poplawski <orion@cora.nwra.com> - 1:1.2.0-0.6.git08b40192975
- Rebuild for OCaml 4.00.0.

* Fri Jan  6 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.0-0.5.git08b40192975
- Update to git commit 08b40192975 (dated 2011-09-11).
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.0-0.4.gita5c5ee9f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 5 2011 Orion Poplawski <orion@cora.nwra.com> - 1:1.2.0-0.3.gita5c5ee9f
- Rebuild for OCaml 3.12

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.0-0.2.gita5c5ee9f
- Rebuild for OCaml 3.11.2.

* Mon Dec  7 2009 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.0-0.1.gita5c5ee9f
- So we are wrong, version numbers did NOT roll backwards.
- Revert to current git head (a5c5ee9f) which is a pre-release of 1.2.0
  (RHBZ#541542).
- Replace %%define with %%global.
- Patch0 is now upstream.
- Checked package with rpmlint - no problems.

* Thu Nov 26 2009 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.0-2
- ocaml-cairo-devel requires ocaml-lablgtk-devel (RHBZ#541427).

* Thu Oct  8 2009 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.0-1
- New upstream version 1.0.0.
- Yes, version number really did roll backwards, so now we're using Epoch.
- Patch for compatibility with OCaml 3.11.1 (renamed bigarray structs).

* Tue Sep 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.0.cvs20080301-11
- Force rebuild against newer lablgtk.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.cvs20080301-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.0.cvs20080301-9
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.cvs20080301-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  7 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.0.cvs20080301-7
- Rebuild against updated lablgtk.

* Tue Dec  9 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0.cvs20080301-6
- Include cairo.a and cairo_lablgtk.a (fixes BZ 475349).

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0.cvs20080301-5
- Rebuild.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0.cvs20080301-4
- Rebuild for OCaml 3.11.0

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0.cvs20080301-3
- Rebuild for OCaml 3.10.2

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0.cvs20080301-2
- Upgrade to latest CVS.
- Include instructions on how check out versions from CVS.
- Build for ppc64.

* Fri Feb 29 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0.cvs20080224-2
- Added BRs for automake and gtk2-devel.

* Sun Feb 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.0.cvs20080224-1
- Initial RPM release.

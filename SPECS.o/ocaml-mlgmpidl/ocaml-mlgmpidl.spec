%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

%global svndate 20120830

Name:           ocaml-mlgmpidl
Version:        1.2.1
Release:        0.9.%{svndate}%{?dist}
Summary:        OCaml interface to GMP and MPFR libraries
Summary(zh_CN.UTF-8): GMP 和 MPFR 库的 OCaml 接口
Group:          Development/Libraries
License:        LGPLv2

URL:            http://www.inrialpes.fr/pop-art/people/bjeannet/mlxxxidl-forge/mlgmpidl/

# There is no official upstream release for 1.2.1 (although it is tagged
# in upstream SVN).  So I built this tarball from the upstream
# *trunk*, since it contains additional fixes for OCaml 3.12:
#
#   svn checkout svn://scm.gforge.inria.fr/svnroot/mlxxxidl/
#   cd mlxxxidl/mlgmpidl
#   tar zcf mlgmpidl-YYYYMMDD.tar.gz trunk
#
Source0:        mlgmpidl-%{svndate}.tar.gz

Source1:        mlgmpidl_test.ml
Source2:        mlgmpidl_test_result

Patch0:         mlgmpidl-1.2-Makefile.patch

BuildRequires:  ocaml
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-camlidl-devel
BuildRequires:  gmp-devel
BuildRequires:  mpfr-devel
# BuildRequires for documentation build
BuildRequires:  tex(latex)
BuildRequires:  tex(ecrm1000.tfm)
BuildRequires:  tex(fullpage.sty)
BuildRequires:  ghostscript


%description
MLGMPIDL is an OCaml interface to the GMP and MPFR rational and real
number math libraries. Although there is another such interface, this
one is different in that it provides a more imperative (rather than
functional) interface to conserve memory and that this one uses
CAMLIDL to take care of the C/OCaml interface in a convenient and
modular way.

%description -l zh_CN.UTF-8
GMP 和 MPFR 库的 OCaml 接口。

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

%package        doc
Summary:        Documentation files for %{name}
Summary(zh_CN.UTF-8): %{name} 的文档
Group:          Documentation
Group(zh_CN.UTF-8): 文档

%description    doc
The %{name}-doc package contains documentation for using %{name}.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q -n trunk
cp %{SOURCE1} %{SOURCE2} .

# Patch makefile to take custom locations for libraries and installing
%patch0


%build
mv Makefile.config.model Makefile.config

%global ocaml_lib_dir %{_libdir}/ocaml
%global my_ocaml_lib_dir %{ocaml_lib_dir}/gmp

# Upstream Makefile is NOT safe to be called in parallel.
unset MAKEFLAGS

make PREFIX=%{_prefix} GMP_LIBDIR=%{_libdir} MPFR_LIBDIR=%{_libdir} \
     CAML_LIBDIR=%{ocaml_lib_dir} CAMLIDL_LIBDIR=%{ocaml_lib_dir} \
     MLGMPIDL_LIBDIR=%{_libdir} all
make mlgmpidl.dvi
make html
dvipdf mlgmpidl.dvi


%check
ocamlc -ccopt -L. -custom -dllib %{_libdir}/libgmp.so gmp.cma bigarray.cma mlgmpidl_test.ml
./a.out > mlgmpidl_test_myresult
diff mlgmpidl_test_myresult mlgmpidl_test_result


%install
# Upstream Makefile is NOT safe to be called in parallel.
unset MAKEFLAGS

# Library uses ocamlfind install to install itself.  Set up environment
# so that it works.
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs

make install

# Upstream now puts gmp_caml.h into the OCaml libdir (previously it
# was in %{_includedir}).  It's not clear if this is a bug or intended
# change, but move it to %{_includedir}.
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mv $RPM_BUILD_ROOT%{my_ocaml_lib_dir}/gmp_caml.h $RPM_BUILD_ROOT%{_includedir}

# Install Documentation
%define doc_dir %{_docdir}/%{name}
mkdir -p %{buildroot}%{doc_dir}
cp -p *.pdf %{buildroot}%{doc_dir}
cp -pr html %{buildroot}%{doc_dir}
magic_rpm_clean.sh

%files
%{my_ocaml_lib_dir}
%if %opt
%exclude %{my_ocaml_lib_dir}/*.cmx*
%endif
%exclude %{my_ocaml_lib_dir}/*.idl
%exclude %{my_ocaml_lib_dir}/*.mli
%exclude %{my_ocaml_lib_dir}/*.a
%{ocaml_lib_dir}/stublibs/*.so
%{ocaml_lib_dir}/stublibs/*.so.owner
%doc COPYING README


%files devel
%{_includedir}/*
%if %opt
%{my_ocaml_lib_dir}/*.cmx*
%endif
%{my_ocaml_lib_dir}/*.idl
%{my_ocaml_lib_dir}/*.mli
%{my_ocaml_lib_dir}/*.a


%files doc
%{_docdir}/%{name}


%changelog
* Mon Mar 09 2015 Liu Di <liudidi@gmail.com> - 1.2.1-0.9.20120830
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 1.2.1-0.8.20120830
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-0.7.20120830
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-0.6.20120830
- Remove ocaml_arches macro (RHBZ#1087794).

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-0.5.20120830
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.
- Do not prevent stripping -- not needed for modern OCaml.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-0.4.20120830
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-0.3.20120830
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 13 2012 Jerry James <loganjerry@gmail.com> - 1.2.1-0.2.20120830
- fullpage.sty is available in TeXLive 2012; use it

* Wed Oct 17 2012 Jerry James <loganjerry@gmail.com> - 1.2.1-0.1.20120830
- Rebuild for OCaml 4.00.1.
- Update to latest upstream SVN.
- Regenerate patch with fuzz.
- Drop fix for \textquotesingle; fixed upstream.
- Replace use of old fullpage style with use of geometry package.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.5.20120508
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2-0.4.20120508
- Rebuild for OCaml 4.00.0.

* Sat Jun  9 2012 Jerry James <loganjerry@gmail.com> - 1.2-0.3.20120508
- Rebuild for OCaml 4.00.0
- Fix for undefined control sequence \textquotesingle
- Minor spec file cleanups

* Tue May  8 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2-0.2.20120508
- Update to latest upstream SVN.
- Change define -> global.
- Don't create or install a META file, as upstream now creates one
  (RHBZ#819785).
- Remove patch1, no longer needed.
- Library now uses 'ocamlfind install' to install itself.
- Library has moved from 'mlgmpidl' to 'gmp' directory.
- gmptop (toplevel) has disappeared from upstream, so remove it.  We
  can also get rid of the prelink hacks.
- Package stublibs.
- Add missing BR ocaml-findlib-devel.

* Mon Jan  9 2012 Jerry James <loganjerry@gmail.com> - 1.1-7
- Rebuild for OCaml 3.12.1
- Minor spec file cleanups

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Richard W.M. Jones <rjones@redhat.com> - 1.1-6
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).
- Remove GMP_RND_MAX and mpfr_random, both no longer in GMP/MPFR.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.1-4
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.1-2
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Thu Apr 02 2009 Alan Dunn <amdunn@gmail.com> 1.1-1
- New upstream version incorporates functional interface to Mpfr.
* Sat Mar 28 2009 Alan Dunn <amdunn@gmail.com> 1.0-1
- Initial Fedora RPM version.

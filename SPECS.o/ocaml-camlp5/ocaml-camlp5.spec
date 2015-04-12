%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-camlp5
Version: 6.12
Release: 1%{?dist}
Summary:        Classical version of camlp4 OCaml preprocessor
Summary(zh_CN.UTF-8): camlp4 OCaml 预处理器的经典版本

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        BSD
URL:            http://camlp5.gforge.inria.fr/

Source0:        http://camlp5.gforge.inria.fr/distrib/src/camlp5-%{version}.tgz

BuildRequires:  ocaml
BuildRequires:  ocaml-ocamldoc

%global __ocaml_requires_opts -i Asttypes -i Parsetree -i Pa_extend
%global __ocaml_provides_opts -i Dynlink -i Dynlinkaux -i Pa_extend

%description
Camlp5 is a preprocessor-pretty-printer of OCaml.

It is the continuation of the classical camlp4 with new features.

OCaml 3.10 and above have an official camlp4 which is incompatible
with classical (<= 3.09) versions.  You can find that in the
ocaml-camlp4 package.

%description -l zh_CN.UTF-8
camlp4 OCaml 预处理器的经典版本。

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
%setup -q -n camlp5-%{version}

# Build with debug information
sed -i 's,WARNERR="-warn-error A",WARNERR="-g -warn-error A",' configure
sed -i 's,-linkall,& -g,g' top/Makefile
for fil in compile/compile.sh $(find . -name Makefile); do
  sed -i 's,\$(OCAMLN)c,& -g,;s,\$(OCAMLN)opt,& -g,;s,LINKFLAGS=,&-g ,' $fil
done

# But don't build pa_lisp with debug information because it triggers this:
# Fatal error: exception Assert_failure("asmcomp/emitaux.ml", 226, 4)
sed -i 's/$(WARNERR)/-warn-error A/' etc/Makefile.withnew


%build
./configure
%if %opt
# For ppc64 we need a larger stack than default to compile some files
# because the stages in the OCaml compiler are not mutually tail
# recursive.
%ifarch ppc64 ppc64le
ulimit -a
ulimit -Hs 65536
ulimit -Ss 65536
%endif
make world.opt
%else
make world
%endif
make -C doc/htmlp

%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}
make install \
  LIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml \
  OLIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml \
  BINDIR=$RPM_BUILD_ROOT%{_bindir} \
  MANDIR=$RPM_BUILD_ROOT%{_mandir}
cp -p etc/META $RPM_BUILD_ROOT%{_libdir}/ocaml/camlp5
rm -f doc/html/.cvsignore doc/htmlp/{.cvsignore,*.sh,Makefile,html2*}
magic_rpm_clean.sh

%files
%doc README LICENSE
%{_libdir}/ocaml/camlp5
%if %opt
%exclude %{_libdir}/ocaml/camlp5/*.a
%exclude %{_libdir}/ocaml/camlp5/*.cmxa
%exclude %{_libdir}/ocaml/camlp5/*.cmx
%endif
%exclude %{_libdir}/ocaml/camlp5/*.mli


%files devel
%doc CHANGES ICHANGES DEVEL UPGRADING doc/html
%if %opt
%{_libdir}/ocaml/camlp5/*.a
%{_libdir}/ocaml/camlp5/*.cmxa
%{_libdir}/ocaml/camlp5/*.cmx
%endif
%{_libdir}/ocaml/camlp5/*.mli
%{_bindir}/camlp5*
%{_bindir}/mkcamlp5*
%{_bindir}/ocpp5
%{_mandir}/man1/*.1*


%changelog
* Thu Mar 05 2015 Liu Di <liudidi@gmail.com> - 6.12-1
- 更新到 6.12

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 6.11-5
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 6.11-3
- Remove ocaml_arches macro (RHBZ#1087794).

* Thu Apr 10 2014 Michel Normand <normand@linux.vnet.ibm.com> 6.11-2
- increase stack size for ppc64/ppc64le (RHBZ#1085850)

* Sat Sep 14 2013 Jerry James <loganjerry@gmail.com> - 6.11-1
- New upstream version 6.11 (provides OCaml 4.01.0 support)
- Build with debug information
- Drop upstreamed -typevar patch
- Upstream now provides its own META file

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Jerry James <loganjerry@gmail.com> - 6.07-1
- New upstream version 6.07 (provides OCaml 4.00.1 support)
- Add -typevar patch to fix the build

* Sat Jul 28 2012 Richard W.M. Jones <rjones@redhat.com> - 6.06-4
- Rebuild for OCaml 4.00.0 official release.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 6.06-2
- Rebuild for OCaml 4.00.0.

* Fri Jun  8 2012 Jerry James <loganjerry@gmail.com> - 6.06-1
- New upstream version 6.06 (provides OCaml 4.0 support)
- Add HTML documentation to the -devel package

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 6.02.3-2
- Rebuild for OCaml 3.12.1.

* Thu Oct 27 2011 Jerry James <loganjerry@gmail.com> - 6.02.3-1
- New upstream version 6.02.3 (bz 691913).
- Switch from ExcludeArch to ExclusiveArch %%{ocaml_arches}.
- Drop unnecessary spec file elements (BuildRoot, etc.).
- Preserve timestamp on META.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.02.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 6.02.1-1
- New upstream version 6.02.1.
- Remove upstream patches (both upstream).
- Rebuild for OCaml 3.12.0.

* Wed Jan 13 2010 Richard W.M. Jones <rjones@redhat.com> - 5.12-6
- Ignore bogus provides Dynlink and Dynlinkaux.

* Wed Jan  6 2010 Richard W.M. Jones <rjones@redhat.com> - 5.12-5
- Ignore ocaml(Pa_extend) bogus generated requires and provides.

* Tue Jan  5 2010 Richard W.M. Jones <rjones@redhat.com> - 5.12-4
- Include Debian patch to fix support for OCaml 3.11.2.
- Include Debian patch to fix typos in man page.
- Replace %%define with %%global.
- Use upstream RPM 4.8 OCaml dependency generator.
- Put ./configure in %%build section.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 5.12-3
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 5.12-1
- New upstream version 5.12, excepted to fix 3.11.1 build problems.

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 5.11-1
- Rebuild for OCaml 3.11.1
- New upstream version 5.11.
- Remove META file listed twice in %%files.

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 5.10-2
- Rebuild for OCaml 3.11.0+rc1.

* Thu Nov 20 2008 Richard W.M. Jones <rjones@redhat.com> - 5.10-1
- New upstream version 5.10.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 5.09-2
- Rebuild for OCaml 3.11.0

* Sun Aug 31 2008 Richard W.M. Jones <rjones@redhat.com> - 5.09-1
- New upstream version 5.09.

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 5.08-3
- Rebuild for OCaml 3.10.2.

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 5.08-2
- Build on ppc64.

* Thu Feb 21 2008 Richard W.M. Jones <rjones@redhat.com> - 5.08-1
- New upstream version 5.08.
- BR ocaml >= 3.10.1.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 5.04-2
- Strip the *.opt binaries.

* Thu Dec 13 2007 Stijn Hoop <stijn@win.tue.nl> - 5.04-1
- Update to 5.04

* Wed Aug  8 2007 Richard W.M. Jones <rjones@redhat.com> - 4.07-2
- Add a META file.

* Wed Aug  8 2007 Richard W.M. Jones <rjones@redhat.com> - 4.07-1
- Initial RPM release.

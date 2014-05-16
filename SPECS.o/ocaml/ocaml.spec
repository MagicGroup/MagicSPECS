Name:           ocaml
Version:        4.00.1
Release:        2%{?dist}

Summary:        OCaml compiler and programming environment

License:        QPL and (LGPLv2+ with exceptions)

URL:            http://www.ocaml.org

Source0:        http://caml.inria.fr/pub/distrib/ocaml-4.00/ocaml-%{version}.tar.bz2
Source1:        http://caml.inria.fr/pub/distrib/ocaml-4.00/ocaml-4.00-refman-html.tar.gz
Source2:        http://caml.inria.fr/pub/distrib/ocaml-4.00/ocaml-4.00-refman.pdf
Source3:        http://caml.inria.fr/pub/distrib/ocaml-4.00/ocaml-4.00-refman.info.tar.gz

# IMPORTANT NOTE:
#
# These patches are generated from unpacked sources stored in a
# fedorahosted git repository.  If you change the patches here, they
# will be OVERWRITTEN by the next update.  Instead, request commit
# access to the fedorahosted project:
#
# http://git.fedorahosted.org/git/?p=fedora-ocaml.git
#
# ALTERNATIVELY add a patch to the end of the list (leaving the
# existing patches unchanged) adding a comment to note that it should
# be incorporated into the git repo at a later time.
#
Patch0001:      0001-Add-.gitignore-file-to-ignore-generated-files.patch
Patch0002:      0002-Ensure-empty-compilerlibs-directory-is-created-by-gi.patch
Patch0003:      0003-ocamlbyteinfo-ocamlplugininfo-Useful-utilities-from-.patch
Patch0004:      0004-Don-t-add-rpaths-to-libraries.patch
Patch0005:      0005-configure-Allow-user-defined-C-compiler-flags.patch
Patch0006:      0006-Add-support-for-ppc64.patch

BuildRequires:  ncurses-devel
BuildRequires:  gdbm-devel
BuildRequires:  tcl-devel
BuildRequires:  tk-devel
BuildRequires:  emacs
BuildRequires:  gawk
BuildRequires:  perl
BuildRequires:  util-linux
BuildRequires:  libICE-devel
BuildRequires:  libSM-devel
BuildRequires:  libX11-devel
BuildRequires:  libXaw-devel
BuildRequires:  libXext-devel
BuildRequires:  libXft-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXrender-devel
BuildRequires:  libXt-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  chrpath

# git is required for patch management.
BuildRequires:  git

Requires:       gcc
Requires:       ncurses-devel
Requires:       gdbm-devel
Requires:       rpm-build >= 4.8.0

Provides:       ocaml(compiler) = %{version}

# We can compile OCaml on just about anything, but the native code
# backend is only available on a subset of architectures.
ExclusiveArch:  alpha %{arm} ia64 %{ix86} x86_64 ppc ppc64 sparc sparcv9 mips64el

%ifarch %{arm} %{ix86} ppc ppc64 sparc sparcv9 x86_64
%global native_compiler 1
%else
%global native_compiler 0
%endif

%ifarch %{arm} %{ix86} ppc ppc64 sparc sparcv9 x86_64
%global natdynlink 1
%else
%global natdynlink 0
%endif

%global __ocaml_requires_opts -c -f '%{buildroot}%{_bindir}/ocamlrun %{buildroot}%{_bindir}/ocamlobjinfo'
%global __ocaml_provides_opts -f '%{buildroot}%{_bindir}/ocamlrun %{buildroot}%{_bindir}/ocamlobjinfo'


%description
OCaml is a high-level, strongly-typed, functional and object-oriented
programming language from the ML family of languages.

This package comprises two batch compilers (a fast bytecode compiler
and an optimizing native-code compiler), an interactive toplevel system,
parsing tools (Lex,Yacc,Camlp4), a replay debugger, a documentation generator,
and a comprehensive library.


%package runtime
Summary:        OCaml runtime environment
Requires:       util-linux
Provides:       ocaml(runtime) = %{version}

%description runtime
OCaml is a high-level, strongly-typed, functional and object-oriented
programming language from the ML family of languages.

This package contains the runtime environment needed to run OCaml
bytecode.


%package source
Summary:        Source code for OCaml libraries
Requires:       ocaml = %{version}-%{release}

%description source
Source code for OCaml libraries.


%package x11
Summary:        X11 support for OCaml
Requires:       ocaml-runtime = %{version}-%{release}
Requires:       libX11-devel

%description x11
X11 support for OCaml.


%package labltk
Summary:        Tk bindings for OCaml
Requires:       ocaml-runtime = %{version}-%{release}

%description labltk
Labltk is a library for interfacing OCaml with the scripting language
Tcl/Tk.

This package contains the runtime files.


%package labltk-devel
Summary:        Development files for labltk
Requires:       ocaml = %{version}-%{release}
Requires:       %{name}-labltk = %{version}-%{release}
Requires:       libX11-devel
Requires:       tcl-devel
Requires:       tk-devel

%description labltk-devel
Labltk is a library for interfacing OCaml with the scripting language
Tcl/Tk.

This package contains the development files.  It includes the ocaml
browser for code editing and library browsing.


%package camlp4
Summary:        Pre-Processor-Pretty-Printer for OCaml
Requires:       ocaml-runtime = %{version}-%{release}

%description camlp4
Camlp4 is a Pre-Processor-Pretty-Printer for OCaml, parsing a source
file and printing some result on standard output.

This package contains the runtime files.


%package camlp4-devel
Summary:        Pre-Processor-Pretty-Printer for OCaml
Requires:       ocaml = %{version}-%{release}
Requires:       %{name}-camlp4 = %{version}-%{release}

%description camlp4-devel
Camlp4 is a Pre-Processor-Pretty-Printer for OCaml, parsing a source
file and printing some result on standard output.

This package contains the development files.


%package ocamldoc
Summary:        Documentation generator for OCaml.
Requires:       ocaml = %{version}-%{release}
Provides:	ocamldoc

%description ocamldoc
Documentation generator for OCaml.


%package emacs
Summary:        Emacs mode for OCaml
Requires:       ocaml = %{version}-%{release}
Requires:       emacs

%description emacs
Emacs mode for OCaml.


%package docs
Summary:        Documentation for OCaml
Requires:       ocaml = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info


%description docs
OCaml is a high-level, strongly-typed, functional and object-oriented
programming language from the ML family of languages.

This package contains documentation in PDF and HTML format as well as
man pages and info files.


%package compiler-libs
Summary:        Compiler libraries for OCaml
Requires:       ocaml = %{version}-%{release}


%description compiler-libs
OCaml is a high-level, strongly-typed, functional and object-oriented
programming language from the ML family of languages.

This package contains some modules used internally by the OCaml
compilers, useful for the development of some OCaml applications.
Note that this exposes internal details of the OCaml compiler which
may not be portable between versions.


%prep
%setup -q -T -b 0 -n %{name}-%{version}
%setup -q -T -D -a 1 -n %{name}-%{version}
%setup -q -T -D -a 3 -n %{name}-%{version}
cp %{SOURCE2} refman.pdf

git init
git config user.email "noone@example.com"
git config user.name "no one"
git add .
git commit -a -q -m "%{version} baseline"
git am %{patches} </dev/null


%build
# make -jN (N > 1) breaks the build.  Therefore we cannot use
# %{?_smp_mflags} nor MAKEFLAGS.
unset MAKEFLAGS

# For ppc64 we need a larger stack than default to compile some files
# because the stages in the OCaml compiler are not mutually tail
# recursive.
%ifarch ppc64
ulimit -a
ulimit -Hs 65536
ulimit -Ss 65536
%endif

CFLAGS="$RPM_OPT_FLAGS" \
./configure \
    -bindir %{_bindir} \
    -libdir %{_libdir}/ocaml \
    -x11lib %{_libdir} \
    -x11include %{_includedir} \
    -mandir %{_mandir}/man1
make world
%if %{native_compiler}
make opt opt.opt
%endif
make -C emacs ocamltags

# Currently these tools are supplied by Debian, but are expected
# to go upstream at some point.
includes="-nostdlib -I stdlib -I utils -I parsing -I typing -I bytecomp -I asmcomp -I driver -I otherlibs/unix -I otherlibs/str -I otherlibs/dynlink"
boot/ocamlrun ./ocamlc $includes dynlinkaux.cmo ocamlbyteinfo.ml -o ocamlbyteinfo
#cp otherlibs/dynlink/natdynlink.ml .
#boot/ocamlrun ./ocamlopt $includes unix.cmxa str.cmxa natdynlink.ml ocamlplugininfo.ml -o ocamlplugininfo


%install
make install \
     BINDIR=$RPM_BUILD_ROOT%{_bindir} \
     LIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml \
     MANDIR=$RPM_BUILD_ROOT%{_mandir}
perl -pi -e "s|^$RPM_BUILD_ROOT||" $RPM_BUILD_ROOT%{_libdir}/ocaml/ld.conf

(
    # install emacs files
    cd emacs;
    make install \
         BINDIR=$RPM_BUILD_ROOT%{_bindir} \
         EMACSDIR=$RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
    make install-ocamltags BINDIR=$RPM_BUILD_ROOT%{_bindir}
)

(
    # install info files
    mkdir -p $RPM_BUILD_ROOT%{_infodir};
    cd infoman; cp ocaml*.gz $RPM_BUILD_ROOT%{_infodir}
)

echo %{version} > $RPM_BUILD_ROOT%{_libdir}/ocaml/fedora-ocaml-release

# Remove rpaths from stublibs .so files.
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs/*.so

install -m 0755 ocamlbyteinfo $RPM_BUILD_ROOT%{_bindir}
#install -m 0755 ocamlplugininfo $RPM_BUILD_ROOT%{_bindir}
magic_rpm_clean.sh

%post docs
/usr/sbin/install-info \
    --entry="* ocaml: (ocaml).   The OCaml compiler and programming environment" \
    --section="Programming Languages" \
    %{_infodir}/%{name}.info \
    %{_infodir}/dir 2>/dev/null || :


%preun docs
if [ $1 -eq 0 ]; then
  /usr/sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir 2>/dev/null || :
fi


%files
%{_bindir}/ocaml
%{_bindir}/ocamlbyteinfo
%{_bindir}/ocamlbuild
%{_bindir}/ocamlbuild.byte
%if %{native_compiler}
%{_bindir}/ocamlbuild.native
%endif
%{_bindir}/ocamlc
%if %{native_compiler}
%{_bindir}/ocamlc.opt
%endif
%{_bindir}/ocamlcp
%{_bindir}/ocamldebug
%{_bindir}/ocamldep
%if %{native_compiler}
%{_bindir}/ocamldep.opt
%endif
%{_bindir}/ocamllex
%if %{native_compiler}
%{_bindir}/ocamllex.opt
%endif
%{_bindir}/ocamlmklib
%{_bindir}/ocamlmktop
%{_bindir}/ocamlobjinfo
%if %{native_compiler}
%{_bindir}/ocamlopt
%{_bindir}/ocamlopt.opt
%{_bindir}/ocamloptp
%endif
#%{_bindir}/ocamlplugininfo
%{_bindir}/ocamlprof
%{_bindir}/ocamlyacc
#%{_libdir}/ocaml/addlabels
#%{_libdir}/ocaml/scrapelabels
%{_libdir}/ocaml/camlheader
%{_libdir}/ocaml/camlheader_ur
%{_libdir}/ocaml/expunge
%{_libdir}/ocaml/extract_crc
%{_libdir}/ocaml/ld.conf
%{_libdir}/ocaml/Makefile.config
%{_libdir}/ocaml/*.a
%if %{natdynlink}
%{_libdir}/ocaml/*.cmxs
%endif
%if %{native_compiler}
%{_libdir}/ocaml/*.cmxa
%{_libdir}/ocaml/*.cmx
%{_libdir}/ocaml/*.o
%endif
%{_libdir}/ocaml/*.mli
%{_libdir}/ocaml/libcamlrun_shared.so
%{_libdir}/ocaml/objinfo_helper
%{_libdir}/ocaml/vmthreads/*.mli
%{_libdir}/ocaml/vmthreads/*.a
%if %{native_compiler}
%{_libdir}/ocaml/threads/*.a
%{_libdir}/ocaml/threads/*.cmxa
%{_libdir}/ocaml/threads/*.cmx
%endif
%{_libdir}/ocaml/caml
%{_libdir}/ocaml/ocamlbuild
%exclude %{_libdir}/ocaml/graphicsX11.mli


%files runtime
%{_bindir}/ocamlrun
%dir %{_libdir}/ocaml
%{_libdir}/ocaml/VERSION
%{_libdir}/ocaml/*.cmo
%{_libdir}/ocaml/*.cmi
%{_libdir}/ocaml/*.cma
%{_libdir}/ocaml/stublibs
%dir %{_libdir}/ocaml/vmthreads
%{_libdir}/ocaml/vmthreads/*.cmi
%{_libdir}/ocaml/vmthreads/*.cma
%dir %{_libdir}/ocaml/threads
%{_libdir}/ocaml/threads/*.cmi
%{_libdir}/ocaml/threads/*.cma
%{_libdir}/ocaml/fedora-ocaml-release
%exclude %{_libdir}/ocaml/graphicsX11.cmi
%exclude %{_libdir}/ocaml/stublibs/dlllabltk.so
#%exclude %{_libdir}/ocaml/stublibs/dlltkanim.so
%doc README LICENSE Changes


%files source
%{_libdir}/ocaml/*.ml


%files x11
%{_libdir}/ocaml/graphicsX11.cmi
%{_libdir}/ocaml/graphicsX11.mli


%files labltk
%{_bindir}/labltk
%dir %{_libdir}/ocaml/labltk
%{_libdir}/ocaml/labltk/*.cmi
%{_libdir}/ocaml/labltk/*.cma
%{_libdir}/ocaml/labltk/*.cmo
%{_libdir}/ocaml/stublibs/dlllabltk.so
#%{_libdir}/ocaml/stublibs/dlltkanim.so


%files labltk-devel
%{_bindir}/ocamlbrowser
%{_libdir}/ocaml/labltk/labltktop
%{_libdir}/ocaml/labltk/pp
%{_libdir}/ocaml/labltk/tkcompiler
%{_libdir}/ocaml/labltk/*.a
%if %{native_compiler}
%{_libdir}/ocaml/labltk/*.cmxa
%{_libdir}/ocaml/labltk/*.cmx
%{_libdir}/ocaml/labltk/*.o
%endif
%{_libdir}/ocaml/labltk/*.mli
%doc otherlibs/labltk/examples_labltk
%doc otherlibs/labltk/examples_camltk


%files camlp4
%dir %{_libdir}/ocaml/camlp4
%{_libdir}/ocaml/camlp4/*.cmi
%{_libdir}/ocaml/camlp4/*.cma
%{_libdir}/ocaml/camlp4/*.cmo
%dir %{_libdir}/ocaml/camlp4/Camlp4Filters
%{_libdir}/ocaml/camlp4/Camlp4Filters/*.cmi
%{_libdir}/ocaml/camlp4/Camlp4Filters/*.cmo
%dir %{_libdir}/ocaml/camlp4/Camlp4Parsers
%{_libdir}/ocaml/camlp4/Camlp4Parsers/*.cmo
%{_libdir}/ocaml/camlp4/Camlp4Parsers/*.cmi
%dir %{_libdir}/ocaml/camlp4/Camlp4Printers
%{_libdir}/ocaml/camlp4/Camlp4Printers/*.cmi
%{_libdir}/ocaml/camlp4/Camlp4Printers/*.cmo
%dir %{_libdir}/ocaml/camlp4/Camlp4Top
%{_libdir}/ocaml/camlp4/Camlp4Top/*.cmi
%{_libdir}/ocaml/camlp4/Camlp4Top/*.cmo


%files camlp4-devel
%{_bindir}/camlp4*
%{_bindir}/mkcamlp4
%if %{native_compiler}
%{_libdir}/ocaml/camlp4/*.a
%{_libdir}/ocaml/camlp4/*.cmxa
%{_libdir}/ocaml/camlp4/*.cmx
%{_libdir}/ocaml/camlp4/*.o
%{_libdir}/ocaml/camlp4/Camlp4Filters/*.cmx
%{_libdir}/ocaml/camlp4/Camlp4Filters/*.o
%{_libdir}/ocaml/camlp4/Camlp4Parsers/*.cmx
%{_libdir}/ocaml/camlp4/Camlp4Parsers/*.o
%{_libdir}/ocaml/camlp4/Camlp4Printers/*.cmx
%{_libdir}/ocaml/camlp4/Camlp4Printers/*.o
%{_libdir}/ocaml/camlp4/Camlp4Top/*.cmx
%{_libdir}/ocaml/camlp4/Camlp4Top/*.o
%endif
%{_mandir}/man1/*


%files ocamldoc
%{_bindir}/ocamldoc*
%{_libdir}/ocaml/ocamldoc
%doc ocamldoc/Changes.txt


%files docs
%doc refman.pdf htmlman
%{_infodir}/*
%if %{native_compiler}
%{_mandir}/man3/*
%endif


%files emacs
%{_datadir}/emacs/site-lisp/*
%{_bindir}/ocamltags
%doc emacs/README


%files compiler-libs
%dir %{_libdir}/ocaml/compiler-libs
%{_libdir}/ocaml/compiler-libs/*.cmi
%{_libdir}/ocaml/compiler-libs/*.cmo
%{_libdir}/ocaml/compiler-libs/*.cma
%if %{native_compiler}
%{_libdir}/ocaml/compiler-libs/*.a
%{_libdir}/ocaml/compiler-libs/*.cmxa
%{_libdir}/ocaml/compiler-libs/*.cmx
%{_libdir}/ocaml/compiler-libs/*.o
%endif


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 4.00.1-2
- 为 Magic 3.0 重建

* Tue Oct 16 2012 Richard W.M. Jones <rjones@redhat.com> - 4.00.1-1
- Update to upstream version 4.00.1.
- Clean up the spec file further.

* Thu Aug 16 2012 Richard W.M. Jones <rjones@redhat.com> - 4.00.0-2
- ppc supports natdynlink.

* Sat Jul 28 2012 Richard W.M. Jones <rjones@redhat.com> - 4.00.0-1
- Upgrade to OCaml 4.00.0 official release.
- Remove one patch (add -lpthread) which went upstream.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.00.0-0.6.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 4.00.0-0.5.beta2
- No change, just fix up changelog.

* Thu Jun  7 2012 Richard W.M. Jones <rjones@redhat.com> 4.00.0-0.3.beta2
- Upgrade to OCaml 4.00.0 beta 2.
- The language is now officially called OCaml (not Objective Caml, O'Caml etc)
- Rebase patches on top:
  . New ARM backend patch no longer required, since upstream.
  . Replacement config.guess, config.sub no longer required, since upstream
    versions are newer.
- PPC64 backend rebased and fixed.
  . Increase the default size of the stack when compiling.
- New tool: ocamloptp (ocamlopt profiler).
- New VERSION file in ocaml-runtime package.
- New ocaml-compiler-libs subpackage.
- Rearrange ExclusiveArch alphanumerically.
- alpha, ia64 native backends have been removed upstream, so they are
  no longer supported as native compiler targets.
- Remove defattr.
- Make OCaml dependency generator self-contained so it doesn't need
  previous version of OCaml around.

* Wed Jun  6 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-12
- ppc64: Include fix for minor heap corruption because of unaligned
  minor heap register (RHBZ#826649).
- Unset MAKEFLAGS before running build.

* Wed Jun  6 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-11
- ppc64: Fix position of stack arguments to external C functions
  when there are more than 8 parameters.

* Tue Jun  5 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-10
- Include patch to link dllthreads.so with -lpthread explicitly, to
  fix problem with 'pthread_atfork' symbol missing (statically linked)
  on ppc64.

* Sun Jun  3 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-9
- Include svn rev 12548 to fix invalid generation of Thumb-2 branch
  instruction TBH (upstream PR#5623, RHBZ#821153).

* Wed May 29 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-8
- Modify the ppc64 patch to reduce the delta between power64 and
  upstream power backends.
- Clean up the spec file and bring it up to modern standards.
  * Remove patch fuzz directive.
  * Remove buildroot directive.
  * Rearrange source unpacking.
  * Remove chmod of GNU config.* files, since git does it.
  * Don't need to remove buildroot in install section.
  * Remove clean section.
  * git am </dev/null to avoid hang (thanks Adam Jackson).
- Note there is no functional change in the above.

* Tue May 29 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-6
- Move patches to external git repo:
  http://git.fedorahosted.org/git/?p=fedora-ocaml.git
  There should be no change introduced here.

* Tue May 15 2012 Karsten Hopp <karsten@redhat.com> 3.12.1-4
- ppc64 got broken by the new ARM backend, add a minor patch

* Sat Apr 28 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-3
- New ARM backend by Benedikt Meurer, backported to OCaml 3.12.1.
  This has several advantages, including enabling natdynlink on ARM.
- Provide updated config.guess and config.sub (from OCaml upstream tree).

* Thu Jan 12 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-2
- add back ocaml-ppc64.patch for ppc secondary arch, drop .cmxs files
  from file list on ppc (cherry picked from F16 - this should have
  gone into Rawhide originally then been cherry picked back to F16)

* Fri Jan  6 2012 Richard W.M. Jones <rjones@redhat.com> - 3.12.1-1
- New upstream version 3.12.1.  This is a bugfix update.

* Thu Dec  8 2011 Richard W.M. Jones <rjones@redhat.com> - 3.12.0-7
- Allow this package to be compiled on platforms without native
  support and/or natdynlink, specifically ppc64.  This updates (and
  hopefully does not break) DJ's previous *.cmxs change for arm.

* Fri Sep 23 2011 DJ Delorie <dj@redhat.com> - 3.12.0-6
- Add arm type directive patch.
- Allow more arm arches.
- Don't package *.cmxs on arm.

* Wed Mar 30 2011 Richard W.M. Jones <rjones@redhat.com> - 3.12.0-5
- Fix for invalid assembler generation (RHBZ#691896).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 3.12.0-3
- Rebuild with self.

* Tue Jan  4 2011 Richard W.M. Jones <rjones@redhat.com> - 3.12.0-2
- Try depending on OCaml BR to fix:
  /usr/lib/rpm/ocaml-find-provides.sh: /builddir/build/BUILDROOT/ocaml-3.12.0-1.fc15.i386/usr/bin/ocamlobjinfo: /usr/bin/ocamlrun: bad interpreter: No such file or directory

* Tue Jan  4 2011 Richard W.M. Jones <rjones@redhat.com> - 3.12.0-1
- New upstream version 3.12.0.
  http://fedoraproject.org/wiki/Features/OCaml3.12
- Remove ppc64 support patch.
- Rebase rpath removal patch.
- ocamlobjinfo is now an official tool, so no need to compile it by hand.
  Add objinfo_helper.
- Disable ocamlplugininfo.
- Remove addlabels, scrapelabels.
- Remove ocaml/stublibs/dlltkanim.so.

* Fri Jan 29 2010 Richard W.M. Jones <rjones@redhat.com> - 3.11.2-2
- Update reference manual to latest version from website.

* Wed Jan 20 2010 Richard W.M. Jones <rjones@redhat.com> - 3.11.2-1
- Update to 3.11.2 official release.

* Tue Jan  5 2010 Richard W.M. Jones <rjones@redhat.com> - 3.11.2-0.rc1.2
- ocaml-labltk-devel should require tcl-devel and tk-devel.

* Tue Dec 29 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.2-0.rc1.1
- Update to (release candidate) 3.11.2+rc1.

* Wed Dec 16 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-8
- Use __ocaml_requires_opts / __ocaml_provides_opts.

* Wed Dec 16 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-7
- Remove ocaml-find-{requires,provides}.sh from this package.  These are
  now in upstream RPM 4.8 (RHBZ#545116).
- define -> global in a few places.

* Thu Nov 05 2009 Dennis Gilmore <dennis@ausil.us> - 3.11.1-6
- include sparcv9 in the arch list

* Tue Oct 27 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-5
- Install ocaml.info files correctly (RHBZ#531204).

* Fri Oct 16 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-4
- Set includes so building the *info programs works without
  having OCaml already installed.

* Fri Oct 16 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-3
- Add ocamlbyteinfo and ocamlplugininfo programs from Debian.

* Sun Oct  4 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-2
- ocaml-find-requires.sh: Calculate runtime version using ocamlrun
  -version instead of fedora-ocaml-release file.

* Wed Sep 30 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-1
- OCaml 3.11.1 (this is virtually the same as the release candidate
  that we were using for Fedora 12).

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.1-0.rc1.2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun  3 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-0.rc1.2
- Remember to upload the source this time.

* Wed Jun  3 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-0.rc1.1
- New upstream release candidate 3.11.1+rc1.
- Remove ocamlbuild -where patch (now upstream).

* Tue Jun  2 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-0.rc0.3
- Move dllgraphics.so into runtime package (RHBZ#468506).

* Tue May 26 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-0.rc0.2
- Backport ocamlbuild -where fix.

* Fri May 22 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-0.rc0.1
- 3.11.1 release candidate 0.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0-1
- Official release of 3.11.0.

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0-0.6.rc1
- Fixed sources file.

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0-0.5.rc1
- New upstream version 3.11.0+rc1.

* Mon Nov 24 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0-0.4.beta1
- Rebuild.

* Thu Nov 20 2008 Rex Dieter <rdieter@fedoraproject.org> - 3.11.0-0.3.beta1
- fix NVR to match packaging guidelines

* Thu Nov 20 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0+beta1-2
- Fix Invalid_argument("String.index_from") with patch from upstream.

* Tue Nov 18 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0+beta1-1
- Rebuild for major new upstream release of 3.11.0 for Fedora 11.

* Thu Aug 29 2008 Richard W.M. Jones <rjones@redhat.com> - 3.10.2-5
- Rebuild with patch fuzz.

* Mon Jun  9 2008 Richard W.M. Jones <rjones@redhat.com> - 3.10.2-4
- Add ocaml-3.11-dev12-no-executable-stack.patch (bz #450551).

* Wed Jun  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3.10.2-3
- ocaml-ocamldoc provides ocamldoc (bz #449931).
- REMOVED provides of labltk, camlp4.  Those are libraries and all
  packages should now depend on ocaml-labltk / ocaml-camlp4 / -devel
  as appropriate.

* Thu May  8 2008 Richard W.M. Jones <rjones@redhat.com> - 3.10.2-2
- Pass MAP_32BIT to mmap (bz #445545).

* Mon Apr 21 2008 Richard W.M. Jones <rjones@redhat.com> - 3.10.2-1
- New upstream version 3.10.2 for Fedora 10.
- Cleaned up several rpmlint errors & warnings.

* Fri Feb 29 2008 David Woodhouse <dwmw2@infradead.org> - 3.10.1-2
- ppc64 port

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 3.10.1-1
- new upstream version 3.10.1

* Fri Jan  4 2008 Gerard Milmeister <gemi@bluewin.ch> - 3.10.0-8
- patch for building with tcl/tk 8.5

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 3.10.0-7
- Run chrpath to delete rpaths used on some of the stublibs.
- Ignore Parsetree module in dependency calculation.
- Fixed ocaml-find-{requires,provides}.sh regexp calculation so it doesn't
  over-match module names.

* Mon Sep  3 2007 Richard W.M. Jones <rjones@redhat.com> - 3.10.0-6
- ocaml-runtime provides ocaml(runtime) = 3.10.0, and
  ocaml-find-requires.sh modified so that it adds this requires
  to other packages.  Now can upgrade base ocaml packages without
  needing to rebuild everything else.

* Mon Sep  3 2007 Richard W.M. Jones <rjones@redhat.com> - 3.10.0-5
- Don't include the release number in fedora-ocaml-release file, so
  that packages built against this won't depend on the Fedora release.

* Wed Aug 29 2007 Gerard Milmeister <gemi@bluewin.ch> - 3.10.0-4
- added BR util-linux-ng

* Wed Aug 29 2007 Gerard Milmeister <gemi@bluewin.ch> - 3.10.0-3
- added BR gawk

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 3.10.0-2
- Rebuild for selinux ppc32 issue.

* Sat Jun  2 2007 Gerard Milmeister <gemi@bluewin.ch> - 3.10.0-1
- new version 3.10.0
- split off devel packages
- rename subpackages to use ocaml- prefix

* Thu May 24 2007 Gerard Milmeister <gemi@bluewin.ch> - 3.09.3-2
- added ocamlobjinfo

* Sat Dec  2 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.3-1
- new version 3.09.3

* Mon Aug 28 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.2-2
- Rebuild for FE6

* Sun Apr 30 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.2-1
- new version 3.09.2

* Fri Feb 17 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.1-2
- Rebuild for Fedora Extras 5

* Thu Jan  5 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.1-1
- new version 3.09.1

* Sun Jan  1 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.0-1
- new version 3.09.0

* Sun Sep 11 2005 Gerard Milmeister <gemi@bluewin.ch> - 3.08.4-1
- New Version 3.08.4

* Wed May 25 2005 Toshio Kuratomi <toshio-tiki-lounge.com> - 3.08.3-5
- Bump and re-release as last build failed due to rawhide syncing.

* Sun May 22 2005 Toshio Kuratomi <toshio-tiki-lounge.com> - 3.08.3-4
- Fix for gcc4 and the 32 bit assembly in otherlibs/num.
- Fix to allow compilation with RPM_OPT_FLAG defined -O level.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 3.08.3-3
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Mar 26 2005 Gerard Milmeister <gemi@bluewin.ch> - 3.08.3-1
- New Version 3.08.3

* Sat Feb 12 2005 Gerard Milmeister <gemi@bluewin.ch> - 0:3.08.2-2
- Added patch for removing rpath from shared libs

* Sat Feb 12 2005 Gerard Milmeister <gemi@bluewin.ch> - 0:3.08.2-1
- New Version 3.08.2

* Thu Dec 30 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:3.07-6
- add -x11lib _prefix/X11R6/_lib to configure; fixes labltk build
  on x86_64

* Tue Dec  2 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:3.07-0.fdr.5
- ocamldoc -> ocaml-ocamldoc
- ocaml-doc -> ocaml-docs

* Fri Nov 28 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:3.07-0.fdr.4
- Make separate packages for labltk, camlp4, ocamldoc, emacs and documentation

* Thu Nov 27 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:3.07-0.fdr.2
- Changed license tag
- Register info files
- Honor RPM_OPT_FLAGS
- New Patch

* Fri Oct 31 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:3.07-0.fdr.1
- First Fedora release

* Mon Oct 13 2003 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Updated to 3.07.

* Wed Apr  9 2003 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Rebuilt for Red Hat 9.

* Tue Nov 26 2002 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Added _mandir/mano/* entry

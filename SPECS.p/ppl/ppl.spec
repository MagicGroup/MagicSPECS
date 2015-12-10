Name:			ppl
Version:		1.1
Release:		14%{?dist}
Summary:		The Parma Polyhedra Library: a library of numerical abstractions
Group:			Development/Libraries
License:		GPLv3+
URL:			http://www.cs.unipr.it/ppl/
Source0:		ftp://ftp.cs.unipr.it/pub/ppl/releases/%{version}/%{name}-%{version}.tar.bz2
Source1:		ppl.hh
Source2:		ppl_c.h
Requires(post):		/sbin/ldconfig
Requires(postun):	/sbin/ldconfig
# Merged into ppl as of 0.12
Provides:		ppl-pwl = %{version}-%{release}
Obsoletes:		ppl-pwl <= 0.11.2-11
BuildRequires:		gmp-devel >= 4.1.3, m4 >= 1.4.8
Patch0:			%{name}-cstddef.patch
Patch1:			%{name}-PlLong.patch
Patch2:			%{name}-gcc5.patch
Patch3:			%{name}-swiprolog.patch

%description
The Parma Polyhedra Library (PPL) is a library for the manipulation of
(not necessarily closed) convex polyhedra and other numerical
abstractions.  The applications of convex polyhedra include program
analysis, optimized compilation, integer and combinatorial
optimization and statistical data-editing.  The Parma Polyhedra
Library comes with several user friendly interfaces, is fully dynamic
(available virtual memory is the only limitation to the dimension of
anything), written in accordance to all the applicable standards,
exception-safe, rather efficient, thoroughly documented, and free
software.  This package provides all what is necessary to run
applications using the PPL through its C and C++ interfaces.

%package devel
Summary:	Development tools for the Parma Polyhedra Library C and C++ interfaces
Requires:	%{name}%{?_isa} = %{version}-%{release}, gmp-devel%{?_isa} >= 4.1.3
# Merged into ppl as of 0.12
Provides:	ppl-pwl-devel = %{version}-%{release}
Obsoletes:	ppl-pwl-devel <= 0.11.2-11

%description devel
The header files, Autoconf macro and minimal documentation for
developing applications using the Parma Polyhedra Library through
its C and C++ interfaces.

%package static
Summary:	Static archives for the Parma Polyhedra Library C and C++ interfaces
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
# Merged into ppl as of 0.12
Provides:	ppl-pwl-static = %{version}-%{release}
Obsoletes:	ppl-pwl-static <= 0.11.2-11

%description static
The static archives for the Parma Polyhedra Library C and C++ interfaces.

%package utils
Summary:	Utilities using the Parma Polyhedra Library
Requires:	%{name}%{?_isa} = %{version}-%{release}
BuildRequires:	glpk-devel >= 4.13

%description utils
This package contains the mixed integer linear programming solver ppl_lpsol.
the program ppl_lcdd for vertex/facet enumeration of convex polyhedra,
and the parametric integer programming solver ppl_pips.

# This is the explicit list of arches gprolog supports
%ifarch x86_64 %{ix86} ppc alpha
%package gprolog
# The `gprolog' package is not available on ppc64:
# the GNU Prolog interface must thus be disabled for that architecture.
Summary:	The GNU Prolog interface of the Parma Polyhedra Library
BuildRequires:	gprolog >= 1.2.19
Requires:	%{name}%{?_isa} = %{version}-%{release}, gprolog%{?_isa} >= 1.2.19

%description gprolog
This package adds GNU Prolog support to the Parma Polyhedra Library (PPL).
Install this package if you want to use the library in GNU Prolog programs.
%endif

# This is the explicit list of arches gprolog supports
%ifarch x86_64 %{ix86} ppc alpha
%package gprolog-static
Summary:	The static archive for the GNU Prolog interface of the Parma Polyhedra Library
Requires:	%{name}-gprolog%{?_isa} = %{version}-%{release}

%description gprolog-static
This package contains the static archive for the GNU Prolog interface
of the Parma Polyhedra Library.
%endif

%package swiprolog
Summary:	The SWI-Prolog interface of the Parma Polyhedra Library
BuildRequires:	pl >= 5.10.2-3, pl-devel >= 5.10.2-3
Requires:	%{name}%{?_isa} = %{version}-%{release}, pl%{?_isa} >= 5.10.2-3

%description swiprolog
This package adds SWI-Prolog support to the Parma Polyhedra Library.
Install this package if you want to use the library in SWI-Prolog programs.

%package swiprolog-static
Summary:	The static archive for the SWI-Prolog interface of the Parma Polyhedra Library
BuildRequires:	pl >= 5.10.2-3, pl-devel >= 5.10.2-3, pl-static >= 5.10.2-3
Requires:	%{name}-swiprolog%{?_isa} = %{version}-%{release}

%description swiprolog-static
This package contains the static archive for the SWI-Prolog interface
of the Parma Polyhedra Library.

%ifnarch sparc64 sparcv9 %{arm} ppc %{power64}
%package yap
Summary:	The YAP Prolog interface of the Parma Polyhedra Library
BuildRequires:	yap-devel >= 5.1.1
Requires:	%{name}%{?_isa} = %{version}-%{release}, yap%{?_isa} >= 5.1.1
Obsoletes:	ppl-yap-static

%description yap
This package adds YAP Prolog support to the Parma Polyhedra Library (PPL).
Install this package if you want to use the library in YAP Prolog programs.
%endif

%package java
Summary:	The Java interface of the Parma Polyhedra Library
BuildRequires:	java-devel >= 1:1.6.0
Requires:	java-headless >= 1:1.6.0
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description java
This package adds Java support to the Parma Polyhedra Library.
Install this package if you want to use the library in Java programs.

%package java-javadoc
Summary:	Javadocs for %{name}-java
Requires:	%{name}-java%{?_isa} = %{version}-%{release}

%description java-javadoc
This package contains the API documentation for Java interface
of the Parma Polyhedra Library.

%package docs
Summary:	Documentation for the Parma Polyhedra Library
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description docs
This package contains all the documentations required by programmers
using the Parma Polyhedra Library (PPL).
Install this package if you want to program with the PPL.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPPFLAGS="-I%{_includedir}/glpk"
# This is the explicit list of arches gprolog supports
%ifarch x86_64 %{ix86} ppc alpha
CPPFLAGS="$CPPFLAGS -I%{_libdir}/gprolog-`gprolog --version 2>&1 | head -1 | sed -e "s/.* \([^ ]*\)$/\1/g"`/include"
%endif
%ifnarch sparc64 sparcv9 %{arm} ppc %{power64}
CPPFLAGS="$CPPFLAGS -I`swipl -dump-runtime-variables | grep PLBASE= | sed 's/PLBASE="\(.*\)";/\1/'`/include"
CPPFLAGS="$CPPFLAGS -I%{_includedir}/Yap"
%endif
%configure --docdir=%{_datadir}/doc/%{name} --enable-shared --disable-rpath --enable-interfaces="c++ c gnu_prolog swi_prolog yap_prolog java" CPPFLAGS="$CPPFLAGS"
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} INSTALL="%{__install} -p" install
rm -f %{buildroot}%{_libdir}/*.la %{buildroot}%{_libdir}/%{name}/*.la

# In order to avoid multiarch conflicts when installed for multiple
# architectures (e.g., i386 and x86_64), we rename the header files
# of the ppl-devel package.  They are substituted with ad-hoc 
# switchers that select the appropriate header file depending on
# the architecture for which the compiler is compiling.

# Since our header files only depend on the sizeof things, we smash
# ix86 onto i386 and arm* onto arm.  For the SuperH RISC engine family,
# we smash sh3 and sh4 onto sh.
normalized_arch=%{_arch}
%ifarch %{ix86}
normalized_arch=i386
%endif
%ifarch %{arm}
normalized_arch=arm
%endif
%ifarch sh3 sh4
normalized_arch=sh
%endif

mv %{buildroot}/%{_includedir}/ppl.hh %{buildroot}/%{_includedir}/ppl-${normalized_arch}.hh
install -m644 %{SOURCE1} %{buildroot}/%{_includedir}/ppl.hh
mv %{buildroot}/%{_includedir}/ppl_c.h %{buildroot}/%{_includedir}/ppl_c-${normalized_arch}.h
install -m644 %{SOURCE2} %{buildroot}/%{_includedir}/ppl_c.h

# Install the Javadocs for ppl-java.
mkdir -p %{buildroot}%{_javadocdir}
mv \
%{buildroot}/%{_datadir}/doc/%{name}/ppl-user-java-interface-%{version}-html \
%{buildroot}%{_javadocdir}/%{name}-java

%files
%doc %{_datadir}/doc/%{name}/BUGS
%doc %{_datadir}/doc/%{name}/COPYING
%doc %{_datadir}/doc/%{name}/CREDITS
%doc %{_datadir}/doc/%{name}/NEWS
%doc %{_datadir}/doc/%{name}/README
%doc %{_datadir}/doc/%{name}/README.configure
%doc %{_datadir}/doc/%{name}/TODO
%doc %{_datadir}/doc/%{name}/gpl.txt
%{_libdir}/libppl.so.*
%{_libdir}/libppl_c.so.*
%{_bindir}/ppl-config
%{_mandir}/man1/ppl-config.1.gz
%dir %{_libdir}/%{name}
%dir %{_datadir}/doc/%{name}
%dir %{_datadir}/ppl/

%files devel
%{_includedir}/ppl*.hh
%{_includedir}/ppl_c*.h
%{_libdir}/libppl.so
%{_libdir}/libppl_c.so
%{_mandir}/man3/libppl.3.gz
%{_mandir}/man3/libppl_c.3.gz
%{_datadir}/aclocal/ppl.m4
%{_datadir}/aclocal/ppl_c.m4

%files static
%{_libdir}/libppl.a
%{_libdir}/libppl_c.a

%files utils
%{_bindir}/ppl_lcdd
%{_bindir}/ppl_lpsol
%{_bindir}/ppl_pips
%{_mandir}/man1/ppl_lcdd.1.gz
%{_mandir}/man1/ppl_lpsol.1.gz
%{_mandir}/man1/ppl_pips.1.gz

%ifarch x86_64 %{ix86} ppc alpha
%files gprolog
%doc interfaces/Prolog/GNU/README.gprolog
%{_bindir}/ppl_gprolog
%{_datadir}/ppl/ppl_gprolog.pl
%{_libdir}/%{name}/libppl_gprolog.so
%endif

# This is the explicit list of arches gprolog supports
%ifarch x86_64 %{ix86} ppc alpha
%files gprolog-static
%{_libdir}/%{name}/libppl_gprolog.a
%endif

%files swiprolog
%doc interfaces/Prolog/SWI/README.swiprolog
# No longer installed on shared builds
# %{_bindir}/ppl_pl
%{_libdir}/%{name}/libppl_swiprolog.so
%{_datadir}/%{name}/ppl_swiprolog.pl

%files swiprolog-static
%{_libdir}/%{name}/libppl_swiprolog.a

%ifnarch sparc64 sparcv9 %{arm} ppc %{power64}
%files yap
%doc interfaces/Prolog/YAP/README.yap
%{_datadir}/%{name}/ppl_yap.pl
%{_libdir}/%{name}/ppl_yap.so
%endif

%files java
%doc interfaces/Java/README.java
%{_libdir}/%{name}/libppl_java.so
%{_libdir}/%{name}/ppl_java.jar

%files java-javadoc
%{_javadocdir}/%{name}-java

%files docs
%doc %{_datadir}/doc/%{name}/ChangeLog*
%doc %{_datadir}/doc/%{name}/README.doc
%doc %{_datadir}/doc/%{name}/fdl.*
%doc %{_datadir}/doc/%{name}/gpl.pdf
%doc %{_datadir}/doc/%{name}/gpl.ps.gz
%doc %{_datadir}/doc/%{name}/ppl-user-%{version}-html/
%doc %{_datadir}/doc/%{name}/ppl-user-c-interface-%{version}-html/
%doc %{_datadir}/doc/%{name}/ppl-user-prolog-interface-%{version}-html/
%doc %{_datadir}/doc/%{name}/ppl-user-%{version}.pdf
%doc %{_datadir}/doc/%{name}/ppl-user-c-interface-%{version}.pdf
%doc %{_datadir}/doc/%{name}/ppl-user-java-interface-%{version}.pdf
%doc %{_datadir}/doc/%{name}/ppl-user-prolog-interface-%{version}.pdf
%doc %{_datadir}/doc/%{name}/ppl-user-%{version}.ps.gz
%doc %{_datadir}/doc/%{name}/ppl-user-c-interface-%{version}.ps.gz
%doc %{_datadir}/doc/%{name}/ppl-user-java-interface-%{version}.ps.gz
%doc %{_datadir}/doc/%{name}/ppl-user-prolog-interface-%{version}.ps.gz

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.1-14
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.1-13
- 为 Magic 3.0 重建

* Sun Aug 02 2015 Liu Di <liudidi@gmail.com> - 1.1-12
- 为 Magic 3.0 重建

* Tue Jun 30 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.1-11
- Rebuild with newer pl
- Remove jpackage-utils dependency

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 14 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.1-9
- Rebuild with newer pl

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.1-8
- Rebuilt for GCC 5 C++11 ABI change

* Sun Feb  8 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.1-7
- Correct build with gcc 5.0.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 22 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.1-5
- fix FTBFS on aarch64

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Brent Baude <baude@us.ibm.com> - 1.1-3
- Fixing include detection for ppc64 and ppc64le

* Thu May 22 2014 Brent Baude <baude@us.ibm.com> - 1.1-2
- Replace ppc64 arch with power64 macro

* Tue Apr 29 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.1-1
- Update to latest upstream release
- Remove patches added upstream
- Add new cstddef patch to build recent gcc
- Correct bogus dates in chagelog
- Remove hack with explicit provides of (wrong) library major

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.0-5.10
- Use Requires: java-headless rebuild (#1067528)

* Thu Mar 13 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.0-4.10
- Rebuild with newer pl

* Fri Dec 27 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.0-4.9
- Rebuild with newer pl

* Fri Dec  6 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.0-4.8
- Rebuild with newer pl

* Thu Sep  5 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.0-4.7
- Rebuild with newer pl

* Tue Aug  6 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.0-4.6
- Rebuild with newer glpk
- Adapt to unversioned docdir (#994050)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb  7 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.0-3.5
- The gmp patch itself is conditional, no need to conditionally apply
- Correct jpackage-utils requires as it is noarch
- Correct java requires as the virtual provides in noarch
- Rebuild for newer swiprolog and glpk (#907477, #905420)

* Wed Jan 30 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.0-3.4
- Correct problem with gmp 5.1.0 or newer (#905420)

* Wed Dec 26 2012 Kevin Fenzi <kevin@scrye.com> 1.0-3.3
- Rebuild for new libswipl

* Wed Dec  5 2012 Dan Horák <dan[at]danny.cz> - 1.0-3.2
- fix the hack for all 64-bit platforms

* Tue Dec  4 2012 Tom Callaway <spot@fedoraproject.org> - 1.0-3.1
- bring ugly hack back long enough to rebuild mingw

* Mon Dec  3 2012 Tom Callaway <spot@fedoraproject.org> - 1.0-3
- undo ugly hack

* Mon Dec  3 2012 Tom Callaway <spot@fedoraproject.org> - 1.0-2
- ignore this ugly hack, it is going away asap

* Fri Nov 30 2012 Tom Callaway <spot@fedoraproject.org> - 1.0-1
- update to 1.0
- spec cleanup

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.11.2-9
- Explicitly include supported gprolog arches

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.2-8
- Rebuilt for c++ ABI breakage

* Thu Feb 23 2012 Karsten Hopp <karsten@redhat.com> 0.11.2-7
- don't require yap on ppc and ppc64, it is broken there: bz 790625

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 23 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.11.2-5
- Own doc dir in -pwl.

* Tue Nov 01 2011 Kevin Fenzi <kevin@scrye.com> - 0.11.2-4
- Rebuild for new gmp

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.2-3.2
- Rebuilt for glibc bug#747377

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.11.2-2.2
- rebuild with new gmp without compat lib

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 0.11.2-2.1
- rebuild with new gmp

* Tue May 31 2011 Peter Robinson <pbrobinson@gmail.com> - 0.11.2-2
- Merge 15 Branch to master as its newer
- Add ARM to platform excludes

* Mon Feb 28 2011 Roberto Bagnara <bagnara@cs.unipr.it> - 0.11.2-1
- Updated for PPL 0.11.2.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 11 2009 Caolán McNamara <caolanm@redhat.com> - 0.10.2-10
- Resolves: rhbz#521588 stick pl include before Yap include to stop 
  configure-time misdetection to resolve FTBFS

* Wed Aug 19 2009 Roberto Bagnara <bagnara@cs.unipr.it> - 0.10.2-9
- Force rebuild.

* Fri Aug 14 2009 Roberto Bagnara <bagnara@cs.unipr.it> - 0.10.2-8
- Force rebuild.

* Fri Aug 14 2009 Roberto Bagnara <bagnara@cs.unipr.it> - 0.10.2-7
- Force rebuild.

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.10.2-6
- Use bzipped upstream tarball.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Roberto Bagnara <bagnara@cs.unipr.it> 0.10.2-4
- Force rebuild.

* Fri Jun 19 2009 Roberto Bagnara <bagnara@cs.unipr.it> 0.10.2-3
- The `gprolog' and `yap' packages are not available on the sparc64 and
  sparcv9 architectures: so do `ppl-gprolog', `ppl-gprolog-static' and
  `ppl-yap'.

* Sat Apr 18 2009 Roberto Bagnara <bagnara@cs.unipr.it> 0.10.2-2
- Force rebuild.

* Sat Apr 18 2009 Roberto Bagnara <bagnara@cs.unipr.it> 0.10.2-1
- Updated for PPL 0.10.2.

* Tue Apr 14 2009 Roberto Bagnara <bagnara@cs.unipr.it> 0.10.1-1
- Updated for PPL 0.10.1.

* Sun Mar 29 2009 Roberto Bagnara <bagnara@cs.unipr.it> 0.10-11
- Moved changelogs and PostScript and PDF versions of the GPL to the
  `docs' subpackages. This saves considerable space on the live media.

* Tue Mar 24 2009 Roberto Bagnara <bagnara@cs.unipr.it> 0.10-10
- There are no GNU Prolog packages available on ia64: disable the GNU Prolog
  interface also on those platforms (besides ppc64, s390 and s390x).

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild.

* Wed Feb 18 2009 Roberto Bagnara <bagnara@cs.unipr.it> 0.10-8
- Install the documentation according to the Fedora packaging conventions.

* Tue Feb 17 2009 Karsten Hopp <karsten@redhat.comt> 0.10-7
- There are no GNU Prolog packages available on s390 and s390x: disable
  the GNU Prolog interface also on those platforms (besides ppc64).

* Wed Feb 04 2009 Roberto Bagnara <bagnara@cs.unipr.it> 0.10-6
- Better workaround for the bug affecting PPL 0.10 on big-endian
  architectures.

* Tue Feb 03 2009 Roberto Bagnara <bagnara@cs.unipr.it> 0.10-5
- Work around the bug affecting PPL 0.10 on big-endian architectures.

* Fri Dec 05 2008 Roberto Bagnara <bagnara@cs.unipr.it> 0.10-4
- Added `%%dir %%{_datadir}/doc/pwl' to the `%%files' section
  of the `ppl-pwl' package.

* Tue Nov 04 2008 Roberto Bagnara <bagnara@cs.unipr.it> 0.10-3
- Fixed the requirements of the `ppl-java' package.

* Tue Nov 04 2008 Roberto Bagnara <bagnara@cs.unipr.it> 0.10-2
- Added m4 >= 1.4.8 to build requirements.

* Tue Nov 04 2008 Roberto Bagnara <bagnara@cs.unipr.it> 0.10-1
- Updated and extended for PPL 0.10.  In particular, the `ppl-config'
  program, being useful also for non-development activities, has been
  brought back to the main package.

* Tue Sep 30 2008 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-25
- The `swiprolog' package now requires pl >= 5.6.57-2.

* Mon Sep 08 2008 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-24
- Changed ppl-0.9-swiprolog.patch so as to invoke `plld' with
  the `-v' option.

* Mon Sep 08 2008 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-23
- Fixed ppl-0.9-swiprolog.patch.

* Mon Sep 08 2008 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-22
- Implemented a workaround to cope with the new location of SWI-Prolog.h.

* Mon Sep 08 2008 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-21
- Fixed the SWI-Prolog interface dependencies.

* Mon May 19 2008 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-20
- Added Requires /sbin/ldconfig.

* Wed Feb 13 2008 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-19
- Include a patch to supply a missing inclusions of <cstdlib>.

* Wed Jan 09 2008 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-18
- Avoid multiarch conflicts when installed for multiple architectures.

* Sun Dec 23 2007 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-17
- The SWI-Prolog `pl' package is temporarily not available on the ppc64
  architecture: temporarily disabled `ppl-swiprolog' and
  `ppl-swiprolog-static' on that architecture.

* Sat Sep 29 2007 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-16
- The value of the `License' tag is now `GPLv2+'.
- `ppl-swiprolog' dependency on `readline-devel' removed (again).

* Mon Sep 24 2007 Jesse Keating <jkeating@redhat.com> 0.9-15
- Rebuild for new libgmpxx.

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> 0.9-14
- Rebuild for selinux ppc32 issue.

* Fri Jul 06 2007 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-13
- Bug 246815 had been fixed: YAP support enabled again.

* Thu Jul 05 2007 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-12
- Disable YAP support until bug 246815 is fixed.
- Bug 243084 has been fixed: `ppl-swiprolog' dependency on `readline-devel'
  removed.

* Thu Jul 05 2007 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-11
- The `gprolog' package is not available on the ppc64 architecture:
  so do `ppl-gprolog' and `ppl-gprolog-static'.

* Tue Jul 03 2007 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-10
- Use `%%{buildroot}' consistently, instead of  `$RPM_BUILD_ROOT'.

* Mon Jul 02 2007 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-9
- Patch NEWS, TODO and doc/definitions.dox so as to use the
  UTF-8 encoding instead of ISO-8859.

* Tue Jun 12 2007 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-8
- Patch the `libtool' script after `%%configure' so as to fix
  the rpath issue.
- Revised the description of the `devel' package.
- Include also the `TODO' file in the documentation of the main package.

* Thu Jun 07 2007 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-7
- `%%install' commands revised.

* Thu Jun 07 2007 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-6
- All the static archives are now in `*-static' packages.
- Packages `ppl-gprolog-devel', `ppl-swiprolog-devel' and `ppl-yap-devel'
  renamed `ppl-gprolog', `ppl-swiprolog' and `ppl-yap',
  respectively.
- As a workaround for a bug in the `pl' package (Bugzilla Bug 243084),
  `ppl-swiprolog' is now dependent on `readline-devel'.
- Added `%%dir %%{_datadir}/doc/%%{name}'.
- The `ppl-user-0.9-html' documentation directory is now properly listed.
- Remove installed *.la files.
- Added a `ppl-0.9-configure.patch' to avoid overriding CFLAGS and CXXFLAGS.

* Wed Jun 06 2007 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-5
- Use `%%{_includedir}' and `%%{_libdir}' instead of `/usr/include'
  and `/usr/lib', respectively.
- Use `%%{_datadir}/doc/%%{name}' instead of `/usr/share/doc/ppl'.
- Replaced `%%defattr(-,root,root)' with `%%defattr(-,root,root,-)'.

* Fri Feb 23 2007 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-4
- The user manual (in various formats) is now in the `docs' package.

* Thu Feb 22 2007 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-3
- Dependencies for YAP fixed.
- Make sure the header files of GNU Prolog and YAP are found.

* Wed Feb 21 2007 Roberto Bagnara <bagnara@cs.unipr.it>
- Added missing dependencies.

* Sun Feb 18 2007 Roberto Bagnara <bagnara@cs.unipr.it>
- `%%doc' tags corrected for the Prolog interfaces.
- Tabs used consistently instead of spaces.

* Sat Feb 17 2007 Roberto Bagnara <bagnara@cs.unipr.it>
- Make `swiprolog-devel' depend on `pl' (at leat 5.6); documentation added.
- The `yap' package has been renamed `yap-devel' and completed.
- The `gprolog' package has been renamed `gprolog-devel' and completed.
- The `ppl_lcdd' and `ppl_lpsol' programs are now in a new `utils' package.
- The `ppl-config' program is now in the `devel' package.
- Modified the configuration command so that the `glpk-devel' include files
  are found.

* Sun Feb 11 2007 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-2
- The `%%_libdir/ppl' is no longer orphaned.
- Use `make %%{?_smp_mflags}' for building.
- The `swi' package has been renamed `swiprolog-devel'.

* Sat Feb 10 2007 Roberto Bagnara <bagnara@cs.unipr.it>
- Added the `%%changelog' section.
- `Release' set to 2.
- `Packager' and `Vendor' tags removed.
- `Summary' fields are no longer ended with a dot.
- The value of the `License' tag is now `GPL'.
- Removed unused definition of `builddir'.
- The `Name', `Version' and `Release' tags are now directly defined.
- Commented out the efinitions of the `Require' and `Prefix' tags.
- Set the `BuildRequires' tag to `gmp-devel'.
- Exploit the features of `%%setup', `%%configure', `%%install',
  `%%post' and `%%postun'.
- Mixed use of spaces and tabs avoided.
- Do configure with the --disable-rpath option so as to avoid
  hardcoding the path to search libraries.
- Do not include libtool archive files.
- Packages reorganized.

* Mon Jan 16 2006 Roberto Bagnara <bagnara@cs.unipr.it> 0.9-1
- Install gzipped man pages.
- The `Copyright' tag is no longer supported: use `License' instead.

* Wed Jan 11 2006 Roberto Bagnara <bagnara@cs.unipr.it>
- Include `ppl-config' in `%%{_bindir}' and the man pages in
  `%%{_mandir}/man1'.

* Tue Jan 10 2006 Roberto Bagnara <bagnara@cs.unipr.it>
- Require gcc-c++ to be at least 4.0.2.
- Distribute also `ppl_lpsol'.

* Tue Mar 01 2005 Roberto Bagnara <bagnara@cs.unipr.it>
- Wrong dependency fixed.

* Mon Feb 28 2005 Roberto Bagnara <bagnara@cs.unipr.it>
- URL for the source fixed.

* Fri Dec 24 2004 Roberto Bagnara <bagnara@cs.unipr.it>
- Sentence fixed.

* Thu Dec 23 2004 Roberto Bagnara <bagnara@cs.unipr.it>
- The file doc/README has been renamed README.doc so as not to conflict
  with the library's main README file.
- Require gcc-c++ to be exactly version 3.4.1.
- `Summary' updated to reflect the fact that the library now provides
  numerical abstractions other than convex polyhedra.

* Wed Aug 18 2004 Roberto Bagnara <bagnara@cs.unipr.it>
- Distribute more documentation.

* Mon Aug 16 2004 Roberto Bagnara <bagnara@cs.unipr.it>
- Added the `ppl_lcdd' program to the main package.
- Require gcc-c++ to be exactly version 3.4.1.
- We require gmp at least 4.1.3.

* Wed Jul 30 2003 Roberto Bagnara <bagnara@cs.unipr.it>
- Build an RPM package also for the PWL.
- The Prolog interfaces depend on the PWL.

* Tue Mar 04 2003 Roberto Bagnara <bagnara@cs.unipr.it>
- We require gmp at least 4.1.2.

* Fri Oct 04 2002 Roberto Bagnara <bagnara@cs.unipr.it>
- Require gcc-c++ 3.2 or later version.
- Require gmp 4.1 or later version.

* Sun Jun 30 2002 Roberto Bagnara <bagnara@cs.unipr.it>
- Mention not necessarily closed convex polyhedra in the main `%%description'.

* Tue Jun 25 2002 Roberto Bagnara <bagnara@cs.unipr.it>
- `%%files' section for gprolog package fixed.

* Mon Jun 24 2002 Roberto Bagnara <bagnara@cs.unipr.it>
- `%%files' section fixed for the yap package.
- The `%%files' sections of each package are now complete.

* Wed Jun 12 2002 Roberto Bagnara <bagnara@cs.unipr.it>
- Added file list for package gprolog.
- Updated file list for package swi.

* Thu Jun 06 2002 Roberto Bagnara <bagnara@cs.unipr.it>
- The `swi' package has now its `%%files' section.

* Wed Jun 05 2002 Roberto Bagnara <bagnara@cs.unipr.it>
- We will build several RPM packages out of our source tree.

* Mon Mar 04 2002 Roberto Bagnara <bagnara@cs.unipr.it>
- Require gcc-c++ 3.0.4 or later version.
- Require gmp 4.0.1 or later version.

* Sun Jan 27 2002 Roberto Bagnara <bagnara@cs.unipr.it>
- The move to libtool is complete: we can now build and distribute
  (with, e.g., RPM) static and dynamic versions of the library.

* Tue Oct 16 2001 Roberto Bagnara <bagnara@cs.unipr.it>
- Changed `Summary'.
- Changed `Packager' in view of PGP signatures.
- Changed `Group' to `Development/Libraries'.
- Require gcc-c++ 2.96-85 or later version.

* Mon Oct 15 2001 Roberto Bagnara <bagnara@cs.unipr.it>
- Now we build a relocatable package.

* Mon Oct 15 2001 Roberto Bagnara <bagnara@cs.unipr.it>
- A first cut at a working RPM spec file.

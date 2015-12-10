# BEAM is experimantal and some interpreter code unimplemented. See
# README.EAM.html for more details.
%global use_eam 0

Name:       yap
Version:    6.2.2
Release:    8%{?dist}
Summary:    High-performance Prolog Compiler
Summary(zh_CN.UTF-8): 高性能的 Prolog 编译器
Group:      Development/Languages
Group(zh_CN.UTF-8): 开发/语言
# README                            Perl Artistic license 2 and the FSF's LGPL
# packages/ProbLog/                         Artistic 2.0
# COPYING                                   LGPL
# LGPL/pillow/pillow.pl                     LGPLv2+
# packages/clib/sha1/sha2.c                 BSD or GPL
# packages/http/examples/demo_threads.pl    GPLv2+
License:    Artistic 2.0 and LGPLv2+ and (BSD or GPL+) and (GPLv2+)
URL:        http://www.ncc.up.pt/~vsc/Yap/
Source:     %{url}%{name}-%{version}.tar.gz
Patch1:     Yap-noni386.patch
Patch2:     yap-6.2.0-Locate-mysql-by-mysql_config.patch
Patch3:     yap-6.2.0-Install-directory-for-info-pages.patch
Patch4:     yap-6.2.0-Install-http-CSS-files-into-PLTARGET.patch
Patch5:     yap-6.2.0-Do-not-install-README-etc.patch
Patch6:     yap-6.2.0-Install-info-pages-non-executable.patch
Patch7:     yap-6.2.0-Do-not-install-info-dir-index.patch
# fix non-x86 build with recent gcc
Patch8:     yap-6.2.0-gprof-macro.patch
# Fix compilation of PLStream package on PPC
Patch9:     yap-6.2.0-Remove-feature-macro.patch
# Reported to upstream <yap-users@lists.sourceforge.net>
Patch10:    yap-6.2.2-Off-by-one-error-when-initializing-yap_flags.patch
# texinfo fix
Patch11:    yap-6.2.2-texinfo.patch
# yap 6.2.2 does not work on PPC (bug #790625)
ExcludeArch:    ppc ppc64
BuildRequires:  autoconf
BuildRequires:  gmp-devel
BuildRequires:  mysql-devel
# TODO: BuildRequires:  openmpi-devel
BuildRequires:  readline-devel
BuildRequires:  texinfo
BuildRequires:  unixODBC-devel
BuildRequires:  zlib-devel
Requires(post):   /sbin/install-info, /sbin/ldconfig
Requires(postun): /sbin/install-info, /sbin/ldconfig

# Do not export provides and requires on private libraries
%filter_provides_in /usr/lib64/Yap/
%filter_from_requires /^libplstream.so(/d
%filter_setup

%description
A high-performance Prolog compiler developed at LIACC, Universidade do
Porto. The Prolog engine is based in the WAM (Warren Abstract
Machine), with several optimizations for better performance. YAP
follows the Edinburgh tradition, and is largely compatible with the
ISO-Prolog standard and with Quintus and SICStus Prolog.

%description -l zh_CN.UTF-8
高性能的 Prolog 编译器。

%package devel
Summary:    C-Interface development files for Yap
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:      Development/Languages
Group(zh_CN.UTF-8): 开发/语言
Requires:   %{name} = %{version}-%{release}

%description devel
C-Interface development files for Yap.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package docs
Summary:    Documentation for Yap
Summary(zh_CN.UTF-8): %{name} 的文档
Group:      Development/Languages
Group(zh_CN.UTF-8): 开发/语言
BuildArch:  noarch
Requires:   %{name} = %{version}-%{release}

%description docs
Documentation for Yap.
%description docs -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q
%patch1 -p1
%patch2 -p1 -b .mysql_config
%patch3 -p1 -b .install_info_directory
%patch4 -p1 -b .install_css_into_pltarget
%patch5 -p1 -b .do_not_install_readme
%patch6 -p1 -b .non_executable_info
%patch7 -p1 -b .do_not_install_info_index
%patch8 -p1 -b .macro
%patch9 -p1 -b .remove_feature_macro
%patch10 -p1 -b .initialization
%patch11 -p1

# remove redundant RPATH
sed -i 's/-Wl,-R\(,\)\{0,1\}\\$(LIBDIR)//' configure.in
# transform RPATH into RUN_PATH. Private libraries dlopen()ed depend each on
# other
sed -i 's/-Wl,-R/-Wl,--enable-new-dtags,-R/g' configure.in
# Add soname to library
sed -i -e 's/\(-soname=\$DYNYAPLIB\)/\1.%{version}/' configure.in

# Regerenate configure because of patching
autoconf

# chr and clpqr are optional and they are a copy from SWI Prolog (LGPLv2+)
# TODO: Unbundle chr and clpqr libraries as subpackages

# Add soname to library and symlink from unversioned to versioned one
sed -i \
    -e '/@YAPLIB_LD@/ s/\(-o @YAPLIB@\)\(.*\)/\1.%{version}\2\n\tln -s @YAPLIB@.%{version} @YAPLIB@/' \
    -e '/@INSTALL_DLLS@.* @YAPLIB@/ s/\(@YAPLIB@\)\(.*\)/\1.%{version}\2\n\t@LN_S@ @YAPLIB@.%{version} $(DESTDIR)$(LIBDIR)\/@YAPLIB@/' \
    Makefile.in

# Fix file encoding
for F in README changes.css; do
    tr -d '\r' < "$F" > "${F}.new"
    touch -r "$F"{,.new}
    mv "$F"{.new,}
done
for F in docs/yap.tex TO_DO; do
    iconv -f iso-8859-1 -t utf-8 < "$F" > "${F}.new"
    sed -i -e '/mode: texinfo/ s/\(coding: \)latin-1/\1utf-8/' "${F}.new"
    touch -r "$F"{,.new}
    mv "$F"{.new,}
done

# Fix file permissions
chmod -x COPYING packages/http/examples/demo_inetd
# Permissions for debuginfo content
find -name '*.h' -exec chmod 0644 '{}' ';'
find -name '*.c' -exec chmod 0644 '{}' ';'


%build
# % define optflags $(echo $RPM_OPT_FLAGS | sed 's|-fstack-protector||')
%configure \
    --enable-coroutining \
    --enable-max-performance \
    --enable-depth-limit \
    --enable-dynamic-loading \
    --enable-myddas \
%if %{use_eam}
    --enable-eam \
%endif
    --enable-chr \
    --enable-clpqr
# TODO: --with-java

make %{?_smp_mflags}
make %{?_smp_mflags} info


%install
make DESTDIR=$RPM_BUILD_ROOT install
make DESTDIR=$RPM_BUILD_ROOT install_info

# fix permissions and flags
chmod 0644 $RPM_BUILD_ROOT%{_datadir}/Yap/pl/*
chmod 0644 $RPM_BUILD_ROOT%{_includedir}/Yap/*

# Move installed examples to docs dir
%global documentation docs-documentation
for P in clpbn; do 
    mkdir -p "%{documentation}/examples/${P}"
    mv "$RPM_BUILD_ROOT%{_datadir}/Yap/${P}/examples/"* \
        "%{documentation}/examples/${P}"
    rmdir "$RPM_BUILD_ROOT%{_datadir}/Yap/${P}/examples"
done
for P in minisat problog; do 
    mkdir -p "%{documentation}/examples/${P}"
    mv "$RPM_BUILD_ROOT%{_datadir}/Yap/${P}_examples/"* \
        "%{documentation}/examples/${P}"
    rmdir "$RPM_BUILD_ROOT%{_datadir}/Yap/${P}_examples"
done
# Copy not-installed examples to docs dir
# CLPBN/*, swi-minisat2 installed already
# TODO: jpl documentation with java support
# TODO: mpi documentation with mpi support
for P in pyswip cplint http plunit; do 
    mkdir -p "%{documentation}/examples/${P}"
    cp -a "packages/${P}/examples/"* "%{documentation}/examples/${P}"
done
for P in LGPL/pillow; do 
    mkdir -p "%{documentation}/examples/${P}"
    cp -a "${P}/examples/"* "%{documentation}/examples/${P}"
done

# Remove empty files
for F in $RPM_BUILD_ROOT%{_datadir}/Yap/myddas_top_level.yap \
    %{documentation}/examples/cplint/coin.uni; do
    test -s "$F" || rm "$F"
done


%post
/sbin/install-info %{_infodir}/yap.info --section "Programming Languages" %{_infodir}/dir 2>/dev/null || :
/sbin/install-info %{_infodir}/pillow_doc.info --section "Programming Languages" %{_infodir}/dir 2>/dev/null || :
/sbin/ldconfig


%postun
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/yap.info %{_infodir}/dir 2>/dev/null || :
  /sbin/install-info --delete %{_infodir}/pillow_doc.info %{_infodir}/dir 2>/dev/null || :
fi
/sbin/ldconfig


%files
%doc Artistic changes* COPYING GIT README TO_DO
%if %{use_eam}
%doc README.EAM.html
%endif
%{_bindir}/yap
%{_datadir}/Yap
%{_libdir}/Yap
%{_libdir}/libYap.so.*
%{_infodir}/*


%files devel
%{_libdir}/libYap.so
%{_includedir}/Yap


%files docs
%doc LGPL/pillow/doc/pillow_doc_html/*
%doc LGPL/pillow/doc/article.ps.gz
%doc %{documentation}/*


%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 6.2.2-8
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 6.2.2-7
- 为 Magic 3.0 重建

* Tue Oct 27 2015 Liu Di <liudidi@gmail.com> - 6.2.2-6
- 为 Magic 3.0 重建

* Mon Jan 07 2013 Petr Pisar <ppisar@redhat.com> - 6.2.2-5
- Fix off-by-one error when initializing yap_flags

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 23 2012 Petr Pisar <ppisar@redhat.com> - 6.2.2-3
- yap 6.2.2 does not work on PPC (bug #790625)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 09 2011 Petr Pisar <ppisar@redhat.com> - 6.2.2-1
- 6.2.2 bump

* Wed Dec 07 2011 Petr Pisar <ppisar@redhat.com> - 6.2.0-6
- Fix building on PowerPC (bug #751144)

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 6.2.0-5.2
- rebuild with new gmp without compat lib

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 6.2.0-5.1
- rebuild with new gmp

* Thu Jun 23 2011 Dan Horák <dan@danny.cz> - 6.2.0-5
- fix non-x86 builds with recent gcc

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 6.2.0-4
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Wed Mar 23 2011 Petr Pisar <ppisar@redhat.com> - 6.2.0-3
- Rebuild against mysql 5.5.10

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 04 2011 Petr Pisar <ppisar@redhat.com> - 6.2.0-1
- Reorder metadata in spec file
- 6.2.0 bump
- Remove uneeded Yap-creat.patch
- Remove uneeded Yap-5.1.1-config.sub.patch
- Locate mysql by mysql_config
- Fix info pages installation
- Logtalk is no logner distributed with yap
- Install http module CSS files to correct place
- Convert TO_DO into UTF-8
- Make COPYING non-executable
- Remove empty myddas_top_level.yap file
- Fix soname injection
- Fix BuildRequires
- Package clpbn examples
- Fix Source URL
- Clean exported Requires
- Correct RPATH
- Enable chr and clpqr libraries installation (still bundled with source tar
  ball) 
- Package uninstalled examples

* Wed Dec 08 2010 Petr Pisar <ppisar@redhat.com> - 5.1.3-3
- Hack SWI-compatible libraries build system to be compilable (bug #660965)
- Correct spec file syntax (white spaces, percentages)
- Convert documentation into UTF-8/CR
- Do not put unversioned library into main package
- Make docs subpackege architecture independent

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 15 2009 Gerard Milmeister <gemi@bluewin.ch> - 5.1.3-1
- new release 5.1.3

* Sun Mar 01 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 5.1.1-13
- Add Yap-5.1.1-config.sub.patch: 
  Upgrade outdated config.sub to fix rebuild breakdown on ppc64.

* Fri Jul 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.1.1-11
- fix license tag

* Thu Apr 10 2008 Gerard Milmeister <gemi@bluewin.ch> - 5.1.1-10
- enable rpm_opt_flags
- patch for incorrect open call with O_CREAT

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.1.1-9
- Autorebuild for GCC 4.3

* Sat Oct 20 2007 Gerard Milmeister <gemi@bluewin.ch> - 5.1.1-8
- fix library path for 64-bit platforms

* Wed Aug 29 2007 Gerard Milmeister <gemi@bluewin.ch> - 5.1.1-7
- replaced ld -shared with gcc -shared

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 5.1.1-6
- Rebuild for selinux ppc32 issue.

* Thu Jul  5 2007 Gerard Milmeister <gemi@bluewin.ch> - 5.1.1-5
- also build libYap.so

* Fri May 11 2007 Gerard Milmeister <gemi@bluewin.ch> - 5.1.1-3
- remove -fstack-protector from optflags in order to enable
  loading of .so modules

* Mon Aug 28 2006 Gerard Milmeister <gemi@bluewin.ch> - 5.1.1-2
- Rebuild for FE6

* Mon May  1 2006 Gerard Milmeister <gemi@bluewin.ch> - 5.1.1-1
- new version 5.1.1
- split off devel and docs packages

* Fri Feb 17 2006 Gerard Milmeister <gemi@bluewin.ch> - 5.0.1-2
- Rebuild for Fedora Extras 5

* Tue Oct 25 2005 Gerard Milmeister <gemi@bluewin.ch> - 5.0.1-1
- New Version 5.0.1

* Wed Sep  7 2005 Gerard Milmeister <gemi@bluewin.ch> - 5.0.0-1
- New Version 5.0.0

* Sat Jun 18 2005 Gerard Milmeister <gemi@bluewin.ch> - 4.5.5-5
- Use %%{_prefix}/lib for x86_64

* Sat Jun 18 2005 Gerard Milmeister <gemi@bluewin.ch> - 4.5.5-4
- Fix for non-i386 compilers

* Sat Jun 18 2005 Gerard Milmeister <gemi@bluewin.ch> - 4.5.5-3
- Compiler fix for FC4

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Feb 12 2005 Gerard Milmeister <gemi@bluewin.ch> - 0:4.5.5-1
- New Version 4.5.5

* Mon Nov 29 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:4.5.3-0.fdr.1
- New Version 4.5.3

* Sat Mar 13 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:4.5.2-0.fdr.1
- New Version 4.5.2

* Sat Nov 22 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:4.4.3-0.fdr.1
- First Fedora release

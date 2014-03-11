Summary: An ELF prelinking utility
Name: prelink
Version: 0.4.6
Release: 5%{?dist}
%global svnver 195
License: GPLv2+
Group: System Environment/Base
%define date 20111012
# svn export svn://sourceware.org/svn/prelink/trunk@%{svnver} prelink
# tar cf - prelink | bzip2 -9 > prelink-%{date}.tar.bz2
Source: http://people.redhat.com/jakub/prelink/prelink-%{date}.tar.bz2
Source2: prelink.conf
Source3: prelink.cron
Source4: prelink.sysconfig

BuildRequires: elfutils-libelf-devel-static
BuildRequires: glibc-static
Requires: glibc >= 2.2.4-18, coreutils, findutils
Requires: util-linux, gawk, grep
# For now
ExclusiveArch: %{ix86} alpha sparc sparcv9 sparc64 s390 s390x x86_64 ppc ppc64 %{arm} mips64el

%description
The prelink package contains a utility which modifies ELF shared libraries
and executables, so that far fewer relocations need to be resolved at runtime
and thus programs come up faster.

%prep
%setup -q -n prelink

%build
sed -i -e '/^prelink_LDADD/s/$/ -lpthread/' src/Makefile.{am,in}
%configure --disable-shared
make %{_smp_mflags}

%install
%{makeinstall}
mkdir -p %{buildroot}%{_sysconfdir}/rpm
cp -a %{SOURCE2} %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_sysconfdir}/{sysconfig,cron.daily,prelink.conf.d}
cp -a %{SOURCE3} %{buildroot}%{_sysconfdir}/cron.daily/prelink
cp -a %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/prelink
chmod 755 %{buildroot}%{_sysconfdir}/cron.daily/prelink
chmod 644 %{buildroot}%{_sysconfdir}/{sysconfig/prelink,prelink.conf}
cat > %{buildroot}%{_sysconfdir}/rpm/macros.prelink <<"EOF"
# rpm-4.1 verifies prelinked libraries using a prelink undo helper.
#       Note: The 2nd token is used as argv[0] and "library" is a
#       placeholder that will be deleted and replaced with the appropriate
#       library file path.
%%__prelink_undo_cmd     /usr/sbin/prelink prelink -y library
EOF
chmod 644 %{buildroot}%{_sysconfdir}/rpm/macros.prelink
mkdir -p %{buildroot}%{_mandir}/man5
echo '.so man8/prelink.8' > %{buildroot}%{_mandir}/man5/prelink.conf.5
chmod 644 %{buildroot}%{_mandir}/man5/prelink.conf.5

mkdir -p %{buildroot}/var/{lib,log}/prelink
touch %{buildroot}/var/lib/prelink/full
touch %{buildroot}/var/lib/prelink/quick
touch %{buildroot}/var/lib/prelink/force
touch %{buildroot}/var/log/prelink/prelink.log

#prelink wreaks havoc on sparc systems lets make sure its disabled by default there
%ifarch %{sparc}
sed -i -e 's|PRELINKING=yes|PRELINKING=no|g' %{buildroot}%{_sysconfdir}/sysconfig/prelink
%endif

%post
touch /var/lib/prelink/force

%files
%defattr(-,root,root)
%doc doc/prelink.pdf
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/prelink.conf
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/sysconfig/prelink
%{_sysconfdir}/rpm/macros.prelink
%dir %attr(0755,root,root) %{_sysconfdir}/prelink.conf.d
%{_sysconfdir}/cron.daily/prelink
%{_prefix}/sbin/prelink
%{_prefix}/bin/execstack
%{_mandir}/man5/prelink.conf.5*
%{_mandir}/man8/prelink.8*
%{_mandir}/man8/execstack.8*
%dir /var/lib/prelink
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/lib/prelink/full
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/lib/prelink/quick
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/lib/prelink/force
%dir /var/log/prelink
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/log/prelink/prelink.log

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.4.6-5
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 12 2011 Jakub Jelinek <jakub@redhat.com> 0.4.6-3
- add --layout-page-size=N option, default to --layout-page-size=32768
  on AMD Bulldozer (#739460)
- handle 0%%{?rhel} >= 7 like 0%%{?fedora} >= 13

* Fri Aug 26 2011 Jakub Jelinek <jakub@redhat.com> 0.4.6-2
- fix cxx3.sh for ppc

* Fri Aug 26 2011 Jakub Jelinek <jakub@redhat.com> 0.4.6-1
- enable for arm (#733089)
  - adjust arm default dynamic linker
  - fix up fast PIE detection to handle PT_LOPROC ... PT_HIPROC phdrs
    before PT_PHDR
  - disable cxx{1,2}.sh test checking for conflict removal on arm
    due to EABI weirdnesses, add new cxx3.sh test that tests conflict
    removal even on arm

* Wed Jun 22 2011 Jakub Jelinek <jakub@redhat.com> 0.4.5-3
- handle DW_OP_GNU_parameter_ref

* Tue May 31 2011 Jakub Jelinek <jakub@redhat.com> 0.4.5-2
- handle DW_OP_GNU_{{const,regval,deref}_type,convert,reinterpret}

* Fri Apr  1 2011 Jakub Jelinek <jakub@redhat.com> 0.4.5-1
- handle DW_OP_GNU_entry_value and DW_AT_GNU_call_site*

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 23 2010 Jakub Jelinek <jakub@redhat.com> 0.4.4-1
- support copying over extended attributes (#456105)
- handle DW_OP_GNU_implicit_pointer, fix handling of DW_OP_call_ref

* Wed Jul 14 2010 Jakub Jelinek <jakub@redhat.com> 0.4.3-4
- for prelink -u -o ... if no .gnu.prelink_undo section is
  present just pass through the original bits to the output file
  instead of saving the ELF file using libelf into a temporary
  and then copying over or renaming that to the final output file
  (#614382)

* Fri Apr 23 2010 Jakub Jelinek <jakub@redhat.com> 0.4.3-3
- move /var/lib/misc/prelink.{force,quick,full} to
  /var/lib/prelink/{force,quick,full} (#584319)

* Tue Apr 13 2010 Jakub Jelinek <jakub@redhat.com> 0.4.3-2
- run restorecon on /var/lib/misc/prelink.force (#581959)

* Tue Apr 13 2010 Jakub Jelinek <jakub@redhat.com> 0.4.3-1
- add support for prelink -u -o - library
- add DWARF4 support
- fix up reloc{8,9}.sh for sparc64, reenable testing on sparc64

* Mon Apr 12 2010 Jakub Jelinek <jakub@redhat.com> 0.4.2-7
- BuildReq libselinux-utils (#571724)
- handle R_390_{PC32DBL,16,PC16,PC16DBL,8} relocations in 31-bit objects
  (#552635)
- add prelink.conf(5) man page as a link to prelink(8) (#528933)

* Mon Mar 08 2010 Dennis Gilmore <dennis@ausil.us> 0.4.2-6
- disable tests on sparc64 bz#571551
- disable prelink from running on sparc arches

* Wed Dec 16 2009 Jakub Jelinek <jakub@redhat.com> 0.4.2-5
- change textrel tests, so that even if getenforce exists, but
  fails, textrel tests aren't run

* Wed Nov  4 2009 Jakub Jelinek <jakub@redhat.com> 0.4.2-4
- add support for STT_GNU_IFUNC on ppc/ppc64, R_PPC_IRELATIVE and
  R_PPC64_{IRELATIVE,JMP_IREL}

* Fri Sep 25 2009 Jakub Jelinek <jakub@redhat.com> 0.4.2-3
- fix DW_OP_implicit_value handling

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  9 2009 Jakub Jelinek <jakub@redhat.com> 0.4.2-1
- don't look for *_IRELATIVE relocations in .gnu.conflict section in binaries

* Sun Jul  5 2009 Jakub Jelinek <jakub@redhat.com> 0.4.1-1
- add support for STT_GNU_IFUNC on i?86/x86_64 and R_{386,X86_64}_IRELATIVE
- add support for DWARF3/DWARF4 features generated newly by recent
  gccs
- temporarily link prelink against -lpthread to workaround -lselinux
  issue

* Wed Mar 11 2009 Jakub Jelinek <jakub@redhat.com> 0.4.0-7
- fix prelinking on ppc64

* Tue Mar 10 2009 Jakub Jelinek <jakub@redhat.com> 0.4.0-6
- BuildRequire glibc-static
- rebuilt with gcc 4.4
- sparc64 and ARM TLS support

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.4.0-4
- fix license tag

* Tue Apr  8 2008 Jakub Jelinek <jakub@redhat.com> 0.4.0-3
- BuildRequire libselinux-static rather than libselinux-devel (#440749)

* Tue Oct  9 2007 Jakub Jelinek <jakub@redhat.com> 0.4.0-1
- add support for -c /etc/prelink.conf.d/*.conf in prelink.conf (#244452)
- remove no longer existent directories from default prelink.conf (#248694)
- reenabled prelink C++ optimizations which have not triggered any longer
  since _ZT[IV]* moved into .data.rel.ro section from .data
- fixed performance issues in C++ optimizations, especially on GCJ
  CNI programs (#314051)
- other performance improvements, prelink -avmR after prelink -ua now
  takes roughly 3m4s real time instead of 20m27s before
- don't run TEXTREL tests if SELinux is enforcing (#245928)

* Fri Dec  1 2006 Jakub Jelinek <jakub@redhat.com> 0.3.10-1
- MIPS support (Richard Sandiford)
- don't leave temporary files behind on prelink --verify failures (#199251)

* Fri Oct 27 2006 Jakub Jelinek <jakub@redhat.com> 0.3.9-4
- fix adjusting of .debug_ranges if end of range is at the end of some
  section and there is padding before the following one

* Mon Oct 23 2006 Jakub Jelinek <jakub@redhat.com> 0.3.9-3
- rebuilt

* Fri Jul 28 2006 Alexandre Oliva <aoliva@redhat.com> 0.3.9-2
- avoid SEGFAULT when sorting cache entries (#197451)

* Wed Jul 12 2006 Jakub Jelinek <jakub@redhat.com> 0.3.9-1
- DT_GNU_HASH support
- handle N_BNSYM and N_ENSYM stabs (#198203)
- handle upgrades from prelink with smaller maxpagesize to prelink
  with larger maxpagesize (#196941)

* Wed Jun 21 2006 Jakub Jelinek <jakub@redhat.com> 0.3.8-1
- fix -q mode canonicalization fix, speed up filename canonicalization
  by caching canonicalization for directories (#145983, #188062)
- remove bogus e_shoff assertion check (#194016)
- move prelink log file to /var/log/prelink/prelink.log (#194473)
- increase x86-64 maxpagesize to 2MB

* Mon May 22 2006 Jakub Jelinek <jakub@redhat.com> 0.3.7-1
- in -q mode, recheck the canonicalized filename to avoid
  overwriting symlinks with regular files (#145983, #188062)
- allow prelinking of binaries with .tbss section

* Mon Feb 13 2006 Jakub Jelinek <jakub@redhat.com> 0.3.6-3
- rebuilt again, disable -Wl,-z,nocopyreloc tests on x86_64,
  nocopyreloc really doesn't work on this platform (#180552)

* Wed Dec 12 2005 Jakub Jelinek <jakub@redhat.com> 0.3.6-2
- rebuilt with GCC 4.1
- link against newer glibc to fix MALLOC_PERTURB_ bug on 64-bit
  arches

* Thu Sep  1 2005 Jakub Jelinek <jakub@redhat.com> 0.3.6-1
- remove kernel requires - installed kernel doesn't imply running
  kernel anyway and in FC5 kernels older than 2.4.20 can't be used
  anyway, as LinuxThreads are no longer included
- don't relocate stabs N_{B,D,}SLINE (reported by Ashley Pittman)

* Fri Jul 29 2005 Jakub Jelinek <jakub@redhat.com> 0.3.5-2
- on ppc32 handle -mbss-plt .got sections created with -msecure-plt
  capable binutils (#164615)

* Fri Jun 10 2005 Jakub Jelinek <jakub@redhat.com> 0.3.5-1
- support for ppc32 -msecure-plt libraries and binaries
- don't crash if d_tag is invalid (#155605)
- rebuilt against robustified libelf (CAN-2005-1704)
- fix handling of libraries and binaries given on command
  line without any / characters in the filename

* Mon Mar 14 2005 Jakub Jelinek <jakub@redhat.com> 0.3.4-3
- fix relocation of .debug_loc (#150194)

* Sat Mar  5 2005 Jakub Jelinek <jakub@redhat.com> 0.3.4-2
- rebuilt with GCC 4

* Mon Feb  7 2005 Jakub Jelinek <jakub@redhat.com> 0.3.4-1
- fix prelink -uo when linked against libselinux (#146637)
  and when the -o argument filename is on a different filesystem
  than the object that needs undoing

* Tue Nov 23 2004 Jakub Jelinek <jakub@redhat.com> 0.3.3-1
- if layout code needs to re-prelink some library, make sure
  all libraries that depend on it are re-prelinked too (#140081)
- add several more checks before deciding it is ok to prelink a binary
  (even if another bug like #140081 was in, these checks should hopefully
  catch it and refuse to (re-)prelink the binary)
- added new PRELINK_NONRPM_CHECK_INTERVAL variable to %{_sysconfdir}/prelink,
  defaulting to 7 days.  Prelink nightly job will not do anything
  if that interval has not elapsed since last prelinking and
  and the rpm database has not been modified since that prelinking.
  This is useful if you rely on rpm/up2date/yum/apt-rpm for library
  and binary updates.  If you combine it with other means (installs
  from source, tarballs etc.), you probably want to
  set PRELINK_NONRPM_CHECK_INTERVAL=0.
- update prelink man page (#126468)

* Tue Oct 12 2004 Jakub Jelinek <jakub@redhat.com> 0.3.2-11
- update PT_PHDR program header if present when adding new program
  headers (#133734)

* Sat Oct  2 2004 Jakub Jelinek <jakub@redhat.com> 0.3.2-10
- support for non-absolute blacklist glob patterns (e.g. -b *.la)
- cache information about non-prelinkable files (non-ELF, statically linked,
  too small .dynamic, DT_TEXTREL with conflicts against it; #132056)
- other speedups for prelink -aq
- for --verify, make sure only read-only fd's are opened for the
  unprelinked temporary file, otherwise a kernel might ETXTBUSY on it
  (#133317)
- change warning message if some object's dependencies can't be found
- add buildrequires libselinux-devel and use %%{_tmppath} instead
  of /var/tmp in Buildroot (#132879)

* Wed Sep  8 2004 Jakub Jelinek <jakub@redhat.com> 0.3.2-8
- handle overlapping .opd sections on ppc64

* Tue Sep  7 2004 Jakub Jelinek <jakub@redhat.com> 0.3.2-7
- fix warning messages if setting of security context fails

* Wed Jul  7 2004 Jakub Jelinek <jakub@redhat.com> 0.3.2-6
- change sed separator in testsuite scripts from | to , if \|
  is present in regexps, as that invokes undefined behaviour
  which changed between GNU sed 4.0.9 and 4.1

* Wed Jul  7 2004 Jakub Jelinek <jakub@redhat.com> 0.3.2-5
- skip vDSO in ldd /sbin/init output when determining if /sbin/telinit -u
  should be run (#127350)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 20 2004 Jakub Jelinek <jakub@redhat.com> 0.3.2-3
- 4 SPARC 64-bit fixes
- use $CC instead of gcc when checking for TLS support in tls*.sh

* Thu May 20 2004 Jakub Jelinek <jakub@redhat.com> 0.3.2-2
- add 2 new TLS testcases (one that fails e.g. with glibc < 2.3.3-28
  on IA-32)
- SPARC TLS support

* Wed May  5 2004 Jakub Jelinek <jakub@redhat.com> 0.3.2-1
- fix cxx.c:68: find_cxx_sym: Assertive `n < ndeps' failed problem
  on 32-bit architectures (#118522)
- build prelink.cache into temporary file and atomically rename over
  (#121109)

* Wed Mar 17 2004 Jakub Jelinek <jakub@redhat.com> 0.3.1-2
- unlink temporary files if renaming to the destination or setting of
  security context failed (#118251)
- fix bi-architecture prelinking (#118226)
- if prelink called from the cron script fails, note the exit status
  into /var/log/prelink.log

* Thu Mar  4 2004 Jakub Jelinek <jakub@redhat.com> 0.3.1-1
- add prelink documentation (PDF format)
- fix assertion failures on PPC (.sdynbss related, #115925)
- fix prelink --help (#115202)
- avoid free on uninitialized variable in one error path (#117332)
- s/i386/%%{ix86}/ to make mharris happy

* Mon Feb 16 2004 Jakub Jelinek <jakub@redhat.com> 0.3.0-21
- fix prelink abort in certain cases where a new PT_LOAD segment
  needs to be added (seen on AMD64)

* Thu Jan 29 2004 Jakub Jelinek <jakub@redhat.com> 0.3.0-20
- clearify message about unlisted dependencies
- don't do SELinux context copying if is_selinux_enabled () < 0

* Tue Jan 27 2004 Jakub Jelinek <jakub@redhat.com> 0.3.0-19
- refuse to prelink objects whose dependencies as reported by
  ldd don't include all dependencies transitively (this can
  happen when using RPATH and a shared library with the same
  SONAME exists both in that RPATH and either another RPATH
  or standard library directories)
- add testcase for this
- rework .dynsym/.symtab STT_SECTION translation, so that it works
  with binutils which put only sections not generated by the linker
  into .dynsym for shared libraries
- fix make check, so that it is not confused by 2.6.x kernel
  VDSOs

* Thu Jan 15 2004 Jakub Jelinek <jakub@redhat.com> 0.3.0-18
- allow R_*_JU?MP_SLOT relocs to point also into .got.plt
  sections on IA32/AMD64/ARM/s390/s390x/SH

* Tue Dec  9 2003 Jakub Jelinek <jakub@redhat.com> 0.3.0-17
- set SELinux security context immediately before renaming,
  not before

* Tue Nov 18 2003 Jakub Jelinek <jakub@redhat.com> 0.3.0-15
- blacklist support
- use FTW_ACTIONRETVAL if available to avoid even stating of
  files in blacklisted directory trees
- SELinux support

* Tue Oct 28 2003 Jakub Jelinek <jakub@redhat.com> 0.3.0-13
- added execstack.8 manpage
- changed order of columns in execstack --query output

* Tue Oct 28 2003 Jakub Jelinek <jakub@redhat.com> 0.3.0-12
- added execstack tool
- added -o option, to be used together with -u
- free temp_filename in close_dso

* Mon Oct 27 2003 Jakub Jelinek <jakub@redhat.com> 0.3.0-11
- fix adjustement of DT_VALRNGLO .. DT_VALRNGHI and
  DT_ADDRRNGLO .. DT_ADDRRNGHI dynamic tags when relocating shared
  libraries
- never adjust p_vaddr/p_paddr/p_offset of PT_GNU_STACK segment
- allow shell wildcards in %{_sysconfdir}/prelink.conf
- fix REL->RELA conversion of shared libraries if .rel.dyn
  or .rel.plt are last sections in readonly PT_LOAD segment
- force full reprelinking on prelink upgrades (well, first time
  the cron job is run after the upgrade)
- require coreutils, findutils, util-linux, gawk and grep

* Fri Oct 24 2003 Jakub Jelinek <jakub@redhat.com> 0.3.0-10
- avoid removing PT_GNU_STACK segment if decreasing first PT_LOAD segment's
  p_vaddr on IA-32

* Mon Oct 13 2003 Jakub Jelinek <jakub@redhat.com> 0.3.0-9
- avoid prelink crash if first dependency is to be prelinked because
  of address space overlaps

* Thu Oct  9 2003 Jakub Jelinek <jakub@redhat.com> 0.3.0-8
- use /var/lib/misc/prelink.full instead of /var/run/prelink.full for last
  full prelink timestamp (#106721)
- warn about UPX compressed binaries or libraries/binaries without section
  headers (neither can be prelinked obviously)

* Mon Oct  6 2003 Jakub Jelinek <jakub@redhat.com> 0.3.0-7
- don't rely on malloc/calloc/realloc with size 0 returning a unique pointer
- fix testsuite, so that it works even if installed glibc/libstdc++
  is already prelinked

* Wed Sep 17 2003 Jakub Jelinek <jakub@redhat.com> 0.3.0-6
- fix comment in %{_sysconfdir}/sysconfig/prelink (#106217)

* Tue Sep  2 2003 Jakub Jelinek <jakub@redhat.com> 0.3.0-5
- fix prelink segfault on -z nocombreloc libraries (#103404)
- run one make check round with -Wl,-z,nocombreloc to test handling
  of nocombreloc binaries and libraries

* Fri Aug 15 2003 Jakub Jelinek <jakub@redhat.com> 0.3.0-4
- redirect prelink's stderr from the cron job to prelink.log (#102456)

* Mon Aug 11 2003 Jakub Jelinek <jakub@redhat.com> 0.3.0-3
- fix DT_CHECKSUM computation - do STT_LOCAL symbol frobbing and .mdebug
  updates write_dso would do also before checksum computation (#89953)

* Fri Aug  8 2003 Jakub Jelinek <jakub@redhat.com> 0.3.0-2
- avoid assertion failures when changing PROGBITS .bss back into
  NOBITS .bss (#101813)
- add 2 new tests for it

* Tue Aug  5 2003 Jakub Jelinek <jakub@redhat.com> 0.3.0-1
- run prelink from cron automatically, add %{_sysconfdir}/sysconfig/prelink
  to configure it
- update manual page

* Tue Jul  1 2003 Jakub Jelinek <jakub@redhat.com> 0.2.1-2
- fix a thinko in the library path checking code
- change R_386_GLOB_DAT into R_386_32 in .gnu.conflict, similarly
  R_X86_64_GLOB_DAT and R_X86_64_64
- fix a bug in find_free_space which caused
  "section file offsets not monotonically increasing" errors on some
  IA-32 binaries
- add --md5 and --sha options
- use mmap during --verify if possible
- add */lib64 directories to prelink.conf

* Mon Jun 30 2003 Jakub Jelinek <jakub@redhat.com> 0.2.1-1
- make sure binaries prelinked for the second and later time without
  unprelinking in between verify correctly
- make sure DT_CHECKSUM computation is the same for newly prelinked
  and second or later time prelinked libraries
- dwarf2 abbrev hash bugfix
- don't allow prelinking libraries outside directories specified
  in config file or on the command line
- several new tests for reprelinking
- pack non-alloced sections and section header table tightly after the
  last alloced section

* Wed Jun 18 2003 Jakub Jelinek <jakub@redhat.com> 0.2.0-28
- finish and enable ppc64
- fix ppc BR{,N}TAKEN reloc handling
- fix up sh_offset values of zero-sized or SHT_NOBITS section
  if ld messed them up
- issue error about bogus library dependency chains instead of
  segfaulting (plus testcases for it)

* Fri Jun 13 2003 Jakub Jelinek <jakub@redhat.com> 0.2.0-27
- add --quick mode
- new test for --quick mode and also reprelinking of binary against
  upgraded shared library which needs more conflicts

* Mon Jun  2 2003 Jakub Jelinek <jakub@redhat.com> 0.2.0-26
- don't segfault in C++ optimizations if a conflict from undefined
  to defined value is seen
- some more ppc64 work

* Fri May 30 2003 Jakub Jelinek <jakub@redhat.com> 0.2.0-25
- exec-shield support
- with -R, don't randomize just base address from which all libs
  are layed out, but also slightly randomize order of libraries
  in the layout queue
- add check-harder and check-cycle makefile goals in testsuite/,
  use it during rpm building

* Fri May 23 2003 Jakub Jelinek <jakub@redhat.com> 0.2.0-24
- optimize out conflicts in G++ 3+ virtual tables if they are just
  because some method has been called from a binary and thus there
  is a .plt slot in the binary. This change not only kills lots of conflicts
  on some KDE programs, but also should speed up runtime (not just startup
  time), since the hop through .plt is bypassed
- added new C++ test
- fix a bug in ppc64 fixup .plt code

* Thu May 22 2003 Jakub Jelinek <jakub@redhat.com> 0.2.0-23
- when updating dynamic tags for executable after section reshuffling,
  check section type as well, so that 0 sized sections don't get the
  tags attached instead of the proper ones
- when an address space conflict is found between libraries for the same
  executable during layouting, check properly for all remaining conflicts
  as well

* Thu May 15 2003 Jakub Jelinek <jakub@redhat.com> 0.2.0-22
- don't adjust DT_REL{,A} if it is 0
- allow prelinking of libraries with no dependencies
- fix handling of libraries with no lazy relocs, no normal relocs or no
  relocs at all
- some new tests
- fix SH (Daniel Jacobowitz)

* Mon May  5 2003 Jakub Jelinek <jakub@redhat.com> 0.2.0-21
- fix prelink on AMD64
- 2 new testcases
- fix for debugging prelink_entry_dump/restore

* Fri May  2 2003 Jakub Jelinek <jakub@redhat.com> 0.2.0-20
- ppc TLS
- some ppc64 work
- avoid using trampolines for nested functions
- fix typo in prelink man page (#89247)

* Tue Apr 15 2003 Jakub Jelinek <jakub@redhat.com> 0.2.0-19
- fix find_readonly_space bug which caused doxygen not to be prelinked

* Mon Feb 17 2003 Jakub Jelinek <jakub@redhat.com> 0.2.0-18
- fix section indices in .symtab if non-alloced sections weren't
  originally monotonically increasing
- s390, s390x and Alpha TLS support

* Mon Feb 10 2003 Jakub Jelinek <jakub@redhat.com> 0.2.0-17
- never try to prelink or relocate stripped-to-file debuginfo

* Tue Jan 21 2003 Jakub Jelinek <jakub@redhat.com> 0.2.0-16
- x86-64 TLS support
- added one more tls testcase

* Fri Dec 13 2002 Jakub Jelinek <jakub@redhat.com> 0.2.0-15
- hopefully finished IA-32 TLS support
- require elfutils 0.72 for various data-swapping fixes

* Wed Dec 11 2002 Jakub Jelinek <jakub@redhat.com> 0.2.0-14
- rebuilt against elfutils 0.69 to fix a make check failure on Alpha

* Mon Dec  9 2002 Jakub Jelinek <jakub@redhat.com> 0.2.0-13
- use ELF_F_PERMISSIVE if defined
- be permissive even when doing --reloc-only
- fix up .plt section sh_entsize on Alpha

* Wed Dec  4 2002 Jakub Jelinek <jakub@redhat.com> 0.2.0-12
- some more fixes for elfutils

* Tue Dec  3 2002 Jakub Jelinek <jakub@redhat.com> 0.2.0-11
- make it work with elfutils instead of libelf 0.[78]
- update to newer auto*/libtool
- some more steps towards TLS support, at least --reloc-only should work

* Thu Oct  3 2002 Jakub Jelinek <jakub@redhat.com> 0.2.0-10
- x86-64, s390x and testsuite fixes

* Sun Sep 29 2002 Jakub Jelinek <jakub@redhat.com> 0.2.0-9
- enable on ppc and x86_64
- fix ppc far PLT slot prelink
- support --undo on ppc
- for bug-compatibility with some unnamed OS changed R_SPARC_RELATIVE
  --undo
- tiny steps towards TLS support on IA-32, more will come

* Tue Aug 27 2002 Jakub Jelinek <jakub@redhat.com> 0.2.0-8
- avoid putting garbage into executable's .gnu.liblist sh_link
  if we did not have to grow .dynstr
- don't segfault on bogus sh_link and sh_info values (#72705)

* Mon Aug 26 2002 Jakub Jelinek <jakub@redhat.com> 0.2.0-7
- when growing allocated shared lib sections (for REL->RELA
  conversion), make sure !PF_W and PF_W segments don't end up
  on the same page
- when finding space for sections in an executable, make sure
  it is not included in between two reloc sections
- for non-zero SHN_ABS symbols on 32-bit arches mask high
  32-bits of st_value (libelf 0.8.x is strict here)

* Fri Aug 23 2002 Jakub Jelinek <jakub@redhat.com> 0.2.0-6
- make it work with libelf 0.8.2

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jun 21 2002 Jakub Jelinek <jakub@redhat.com> 0.2.0-4
- add %{_sysconfdir}/rpm/macros.prelink

* Mon Jun 17 2002 Jakub Jelinek <jakub@redhat.com> 0.2.0-1
- added --undo and --verify mode
- new architectures s390, s390x, arm, sh
- handle binaries/shared libraries with non-allocated sections
  without monotonically increasing sh_offsets
- handle .sbss and .sdynbss
- fixed a bug in 64-bit LE/BE read routines
- removed .rel{,a}.dyn reloc conversion/sorting, it was duplicating
  ld's -z combreloc and complicated lots of things
- fixed STB_LOCAL/STT_SECTION symbol adjusting
- use mkstemp for temporary files, allow --verify for binaries/libs
  on read-only filesystems
- added DWARF-2 .debug_ranges adjustement, special case GCC's
  "set base to 0 and make things absolute instead of relative" trick
- allow arches to override default layout mechanism (for ppc)
- added some new tests, test --undo and --verify modes in the testsuite
- alpha: adjust what R_ALPHA_GLOB_DAT points to too
- i386: apply _32 and _PC32 REL relocs, as apply_rel can be called
  for C++ optimizations before REL->RELA conversion
- ppc: layout strategy to satisfy ppc lib location preferences
- sparc64: handle R_SPARC_DISP64
- x86-64: adjust what R_X86_64_RELATIVE points to too
- link prelink statically, esp. because of --verify mode
- run make check during build process

* Mon Oct  1 2001 Jakub Jelinek <jakub@redhat.com> 0.1.3-7
- fix layout code so that -R works
- on IA-32, when there are no R_386_PC32 relocs and no R_386_32 relocs
  with non-zero addend (= memory content), don't convert REL->RELA,
  only switch R_386_32 relocs to R_386_GLOB_DAT
- support creating a new PT_LOAD segment if necessary, if SHT_NOBITS
  sections are small, instead of adding new PT_LOAD segment just add file
  backing to those NOBITS sections
- added testsuite
- new supported architectures (Alpha including .mdebug section support,
  Sparc, Sparc 64-bit, X86_64 (the last one untested)), beginning of PPC
  support

* Thu Sep  6 2001 Jakub Jelinek <jakub@redhat.com> 0.1.3-6
- make sure lib base is always ELF page size aligned

* Wed Aug 29 2001 Jakub Jelinek <jakub@redhat.com> 0.1.3-5
- fix sorting of .rel*.dyn sections, so that all RELATIVE relocs really
  come first
- when DT_RELCOUNT already exists and conversion REL->RELA is done,
  convert it into DT_RELACOUNT
- set conflict lookupent and conflictent to 0 for undefineds
- don't bother with DT_REL*COUNT for apps, they cannot have any RELATIVE
  relocs

* Tue Aug 28 2001 Jakub Jelinek <jakub@redhat.com> 0.1.3-4
- brown paper bag time: when determining if conversion from REL to RELA
  is needed, check all non-PLT rel sections, including last.
  This caused prelinking to fail with -z combreloc compiled libraries.

* Mon Aug 27 2001 Jakub Jelinek <jakub@redhat.com> 0.1.3-3
- don't use .gnu.reloc section, use .rel.dyn or .rela.dyn instead
- put RELATIVE relocs first, not last, so that DT_REL{,A}COUNT
  works
- put in updated glibc patch
- no need for special binutils patch - all is done in the -z combreloc
  patchset

* Tue Jul 24 2001 Jakub Jelinek <jakub@redhat.com> 0.1.3-2
- use the new DT_GNU_CONFLICT/DT_GNU_LIBLIST/SHT_GNU_LIBLIST constants
- unlink *.#prelink# files if necessary

* Wed Jul 18 2001 Jakub Jelinek <jakub@redhat.com> 0.1.3-1
- fix layout.c
- create .gnu.prelink_undo section, --undo and --verify modes will use that
- some more C++ specific optimizations

* Fri Jul 13 2001 Jakub Jelinek <jakub@redhat.com> 0.1.2-1
- bail out early if ELF object does not have sh_offsets
  monotonically increasing
- disallow prelinking if there are conflicts against read-only
  segments in shared libraries (ie. non-pic shared libraries
  - this is better than bailing out for all non-pic shared libraries)
- add some C++ specific optimizations to reduce number of conflicts,
  more to come

* Tue Jul 10 2001 Jakub Jelinek <jakub@redhat.com> 0.1.1-2
- fix incremental prelinking

* Tue Jul 10 2001 Jakub Jelinek <jakub@redhat.com> 0.1.1-1
- relocate stabs and dwarf-2 debugging formats
- support both --all and incremental prelinking
- handle hardlinks
- limit to libraries in %{_sysconfdir}/prelink.conf directories or
  directories from command line

* Tue Jul  3 2001 Jakub Jelinek <jakub@redhat.com> 0.1.0-1
- new package

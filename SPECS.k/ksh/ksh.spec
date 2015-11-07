%global       releasedate 2012-08-01

Name:         ksh
Summary:      The Original ATT Korn Shell
URL:          http://www.kornshell.com/
Group:        System Environment/Shells
License:      EPL
Version:      20120801
Release:      5%{?dist}
Source0:      http://www.research.att.com/~gsf/download/tgz/ast-ksh.%{releasedate}.tgz
Source1:      http://www.research.att.com/~gsf/download/tgz/INIT.%{releasedate}.tgz
Source2:      kshcomp.conf
Source3:      kshrc.rhs
Source4:      dotkshrc
#expected results of test suite
Source5:      expectedresults.log

#don't use not wanted/needed builtins - Fedora/RHEL specific
Patch1:       ksh-20070328-builtins.patch

#fix regression test suite to be usable during packagebuild - Fedora/RHEL specific
Patch2:       ksh-20100826-fixregr.patch

#fix build err
Patch3:       ksh-build-fix.patch

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Conflicts:    pdksh
Requires: coreutils, glibc-common, diffutils
BuildRequires: bison
# regression test suite uses 'ps' from procps
BuildRequires: procps
Requires(post): grep, coreutils, systemd-units
Requires(preun): grep, coreutils

%description
KSH-93 is the most recent version of the KornShell by David Korn of
AT&T Bell Laboratories.
KornShell is a shell programming language, which is upward compatible
with "sh" (the Bourne Shell).

%prep
%setup -q -c
%setup -q -T -D -a 1
%patch1 -p1 -b .builtins
%patch2 -p1 -b .fixregr

#/dev/fd test does not work because of mock
sed -i 's|ls /dev/fd|ls /proc/self/fd|' src/cmd/ksh93/features/options

%ifarch mips64el
%patch3 -p1 -b .build
%endif

%build
./bin/package
./bin/package make mamake ||:
./bin/package make mamake ||:
export CCFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-unknown-pragmas -Wno-parentheses -Wno-unused -Wno-unused-but-set-variable -Wno-cpp"
export CC=gcc
./bin/package "make"

#cp lib/package/LICENSES/epl LICENSE

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{/bin,%{_bindir},%{_mandir}/man1}
install -c -m 755 arch/*/bin/ksh $RPM_BUILD_ROOT/bin/ksh
install -c -m 755 arch/*/bin/shcomp $RPM_BUILD_ROOT%{_bindir}/shcomp
install -c -m 644 arch/*/man/man1/sh.1 $RPM_BUILD_ROOT%{_mandir}/man1/ksh.1
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/skel
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/skel/.kshrc
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/kshrc
install -D -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/binfmt.d/kshcomp.conf

%check
%if 0%{?rhel} > 6
%ifarch s390
exit 0
%endif
%endif

export SHELL=$(ls $(pwd)/arch/*/bin/ksh)
cd src/cmd/ksh93/tests/
ulimit -c unlimited
if [ ! -e /dev/fd ]
then
  echo "ERROR: /dev/fd does not exist, regression tests skipped"
  exit 0
fi
$SHELL ./shtests 2>&1 | tee testresults.log
exit 0
sed -e '/begins at/d' -e '/ 0 error/d' -e 's/at [^\[]*\[/\[/' testresults.log -e '/tests skipped/d' >filteredresults.log
if ! cmp filteredresults.log %{SOURCE5} >/dev/null || ls core.*
then
  echo "Regression tests failed"
  diff -Naurp %{SOURCE5} filteredresults.log
  exit -1
fi

%post
if [ ! -f /etc/shells ]; then
        echo "/bin/ksh" > /etc/shells
else
        if ! grep -q '^/bin/ksh$' /etc/shells ; then
                echo "/bin/ksh" >> /etc/shells
        fi
fi

/bin/systemctl try-restart systemd-binfmt.service >/dev/null 2>&1 || :

%postun
if [ ! -f /bin/ksh ]; then
	sed -i '/^\/bin\/ksh$/ d' /etc/shells
fi

%verifyscript
echo -n "Looking for ksh in /etc/shells... "
if ! grep '^/bin/ksh$' /etc/shells > /dev/null; then
    echo "missing"
    echo "ksh missing from /etc/shells" >&2
else
    echo "found"
fi

%files 
%defattr(-, root, root,-)
%doc src/cmd/ksh93/COMPATIBILITY src/cmd/ksh93/RELEASE src/cmd/ksh93/TYPES 
# LICENSE file is missing, temporarily?
/bin/ksh
/usr/bin/shcomp
%{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/skel/.kshrc
%config(noreplace) %{_sysconfdir}/kshrc
%config(noreplace) %{_sysconfdir}/binfmt.d/kshcomp.conf

%clean
    rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 20120801-5
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 20120801-4
- 为 Magic 3.0 重建

* Fri Sep 14 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120801-3
- fix typo in binfmt config file
- register binary format after package installation

* Thu Sep 13 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120801-2
- add support for direct execution of compiled scripts

* Wed Aug 08 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120801-1
- ksh updated to 20120801

* Tue Jul 31 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120727-1
- ksh updated to 2012-07-27

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120628-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 02 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120628-1
- ksh updated to 20120628

* Wed Jun 27 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120626-1
- ksh updated to 20120626

* Fri Jun 22 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120620-1
- ksh updated to 2012-06-20

* Wed Jun 13 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120612-1
- ksh updated to 20120612

* Mon Jun 04 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120531-1
- ksh updated to 2012-05-31

* Mon Mar 19 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120229-2
- do not hang after return code 12

* Wed Mar 14 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120229-1
- ksh updated to 2012-02-29

* Tue Mar 13 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120214-2
- fix tilda expansion in scripts

* Mon Feb 20 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120214-1
- ksh updated to 20120214

* Mon Feb 06 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120202-1
- ksh updated to 20120202

* Thu Jan 05 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120101-1
- ksh updated to 2012-01-01

* Wed Dec 07 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110630-9
- do not crash when browsing through history containing comment (#733813)

* Wed Dec 07 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110630-8
- do not crash when two subseguent dots are used in variable or command name (#733544)

* Mon Dec 05 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110630-7
- fix: ksh can prematurely exit without crash or any error
- make spec work in epel

* Thu Nov 10 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110630-6
- add files to %%doc

* Thu Oct 06 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110630-5
- ksh sometimes returns wrong exit code when pid numbers are being recycled

* Tue Oct 04 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110630-4
- restore tty settings after timed out read (#572291)

* Fri Aug 12 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110630-3
- do not crash when killing last bg job when there is not any

* Wed Aug 03 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110630-2
- fix: IFS manipulation in a function can cause crash

* Fri Jul 01 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110630-1
- ksh updated to 2011-06-30

* Wed Jun 08 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110505-2
- fix: resume of suspended process using pipes does not work (#708909)

* Mon May 09 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110505-1
- ksh updated to 2011-05-05

* Fri Apr 29 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110428-1
- ksh updated to 2011-04-28

* Mon Apr 18 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110415-1
- ksh updated to 2011-04-15

* Tue Mar 29 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110208-3
- fix array definition being treated as fixed array
- fix suspend crashing ksh

* Mon Mar 07 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110208-2
- fix ( ) compound list altering environment

* Wed Feb 09 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110208-1
- ksh updated to 2011-02-08

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110202-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110202-1
- ksh updated to 2011-02-02

* Wed Feb 02 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110131-1
- ksh updated to 2011-01-31

* Fri Jan 28 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110127-1
- ksh updated to 2011-01-27

* Thu Jan 20 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110118-1
- ksh updated to 2011-01-18

* Mon Jan 17 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110104-1
- ksh updated to 2011-01-04

* Thu Dec 23 2010 Michal Hlavinka <mhlavink@redhat.com> - 20101212-2.20101122
- found ugly regression, reverting to 2010-11-22 (with io race patch) for now

* Thu Dec 16 2010 Michal Hlavinka <mhlavink@redhat.com> - 20101212-1
- ksh updated to 2010-12-12

* Mon Dec 06 2010 Michal Hlavinka <mhlavink@redhat.com> - 20101201-2
- fix file io race condition when file was created, but still does not exist

* Fri Dec 03 2010 Michal Hlavinka <mhlavink@redhat.com> - 20101201-1
- ksh updated to 2010-12-01

* Tue Nov 23 2010 Michal Hlavinka <mhlavink@redhat.com> - 20101122-1
- ksh updated to 2010-11-22

* Mon Nov 01 2010 Michal Hlavinka <mhlavink@redhat.com> - 20101026-1
- ksh updated to 2010-10-26

* Tue Oct 12 2010 Michal Hlavinka <mhlavink@redhat.com> - 20101010-1
- ksh updated to 2010-10-10

* Fri Oct 08 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100924-2
- disable only known to be broken builtins, let other enabled
- skip regression tests if /dev/fd is missing

* Tue Sep 28 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100924-1
- ksh updated to 2010-09-24

* Mon Aug 30 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100826-1
- ksh updated to 2010-08-26
- make regression test suite usable during package build

* Fri Aug 13 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100811-1
- ksh updated to 2010-08-11

* Thu Jul 08 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100701-1
- updated to 2010-07-01

* Fri Jun 25 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100621-1
- updated to 2010-06-21

* Tue Jun 15 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100527-2
- add shcomp for shell compiling

* Thu Jun 10 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100527-1
- updated to 2010-05-27

* Mon May 31 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100309-6
- add pathmunge to /etc/kshrc

* Wed May 05 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100309-5
- fix rare cd builtin crash (#578582)

* Wed May 05 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100309-4
- fix infinite loop when whence builtin is used with -q option (#587127)
- fix stdin for double command substitution (#584007)

* Mon Mar 29 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100309-3
- fix typo in last patch

* Fri Mar 26 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100309-2
- restore tty settings after timed out read for utf-8 locale

* Wed Mar 10 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100309-1
- updated to 2010-03-09
- fix mock building - detection of /dev/fd/X

* Mon Jan 04 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100202-1
- updated to 2010-02-02

* Mon Jan 04 2010 Michal Hlavinka <mhlavink@redhat.com> - 20091224-1
- updated to 2009-12-24

* Mon Dec 07 2009 Michal Hlavinka <mhlavink@redhat.com> - 20091206-1
- updated to 2009-12-06

* Fri Dec 04 2009 Michal Hlavinka <mhlavink@redhat.com> - 20091130-1
- updated to 2009-11-30

* Wed Nov 18 2009 Michal Hlavinka <mhlavink@redhat.com> - 20091021-1
- updated to 2009-10-21

* Thu Aug 27 2009 Michal Hlavinka <mhlavink@redhat.com> - 20090630-1
- updated to 2009-06-30

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090505-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 11 2009 Michal Hlavinka <mhalvink@redhat.com> - 20090505-1
- updated to 2009-05-05

* Tue May 05 2009 Michal Hlavinka <mhalvink@redhat.com> - 20090501-1
- updated to 2009-05-01

* Tue Mar 10 2009 Michal Hlavinka <mhlavink@redhat.com> - 20081104-3
- fix typos in spec file

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20081104-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 21 2009 Michal Hlavinka <mhlavink@redhat.com> 20081104-1
- update to 2008-11-04
- ast-ksh-locales are not useable remove them

* Tue Oct 21 2008 Michal Hlavinka <mhlavink@redhat.com> 20080725-4
- fix #467025 - Ksh fails to initialise environment when login from graphic console

* Wed Aug 06 2008 Tomas Smetana <tsmetana@redhat.com> 20080725-3
- fix BuildRequires, rebuild

* Tue Aug  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 20080725-2
- fix license tag

* Mon Jul 28 2008 Tomas Smetana <tsmetana@redhat.com> 20080725-1
- new upstream version

* Thu Jun 26 2008 Tomas Smetana <tsmetana@redhat.com> 20080624-1
- new upstream version

* Mon Feb 11 2008 Tomas Smetana <tsmetana@redhat.com> 20080202-1
- new upstream version

* Wed Jan 30 2008 Tomas Smetana <tsmetana@redhat.com> 20071105-3
- fix #430602 - ksh segfaults after unsetting OPTIND

* Mon Jan 07 2008 Tomas Smetana <tsmetana@redhat.com> 20071105-2
- fix #405381 - ksh will not handle $(xxx) when typeset -r IFS
- fix #386501 - bad group in spec file

* Wed Nov 07 2007 Tomas Smetana <tsmetana@redhat.com> 20071105-1
- new upstream version

* Wed Aug 22 2007 Tomas Smetana <tsmetana@redhat.com> 20070628-1.1
- rebuild

* Thu Jul 12 2007 Tomas Smetana <tsmetana@redhat.com> 20070628-1
- new upstream version
- fix unaligned access messages (Related: #219420)

* Tue May 22 2007 Tomas Smetana <tsmetana@redhat.com> 20070328-2
- fix wrong exit status of spawned process after SIGSTOP
- fix building of debuginfo package, add %%{?dist} to release
- fix handling of SIGTTOU in non-interactive shell
- remove useless builtins

* Thu Apr 19 2007 Tomas Smetana <tsmetana@redhat.com> 20070328-1
- new upstream source
- fix login shell invocation (#182397)
- fix memory leak

* Wed Feb 21 2007 Karsten Hopp <karsten@redhat.com> 20070111-1
- new upstream version
- fix invalid write in uname function

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 20060214-1.1
- rebuild

* Thu Jun 01 2006 Karsten Hopp <karsten@redhat.de> 20060214-1
- new upstream source

* Mon Feb 27 2006 Karsten Hopp <karsten@redhat.de> 20060124-3
- PreReq grep, coreutils (#182835)

* Tue Feb 14 2006 Karsten Hopp <karsten@redhat.de> 20060124-2
- make it build in chroots (#180561)

* Mon Feb 13 2006 Karsten Hopp <karsten@redhat.de> 20060124-1
- version 20060124

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 20050202-5.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Karsten Hopp <karsten@redhat.de> 20050202-5
- rebuild

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 20050202-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 02 2006 Karsten Hopp <karsten@redhat.de> 20050202-4
- fix uname -i output
- fix loop (*-path.patch)
- conflict pdksh instead of obsoleting it

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com> 20050202-3.1
- rebuilt for new gcj

* Tue May 10 2005 Karsten Hopp <karsten@redhat.de> 20050202-3
- enable debuginfo

* Tue Mar 15 2005 Karsten Hopp <karsten@redhat.de> 20050202-2
- add /usr/bin/ksh link for compatibility with pdksh scripts (#151134)

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 20050202-1 
- update and rebuild with gcc-4

* Tue Mar 01 2005 Karsten Hopp <karsten@redhat.de> 20041225-2 
- fix gcc4 build 

* Fri Jan 21 2005 Karsten Hopp <karsten@redhat.de> 20041225-1
- rebuild with new ksh tarball (license change)

* Tue Nov 02 2004 Karsten Hopp <karsten@redhat.de> 20040229-11
- disable ia64 for now

* Fri Oct 15 2004 Karsten Hopp <karsten@redhat.de> 20040229-9 
- rebuild

* Thu Sep 02 2004 Nalin Dahyabhai <nalin@redhat.com> 20040229-8
- remove '&' from summary

* Thu Sep 02 2004 Bill Nottingham <notting@redhat.com> 20040229-7
- obsolete pdksh (#131303)

* Mon Aug 02 2004 Karsten Hopp <karsten@redhat.de> 20040229-6
- obsolete ksh93, provide ksh93

* Mon Jul 05 2004 Karsten Hopp <karsten@redhat.de> 20040229-3 
- add /bin/ksh to /etc/shells

* Wed Jun 16 2004 Karsten Hopp <karsten@redhat.de> 20040229-2 
- add ppc64 patch to avoid ppc64 dot symbol problem

* Fri May 28 2004 Karsten Hopp <karsten@redhat.de> 20040229-1 
- initial version


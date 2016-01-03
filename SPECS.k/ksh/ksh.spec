%global       releasedate 20120801
%global       release_date %{lua:reldate=rpm.expand("%{releasedate}");print(("%s-%s-%s"):format(reldate:sub(0,4),reldate:sub(5,6),reldate:sub(7)))}

Name:         ksh
Summary:      The Original ATT Korn Shell
URL:          http://www.kornshell.com/
Group:        System Environment/Shells
#zlib is used for INIT.2010-02-02.tgz/src/cmd/INIT/ratz.c - used only for build tool
#CPL everywhere else (for KSH itself)
License:      CPL
Version:      %{releasedate}
Release:      28%{?dist}
Source0:      http://www.research.att.com/~gsf/download/tgz/ast-ksh.%{release_date}.tgz
Source1:      http://www.research.att.com/~gsf/download/tgz/INIT.%{release_date}.tgz
Source2:      kshcomp.conf
Source3:      kshrc.rhs
Source4:      dotkshrc

# expected results of test suite
Source5:      expectedresults.log

# don't use not wanted/needed builtins - Fedora/RHEL specific
Patch1:       ksh-20070328-builtins.patch

# fix regression test suite to be usable during packagebuild - Fedora/RHEL specific
Patch2:      ksh-20100826-fixregr.patch

# fedora/rhel specific, rhbz#619692
Patch6:       ksh-20080202-manfix.patch

# rhbz#702008
Patch17:      ksh-20100202-pathvar.patch

# rhbz#924440
Patch18:      ksh-20100621-fdstatus.patch

# fixes for regressions found in ksh-20120801 rebase
Patch19:      ksh-20120801-rmdirfix.patch
Patch20:      ksh-20120801-cdfix.patch
Patch21:      ksh-20120801-cdfix2.patch
Patch22:      ksh-20120801-tabfix.patch
Patch23:      ksh-20130214-fixkill.patch

# for ksh <= 2013-05-31, rhbz#960034
Patch24:      ksh-20120801-kshmfix.patch

# for ksh <= 2016-06-28, rhbz#921455
Patch25:      ksh-20120801-memlik.patch

# for ksh <= 2013-03-20, rhbz#922851
Patch26:      ksh-20120801-forkbomb.patch

# for ksh <= 2013-04-19, rhbz#913110
Patch27:      ksh-20120801-macro.patch

# not completely upstream yet, rhbz#858263
Patch29:      ksh-20130628-longer.patch

# for ksh <= 2013-07-19, rhbz#982142
Patch30: ksh-20120801-mlikfiks.patch

# not yet upstream, related to 2012-08-01 rebase
Patch31: ksh-20120801-covsfix.patch

# rhbz#1007816
Patch32: ksh-20100621-manfix3.patch

# rhbz#1016611
Patch33: ksh-20120801-nomulti.patch

# from upstream, rhbz#1036802
Patch34: ksh-20120801-fd2lost.patch

# for ksh <= 2014-01-14, rhbz#1036470
Patch35: ksh-20120801-memlik3.patch

# for ksh <= 2014-03-04, rhbz#1066589
Patch36: ksh-20120801-filecomsubst.patch

# for ksh <= 2014-04-05, rhbz#825520
Patch37: ksh-20120801-crash.patch

# for ksh < 2013-03-19, rhbz#1075635
Patch38: ksh-20120801-sufix.patch

# for ksh < 2014-03, rhbz#1047506
Patch39: ksh-20120801-argvfix.patch

# sent upstream, rhbz#1078698
Patch40: ksh-20140301-fikspand.patch

# for ksh < 2014-04-15, rhbz#1070350
Patch41: ksh-20120801-roundit.patch

# for ksh < 2014-04-15, rhbz#1036931
Patch42: ksh-20120801-heresub.patch

# not included upstream yet, rhbz#1062296
Patch43: ksh-20140415-hokaido.patch

# for ksh < 20121004, rhbz#1083713
Patch44: ksh-20120801-tpstl.patch

# for ksh <= 20120214, rhbz#1023109
Patch45: ksh-20120801-mtty.patch

# sent upstream, rhbz#1019334
Patch46: ksh-20120801-manfix4.patch

# not upstream yet, rhbz#1105138
Patch47: ksh-20120801-fununset.patch

# not upstream yet, rhbz#1102627
Patch48: ksh-20120801-cdfix3.patch

# sent upstream, rhbz#1112306
Patch49: ksh-20120801-locking.patch

# for ksh <= 2013-06-13, rhbz#1133582
Patch50: ksh-20130613-cdfix4.patch
Patch51: ksh-20120801-retfix.patch

# not upstream yet, rhbz#1147645
Patch52: ksh-20120801-oldenvinit.patch

# not upstream yet, rhbz#1160923
Patch53: ksh-20120801-noexeccdfix.patch

# sent upstream, for ksh <= 2014-09-30, rhbz#1168611
Patch54: ksh-20120801-cdfork.patch

# from upsteam, for ksh < 2012-10-04, rhbz#1173668
Patch55: ksh-20120801-emptyarrayinit.patch

# not upstream yet, rhbz#1188377
Patch56: ksh-20120801-xufix.patch

# sent upstream, for ksh <= 2015-02-10, rhbz#1189294
Patch57: ksh-20120801-assoc-unset-leak.patch

# sent upstream, for ksh <= 2014-12-18, rhbz#1176670
Patch58: ksh-20120801-alarmifs.patch

# not yet upstream, rhbz#1116072
Patch59: ksh-20140929-safefd.patch

# workaround, for ksh < 2013-05-24, rhbz#1117404
Patch60: ksh-20120801-trapcom.patch

# for ksh <= 2013-04-09, rhbz#960371
Patch61: ksh-20120801-lexfix.patch
Patch62: ksh-20140801-arraylen.patch
Patch63: ksh-20120801-diskfull.patch
Patch64: ksh-20120801-nohupfork.patch

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
%patch6 -p1 -b .manfix
%patch17 -p1 -b .pathvar
%patch18 -p1 -b .fdstatus
%patch19 -p1 -b .rmdirfix
%patch20 -p1 -b .cdfix
%patch21 -p1 -b .cdfix2
%patch22 -p1 -b .tabfix
%patch23 -p1 -b .fixkill
%patch24 -p1 -b .kshmfix
%patch25 -p1 -b .memlik
%patch26 -p1 -b .forkbomb
%patch27 -p1 -b .macro
%patch29 -p1 -b .longer
%patch30 -p1 -b .mlikfiks
%patch31 -p1 -b .covsfix
%patch32 -p1 -b .manfix3
%patch33 -p1 -b .nomulti
%patch34 -p1 -b .fd2lost
%patch35 -p1 -b .memlik3
%patch36 -p1 -b .filecomsubst
%patch37 -p1 -b .crash
%patch38 -p1 -b .sufix
%patch39 -p1 -b .argvfix
%patch40 -p1 -b .fikspand
%patch41 -p1 -b .roundit
%patch42 -p1 -b .heresub
%patch43 -p1 -b .hokaido
%patch44 -p1 -b .tpstl
%patch45 -p1 -b .mtty
%patch46 -p1 -b .manfix4
%patch47 -p1 -b .fununset
%patch48 -p1 -b .cdfix3
%patch49 -p1 -b .locking
%patch50 -p1 -b .cdfix4
%patch51 -p1 -b .retfix
%patch52 -p1 -b .oldenvinit
%patch53 -p1 -b .noexeccdfix
%patch54 -p1 -b .cdfork
%patch55 -p1 -b .emptyarrayinit
%patch56 -p1 -b .xufix
%patch57 -p1 -b .assoc-unset-leak
%patch58 -p1 -b .alarmifs
%patch59 -p1 -b .safefd
%patch60 -p1 -b .trapcom
%patch61 -p1 -b .lexfix
%patch62 -p1 -b .arraylen
%patch63 -p1 -b .diskfull
%patch64 -p1 -b .nohupfork

#/dev/fd test does not work because of mock
sed -i 's|ls /dev/fd|ls /proc/self/fd|' src/cmd/ksh93/features/options

# sh/main.c was not using CCFLAGS
sed -i '/-c sh\/main.c/s|${mam_cc_FLAGS} |${mam_cc_FLAGS} ${CCFLAGS} |p' src/cmd/ksh93/Mamfile

# disable register for debugging
sed -i 1i"#define register" src/lib/libast/include/ast.h

%build
XTRAFLAGS=""
for f in -Wno-unknown-pragmas -Wno-missing-braces -Wno-unused-result -Wno-return-type -Wno-int-to-pointer-cast -Wno-parentheses -Wno-unused -Wno-unused-but-set-variable -Wno-cpp -P
do
  gcc $f -E - </dev/null >/dev/null 2>&1 && XTRAFLAGS="$XTRAFLAGS $f"
done
./bin/package
./bin/package make mamake ||:
./bin/package make mamake ||:
export CCFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing $XTRAFLAGS"
export CC=gcc
./bin/package make -S

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
[ -f ./skipcheck -o -f ./../skipcheck ] && exit 0 ||:
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
ls core.* 2>/dev/null ||:
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
* Thu Aug 27 2015 Michal Hlavinka <mhlavink@redhat.com> - 20120801-28
- fix: in a login shell "( cmd & )" does nothing (#1217238)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120801-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 06 2015 Michal Hlavinka <mhlavink@redhat.com> - 20120801-26
- do not crash, when disk is full, report an error (#1212994)

* Tue Apr 07 2015 Michal Hlavinka <mhlavink@redhat.com> - 20120801-25
- using trap DEBUG could cause segmentation fault

* Mon Mar 30 2015 Michal Hlavinka <mhlavink@redhat.com> - 20120801-24
- cd builtin could break IO redirection
- fix segfault when handling a trap
- exporting fixed with variable corrupted its data
- and more fixes

* Fri Mar 06 2015 Michal Hlavinka <mhlavink@redhat.com> - 20120801-23
- exporting fixed with variable corrupted its data (#1192027)

* Fri Feb 27 2015 Michal Hlavinka <mhlavink@redhat.com> - 20120801-22
- ksh hangs when command substitution containing a pipe fills out the pipe buffer (#1121204)

* Tue Aug 26 2014 Michal Hlavinka <mhlavink@redhat.com> - 20120801-21
- cd builtin file descriptor operations messed with IO redirections (#1133586)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120801-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Michal Hlavinka <mhlavink@redhat.com> - 20120801-19
- fix segfault in job list code
- do not resend signal on termination (#1092132)
- fix brace expansion on/off
- fix incorrect rounding of numsers 0.5 < |x| <1.0 in printf (#1080940)
- fix parser errors related to the end of the here-document marker
- ksh hangs when command substitution fills out the pipe buffer
- using typeset -l with a restricted variabled caused segmentation fault
- monitor mode was documented incorrectly
- do not crash when unsetting running function from another one (#1105139)
- should report an error when trying to cd into directory without execution bit
- job locking mechanism did not survive compiler optimization
- reading a file via command substitution did not work when any of stdin,
  stdout or stderr were closed (#1070308)
- fix lexical parser crash

* Tue Jun 10 2014 Michal Hlavinka <mhlavink@redhat.com> - 20120801-18
- fix FTBFS(#1107070)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120801-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 11 2014 Michal Hlavinka <mhlavink@redhat.com> - 20120801-16
- ksh could hang when command substitution printed too much data

* Thu Feb 06 2014 Michal Hlavinka <mhlavink@redhat.com> - 20120801-15
- fix lexical parser crash (#960371)

* Fri Jan 17 2014 Michal Hlavinka <mhlavink@redhat.com> - 20120801-14
- fix overflow in subshell loop

* Mon Jan 06 2014 Michal Hlavinka <mhlavink@redhat.com> - 20120801-13
- fix argv rewrite (#1047508)

* Wed Oct 30 2013 Michal Hlavinka <mhlavink@redhat.com> - 20120801-12
- ksh stops on read when monitor mode is enabled

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120801-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 12 2013 Michal Hlavinka <mhlavink@redhat.com> - 20120801-10
- fix memory leak

* Mon Jun 10 2013 Michal Hlavinka <mhlavink@redhat.com> - 20120801-9
- monitor mode in scripts wasn't working

* Thu Mar 07 2013 Michal Hlavinka <mhlavink@redhat.com> - 20120801-8
- fix another reproducer for tab completion

* Fri Feb 22 2013 Michal Hlavinka <mhlavink@redhat.com> - 20120801-7
- do not segfault on kill % (#914669)

* Fri Feb 01 2013 Michal Hlavinka <mhlavink@redhat.com> - 20120801-6
- cd file did not produce any error

* Fri Jan 25 2013 Michal Hlavinka <mhlavink@redhat.com> - 20120801-5
- ksh could not enter directories with path containing /.something (#889748)
- file name autocomplete prevented following numeric input (#889745)

* Wed Nov 21 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120801-4
- bind Home, End, Delete,... key correctly for emacs mode
- do not crash when executed from deleted directory

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

* Wed Jan 21 2009 Michal Hlavinka <mhlavink@redhat.com> 20081104-1
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


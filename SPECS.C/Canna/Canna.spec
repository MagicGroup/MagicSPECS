%global pubdicrhver 20021028
%global zipcodever 20030204
%global cannadicver 0.95c
%global cannadir Canna37p3
%global username      canna
%global homedir       %{_localstatedir}/lib/%{username}
%global gecos         Canna Service User
%global _hardened_build 1

Summary: A Japanese character set input system.
Summary(zh_CN.UTF-8): 日文输入系统
Name: Canna
Version: 3.7p3
Release: 42%{?dist}
# lib/RKindep/cksum.c is licensed under 4-clause BSD, otherwise MIT.
License: MIT and BSD with advertising
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.nec.co.jp/japanese/product/computer/soft/canna/
Source0: http://osdn.dl.sourceforge.jp/canna/9565/%{cannadir}.tar.bz2
Source1: http://cannadic.oucrc.org/cannadic-%{cannadicver}.tar.gz
Source2: pubdic-bonobo-%{pubdicrhver}.tar.bz2
# Dead link? it seems.
#Source3: http://www.coolbrain.net/dl/shion/shion.tar.gz
Source3: shion.tar.gz
# Source4: http://bonobo.gnome.gr.jp/~nakai/canna/zipcode-%{zipcodever}.tar.bz2
Source4: zipcode-%{zipcodever}.tar.bz2
Source21: dot-canna
Source22: cannaping.c
Source30: canna-tmpfiles.conf
Source31: canna.service

Patch0: Canna-conf.patch
Patch2: Canna-3.6-sharedir.patch
Patch4: Canna-3.6-dont-grab-ctrl-o.patch
Patch5: Canna-3.6-fix-warnings.patch
## some dictionaries were ported from SKK-JISYO.*
Patch17: skk-dictionaries.patch
Patch18: Canna-3.6-cannadic.patch
Patch19: Canna-3.6-shion.patch
Patch21: Canna-3.6-bonobo.patch
# Fix for buffer overrun
Patch23: Canna-3.6-wconv.patch
Patch25: Canna-x86_64.patch
Patch27: Canna-3.7p1-notimeout.patch
Patch28: Canna-oldsock.patch
# Patch from the upstream
Patch40: Canna-3.7p1-fix-duplicated-strings.patch
Patch41: Canna-3.7p3-yenbs.patch
Patch42: Canna-3.7p3-redecl.patch
Patch43: Canna-3.7p3-fix-gcc4-warning.patch
Patch44: Canna-3.7p3-no-strip.patch
Patch45: %{name}-3.7p3-fix-format.patch
Patch50: %{name}-aarch64.patch

Requires(pre): shadow-utils
Requires(post): /bin/grep /etc/services /sbin/chkconfig %{__chown} systemd-units
Requires(preun): /sbin/service systemd-units
Requires(postun): /sbin/service systemd-units
Requires: initscripts
BuildRequires: cpp gawk systemd-units
BuildRequires: imake >= 1.0.1-3
Obsoletes: tamago

%description
Canna provides a user interface for inputting Japanese characters.
Canna supports Nemacs (Mule), kinput2, and canuum. All of these tools
can then use a single customization file, Romaji-to-Kana conversion
rules and dictionaries, and input Japanese in the same way. Canna
automatically supports Kana-to-Kanji conversions; the conversions are
based on a client-server model.

%description -l zh_CN.UTF-8
日文输入系统。

%package devel
Summary: Header file and library for developing programs which use Canna.
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: Canna-libs >= %{version}-%{release}

%package libs
Summary: The runtime library for Canna.
Summary(zh_CN.UTF-8): %{name} 的运行库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description devel
The Canna-devel package contains the development files needed to build
programs that will use the Canna Japanese character input system.

%description devel -l zh_CN.UTF-8
%{name} 的开发库。

%description libs
The Canna-libs package contains the runtime library for running
programs with the Canna Japanese input system.

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%prep
%setup -q -c -a 1 -a 2 -a 3 -a 4
cd %{cannadir}
%patch0 -p1 -b .conffix
%patch2 -p1 -b .share
%patch4 -p1 -b .ctrl-o
%patch5 -p1 -b .warnings
%patch17 -p1 -b .skk
%patch18 -p1 -b .cannadic
%patch19 -p1 -b .shion
%patch21 -p1 -b .bonobo
%patch23 -p1 -b .wconv
%ifarch x86_64
%patch25 -p1 -b .x86_64
%endif
%patch27 -p1 -b .notimeout
%patch28 -p1 -b .oldsock
%patch40 -p1 -b .duplicate
%patch41 -p1 -b .yenbs
%patch42 -p1 -b .redecl
%patch43 -p1 -b .gcc4
%patch44 -p1 -b .no-strip
%patch45 -p1 -b .format
cd ..
%patch50 -p1 -b .aarch64

for file in %{cannadir}/{cmd/mkromdic/mkromdic.man,lib/RK/RkIntro.man}; do
	iconv -f euc-jp -t utf-8 < "$file" > "${file}_"
	touch -r $file "${file}_"
	mv "${file}_" "$file"
done

cat $RPM_BUILD_DIR/Canna-%{version}/zipcode-%{zipcodever}/zipcode.t \
	$RPM_BUILD_DIR/Canna-%{version}/zipcode-%{zipcodever}/jigyosyo.t | sort \
	> $RPM_BUILD_DIR/Canna-%{version}/%{cannadir}/dic/ideo/words/zipcode.t

cat $RPM_BUILD_DIR/Canna-%{version}/pubdic-bonobo/*.p | sort >> \
	$RPM_BUILD_DIR/Canna-%{version}/%{cannadir}/dic/ideo/pubdic/y.p

# find CVS files and remove it.
find $RPM_BUILD_DIR/%{name}-%{version} -name .cvsignore -exec rm -f {} \;

%build
export RPM_OPT_FLAGS="$RPM_OPT_FLAGS %{__global_ldflags}"

function builddic() {
  dic=$1
  dicname=`echo $dic | sed -e 's/\(.*\)\..*\$/\1/'`
  case $2 in
    mwd)
      mode="mwd";
      flag="-m";
      ;;
    swd)
      mode="swd";
      flag="-s";
      ;;
    *)
      echo "unknown dictionary type: $2";
      exit 1;
      ;;
  esac
  export buildcannadir=$RPM_BUILD_DIR/%{name}-%{version}/%{cannadir}
  if [ "x$3" = "xsort" ]; then
    $buildcannadir/cmd/splitwd/splitword $dic | $buildcannadir/cmd/forsort/forsort -7 | sort | $buildcannadir/cmd/forsort/forsort -8 | $buildcannadir/cmd/mergewd/mergeword > $dicname.$mode
  else
    cat $dic > $dicname.$mode
  fi
  $buildcannadir/cmd/crxdic/crxdic -D $buildcannadir/dic/ideo/grammar/cnj.bits $flag -o $dicname.cbd -n $dicname $dicname.$mode
  $buildcannadir/cmd/crfreq/crfreq -div 512 -o $dicname.cld $dicname.cbd $dicname.$mode
  rm $dicname.$mode
}

cd %{cannadir}
xmkmf
make Makefile
pushd lib/canna
xmkmf
make sglobal.h
popd
find . -name Makefile | xargs sed -i -e 's/^\(\s*CDEBUGFLAGS\s*=.*\)/\1 $(RPM_OPT_FLAGS)/'
%ifarch ia64
sed -i -e 's/-O2//' Makefile
%endif
# ugly hack to avoid X.Org: no such file or directory issue
sed -i -e 's/$(VENDOR_DEFINES)//' Makefile
make canna
gcc $RPM_OPT_FLAGS -o ./misc/cannaping %{SOURCE22} -I./include -L./lib/canna -lcanna
cd ..

cd cannadic-%{cannadicver}
for i in $RPM_BUILD_DIR/Canna-%{version}/%{cannadir}/cmd/*; do \
if [ -d $i ]; then \
  export PATH=$PATH:$i; \
fi \
done;
export RPM_CANNAIDEO_DIR=$RPM_BUILD_DIR/Canna-%{version}/%{cannadir}/dic/ideo
export RPM_CANNACMD_DIR=$RPM_BUILD_DIR/Canna-%{version}/%{cannadir}/cmd
export RPM_CANNA_POD=$RPM_BUILD_DIR/Canna-%{version}/%{cannadir}/dic/ideo/pubdic/pod
builddic gcanna.ctd mwd none
builddic gcannaf.ctd swd none
cd ..

cd pubdic-bonobo
cat *.p | $RPM_CANNA_POD - -p -i -2 > bonobo.spl
$RPM_CANNACMD_DIR/mergewd/mergeword< bonobo.spl > bonobo.t
rm -rf bonobo.spl
builddic bonobo.t mwd sort
cd ..

cd shion
builddic basho.ctd mwd sort
builddic keisan.ctd mwd sort
builddic pub.ctd mwd sort
builddic scien.ctd mwd none
builddic sup.ctd mwd sort
cd ..

%install
cd %{cannadir}
make libCannaDir=%{_libdir} DESTDIR=$RPM_BUILD_ROOT install
make DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir} MANSUFFIX=1 LIBMANSUFFIX=3 install.man
for i in `find $RPM_BUILD_ROOT%{_mandir}/ja -type f`; do
	iconv -f euc-jp -t utf-8 $i > $i.new && touch -r $i $i.new && mv -f $i.new $i && chmod 444 $i
done
install -p -m755 ./misc/cannaping $RPM_BUILD_ROOT%{_bindir}/cannaping
install -d -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d
install -p -m 0644 %{SOURCE30} $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d/%{name}.conf
cd ..

cd %{cannadir}
mv misc/manual.sed .
rm -fr misc
mkdir misc
mv manual.sed misc
cd ..

cd cannadic-%{cannadicver}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/canna/dic/canna
install -p -m 644 gcanna*.c[bl]d \
	$RPM_BUILD_ROOT%{_localstatedir}/lib/canna/dic/canna
cd ..

cd pubdic-bonobo
install -p -m 644 bonobo*.c[bl]d \
        $RPM_BUILD_ROOT%{_localstatedir}/lib/canna/dic/canna
cd ..

cd shion
install -p -m 644 basho.cld basho.cbd kaom.ctd keisan.cld keisan.cbd \
	pub.cld pub.cbd scien.cld scien.cbd sup.cld sup.cbd \
	$RPM_BUILD_ROOT%{_localstatedir}/lib/canna/dic/canna
cd ..

mkdir -p $RPM_BUILD_ROOT/etc/skel
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -p -m 0644 %SOURCE21 $RPM_BUILD_ROOT/etc/skel/.canna
install -p -m 0644 %SOURCE21 $RPM_BUILD_ROOT/etc/canna/default.canna
install -p -m 0644 %SOURCE31 $RPM_BUILD_ROOT%{_unitdir}/canna.service
## chmod 755 $RPM_BUILD_ROOT/etc/rc.d/init.d/canna

cat > $RPM_BUILD_ROOT%{_sysconfdir}/hosts.canna << EOF
unix
EOF

cat > $RPM_BUILD_ROOT%{_sysconfdir}/canna/cannahost << EOF
unix
EOF

for bin in addwords cpdic delwords lsdic mkdic mvdic rmdic syncdic ; do
	ln -sf catdic $RPM_BUILD_ROOT%{_bindir}/${bin}
done
ln -sf ../bin/catdic $RPM_BUILD_ROOT%{_sbindir}/cannakill

mv $RPM_BUILD_ROOT%{_sysconfdir}/canna/sample $RPM_BUILD_DIR/%{name}-%{version}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/.iroha_unix

# remove the static libraries
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.a


%triggerun -- Canna < 3.7p3-33
/usr/bin/systemd-sysv-convert --save canna >/dev/null 2>&1 || :
/sbin/chkconfig --del canna >/dev/null 2>&1 || :
/bin/systemctl try-restart canna.service >/dev/null 2>&1 || :

%pre
getent group %{username} >/dev/null || groupadd -r %{username}
getent passwd %{username} >/dev/null || useradd -r -g %{username} -d %{homedir} -s /sbin/nologin -c '%{gecos}' %{username}
exit 0

%post
if ! grep -q canna /etc/services
then
	echo "canna		5680/tcp" >>/etc/services
fi
%{__chown} -R %{username}:%{username} %{_localstatedir}/lib/canna
%systemd_post canna.service

%preun
%systemd_preun canna.service

%postun
%systemd_postun_with_restart canna.service

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%lang(ja) %doc %{cannadir}/CHANGES.jp %{cannadir}/OCHANGES.jp
%lang(ja) %doc %{cannadir}/README.jp %{cannadir}/RKCCONF.jp %{cannadir}/WHATIS.jp
%doc %{cannadir}/ChangeLog %{cannadir}/README %{cannadir}/WHATIS
%doc %{cannadir}/Canna.conf
%doc $RPM_BUILD_DIR/%{name}-%{version}/sample
%config %{_sysconfdir}/skel/.canna
%config(noreplace) %{_sysconfdir}/hosts.canna
%config(noreplace) %{_sysconfdir}/canna/cannahost
%dir %{_sysconfdir}/canna
%config %{_sysconfdir}/canna/default.canna
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%{_bindir}/*
%{_datadir}/canna
%{_mandir}/man1/*
%lang(ja) %{_mandir}/ja/man1/*
%defattr (0755,root,root)
%{_sbindir}/cannaserver
%{_sbindir}/cannakill
%defattr (-,%{username},%{username})
%dir %{_localstatedir}/run/.iroha_unix
%{_localstatedir}/lib/canna
%{_localstatedir}/log/canna
%{_unitdir}/canna.service

%files devel
%{_includedir}/canna/
%{_mandir}/man3/*
%lang(ja) %{_mandir}/ja/man3/*
%{_libdir}/libRKC.so
%{_libdir}/libRKC16.so
%{_libdir}/libcanna.so
%{_libdir}/libcanna16.so


%files libs
%{_libdir}/libRKC.so.*
%{_libdir}/libRKC16.so.*
%{_libdir}/libcanna.so.*
%{_libdir}/libcanna16.so.*

%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 3.7p3-42
- 为 Magic 3.0 重建

* Tue Dec 10 2013 Akira TAGOH <tagoh@redhat.com> - 3.7p3-41
- Fix an error when building with -Werror=format-security. (#1037008)

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7p3-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun  3 2013 Akira TAGOH <tagoh@redhat.com> - 3.7p3-39
- Built with PIE enabled. (Dhiru Kholia, #955179)

* Tue Mar 26 2013 Akira TAGOH <tagoh@redhat.com> - 3.7p3-38
- Rebuilt for aarch64 support (#925129)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7p3-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 27 2012 Akira TAGOH <tagoh@redhat.com> - 3.7p3-36
- Update scriptlets with new systemd rpm macros. (#850054)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7p3-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7p3-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Akira TAGOH <tagoh@redhat.com> - 3.7p3-33
- Add native systemd service. (#754826)

* Fri Feb 24 2011 Akira TAGOH <tagoh@redhat.com> - 3.7p3-32
- Do not strip symbols from binaries.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7p3-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Akira TAGOH <tagoh@redhat.com> - 3.7p3-30
- tmpfiles.d support for /var/run/.iroha_unix. (#656555)
- clean up the spec file.

* Mon Jan 18 2010 Akira TAGOH <tagoh@redhat.com> - 3.7p3-29
- Remove the static libraries. (#556034)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7p3-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7p3-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 21 2008 Akira TAGOH <tagoh@redhat.com> - 3.7p3-26
- Fix a source URL.

* Mon Sep  1 2008 Akira TAGOH <tagoh@redhat.com> - 3.7p3-25
- skk-dictionaries.patch: Updated.

* Tue Apr  8 2008 Akira TAGOH <tagoh@redhat.com> - 3.7p3-24
- Don't start the service by default. (#441276)

* Tue Feb 12 2008 Akira TAGOH <tagoh@redhat.com> - 3.7p3-23
- Rebuild for gcc-4.3.

* Tue Oct 30 2007 Akira TAGOH <tagoh@redhat.com> - 3.7p3-22
- Remove the dead link.

* Tue Aug 14 2007 Akira TAGOH <tagoh@redhat.com> - 3.7p3-21
- Update the user and the group handling.

* Mon Aug 13 2007 Akira TAGOH <tagoh@redhat.com> - 3.7p3-20
- Follow UserCreation documentation to have canna user. (#223838)

* Sat Aug 11 2007 Akira TAGOH <tagoh@redhat.com> - 3.7p3-19
- Update an initscript with LSB standard (#246886)

* Fri Aug 10 2007 Akira TAGOH <tagoh@redhat.com>
- Update License tag.

* Tue Mar 27 2007 Akira TAGOH <tagoh@redhat.com> - 3.7p3-18
- Fix missing directory owner. (#233779)

* Tue Feb 13 2007 Akira TAGOH <tagoh@redhat.com> - 3.7p3-17
- cleanups spec file.
- Build with RPM_OPT_FLAGS (#227378)

* Mon Sep 11 2006 Akira TAGOH <tagoh@redhat.com> - 3.7p3-16
- rebuilt

* Wed Jan 25 2006 Akira TAGOH <tagoh@redhat.com> - 3.7p3-15
- BuildRequires imake instead of XFree86-devel. (#178656)

* Mon Sep 26 2005 Akira TAGOH <tagoh@redhat.com> - 3.7p3-14
- Imported into Extras.

* Mon Mar  7 2005 Akira TAGOH <tagoh@redhat.com> - 3.7p3-13
- stop to sort the words on some dictionaries during making the binary
  dictionaries.

* Wed Mar  2 2005 Akira TAGOH <tagoh@redhat.com> - 3.7p3-12
- rebuild for gcc4.
- Canna-3.7p3-fix-gcc4-warning.patch: applied to fix more compiler warnings.

* Tue Feb 22 2005 Akira TAGOH <tagoh@redhat.com> - 3.7p3-11
- updates to cannadic-0.95c

* Mon Jan  3 2005 Bill Nottingham <notting@redhat.com> - 3.7p3-10
- don't use initlog

* Tue Nov 23 2004 Miloslav Trmac <mitr@redhat.com> - 3.7p3-9
- Convert man pages to UTF-8
- Don't use Yen symbol instead of backspace in RkGetDicList man page
- Fix build failure when redeclaring glibc functions

* Thu Nov  4 2004 Akira TAGOH <tagoh@redhat.com> - 3.7p3-8
- rebuilt

* Thu Oct 21 2004 Akira TAGOH <tagoh@redhat.com> - 3.7p3-7
- dot.canna: assigned quit to Escape key to escape with Escape key from
  the mode. (#135039)

* Tue Sep 21 2004 Warren Togami <wtogami@redhat.com> - 3.7p3-6
- remove unnecessary docs

* Wed Sep 08 2004 Akira TAGOH <tagoh@redhat.com> 3.7p3-5
- fixed default.canna to get usability and improve the default behavior without
  proper .canna file.
  NOTE: you must always have proper .canna file however, since your .canna file
  is prior than the default behavior and it probably overrides the default thing.

* Thu Jun 24 2004 Akira TAGOH <tagoh@redhat.com> 3.7p3-4
- Canna-conf.patch: updated to change the socket file directory under /var/run.
- Canna-oldsock.patch: applied to ensure that restarting the daemon works during upgrading.
- made /var/run/.iroha_unix at the build time.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Jun 06 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- use /var/lib/canna in filelist to also include that dir
  in the rpm listing and set proper ownership from rpm and
  not only via the post script

* Mon May 24 2004 Akira TAGOH <tagoh@redhat.com> 3.7p3-1
- New upstream release.
- Canna-3.7p1-pod-fix-wrongparam.patch: removed.

* Wed Apr 14 2004 Akira TAGOH <tagoh@redhat.com> 3.7p1-7
- updates cannadic-0.95b

* Sun Mar 21 2004 Florian La Roche <Florian.LaRoche@redhat.de> 3.7p1-6
- apps owned by root instead of bin

* Wed Mar 17 2004 Akira TAGOH <tagoh@redhat.com> 3.7p1-5
- Canna-3.7p1-fix-duplicated-strings.patch: applied a backport patch from CVS.
  when the characters like 'bbb...' is deleted, the preedit strings is
  duplicated. (#117140)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com> 3.7p1-4.1
- rebuilt

* Thu Feb 19 2004 Akira TAGOH <tagoh@redhat.com> 3.7p1-4
- Canna-3.7p1-notimeout.patch: applied to avoid cant-mount-the-dictionaries issue. (#114886)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 14 2004 Akira TAGOH <tagoh@redhat.com> 3.7p1-2
- fix broken dictionaries on ia64.
- Canna-3.7p1-pod-fix-wrongparam.patch: applied to fix the wrong function parameter. (#113662)

* Fri Jan 09 2004 Akira TAGOH <tagoh@redhat.com> 3.7p1-1
- New upstream release.

* Mon Dec 24 2003 Akira TAGOH <tagoh@redhat.com> 3.7-1
- New upstream release.
- Canna-3.6-cannadic.patch: updated to fix the warning.
- Canna-3.6-fix-warnings.patch: updated.
- Canna-3.6-sleep.patch: removed because it's unnecessary anymore.
- Canna-3.6-fix-ia64-unaligned-access.patch: removed. should be unnecessary.
- canna.init: correct path for cannakill.
- dot-canna: re-enabled fuzokugo entry.

* Wed Dec 10 2003 Akira TAGOH <tagoh@redhat.com> 3.6-25
- updated to cannadic-0.95a

* Fri Oct 10 2003 Akira TAGOH <tagoh@redhat.com> 3.6-24
- Canna-3.6-fix-ia64-unaligned-access.patch: fixed unaligned access on ia64. (#101762)

* Tue Sep 30 2003 Akira TAGOH <tagoh@redhat.com> 3.6-22
- converted Japanese manpages to UTF-8.

* Wed Sep 24 2003 Akira TAGOH <tagoh@redhat.com> 3.6-21
- updates to Canna-3.6p4
- Canna-3.6-fix-segv-amd64.patch: removed.
- dot-canna: comment "fuzokugo" dictionary out. it isn't contained anymore.

* Wed Sep 17 2003 Akira TAGOH <tagoh@redhat.com> 3.6-20.1
- rebuilt

* Wed Sep 17 2003 Akira TAGOH <tagoh@redhat.com> 3.6-20
- Canna-3.6-fix-segv-amd64.patch: applied to fix segfault on x86-64. (#104539)

* Wed Jul 09 2003 Akira TAGOH <tagoh@redhat.com> 3.6-19
- updates to cannadic-0.95

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 23 2003 Akira TAGOH <tagoh@redhat.com> 3.6-17
- updates to cannadic-0.94g

* Mon Apr 21 2003 Akira TAGOH <tagoh@redhat.com> 3.6-16
- rebuild.

* Mon Apr 21 2003 Akira TAGOH <tagoh@redhat.com> 3.6-15
- Canna-3.6-dont-grab-ctrl-o.patch: applied to not grab ctrl-o. (#75865)
- Canna-3.6-fix-warnings.patch: applied to fix some compiler warnings. (#80639)

* Tue Apr 01 2003 Akira TAGOH <tagoh@redhat.com> 3.6-14
- don't ship .cvsignore files.

* Tue Mar 25 2003 Akira TAGOH <tagoh@redhat.com> 3.6-13
- updates to 3.6p3
- clean up
- Canna-3.6-Imakefile.patch: removed an unnecessary patch.
- Canna-3.6-sharedir.patch: find the dictionary files from /usr/share/canna
- Canna-3.6-sleep.patch: to fix very strange problem. when the child process
  tries to kill the parent process, the parent process isn't terminated, and
  it seems that the parent process doesn't still return from fork() and waiting
  on SYS_futex.
- moved cannahost and default.canna to /etc/canna so that config files should be
  moved on /etc.
- moved sample files to /usr/share/doc/Canna-<version>/

* Tue Feb  4 2003 Yukihiro Nakai <ynakai@redhat.com> 3.6-9
- Add cannaping command for init script (#82163)
- Update canna init script (#82163)

* Thu Jan 23 2003 Tim Powers <timp@redhat.com> 3.6-8
- rebuild

* Sat Dec 21 2002 Yukihiro Nakai <ynakai@redhat.com> 3.6-7
- Change shell to /sbin/nologin (#80175)

* Thu Dec 12 2002 Yukihiro Nakai <ynakai@redhat.com> 3.6-5
- Update to 3.6p1

* Thu Nov 28 2002 Yukihiro Nakai <ynakai@redhat.com> 3.6-4
- Disable -O2 on ia64

* Wed Nov 27 2002 Yukihiro Nakai <ynakai@redhat.com> 3.6-3
- Update bonobo
- Update zipcode
- Update cannadic

* Tue Nov 19 2002 Yukihiro Nakai <ynakai@redhat.com> 3.6-1
- Update to 3.6

* Tue Nov 12 2002 Elliot Lee <sopwith@redhat.com> 3.5b2-71
- Remove/fix ldconfig usage in scripts
- _smp_mflags
- Rebuild

* Mon Nov 11 2002 Yukihiro Nakai <ynakai@redhat.com> 3.5b2-70.8.0.1
- Add CANNA-2002-01 patch

* Fri Nov 01 2002 Yukihiro Nakai <ynakai@redhat.com> 3.5b2-70.8.0
- Add wconvert.c buffer overrun fix patch

* Tue Aug 06 2002 Yukihiro Nakai <ynakai@redhat.com> 3.5b2-70
- Delete -inet option from canna.init script (#67217)
- Obsolete tamago with this version (#67217)
- Delete localhost from /etc/hosts.canna

* Fri Aug 02 2002 Yukihiro Nakai <ynakai@redhat.com> 3.5b2-69
- Update zipcode
- Update pubdic-bonobo

* Thu Jul 18 2002 Akira TAGOH <tagoh@redhat.com> 3.5b2-68
- Canna-3.5b2-nonstrip.patch: applied to fix the stripped binary.

* Tue Jul 09 2002 Yukihiro Nakai <ynakai@redhat.com>
- Update zipcode
- Update pubdic-bonobo
- Update Cannadic

* Thu Jun 27 2002 Yukihiro Nakai <ynakai@redhat.com>
- Make users at install(%%pre) (#66306)

* Wed Jun 26 2002 Yukihiro Nakai <ynakai@redhat.com>
- Update pubdic-bonobo

* Thu Jun 06 2002 Yukihiro Nakai <ynakai@redhat.com>
- Update pubdic-bonobo
- Update zipcode

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Mar 28 2002 Yukihiro Nakai <ynakai@redhat.com> 3.5b2-62
- Update cannadic to 0.94b to fix pubdic wrong entry
- Update pubdic-bonobo
- Remove refer to pubdic
- celebrate pubdic-bonobo indepence day

* Tue Feb 26 2002 Yukihiro Nakai <ynakai@redhat.com> 3.5b2-61
- Update cannadic to 0.94

* Wed Jan 30 2002 Yukihiro Nakai <ynakai@redhat.com> 3.5b2-58
- Update zipcode dic
- Update pubdic-bonobo

* Mon Jan 21 2002 Yukihiro Nakai <ynakai@redhat.com> 3.5b2-56
- Update pubdic-bonobo(renamed from pubdic-redhat)

* Sat Jan 12 2002 Yukihiro Nakai <ynakai@redhat.com> 3.5b2-55
- Minor fix for shion
- Update cannadic to 0.93

* Wed Jan  9 2002 Yukihiro Nakai <ynakai@redhat.com> 3.5b2-52
- %%doc fix
- Add pubdic-redhat
- Add dictionary 'shion'

* Sun Jan  6 2002 Yukihiro Nakai <ynakai@redhat.com> 3.5b2-51
- Add cannadic, GPL dictionary

* Thu Aug 30 2001 Yukihiro Nakai <ynakai@redhat.com>
- Set -inet option by default in canna init script and add localhost
  to hosts.canna. It affects to tamago/emacs problem(#52886)

* Wed Aug 29 2001 Yukihiro Nakai <ynakai@redhat.com>
- Apply patch3 in all case

* Thu Aug 23 2001 Jens Petersen <petersen@redhat.com> - 3.5b2-48
- Add defattr before /var/lib/canna, so that files therein not made executable.

* Wed Aug 22 2001 SATO Satoru <ssato@redhat.com> - 3.5b2-47
- cleaned up SPEC (remove meaningless 'Prefix:' tag, use macros, etc.)
- added BuildPrereq: XFree86-devel (xmkmf)
- added some dictionaries ported from skk (#52248)
- added %%config(noreplace) /var/lib/canna/cannahost

* Tue Aug 21 2001 Yukihiro Nakai <ynakai@redhat.com> - 3.5b2-46
- Build fix with (#52088)

* Wed Aug 15 2001 Jens Petersen <petersen@redhat.com> - 3.5b2-45
- Added patch by Ishikawa to make cannaserver listen only on a unix domain
  socket by default (#33420) and create "/var/lib/canna/cannahost" to help
  kinput2 find it.
- Added fix from Ishikawa for "typo" in malloc call in lib/RK/dd.c.

* Tue Aug  9 2001 Yukihiro Nakai <ynakai@redhat.com> - 3.5b2-44
- Off the S bit (#13135)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Mon Apr 23 2001 Yukihiro Nakai <ynakai@redhat.com>
- Add complete ia64 patch

* Tue Apr 17 2001 Bill Nottingham <notting@redhat.com>
- build on ia64 so that dependencies work

* Tue Feb  6 2001 Matt Wilson <msw@redhat.com>
- changed requires on Canna-devel to require Canna-libs, not Canna

* Tue Feb  6 2001 Trond Eivind Glomsrd <teg@redhat.com>
- Display OK or FAILED from initscript (#26111)

* Fri Jan 26 2001 Yukihiro Nakai <ynakai@redhat.com>
- More fix to reduce warning

* Fri Jan 26 2001 Yukihiro Nakai <ynakai@redhat.com>
- Capitalize summary
- Add Requires to Canna-devel
- Minor fix for %%files

* Wed Jan 24 2001 Adrian Havill <havill@redhat.com>
- changed dangerous suid bin/bin uid/gid of server to canna/canna

* Tue Jan 23 2001 Yukihiro Nakai <ynakai@redhat.com>
- Update canna.init (teg@redhat.com>

* Tue Jan 23 2001 Yukihiro Nakai <ynakai@redhat.com>
- Add defattr
- Add post and postun for -libs to ldconfig

* Mon Jan 22 2001 Yukihiro Nakai <ynakai@redhat.com>
- Split the runtime library
- bzip2

* Fri Jan 19 2001 Yukihiro Nakai <ynakai@redhat.com>
- Disable IA64 patch. It seems to cause serious problem.
  (Such IA64 fix is not needed with the newer compiler?)

* Fri Jan 19 2001 Matt Wilson <msw@redhat.com>
- use -DCANNA_WCHAR (revert the the part of the ia64 patch that disables
  -DCANNA_WCHAR

* Tue Dec 19 2000 Yukihiro Nakai <ynakai@redhat.com>
- Add IA64 patch (Not complete)

* Wed Sep 13 2000 ISHIKAWA Mutsumi <ishikawa@redhat.com>
- spcfile typo fix (doc-canna -> dot-canna)

* Wed Sep 13 2000 ISHIKAWA Mutsumi <ishikawa@redhat.com>
- add /etc/skel/.canna

* Thu Sep 12 2000 ISHIKAWA Mutsumi <ishikawa@redhat.com>
- fix initscript

* Mon Sep 11 2000 ISHIKAWA Mutsumi <ishikawa@redhat.com>
- chown bin.bin /usr/sbin/{cannaserver,cannakill},/var/lib/canna
  and /var/log/canna

* Mon Sep 11 2000 ISHIKAWA Mutsumi <ishikawa@redhat.com>
- hosts.canna read bug fix.

* Thu Sep  7 2000 ISHIKAWA Mutsumi <ishikawa@redhat.com>
- move back /etc/init.d -> /etc/rc.d/init.d

* Thu Aug 24 2000 ISHIKAWA Mutsumi <ishikawa@redhat.com>
- chmod +x /etc/init.d/canna

* Fri Aug  4 2000 ISHIKAWA Mutsumi <ishikawa@redhat.com>
- move /etc/rc.d/init.d -> /etc/init.d

* Thu Aug  3 2000 ISHIKAWA Mutsumi <ishikawa@redhat.com>
- rebuilt for RedHat 7.0.
- man directory ja_JP.UJIS -> ja
- Canna-3.5b2.conf.patch modified to install manpages to /usr/share/man
- remove Canna-3.5b2-fhs.patch to install manpages to /usr/share/man

* Tue Jul 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix syntax error in postun
- no need to remove the services entry in postun
- make all symlinks to catdic relative instead of absolute

* Fri Jul 14 2000 Bill Nottingham <notting@redhat.com>
- move initscript back

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul 11 2000 Bill Nottingham <notting@redhat.com>
- don't run by default
- add buffer overflow patch
- add configuration that should in theory only accept connections
  from localhost or unix socket

* Mon Jun 26 2000 Preston Brown <pbrown@redhat.com>
- initscript to /etc/init.d, and updated for new initscript stds.

* Mon Jun 19 2000 Preston Brown <pbrown@redhat.com>
- FHS paths

* Mon Jun 12 2000 Matt Wilson <msw@redhat.com>
- don't redefine bcopy
- add defattr

* Sun Mar 26 2000 Chris Ding <cding@redhat.com>
- ja -> ja_JP.eucJP

* Tue Mar 21 2000 Chris Ding <cding@redhat.com>
- ja_JP.eucJP -> ja

* Thu Mar  9 2000 Matt Wilson <msw@redhat.com>
- build for 6.2, gzip manpages

* Sat Mar  4 2000 Chris Ding <cding@redhat.com>
- ja -> ja_JP.eucJP
- changed group

* Thu Oct 21 1999 Matt Wilson <msw@redhat.com>
- added prereq for grep and cp

* Wed Oct 20 1999 Matt Wilson <msw@redhat.com>
- added prereq for /sbin/chkconfig and /etc/services

* Tue Oct 12 1999 Matt Wilson <msw@redhat.com>
- fixed redirection path for 4 man pages

* Thu Oct  7 1999 Matt Wilson <msw@redhat.com>
- rebuilt against 6.1

* Thu Jun 24 1999 Japanese LinuxPPC Users' Group <jrpm@ppc.linux.or.jp>
- build against Linuxppc R5
- add Oe's stdin patch in Canna-3.5b2-3rh.src.rpm
- change canna.init and spec file for safty shutdown cannaserver. Thanks to Shoichiro Nagata.

* Sun May 30 1999 FURUSAWA,Kazuhisa <kazu@linux.or.jp>
- 4th Release for i386 (glibc2.1).
- Original Packager: Atsushi Yamagata <yamagata@plathome.co.jp>

* Fri Jan 22 1999 Atsushi Yamagata <yamagata@plathome.co.jp>
- 4th release
- changed installed directories (See Canna.conf and INSTALL.jp)
- added post-{un}install scripts for Canna and Canna-devel packages
- added URL, Distribution, Vendor, and Prefix tags

* Tue Nov 04 1997 Atsushi Yamagata <yamagata@jwu.ac.jp>
- 3rd release
- patched for glibc. Thanks Mr. Daisuke Sato <densuke@ga2.so-net.or.jp>
- divided the Canna packege into Canna and Canna-devel

* Sun Jul 27 1997 Atsushi Yamagata <yamagata@jwu.ac.jp>
- 2nd release

* Fri Jul 11 1997 Atsushi Yamagata <yamagata@jwu.ac.jp>
- 1st release


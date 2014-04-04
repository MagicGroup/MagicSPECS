Summary: The basic directory layout for a Linux system
Summary(zh_CN.UTF-8): Linux 系统的基本目录结构
Name: filesystem
Version: 3
Release: 4%{?dist}
License: Public Domain
URL: https://fedorahosted.org/filesystem
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
# Raw source1 URL: https://fedorahosted.org/filesystem/browser/lang-exceptions?format=raw
Source1: https://fedorahosted.org/filesystem/browser/lang-exceptions
Source2: iso_639.sed
Source3: iso_3166.sed
BuildRequires: iso-codes
Requires(pre): setup

# RPM runtime check in the buildroot; this ensures we can not install the
# incompatible filesystem.rpm on unconverted systems
# Requires: rpmlib(X-CheckUnifiedSystemdir)

%description
The filesystem package is one of the basic packages that is installed
on a Linux system. Filesystem contains the basic directory layout
for a Linux operating system, including the correct permissions for
the directories.

%description -l zh_CN.UTF-8
Linux 系统的基本目录结构，包括权限。

%prep
rm -f $RPM_BUILD_DIR/filelist

%build

%install
rm -rf %{buildroot}
mkdir %{buildroot}
install -p -c -m755 %SOURCE2 %{buildroot}/iso_639.sed
install -p -c -m755 %SOURCE3 %{buildroot}/iso_3166.sed

cd %{buildroot}

mkdir -p boot dev \
        etc/{X11/{applnk,fontpath.d},xdg/autostart,opt,pm/{config.d,power.d,sleep.d},xinetd.d,skel,sysconfig,pki} \
        home media mnt opt proc root run/lock srv sys tmp \
        usr/{bin,etc,games,include,%{_lib}/{games,sse2,tls,X11,pm-utils/{module.d,power.d,sleep.d}},lib/{games,locale,modules,sse2},libexec,local/{bin,etc,games,lib,%{_lib},sbin,src,share/{applications,man/man{1,2,3,4,5,6,7,8,9,n,1x,2x,3x,4x,5x,6x,7x,8x,9x},info},libexec,include,},sbin,share/{aclocal,applications,augeas/lenses,backgrounds,desktop-directories,dict,doc,empty,games,ghostscript/conf.d,gnome,icons,idl,info,man/man{1,2,3,4,5,6,7,8,9,n,1x,2x,3x,4x,5x,6x,7x,8x,9x,0p,1p,3p},mime-info,misc,omf,pixmaps,sounds,themes,xsessions,X11},src,src/kernels,src/debug} \
        var/{adm,empty,gopher,lib/{games,misc,rpm-state},local,lock/subsys,log,nis,preserve,run,spool/{mail,lpd,uucp},tmp,db,cache,opt,games,yp}

ln -snf ../var/tmp usr/tmp
ln -snf spool/mail var/mail
ln -snf usr/bin bin
ln -snf usr/sbin sbin
ln -snf usr/lib lib
ln -snf usr/%{_lib} %{_lib}

sed -n -f %{buildroot}/iso_639.sed /usr/share/xml/iso-codes/iso_639.xml \
  >%{buildroot}/iso_639.tab
sed -n -f %{buildroot}/iso_3166.sed /usr/share/xml/iso-codes/iso_3166.xml \
  >%{buildroot}/iso_3166.tab

grep -v "^$" %{buildroot}/iso_639.tab | grep -v "^#" | while read a b c d ; do
    [[ "$d" =~ "^Reserved" ]] && continue
    [[ "$d" =~ "^No linguistic" ]] && continue

    locale=$c
    if [ "$locale" = "XX" ]; then
        locale=$b
    fi
    echo "%lang(${locale})	/usr/share/locale/${locale}" >> $RPM_BUILD_DIR/filelist
    echo "%lang(${locale}) %ghost %config(missingok) /usr/share/man/${locale}" >>$RPM_BUILD_DIR/filelist
done
cat %{SOURCE1} | grep -v "^#" | grep -v "^$" | while read loc ; do
    locale=$loc
    locality=
    special=
    [[ "$locale" =~ "@" ]] && locale=${locale%%%%@*}
    [[ "$locale" =~ "_" ]] && locality=${locale##*_}
    [[ "$locality" =~ "." ]] && locality=${locality%%%%.*}
    [[ "$loc" =~ "_" ]] || [[ "$loc" =~ "@" ]] || special=$loc

    # If the locality is not official, skip it
    if [ -n "$locality" ]; then
        grep -q "^$locality" %{buildroot}/iso_3166.tab || continue
    fi
    # If the locale is not official and not special, skip it
    if [ -z "$special" ]; then
        egrep -q "[[:space:]]${locale%%_*}[[:space:]]" \
           %{buildroot}/iso_639.tab || continue
    fi
    echo "%lang(${locale})	/usr/share/locale/${loc}" >> $RPM_BUILD_DIR/filelist
    echo "%lang(${locale})  %ghost %config(missingok) /usr/share/man/${loc}" >> $RPM_BUILD_DIR/filelist
done

rm -f %{buildroot}/iso_639.tab
rm -f %{buildroot}/iso_639.sed
rm -f %{buildroot}/iso_3166.tab
rm -f %{buildroot}/iso_3166.sed

cat $RPM_BUILD_DIR/filelist | grep "locale" | while read a b ; do
    mkdir -p -m 755 %{buildroot}/$b/LC_MESSAGES
done

cat $RPM_BUILD_DIR/filelist | grep "/share/man" | while read a b c d; do
    mkdir -p -m 755 %{buildroot}/$d/man{1,2,3,4,5,6,7,8,9,n,1x,2x,3x,4x,5x,6x,7x,8x,9x,0p,1p,3p}
done

for i in man{1,2,3,4,5,6,7,8,9,n,1x,2x,3x,4x,5x,6x,7x,8x,9x,0p,1p,3p}; do
   echo "/usr/share/man/$i" >>$RPM_BUILD_DIR/filelist
done

magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%pretrans -p <lua>
--#
--# If we are running in pretrans in a fresh root, there is no /usr and symlinks.
--# We cannot be sure, to be the very first rpm in the transaction list,
--# so, let's create the toplevel symlinks here and the directories they point to.
--# When our rpm is unpacked by cpio, it will set all permissions and modes later.
--#

if posix.stat("/usr") == nil then
    posix.mkdir("/usr")
end

for i,dir in ipairs({"/lib", "/%{_lib}", "/sbin", "/bin"}) do
    if posix.stat("/usr"..dir) == nil then
        posix.mkdir("/usr"..dir)
        if posix.stat(dir, "mode") == nil then
            posix.symlink("usr"..dir, dir)
        end
    end
end

return 0

%post -p <lua>
posix.symlink("../run", "/var/run")
posix.symlink("../run/lock", "/var/lock")

%files -f filelist
%defattr(0755,root,root,-)
%dir %attr(555,root,root) /
/bin
%attr(555,root,root) /boot
/dev
%dir /etc
/etc/X11
/etc/xdg
/etc/opt
/etc/pm
/etc/xinetd.d
/etc/skel
/etc/sysconfig
/etc/pki
/home
/lib
%ifarch x86_64 ppc ppc64 sparc sparc64 s390 s390x mips64el
/%{_lib}
%endif
/media
%dir /mnt
%dir /opt
%attr(555,root,root) /proc
%attr(550,root,root) /root
/run
/sbin
/srv
/sys
%attr(1777,root,root) /tmp
%dir /usr
%attr(555,root,root) /usr/bin
/usr/etc
/usr/games
/usr/include
%attr(555,root,root) /usr/lib
%ifarch x86_64 ppc ppc64 sparc sparc64 s390 s390x mips64el
%attr(555,root,root) /usr/%{_lib}
%endif
/usr/libexec
/usr/local
%attr(555,root,root) /usr/sbin
%dir /usr/share
/usr/share/aclocal
/usr/share/applications
/usr/share/augeas
/usr/share/backgrounds
/usr/share/desktop-directories
/usr/share/dict
/usr/share/doc
%attr(555,root,root) %dir /usr/share/empty
/usr/share/games
/usr/share/ghostscript
/usr/share/gnome
/usr/share/icons
/usr/share/idl
/usr/share/info
%dir /usr/share/locale
%dir /usr/share/man
/usr/share/mime-info
/usr/share/misc
/usr/share/omf
/usr/share/pixmaps
/usr/share/sounds
/usr/share/themes
/usr/share/xsessions
/usr/share/X11
/usr/src
/usr/tmp
%dir /var
/var/adm
/var/cache
/var/db
/var/empty
/var/games
/var/gopher
/var/lib
/var/local
%ghost %dir %attr(755,root,root) /var/lock
%ghost /var/lock/subsys
/var/log
/var/mail
/var/nis
/var/opt
/var/preserve
%ghost %attr(755,root,root) /var/run
%dir /var/spool
%attr(755,root,root) /var/spool/lpd
%attr(775,root,mail) /var/spool/mail
%attr(755,uucp,uucp) /var/spool/uucp
%attr(1777,root,root) /var/tmp
/var/yp

%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 3-4
- 为 Magic 3.0 重建

* Sun Apr 15 2012 Liu Di <liudidi@gmail.com> - 3-3
- 为 Magic 3.0 重建

* Fri Feb  3 2012 Kay Sievers <kay@redhat.com> 3-2
- enable guard against unconverted /bin, /sbin, /lib*
  directories in the filesystem

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 3-1
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Thu Jan 12 2012 Ondrej Vasik <ovasik@redhat.com>  2.4.46-1
- own and create /var/lib/rpm-state (#771713)

* Fri Nov 11 2011 Ondrej Vasik <ovasik@redhat.com>  2.4.45-1
- own and create /var/adm, /var/gopher and /var/spool/uucp
  as these are homedirs for default legacy system accounts
  (#752885)

* Fri Jul 29 2011 Ondrej Vasik <ovasik@redhat.com>  2.4.44-1
- drop ownership of /selinux - moved to /sys/fs/selinux(#726528)

* Tue Jun 28 2011 Ondrej Vasik <ovasik@redhat.com>  2.4.43-1
- add various languages to lang-exceptions(#620063)

* Wed May 18 2011 Ondrej Vasik <ovasik@redhat.com>  2.4.42-1
- Pre: require setup again (#705443)

* Fri Apr 08 2011 Ondrej Vasik <ovasik@redhat.com>  2.4.41-1
- drop filesystem.conf file (#694688)

* Tue Apr 05 2011 Ondrej Vasik <ovasik@redhat.com>  2.4.40-1
- create /run/lock as 755 root:root (#693394)

* Thu Mar 31 2011 Ondrej Vasik <ovasik@redhat.com>  2.4.39-1
- add /run to filesystem (#692124)
- minor spec file cleanup

* Fri Feb 25 2011 Ondrej Vasik <ovasik@redhat.com>  2.4.38-1
- do /var/lock/subsys directory systemd way via tmpfiles.d conf file
  (#656586)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Adam Jackson <ajax@redhat.com> 2.4.37-1
- Drop Prov/Obs: xorg-x11-filesystem and pm-utils-filesystem, both last seen
  in Fedora 11.
- Remove explicit BuildRoot.

* Fri Sep 25 2010 Ondrej Vasik <ovasik@redhat.com>  2.4.36-1
- own /usr/lib/sse2 even on 64-bit (#636748)

* Mon Apr 19 2010 Ondrej Vasik <ovasik@redhat.com>  2.4.35-1
- change permissions on /var/lock from 775 root:lock to
  755 root:root (#581884)

* Thu Apr 08 2010 Ondrej Vasik <ovasik@redhat.com>  2.4.34-1
- drop ownership for /mnt/{floppy,cdrom} subdirs(#173854)

* Thu Mar 04 2010 Ondrej Vasik <ovasik@redhat.com>  2.4.33-1
- do own /usr/share/aclocal (#533962)

* Tue Mar 02 2010 Ondrej Vasik <ovasik@redhat.com>  2.4.32-1
- added sr@ijekavian and sr@ijekavianlatin into lang
  exceptions

* Thu Oct 01 2009 Ondrej Vasik <ovasik@redhat.com>  2.4.31-1
- added zh_CN.GB2312 to lang exceptions(#487568)

* Tue Aug 25 2009 Karsten Hopp <karsten@redhat.com> 2.4.30-2
- fix typo in Provides

* Mon Aug 17 2009 Ondrej Vasik <ovasik@redhat.com> 2.4.30-1
- adjust directory rights for usage of capabilities(#517575)

* Mon Aug 10 2009 Ondrej Vasik <ovasik@redhat.com> 2.4.29-1
- iso_codes package no longer provides tab files, do generate
  them on fly with sed (thanks D. Tardon)

* Wed Aug 05 2009 Ondrej Vasik <ovasik@redhat.com> 2.4.28-1
- Provide/obsolete pm-utils-filesystem, own dirs for pm-utils
  hooks(#515362)
- Do own man sections for /usr/share/man/<locale> dirs (#220265)
- Do own /usr/share/sounds (#515485)

* Tue Aug 04 2009 Adam Jackson <ajax@redhat.com> 2.4.27-1
- Prov/Obs: xorg-x11-filesystem

* Mon Aug 03 2009 Ondrej Vasik <ovasik@redhat.com> 2.4.26-1
- Do own /usr/share/man/<locale> directories (ghosted, missingok) - #220265

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 2.4.25-1
- Remove explicit /usr/lib/X11, everything uses %%_libdir now.

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 2.4.24-1
- Added /usr/share/X11

* Thu Jul 09 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.23-1
- do own /usr/src/debug (#214983)

* Wed Jul 08 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.22-1
- do own interface description directory /usr/share/idl(#451719)
- add a few missing lang-exceptions to filelist(#508309)

* Wed Mar 04 2009 Phil Knirsch <pknirsch@redhat.com> - 2.4.21-1
- Added /usr/share/backgrounds (#487957)
- Added /usr/share/ghostscript/{conf.d} (#302521)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Phil Knirsch <pknirsch@redhat.com> - 2.4.20-1
- Removed ownership of fonts directories (#477046)

* Sat Sep 06 2008 Phil Knirsch <pknirsch@redhat.com> - 2.4.19-1
- Added augeas lenses dir (#461317)

* Tue Jun 24 2008 Phil Knirsch <pknirsch@redhat.com> - 2.4.18-1
- Added comment with raw format lang-exception URL

* Mon Jun 23 2008 Phil Knirsch <pknirsch@redhat.com> - 2.4.17-1
- Added URL for lang-exception source (#225752)

* Wed Jun 18 2008 Phil Knirsch <pknirsch@redhat.com> - 2.4.16-1
- Dropped /etc/news again as we're handling it now correctly (#437462)
- Filesystem is now an official fedorahosted project, part of the review
  changes (#225752)
- Removed duplicate entry in lang_exceptions for ca_ES@valencian (#225752)

* Tue May 27 2008 Phil Knirsch <pknirsch@redhat.com> - 2.4.15-1
- First round of Fedora package review changes (#225752)

* Tue May 20 2008 Phil Knirsch <pknirsch@redhat.com> - 2.4.14-1
- Added /usr/src/kernels to owned and created dirs (#442283)

* Mon Apr 07 2008 Phil Knirsch <pknirsch@redhat.com> - 2.4.13-1
- Added /etc/news to owned and created directories

* Thu Mar 27 2008 Phil Knirsch <pknirsch@redhat.com> - 2.4.12-1
- Added be@latin to lang-exceptions (#231737)
- Added /usr/share/man{0,1,3]p to owned files (#233879)
- Added /usr/share/fonts to owned files (#302141)
- Renamed sr@Latn to sr@latin (#436887)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.4.11-2
- Autorebuild for GCC 4.3

* Mon Aug 13 2007 Phil Knirsch <pknirsch@redhat.com> 2.4.11-1
- Added /etc/X11/fontpath.d and dropped /etc/X11/sysconfig /etc/X11/serverconfig
 (#251707)

* Wed Jul 18 2007 Phil Knirsch <pknirsch@redhat.com> 2.4.10-1
- Replaced gtk-doc with gnome (#247276)

* Tue May 29 2007 Phil Knirsch <pknirsch@redhat.com> 2.4.9-1
- Fixed nasty typo for /etc directories (#241525)

* Fri May 25 2007 Phil Knirsch <pknirsch@redhat.com> 2.4.8-1
- Fixed description to avoid trademark issues (#234093)

* Thu May 24 2007 Phil Knirsch <pknirsch@redhat.com> 2.4.7-1
- Added /etc/fonts/conf.d and /usr/share/themes (#239246)
- Removed /etc/xdg/menus, already owned by redhat-menus (#228779)

* Tue Apr 17 2007 Phil Knirsch <pknirsch@redhat.com> - 2.4.6-1
- Added several more /usr/share directories (#222905)

* Sat Mar 31 2007 Peter Jones <pjones@redhat.com> - 2.4.5-1
- add /usr/local/share/applications

* Fri Mar 30 2007 Jeremy Katz <katzj@redhat.com> - 2.4.4-1
- add /etc/xdg/autostart

* Thu Mar 15 2007 Phil Knirsch <pknirsch@redhat.com> - 2.4.3-1
- Fixed typo for new /etc/xdg entries (#224052)
- One more tiny specile cleanup

* Mon Feb 12 2007 Phil Knirsch <pknirsch@redhat.com> - 2.4.2-1
- Added several missing unowned directories (#224052)
- Tiny specfile cleanups

* Wed Dec 20 2006 Phil Knirsch <pknirsch@redhat.com> - 2.4.1-1
- Dropped the obsolete directories /usr/lib{,64}/gcc-lib (#220235)

* Tue Oct 10 2006 Bill Nottingham <notting@redhat.com> - 2.4.0-1
- create and own /usr/share/locale/*/LC_MESSAGES (#196669)

* Tue Oct 10 2006 Phil Knirsch <pknirsch@redhat.com> - 2.3.8-1
- Added the manXx directories to the ownership of filesystem (#208121)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.3.7-2.1
- rebuild

* Wed Jun 28 2006 Phil Knirsch <pknirsch@redhat.com> - 2.3.7-2
- Fixed games location according to FHS 2.1 (#165425)
- Added {_libdir}/sse2 to owned files (#192853)
- Added /dev to owned files (#192860)
- Added {_datadir}/icons to owned files (#195911)
- Dropped obsolete /etc/X11/starthere (#191163)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.3.7-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.3.7-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 17 2005 Bill Nottingham <notting@redhat.com> - 2.3.7-1
- actually, *do* package /usr/lib/X11, etc, but as directories
- remove /usr/X11R6 heirarchy

* Mon Nov  7 2005 Bill Nottingham <notting@redhat.com> - 2.3.6-1
- don't package /usr/lib/X11 or /usr/bin/X11 symlinks

* Fri Aug 19 2005 Bill Nottingham <notting@redhat.com> - 2.3.5-1
- package / (#165797)

* Mon May 23 2005 Bill Nottingham <notting@redhat.com> - 2.3.4-1
- ship /usr/share/games (#158433, <ville.skytta@iki.fi>)

* Thu May  5 2005 Peter Jones <pjones@redhat.com> - 2.3.3-1
- remove /initrd, since mkinitrd doesn't use it anymore by default

* Wed Apr 20 2005 John Dennis <jdennis@redhat.com> - 2.3.2-1
- add /etc/pki, a place to store keys and certificates

* Wed Mar  9 2005 Bill Nottingham <notting@redhat.com> 2.3.1-1
- don't ship /usr/lib64/X11 in general (#147077)

* Thu Aug 12 2004 Bill Nottingham <notting@redhat.com> 2.3.0-1
- add /media, /srv

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Mar 11 2004 Bill Nottingham <notting@redhat.com> 2.2.4-1
- move /selinux here from SysVinit

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 15 2004 Bill Nottingham <notting@redhat.com> 2.2.3-1
- move /usr/dict to /usr/share/dict (#113645)
- add /usr/lib/locale, /var/empty (#108686,#113036)
- add */%%{_lib}/tls (#113050)

* Fri Nov 21 2003 Bill Nottingham <notting@redhat.com> 2.2.2-1
- add /sys

* Tue Oct 07 2003 Than Ngo <than@redhat.com> 2.2.1-5
- add /usr/share/xsessions

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sun Dec  1 2002 Tim Waugh <twaugh@redhat.com> 2.2.1-2
- Really fix /var/mail

* Thu Nov 28 2002 Bill Nottingham <notting@redhat.com> 2.2.1-1
- fix /var/mail

* Wed Nov 20 2002 Bill Nottingham <notting@redhat.com>
- make arch specific, handle lib/lib64 stuff
- add /usr/libexec, /usr/share/applications

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Aug 20 2001 Bill Nottingham <notting@redhat.com>
- %%ghost /mnt/cdrom, /mnt/floppy (fixes #52046)

* Wed Aug 15 2001 Bill Nottingham <notting@redhat.com>
- add /usr/X11R6/share (#51830)

* Mon Aug 13 2001 Bill Nottingham <notting@redhat.com>
- prereq a particular version of the setup package

* Thu Aug  9 2001 Bill Nottingham <notting@redhat.com>
- remove /mnt/cdrom, /mnt/floppy (updfstab will create them if needed)
- make it noarch again

* Wed Aug  8 2001 Bill Nottingham <notting@redhat.com>
- /var/lock needs to be root.lock, not lock.lock

* Mon Aug  6 2001 Jeff Johnson <jbj@redhat.com>
- lock.lock ownership, 0775 permissions, for /var/lock.

* Tue Jul 17 2001 Bill Nottingham <notting@redhat.com>
- add /etc/sysconfig, /var/yp, /usr/share/pixmaps

* Tue Jul 10 2001 Bill Nottingham <notting@redhat.com>
- add stuff under /etc/X11
- remove extraneous /usr/X11R6/doc (#47490)

* Mon Jun 25 2001 Bill Nottingham <notting@redhat.com>
- don't conflict with rpm

* Fri Jun 22 2001 Bill Nottingham <notting@redhat.com>
- don't own /var/lib/rpm (#43315)
- add some stuff in /usr/local (#36522)

* Thu Jun 21 2001 Bill Nottingham <notting@redhat.com>
- add /initrd

* Thu Jun 07 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- remove noarch
- do not include /mnt/cdrom and /mnt/floppy for s390/s390x

* Mon Apr 16 2001 Bill Nottingham <notting@redhat.com>
- take the group write off of /var/lock

* Fri Jul 21 2000 Bill Nottingham <notting@redhat.com>
- add /usr/share/empty

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Jun 28 2000 Preston Brown <pbrown@redhat.com>
- remove /usr/doc

* Thu Jun 22 2000 Preston Brown <pbrown@redhat.com>
- remove /usr/info

* Sun Jun 19 2000 Bill Nottingham <notting@redhat.com>
- remove /usr/man

* Sat Jun 17 2000 Bill Nottingham <notting@redhat.com>
- /var/spool/lpd should have normal perms (#12272)

* Tue Jun  6 2000 Bill Nottingham <notting@redhat.com>
- add /etc/skel

* Thu Jun 01 2000 Preston Brown <pbrown@redhat.com>
- add /var/spool/lpd to filesystem, owned by user/group lp, tight permissions

* Tue May 23 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Added /etc/xinetd.d

* Mon May 15 2000 Preston Brown <pbrown@redhat.com>
- /etc/opt, /usr/share/{info,man/man*,misc,doc} (FHS 2.1)
- added /var/games.  Data should move from /var/lib/games to there (FHS 2.1)
- bump version up to 2.0 already!

* Thu Apr 13 2000 Jakub Jelinek <jakub@redhat.com>
- removed /var/state, added /var/opt, /var/mail for FHS 2.1 compliance

* Mon Aug 28 1999 Preston Brown <pbrown@redhat.com>
- added /opt, /var/state, /var/cache for FHS compliance (#3966)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Sun Jan 17 1999 Jeff Johnson <jbj@redhat.com>
- don't carry X11R6.1 as directory on sparc.
- /var/tmp/build root (#811)

* Wed Jan 13 1999 Preston Brown <pbrown@redhat.com>
- font directory didn't belong, which I previously misunderstood.  removed.

* Fri Nov 13 1998 Preston Brown <pbrown@redhat.com>
- /usr/share/fonts/default added.

* Fri Oct  9 1998 Bill Nottingham <notting@redhat.com>
- put /mnt/cdrom back in

* Wed Oct  7 1998 Bill Nottingham <notting@redhat.com>
- Changed /root to 0750

* Wed Aug 05 1998 Erik Troan <ewt@redhat.com>
- added /var/db
- set attributes in the spec file; don't depend on the ones in the cpio
  archive
- use a tarball instead of a cpioball

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Sep 09 1997 Erik Troan <ewt@redhat.com>
- made a noarch package

* Wed Jul 09 1997 Erik Troan <ewt@redhat.com>
- added /

* Wed Apr 16 1997 Erik Troan <ewt@redhat.com>
- Changed /proc to 555
- Removed /var/spool/mqueue (which is owned by sendmail)

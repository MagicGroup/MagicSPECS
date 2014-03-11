%define perl_version %(eval "`%{__perl} -V:version`"; echo $version)

Name: pilot-link
Version: 0.12.5
Release: 14%{?dist}
Epoch: 2
# libpisock/md5.c       Public Domain
# libpisock/blob.c      LGPLv2+
# libpisock/contact.c   GPLv2
# kittykiller.c         GPLv2+
License: GPLv2 and GPLv2+ and LGPLv2+ and Public Domain
Group: Applications/Communications
Summary: File transfer utilities between Linux and PalmPilots
URL: http://www.pilot-link.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: http://downloads.pilot-link.org/%{name}-%{version}.tar.bz2
Source3: blacklist-visor
Source4: README.fedora
Source5: 60-pilot.perms
Source6: 69-pilot-link.rules

ExcludeArch: s390 s390x
Patch4: pilot-link-0.12.1-var.patch
Patch6: pilot-link-0.12.2-open.patch
Patch10: pilot-link-0.12.3-clio.patch
Patch11: pilot-link-0.12.5-mp.patch
Patch12: pilot-link-0.12.5-redefinePerlsymbols.patch
Patch13: pilot-link-0.12.5-compiler_warnings.patch

Requires: pilot-link-libs = %{epoch}:%{version}-%{release}

BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: libpng-devel
BuildRequires: readline-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: libusb-devel
BuildRequires: bluez-libs-devel

%description
This suite of tools allows you to upload and download programs and
data files between a Linux/UNIX machine and the PalmPilot. It has a
few extra utilities that will allow for things like syncing the
PalmPilot's calendar app with Ical. Note that you might still need to
consult the sources for pilot-link if you would like the Python, Tcl,
or Perl bindings.

Install pilot-link if you want to synchronize your Palm with your Red
Hat Linux system.

%package devel
Summary: PalmPilot development header files
Group: Development/Libraries
Requires: pilot-link-libs = %{epoch}:%{version}-%{release}
Requires: libpng-devel
Requires: readline-devel

%description devel
This package contains the development headers that are used to build
the pilot-link package. It also includes the static libraries
necessary to build static pilot applications.

If you want to develop PalmPilot synchronizing applications, you'll
need to install pilot-link-devel.

%package perl
Summary: PalmPilot utilies written in perl
Group: Applications/Communications
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: perl(:MODULE_COMPAT_%{perl_version})

%description perl
This package contains utilities that depend on perl

%package libs
Summary: PalmPilot libraries
Group: System Environment/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description libs
Libraries for applications communicating with PalmPilot

%{perl_default_filter}

%prep
%setup -q
%patch4 -p1 -b .var
%patch6 -p1 -b .open
%patch10 -p1 -b .clio
%patch11 -p1 -b .mp
%patch12 -p1 -b .symbol
%patch13 -p1 -b .compiler
iconv -f windows-1252 -t UTF8 doc/README.usb > doc/README.usb.aux
mv doc/README.usb.aux doc/README.usb
iconv -f windows-1252 -t UTF8 ChangeLog > ChangeLog.aux
mv ChangeLog.aux ChangeLog
iconv -f windows-1252 -t UTF8 NEWS > NEWS.aux
mv NEWS.aux NEWS

%build
%configure \
  --with-python=no \
  --with-itcl=no \
  --with-tk=no \
  --with-tcl=no \
  --with-java=no \
  --with-cpp=yes \
  --with-perl=yes \
  --enable-conduits \
  --enable-libusb
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool


make

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot} libdir=%{_libdir} 
make install -C doc/man DESTDIR=%{buildroot} libdir=%{_libdir}

if test -f bindings/Perl/Makefile.PL ; then
   cd bindings/Perl
   perl -pi -e 's|^\$libdir =.*|\$libdir = "%{buildroot}%{_libdir}";|g' Makefile.PL
   CFLAGS="%{optflags}" %{__perl} Makefile.PL INSTALLDIRS=vendor
   make -B || :
   make
   cd ../..
fi

cd bindings/Perl
make pure_install PERL_INSTALL_ROOT=%{buildroot} %{?_smp_mflags}
cd ../..
# remove files and fix perms
find %{buildroot}%{_libdir}/perl5/ -type f -name '.packlist' -exec rm -f {} \;
find %{buildroot}%{_libdir}/perl5/ -type f -name '*.bs' -size 0 -exec rm -f {} \;
find %{buildroot}%{_libdir}/perl5/ -type f -name '*.so' -exec chmod 0755 {} \;
find %{buildroot}%{_libdir}/perl5/ -type f -name '*.pod' -exec rm -f {} \;
rm -f %{buildroot}%{_libdir}/perl5/perllocal.pod
rm -f %{buildroot}%{_libdir}/perl5/*/*/*/PDA/dump.pl

# remove files we don't want to include
rm -f %{buildroot}%{_libdir}/*.la

# remove static libraries
rm -f %{buildroot}%{_libdir}/*.a

# remove broken prog
rm -f %{buildroot}%{_bindir}/pilot-prc

# Put visor to blacklist
mkdir -p %{buildroot}%{_sysconfdir}/modprobe.d/
install -p -m644 %{SOURCE3} %{buildroot}%{_sysconfdir}/modprobe.d/blacklist-visor.conf

# put README.fedora into tree
cp %{SOURCE4} README.fedora

# install visor configs to share/udev
install -p -m644 %{SOURCE5} %{buildroot}%{_datadir}/pilot-link/udev

# now that rules are moved out HAL, install to /lib/udev/
install -d %{buildroot}/usr/lib/udev/rules.d/
install -p -m644 %{SOURCE6} %{buildroot}/usr/lib/udev/rules.d/
magic_rpm_clean.sh

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog README NEWS doc/README.usb doc/README.debugging doc/README.libusb README.fedora
%{_bindir}/*
%exclude %{_bindir}/pilot-ietf2datebook
%exclude %{_bindir}/pilot-sync-plan
%exclude %{_bindir}/pilot-undelete
%{_datadir}/pilot-link
%{_mandir}/man?/*
%exclude %{_mandir}/man1/ietf2datebook*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/aclocal/*.m4

%files perl
%defattr(-,root,root,-)
%{_bindir}/pilot-ietf2datebook
%{_bindir}/pilot-sync-plan
%{_bindir}/pilot-undelete
%{_mandir}/man1/ietf2datebook*
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/PDA*

%files libs
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/*.so.*
%config(noreplace) %{_sysconfdir}/modprobe.d/blacklist-visor.conf
/usr/lib/udev/rules.d/69-pilot-link.rules

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2:0.12.5-14
- 为 Magic 3.0 重建

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.12.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 2:0.12.5-12
- Perl 5.16 rebuild

* Fri Jun 01 2012 Peter Schiffer <pschiffe@redhat.com> - 2:0.12.5-11
- related: #757011
  cleaned patch
- resolves: #733987
  added requires for pilot-link-libs to pilot-link, removed obsoletes
  pilot-link from pilot-link-libs
- resolves: #733989
  moved udev rules to the libs subpackage, so it could be used without
  main package

* Fri Jan 13 2012 Peter Schiffer <pschiffe@redhat.com> - 2:0.12.5-10
- related: #757011
  fix FTBS on 32bit system

* Thu Jan 12 2012 Peter Schiffer <pschiffe@redhat.com> - 2:0.12.5-9
- related: #757011
  fix FTBS

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2:0.12.5-8
- Rebuild for new libpng

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2:0.12.5-7
- Perl mass rebuild
- add patch pilot-link-0.12.5-redefinePerlsymbols.patch - pilot-link was using
  old POLLUTED symbols, which shouldn't be used anymore 717939
- added perl_default_filter - don't provide Pilot.so

* Wed Mar 09 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 2:0.12.5-6
- resolves: #675222
  install-expenses(1) manpage fix

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.12.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan  4 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 2:0.12.5-4
- Resolves: #659292
  split libraries to a separate package

* Mon Nov 12 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 2:0.12.5-2
- Resolves: #642435
  udev rules broken for pilot-link

* Thu Jun 24 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 2:0.12.5-1
- update to 0.12.5

* Fri Jun 18 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 2:0.12.4-10
- fix rules configure file (#599640)

* Wed Jun 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 2:0.12.4-9
- Mass rebuild with perl-5.12.0

* Fri Mar  5 2010 Ivana Hutarova Varekova 2:0.12.4-8
- remove rpath
  fix the license tag
  remove autoreconf and optflags setting

* Tue Jan  5 2010 Jan Gorig <jgorig@redhat.com> 2:0.12.4-7
- fix build (#551970)

* Fri Dec 18 2009 Ivana Hutarova Varekova <varekova@redhat.com> 2:0.12.4-6
- fix source tag, add Public Domain license

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2:0.12.4-5
- rebuild against perl 5.10.1

* Sun Nov 15 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 2:0.12.4-4
- Better udev rules, thanks to Kevin Kofler

* Sun Nov 15 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 2:0.12.4-3
- Install udev rules again, updated for new ACL handling by udev (#529259)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.12.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 28 2009 Ivana Varekova <varekova@redhat.com> - 2:0.12.4-1
- update to 0.12.4
- remove obsolete patches

* Wed Apr 15 2009 Ivana Varekova <varekova@redhat.com> - 2:0.12.3-20
- rename blacklist-visor to blacklist-visor.conf (#494765)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.12.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep 23 2008 Ivana Varekova <varekova@redhat.com> - 2:0.12.3-18 
- extend clio patch - thanks Kevin R. Page

* Fri Sep 19 2008 Ivana Varekova <varekova@redhat.com> - 2:0.12.3-17
- split perl subpackage (461758) - thanks Peter Robinson
- spec file cleanup

* Fri Sep 19 2008 Ivana Varekova <varekova@redhat.com> - 2:0.12.3-16
- add clio patch (454178) - thanks Michael Ekstrand

* Thu Sep 11 2008 - Bastien Nocera <bnocera@redhat.com> - 2:0.12.3-15
- Rebuild

* Sun Jun 15 2008 Kevin Page <krp[AT]fedoraproject org> - 2:0.12.3-14
- corrected documentation for visor module use

* Wed Mar 26 2008 Ivana Varekova <varekova@redhat.com> 2:0.12.3-13
- remove HAL/PolicyKit staff (is in hal package now)

* Tue Mar 25 2008 Ivana Varekova <varekova@redhat.com> 2:0.12.3-12
- resolved 437310: change hal rules (palm rules were added to hal-info)

* Sun Mar  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2:0.12.3-11
- rebuild for perl 5.10.0

* Mon Mar  3 2008 Ivana Varekova <varekova@redhat.com> - 2:0.12.3-10
- Synchronize with F-8 branch:
- add Z22 patch
- change hal rules

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:0.12.3-9
- Rebuild for perl 5.10 (again)

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2:0.12.3-8
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:0.12.3-7
- rebuild for new perl

* Fri Jan 11 2008 Ivana Varekova <varekova@redhat.com> - 2:0.12.3-6
- Synchronize with F-8 branch:
- remove visor modul remove from %%post script
- Change README.fedora use "ttyUSB[13579]" in 60-pilot.rules

* Wed Jan 09 2008 - Bastien Nocera <bnocera@redhat.com> - 2:0.12.3-5
- Add Bluetooth support, with patch from Matt Davey <mcdavey@mrao.cam.ac.uk>
  to avoid crashing when pi_close is called

* Mon Jan  7 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 2:0.12.3-4
- Synchronize with F-8 branch: 
- Add README.fedora and visor configs as fallbacks (#280251: thanks Kevin Page)
- Don't tag HAL/PolicyKit files as %%config (#427840)
- Remove visor module if currently loaded (#280251)

* Fri Jan  4 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 2:0.12.3-3
- Synchronize with F-8 branch: add HAL, PolicyKit rules (#280251)

* Tue Dec 11 2007 Ivana Varekova <varekova@redhat.com> - 2:0.12.3-2
- fix md5 header file

* Thu Nov 22 2007 Ivana Varekova <varekova@redhat.com> - 2:0.12.3-1
- update to 0.12.3
- remove static libraries

* Mon Nov 12 2007 Alex Lancaster <alexlan[AT]fedoraproject org> - 2:0.12.2-7
- Perl bindings need to be compiled after libpisock is installed

* Mon Nov 12 2007 Alex Lancaster <alexlan[AT]fedoraproject org> - 2:0.12.2-6
- Enable Perl bindings
- Include important docs such as README.usb

* Tue Aug 29 2007 Ivana Varekova <varekova@redhat.com> - 2:0.12.2-5
- Rebuild for selinux ppc32 issue.
- fix open function calls

* Fri Jul 27 2007 Ivana Varekova <varekova@redhat.com> - 2:0.12.2-4
- add libusb-devel

* Wed Jun  6 2007 Ivana Varekova <varekova@redhat.com> - 2:0.12.2-3
- Resolves: #240327
   remove IT_PROG_INTLTOOL definition

* Mon Apr 30 2007 Ivana Varekova <varekova@redhat.com> - 2:0.12.2-2
- Resolves: 238239
  fix a syntax error in pilot-link.m4

* Thu Apr 26 2007 Ivana Varekova <varekova@redhat.com> - 2:0.12.2-1
- update to 0.12.2

* Mon Apr 16 2007 Ivana Varekova <varekova@redhat.com> - 2:0.12.1-6
- add --enable-libusb (#236413)

* Fri Mar  9 2007 Ivana Varekova <varekova@redhat.com> - 2:0.12.1-5
- incorporate the package review feedback

* Thu Nov 30 2006 Ivana Varekova <varekova@redhat.com> - 2:0.12.1-4
- fix undefined value problem #156682

* Tue Nov 28 2006 Ivana Varekova <varekova@redhat.com> - 2:0.12.1-3
- add enable-conduits option

* Mon Nov 27 2006 Ivana Varekova <varekova@redhat.com> - 2:0.12.1-2
- Add epoch
- Delete useless patches
- Add Buildrequires autoconf, automake and libtool

* Wed Sep  6 2006 Matthew Barnes <mbarnes@redhat.com> - 0.12.1-1.fc6
- Update to 0.12.1
- Disable all patches for 0.11.

* Tue Jul 18 2006 Ivana Varekova <varekova@redhat.com> 2:0.11.8-16
- fix configure script

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2:0.11.8-15.1
- rebuild

* Fri Apr 21 2006 Than Ngo <than@redhat.com> 2:0.11.8-15
- fix pilot-xfer crash on missing device node #186779, #175334
- don't include unnecessary man page #185147

* Wed Mar 29 2006 Than Ngo <than@redhat.com> 2:0.11.8-14 
- rebuild to get rid of libpisock.so.9

* Wed Mar 29 2006 Than Ngo <than@redhat.com> 2:0.11.8-13
- downgrade to stable release 0.11.8

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:0.12.0-0.pre4.5.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:0.12.0-0.pre4.5.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Aug 30 2005 Than Ngo <than@redhat.com> 0.12.0-0.pre4.5
- pre5 cvs snapshots
- remove several patches which included new upstream

* Tue Aug 16 2005 Than Ngo <than@redhat.com> 0.12.0-0.pre4.4
- apply patch to fix pilot-xfer crash #166037

* Tue Jul 26 2005 Than Ngo <than@redhat.com> 0.12.0-0.pre4.3
- apply patch to fix gcc warnings #164203

* Tue Jun 28 2005 Than Ngo <than@redhat.com> 0.12.0-0.pre4.2
- fix c++ build problem 

* Wed Jun 15 2005 Than Ngo <than@redhat.com> 0.12.0-0.pre4.1
- 0.12.0-pre4
- remove pilot-link-0.12.0-pre3-buffer.patch, it's included in new upstream

* Thu Jun 09 2005 Than Ngo <than@redhat.com> 0.12.0-0.pre3.2
- fix non utf-8 in changelog #159582

* Wed Jun 08 2005 Than Ngo <than@redhat.com> 0.12.0-0.pre3.1
- apply patch to fix compiler warnings

* Wed Jun 08 2005 Than Ngo <than@redhat.com> 0.12.0-0.pre3.0
- 0.12.0-pre3

* Sun Mar 13 2005 Than Ngo <than@redhat.com> 0.12.0-0.pre2.0
- 0.12.0-pre2
- fix build gcc 4 problem

* Mon Jan 24 2005 Than Ngo <than@redhat.com> 0.11.8-10
- Add patch to cleanup bad code #146001

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 0.11.8-9
- Rebuilt for new readline.

* Fri Aug  6 2004 Tim Waugh <twaugh@redhat.com> 0.11.8-8
- Fixed underquoted m4 definitions.

* Tue Jul 27 2004 Than Ngo <than@redhat.com> 0.11.8-7
- add patch to fix problem in loading data into Palm

* Wed Jun 30 2004 Than Ngo <than@redhat.com> 0.11.8-6
- add fix to avoid an out-of bounds array access
- add buildprereq on readline-devel, libpng-devel, bug #111119
- add patch to fix segfault in Net Library, bug #125878

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 24 2004 Than Ngo <than@redhat.com> 1:0.11.8-4
- fix build problem with new libpng

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Dec 17 2003 Than Ngo <than@redhat.com> 1:0.11.8-2
- Updated Url

* Fri Sep 26 2003 Harald Hoyer <harald@redhat.de> 1:0.11.8-1
- 0.11.8

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May  7 2003 Than Ngo <than@redhat.com> 0.11.7-1
- 0.11.7

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sun Dec  8 2002 Than Ngo <than@redhat.com> 0.11.5-3
- cleanup some bad codes (from d.binderman@virgin.net) bug #79237
- fix dependency issues

* Mon Nov  4 2002 Jeremy Katz <katzj@redhat.com> 0.11.5-2
- pilot-link-devel needs to require the epoch on the main package

* Sat Nov  2 2002 Jeremy Katz <katzj@redhat.com> 0.11.5-1
- update to 0.11.5

* Wed Aug 28 2002 Than Ngo <than@redhat.com> 0.11.3-3
- rpath issue

* Sun Aug 25 2002 Than Ngo <than@redhat.com> 0.11.3-2
- multilib bugs in specfile (bug #72556)

* Thu Aug 22 2002 Than Ngo <than@redhat.com> 0.11.3-1
- 0.11.3 fixed a bug in the process, which was causing some issues with J-Pilot

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Tue Aug  6 2002 Than Ngo <than@redhat.com> 0.11.2-1
- 0.11.2 (bug #70889)
- add missing static library

* Mon Jul 22 2002 Tim Powers <timp@redhat.com> 0.11.0-4
- rebuild using gcc-3.2-0.1

* Thu Jul 18 2002 Tim Powers <timp@redhat.com> 0.11.0-3
- add %%{_libdir}/libpisock++.so and %%{_libdir}/libpisock++.so.* to
  the file lists to fix the broken deps

* Thu Jul 18 2002 Than Ngo <than@redhat.com> 0.11.0-2
- Added missing some symlinks

* Thu Jul 18 2002 Than Ngo <than@redhat.com> 0.11.0-1
- 0.11.0 (bug #69135)
- Adapted patches into 0.11.0

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Than Ngo <than@redhat.com> 0.9.5-19
- don't forcibly strip binaries

* Mon Jun 11 2002 Than Ngo <than@redhat.com> 0.9.5-18
- get rid of tcl/tk dependency (bug #66480)

* Wed Jun 05 2002 Than Ngo <than@redhat.com> 0.9.5-17
- add rpmlint filter rpmlint bug #66008
- add malsync-supporting bug #64882

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Feb 21 2002 Jeremy Katz <katzj@redhat.com> 0.9.5-13
- free trip through the build system

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 0.9.5-12
- automated rebuild

* Mon Dec 31 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.9.5-11
- fix build with gcc 3.1

* Mon Nov 12 2001 Than Ngo <than@redhat.com> 0.9.5-10
- add patch for building against gcc 3

* Thu Sep 20 2001 Than Ngo <than@redhat.com> 0.9.5-9
- update to 0.9.5 release (bug #53430) 
- fix bug #53807
- add Url

* Fri Aug 10 2001 Than Ngo <than@redhat.com>
- add epoch (bug #51429)

* Mon Jul 16 2001 Trond Eivind Glomsrød <teg@redhat.com>
- s/Copyright/License/
- Add dependency on main package for the devel subpackage

* Tue Jun 19 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add ExcludeArch: s390 s390x

* Fri Jun 15 2001 Than Ngo <than@redhat.com>
- fix to build against libtool (bug #43800)

* Fri May 11 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.9.5-4
- rebuild with new readline

* Fri Apr 27 2001 Bill Nottingham <notting@redhat.com>
- rebuild for C++ exception handling on ia64

* Thu Feb 01 2001 Than Ngo <than@redhat.com>
- cleanup patch from Jürgen Stuber to fix "Weird packet" error  (Bug #25360)

* Mon Nov 20 2000 Than Ngo <than@redhat.com>
- update 0.9.5pre3 snapshot from CVS
- fix up broken codes

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul  4 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Mon Jun  5 2000 Matt Wilson <msw@redhat.com>
- defattr on devel package

* Sat Jun  3 2000 Matt Wilson <msw@redhat.com>
- rebuilt against tcl-8.3.1

* Wed May 31 2000 Matt Wilson <msw@redhat.com>
- fix building with egcs 2.96 and gcc 2.2, build against new libstdc++
- use _mandir macro

* Wed Apr  5 2000 Bill Nottingham <notting@redhat.com>
- rebuild against current ncurses/readline

* Sun Mar 26 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- call ldconfig directly from postun

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- gzip man pages

* Wed Oct 20 1999 Preston Brown <pbrown@redhat.com>
- upgrade to pilot-link 0.9.3, rewrite spec.

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- strip binaries

* Tue Mar 30 1999 Preston Brown <pbrown@redhat.com>
- added missing files from devel subpackage

* Fri Mar 26 1999 Preston Brown <pbrown@redhat.com>
- move /usr/lib/pix to /usr/lib/pilot-link (dumb, BAD name)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Thu Jan 21 1999 Bill Nottingham <notting@redhat.com>
- arm fix

* Fri Sep 24 1998 Michael Maher <mike@redhat.com>
- cleaned up spec file, updated package

* Tue May 19 1998 Michael Maher <mike@redhat.com>
- updated rpm

* Thu Jan 29 1998 Otto Hammersmith <otto@redhat.com>
- added changelog
- updated to 0.8.9
- removed explicit requires for /usr/bin/perl


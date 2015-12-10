Summary: A utility for setting up encrypted disks
Summary(zh_CN.UTF-8): 设置加密磁盘的工具
Name: cryptsetup
Version: 1.6.8
Release: 5%{?dist}
License: GPLv2+ and LGPLv2+
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL: http://cryptsetup.googlecode.com/
BuildRequires: libgcrypt-devel, popt-devel, device-mapper-devel
BuildRequires: libgpg-error-devel, libuuid-devel
BuildRequires: python-devel, libpwquality-devel
BuildRequires: fipscheck-devel >= 1.3.0
Provides: cryptsetup-luks = %{version}-%{release}
Obsoletes: cryptsetup-luks < 1.4.0
Requires: cryptsetup-libs = %{version}-%{release}
Requires: fipscheck-lib%{_isa} >= 1.3.0
Requires: libpwquality >= 1.2.0

%define upstream_version %{version}
Source0: https://www.kernel.org/pub/linux/utils/cryptsetup/v1.6/cryptsetup-%{upstream_version}.tar.xz

%description
The cryptsetup package contains a utility for setting up
disk encryption using dm-crypt kernel module.

%package devel
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libgcrypt-devel > 1.1.42, device-mapper-devel, libuuid-devel
Requires: pkgconfig
Summary: Headers and libraries for using encrypted file systems
Provides: cryptsetup-luks-devel = %{version}-%{release}
Obsoletes: cryptsetup-luks-devel < 1.4.0

%description devel
The cryptsetup-devel package contains libraries and header files
used for writing code that makes use of disk encryption.

%package libs
Group: System Environment/Libraries
Summary: Cryptsetup shared library
Provides: cryptsetup-luks-libs = %{version}-%{release}
Obsoletes: cryptsetup-luks-libs < 1.4.0
Requires: fipscheck-lib%{_isa} >= 1.3.0
# Need support for fixed gcrypt PBKDF2 and fixed Whirlpool hash.
Requires: libgcrypt >= 1.6.1

%description libs
This package contains the cryptsetup shared library, libcryptsetup.

%package -n veritysetup
Group: Applications/System
Summary: A utility for setting up dm-verity volumes
Requires: cryptsetup-libs = %{version}-%{release}

%description -n veritysetup
The veritysetup package contains a utility for setting up
disk verification using dm-verity kernel module.

%package reencrypt
Group: Applications/System
Summary: A utility for offline reencryption of LUKS encrypted disks.
Requires: cryptsetup-libs = %{version}-%{release}

%description reencrypt
This package contains cryptsetup-reencrypt utility which
can be used for offline reencryption of disk in situ.

%package python
Group: System Environment/Libraries
Summary: Python bindings for libcryptsetup
Requires: %{name}-libs = %{version}-%{release}
Provides: python-cryptsetup = %{version}-%{release}
Obsoletes: python-cryptsetup < 1.4.0

%description python
This package provides Python bindings for libcryptsetup, a library
for setting up disk encryption using dm-crypt kernel module.

%prep
%setup -q -n cryptsetup-%{upstream_version}
chmod -x python/pycryptsetup-test.py
chmod -x misc/dracut_90reencrypt/*

%build
%configure --enable-python --enable-fips --enable-cryptsetup-reencrypt --enable-pwquality %{?configure_pbkdf2}
# remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
# Generate HMAC checksums (FIPS)
%define __spec_install_post \
  %{?__debug_package:%{__debug_install_post}} \
  %{__arch_install_post} \
  %{__os_install_post} \
  fipshmac -d %{buildroot}/%{_libdir}/fipscheck %{buildroot}/%{_libdir}/libcryptsetup.so.* \
%{nil}

make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/%{_libdir}/*.la
install -d %{buildroot}/%{_libdir}/fipscheck
%find_lang cryptsetup

%post -n cryptsetup-libs -p /sbin/ldconfig

%postun -n cryptsetup-libs -p /sbin/ldconfig

%files
%doc COPYING AUTHORS FAQ docs/*ReleaseNotes
%{_mandir}/man8/cryptsetup.8.gz
%{_sbindir}/cryptsetup

%files -n veritysetup
%doc COPYING
%{_mandir}/man8/veritysetup.8.gz
%{_sbindir}/veritysetup

%files reencrypt
%doc COPYING misc/dracut_90reencrypt
%{_mandir}/man8/cryptsetup-reencrypt.8.gz
%{_sbindir}/cryptsetup-reencrypt

%files devel
%doc docs/examples/*
%{_includedir}/libcryptsetup.h
%{_libdir}/libcryptsetup.so
%{_libdir}/pkgconfig/libcryptsetup.pc

%files libs -f cryptsetup.lang
%doc COPYING COPYING.LGPL
%{_libdir}/libcryptsetup.so.*
%{_libdir}/fipscheck/libcryptsetup.so.*.hmac

%files python
%doc COPYING.LGPL python/pycryptsetup-test.py
%exclude %{python_sitearch}/pycryptsetup.la
%{python_sitearch}/pycryptsetup.so

%clean

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1.6.8-5
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 1.6.8-4
- 更新到 1.6.8

* Sun Mar 02 2014 Milan Broz <gmazyland@gmail.com> - 1.6.4-2
- Require libgcrypt 1.6.1 (with fixed PBKDF2 and Whirlpool hash).

* Thu Feb 27 2014 Milan Broz <gmazyland@gmail.com> - 1.6.4-1
- Update to cryptsetup 1.6.4.

* Tue Jan 07 2014 Ondrej Kozina <okozina@redhat.com> - 1.6.3-2
- remove useless hmac checksum

* Fri Dec 13 2013 Milan Broz <gmazyland@gmail.com> - 1.6.3-1
- Update to cryptsetup 1.6.3.

* Sun Aug 04 2013 Milan Broz <gmazyland@gmail.com> - 1.6.2-1
- Update to cryptsetup 1.6.2.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 31 2013 Milan Broz <gmazyland@gmail.com> - 1.6.1-1
- Update to cryptsetup 1.6.1.
- Install ReleaseNotes files instead of empty Changelog file.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 14 2013 Milan Broz <mbroz@redhat.com> - 1.6.0-1
- Update to cryptsetup 1.6.0.
- Change default LUKS encryption mode to aes-xts-plain64 (AES128).
- Force use of gcrypt PBKDF2 instead of internal implementation.

* Sat Dec 29 2012 Milan Broz <mbroz@redhat.com> - 1.6.0-0.1
- Update to cryptsetup 1.6.0-rc1.
- Relax license to GPLv2+ according to new release.
- Compile cryptsetup with libpwquality support.

* Tue Oct 16 2012 Milan Broz <mbroz@redhat.com> - 1.5.1-1
- Update to cryptsetup 1.5.1.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Milan Broz <mbroz@redhat.com> - 1.5.0-1
- Update to cryptsetup 1.5.0.

* Wed Jun 20 2012 Milan Broz <mbroz@redhat.com> - 1.5.0-0.2
- Update to cryptsetup 1.5.0-rc2.
- Add cryptsetup-reencrypt subpackage.

* Mon Jun 11 2012 Milan Broz <mbroz@redhat.com> - 1.5.0-0.1
- Update to cryptsetup 1.5.0-rc1.
- Add veritysetup subpackage.
- Move localization files to libs subpackage.

* Thu May 31 2012 Milan Broz <mbroz@redhat.com> - 1.4.3-2
- Build with fipscheck (verification in fips mode).
- Clean up spec file, use install to /usr.

* Thu May 31 2012 Milan Broz <mbroz@redhat.com> - 1.4.3-1
- Update to cryptsetup 1.4.3.

* Thu Apr 12 2012 Milan Broz <mbroz@redhat.com> - 1.4.2-1
- Update to cryptsetup 1.4.2.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 09 2011 Milan Broz <mbroz@redhat.com> - 1.4.1-1
- Update to cryptsetup 1.4.1.
- Add Python cryptsetup bindings.
- Obsolete separate python-cryptsetup package.

* Wed Oct 26 2011 Milan Broz <mbroz@redhat.com> - 1.4.0-1
- Update to cryptsetup 1.4.0.

* Mon Oct 10 2011 Milan Broz <mbroz@redhat.com> - 1.4.0-0.1
- Update to cryptsetup 1.4.0-rc1.
- Rename package back from cryptsetup-luks to cryptsetup.

* Wed Jun 22 2011 Milan Broz <mbroz@redhat.com> - 1.3.1-2
- Fix return code for status command when device doesn't exist.

* Tue May 24 2011 Milan Broz <mbroz@redhat.com> - 1.3.1-1
- Update to cryptsetup 1.3.1.

* Tue Apr 05 2011 Milan Broz <mbroz@redhat.com> - 1.3.0-1
- Update to cryptsetup 1.3.0.

* Tue Mar 22 2011 Milan Broz <mbroz@redhat.com> - 1.3.0-0.2
- Update to cryptsetup 1.3.0-rc2

* Mon Mar 14 2011 Milan Broz <mbroz@redhat.com> - 1.3.0-0.1
- Update to cryptsetup 1.3.0-rc1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Milan Broz <mbroz@redhat.com> - 1.2.0-1
- Update to cryptsetup 1.2.0

* Thu Nov 25 2010 Milan Broz <mbroz@redhat.com> - 1.2.0-0.2
- Fix crypt_activate_by_keyfile() to work with PLAIN devices.

* Tue Nov 16 2010 Milan Broz <mbroz@redhat.com> - 1.2.0-0.1
- Add FAQ to documentation.
- Update to cryptsetup 1.2.0-rc1

* Sat Jul 03 2010 Milan Broz <mbroz@redhat.com> - 1.1.3-1
- Update to cryptsetup 1.1.3

* Mon Jun 07 2010 Milan Broz <mbroz@redhat.com> - 1.1.2-2
- Fix alignment ioctl use.
- Fix API activation calls to handle NULL device name.

* Sun May 30 2010 Milan Broz <mbroz@redhat.com> - 1.1.2-1
- Update to cryptsetup 1.1.2
- Fix luksOpen handling of new line char on stdin.

* Sun May 23 2010 Milan Broz <mbroz@redhat.com> - 1.1.1-1
- Update to cryptsetup 1.1.1
- Fix luksClose for stacked LUKS/LVM devices.

* Mon May 03 2010 Milan Broz <mbroz@redhat.com> - 1.1.1-0.2
- Update to cryptsetup 1.1.1-rc2.

* Sat May 01 2010 Milan Broz <mbroz@redhat.com> - 1.1.1-0.1
- Update to cryptsetup 1.1.1-rc1.

* Sun Jan 17 2010 Milan Broz <mbroz@redhat.com> - 1.1.0-1
- Update to cryptsetup 1.1.0.

* Fri Jan 15 2010 Milan Broz <mbroz@redhat.com> - 1.1.0-0.6
- Fix gcrypt initialisation.
- Fix backward compatibility for hash algorithm (uppercase).

* Wed Dec 30 2009 Milan Broz <mbroz@redhat.com> - 1.1.0-0.5
- Update to cryptsetup 1.1.0-rc4

* Mon Nov 16 2009 Milan Broz <mbroz@redhat.com> - 1.1.0-0.4
- Update to cryptsetup 1.1.0-rc3

* Thu Oct 01 2009 Milan Broz <mbroz@redhat.com> - 1.1.0-0.3
- Update to cryptsetup 1.1.0-rc2
- Fix libcryptsetup to properly export only versioned symbols.

* Tue Sep 29 2009 Milan Broz <mbroz@redhat.com> - 1.1.0-0.2
- Update to cryptsetup 1.1.0-rc1
- Add luksHeaderBackup and luksHeaderRestore commands.

* Fri Sep 11 2009 Milan Broz <mbroz@redhat.com> - 1.1.0-0.1
- Update to new upstream testing version with new API interface.
- Add luksSuspend and luksResume commands.
- Introduce pkgconfig.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Milan Broz <mbroz@redhat.com> - 1.0.7-1
- Update to upstream final release.
- Split libs subpackage.
- Remove rpath setting from cryptsetup binary.

* Wed Jul 15 2009 Till Maas <opensource@till.name> - 1.0.7-0.2
- update BR because of libuuid splitout from e2fsprogs

* Mon Jun 22 2009 Milan Broz <mbroz@redhat.com> - 1.0.7-0.1
- Update to new upstream 1.0.7-rc1.

- Wipe old fs headers to not confuse blkid (#468062)
* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 30 2008 Milan Broz <mbroz@redhat.com> - 1.0.6-6
- Wipe old fs headers to not confuse blkid (#468062)

* Tue Sep 23 2008 Milan Broz <mbroz@redhat.com> - 1.0.6-5
- Change new project home page.
- Print more descriptive messages for initialization errors.
- Refresh patches to versions commited upstream.

* Sat Sep 06 2008 Milan Broz <mbroz@redhat.com> - 1.0.6-4
- Fix close of zero decriptor.
- Fix udevsettle delays - use temporary crypt device remapping.

* Wed May 28 2008 Till Maas <opensource till name> - 1.0.6-3
- remove a duplicate sentence from the manpage (RH #448705)
- add patch metadata about upstream status

* Tue Apr 15 2008 Bill Nottinghm <notting@redhat.com> - 1.0.6-2
- Add the device to the luksOpen prompt (#433406)
- Use iconv, not recode (#442574)

* Thu Mar 13 2008 Till Maas <opensource till name> - 1.0.6-1
- Update to latest version
- remove patches that have been merged upstream

* Mon Mar 03 2008 Till Maas <opensource till name> - 1.0.6-0.1.pre2
- Update to new version with several bugfixes
- remove patches that have been merged upstream
- add patch from cryptsetup newsgroup
- fix typo / missing luksRemoveKey in manpage (patch)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.5-9
- Autorebuild for GCC 4.3

* Sat Jan 19 2008 Peter Jones <pjones@redhat.com> - 1.0.5-8
- Rebuild for broken deps.

* Thu Aug 30 2007 Till Maas <opensource till name> - 1.0.5-7
- update URL
- update license tag
- recode ChangeLog from latin1 to uf8
- add smp_mflags to make

* Fri Aug 24 2007 Till Maas <opensource till name> - 1.0.5-6
- cleanup BuildRequires:
- removed versions, packages in Fedora are new enough
- changed popt to popt-devel

* Thu Aug 23 2007 Till Maas <opensource till name> - 1.0.5-5
- fix devel subpackage requires
- remove empty NEWS README
- remove uneeded INSTALL
- remove uneeded ldconfig requires
- add readonly detection patch

* Wed Aug 08 2007 Till Maas <opensource till name> - 1.0.5-4
- disable patch2, libsepol is now detected by configure
- move libcryptsetup.so to %%{_libdir} instead of /%%{_lib}

* Fri Jul 27 2007 Till Maas <opensource till name> - 1.0.5-3
- Use /%%{_lib} instead of /lib to use /lib64 on 64bit archs

* Thu Jul 26 2007 Till Maas <opensource till name> - 1.0.5-2
- Use /lib as libdir (#243228)
- sync header and library (#215349)
- do not use %%makeinstall (recommended by PackageGuidelines)
- select sbindir with %%configure instead with make
- add TODO

* Wed Jun 13 2007 Jeremy Katz <katzj@redhat.com> - 1.0.5-1
- update to 1.0.5

* Mon Jun 04 2007 Peter Jones <pjones@redhat.com> - 1.0.3-5
- Don't build static any more.

* Mon Feb 05 2007 Alasdair Kergon <agk@redhat.com> - 1.0.3-4
- Add build dependency on new device-mapper-devel package.
- Add preun and post ldconfig requirements.
- Update BuildRoot.

* Wed Nov  1 2006 Peter Jones <pjones@redhat.com> - 1.0.3-3
- Require newer libselinux (#213414)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.3-2.1
- rebuild

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 1.0.3-2
- put shared libs in the right subpackages

* Fri Apr  7 2006 Bill Nottingham <notting@redhat.com> 1.0.3-1
- update to final 1.0.3

* Mon Feb 27 2006 Bill Nottingham <notting@redhat.com> 1.0.3-0.rc2
- update to 1.0.3rc2, fixes bug with HAL & encrypted devices (#182658)

* Wed Feb 22 2006 Bill Nottingham <notting@redhat.com> 1.0.3-0.rc1
- update to 1.0.3rc1, reverts changes to default encryption type

* Tue Feb 21 2006 Bill Nottingham <notting@redhat.com> 1.0.2-1
- update to 1.0.2, fix incompatiblity with old cryptsetup (#176726)

* Mon Feb 20 2006 Karsten Hopp <karsten@redhat.de> 1.0.1-5
- BuildRequires: libselinux-devel

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-4.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-4.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Dec  5 2005 Bill Nottingham <notting@redhat.com> 1.0.1-4
- rebuild against new libdevmapper

* Thu Oct 13 2005 Florian La Roche <laroche@redhat.com>
- add -lsepol to rebuild on current fc5

* Mon Aug 22 2005 Karel Zak <kzak@redhat.com> 1.0.1-2
- fix cryptsetup help for isLuks action

* Fri Jul  1 2005 Bill Nottingham <notting@redhat.com> 1.0.1-1
- update to 1.0.1 - fixes incompatiblity with previous cryptsetup for
  piped passwords

* Thu Jun 16 2005 Bill Nottingham <notting@redhat.com> 1.0-2
- add patch for 32/64 bit compatibility (#160445, <redhat@paukstadt.de>)

* Tue Mar 29 2005 Bill Nottingham <notting@redhat.com> 1.0-1
- update to 1.0

* Thu Mar 10 2005 Bill Nottingham <notting@redhat.com> 0.993-1
- switch to cryptsetup-luks, for LUKS support

* Tue Oct 12 2004 Bill Nottingham <notting@redhat.com> 0.1-4
- oops, make that *everything* static (#129926)

* Tue Aug 31 2004 Bill Nottingham <notting@redhat.com> 0.1-3
- link some things static, move to /sbin (#129926)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 16 2004 Bill Nottingham <notting@redhat.com> 0.1-1
- initial packaging

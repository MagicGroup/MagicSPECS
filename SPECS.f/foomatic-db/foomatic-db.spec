%global dbver_rel 4.0
# When you change dbver_snap, rebuild also foomatic against this build to pick up new IEEE 1284 Device IDs.
# The postscriptdriver tags get put onto foomatic, because that's there the actual CUPS driver lives.
%global dbver_snap 20140403

Summary: Database of printers and printer drivers
Name: foomatic-db
Version: %{dbver_rel}
Release: 40.%{dbver_snap}%{?dist}
License: GPLv2+
Group: System Environment/Libraries
Requires: %{name}-filesystem = %{version}-%{release}
Requires: %{name}-ppds = %{version}-%{release}

Source0: http://www.openprinting.org/download/foomatic/foomatic-db-%{dbver_rel}-%{dbver_snap}.tar.gz

Patch1: foomatic-db-device-ids-20120103.patch

Url: http://www.openprinting.org
BuildArch: noarch

# Make sure we get postscriptdriver tags.
BuildRequires: python-cups

# Build requires cups so that configure knows where to put PPDs.
BuildRequires: cups

%description
This is the database of printers, printer drivers, and driver options
for Foomatic.

The site http://www.openprinting.org/ is based on this database.

%package filesystem
Summary: Directory layout for the foomatic package
License: Public Domain
Group: System Environment/Base

%description filesystem

Directory layout for the foomatic package.

%package ppds
Summary: PPDs from printer manufacturers
License: GPLv2+ and MIT
Group: System Environment/Libraries
# We ship a symlink in a directory owned by cups
BuildRequires: cups
Requires: cups
Requires: sed
Requires: %{name}-filesystem = %{version}-%{release}

%description ppds
PPDs from printer manufacturers.

%prep
%setup -q -n foomatic-db-%{dbver_snap}

find -type d | xargs chmod g-s

pushd db/source

# For gutenprint printers, use gutenprint-ijs-simplified.5.2.
perl -pi -e 's,>gutenprint<,>gutenprint-ijs-simplified.5.2<,' printer/*.xml

# Remove Samsung-CLP-300/315 (bug #625505), Samsung-CLP-610/620 (bug #967930)
find printer -name '*.xml' |grep -E 'Samsung-CLP-300|Samsung-CLP-315|Samsung-CLP-610|Samsung-CLP-620'|xargs rm -vf
# Remove references to foo2zjs, foo2oak, foo2hp and foo2qpdl (bug #208851).
# foo2zjs-z1, foo2zjs-z2, foo2zjs-z3 (bug #967930)
# foo2lava, foo2kyo, foo2xqx (bug #438319)
# foo2slx and foo2hiperc (bug #518267)
for x in zjs zjs-z1 zjs-z2 zjs-z3 oak oak-z1 hp qpdl lava kyo xqx slx hiperc
do
  find printer -name '*.xml' |xargs grep -l "<driver>foo2${x}"|xargs rm -vf
  rm -f driver/foo2${x}.xml opt/foo2${x}-*
done
# Same for m2300w/m2400w
find printer -name '*.xml' |xargs grep -l '<driver>m2[34]00w<'|xargs rm -vf
rm -f driver/m2300w.xml driver/m2400w.xml opt/m2300w-*
# Same for all these.
for x in drv_x125 ml85p pbm2lwxl pbmtozjs bjc800j
do
  find printer -name '*.xml' |xargs grep -l "<driver>${x}</driver>"|xargs rm -vf
  rm -vf driver/${x}.xml opt/${x}-*
done

# Remove Brother P-touch (bug #560610, comment #10)
rm -vf driver/ptouch.xml
rm -vf printer/Brother-PT-*.xml
rm -vf printer/Brother-QL-*.xml
rm -vf opt/Brother-Ptouch-*.xml

popd

# foomatic-db patches
# Don't use "-b" when patching PPD files as the backups will be packaged.

# Device IDs for:
# Brother MFC-8840D (#678065)
# HP LaserJet M1522nf MFP (#745499)
# Lexmark C453 (#770169)
# HP DeskJet 720C (bug #797099)
# Kyocera FS-1118MFP (bug #782377)
%patch1 -p1

# Use sed instead of perl in the PPDs (bug #512739).
find db/source/PPD -type f -name '*.ppd' | xargs perl -pi -e 's,perl -p,sed,'

%build
%configure
make PREFIX=%{_prefix}


%install
make	DESTDIR=%buildroot PREFIX=%{_prefix} \
	install

# Remove ghostscript UPP drivers that are gone in 7.07
rm -f %{buildroot}%{_datadir}/foomatic/db/source/driver/{bjc6000a1,PM760p,PM820p,s400a1,sharp,Stc670pl,Stc670p,Stc680p,Stc760p,Stc777p,Stp720p,Stp870p}.upp.xml

find %{buildroot}%{_datadir}/foomatic/db/source/ -type f | xargs chmod 0644

mkdir %{buildroot}%{_datadir}/foomatic/db/source/PPD/Custom

rm -f	%{buildroot}%{_datadir}/foomatic/db/source/PPD/Kyocera/*.htm \
	%{buildroot}%{_datadir}/cups/model/3-distribution

# Convert absolute symlink to relative.
rm -f %{buildroot}%{_datadir}/cups/model/foomatic-db-ppds
ln -sf ../../foomatic/db/source/PPD %{buildroot}%{_datadir}/cups/model/foomatic-db-ppds

%files filesystem
%dir %{_datadir}/foomatic
%dir %{_datadir}/foomatic/db
%dir %{_datadir}/foomatic/db/source

%files
%doc db/source/PPD/Kyocera/*.htm
%doc README
%{_datadir}/foomatic/db/oldprinterids
%{_datadir}/foomatic/db/source/printer
%{_datadir}/foomatic/db/source/driver
%{_datadir}/foomatic/db/source/opt
%{_datadir}/foomatic/xmlschema

%files ppds
%doc COPYING
%{_datadir}/foomatic/db/source/PPD
%{_datadir}/cups/model/foomatic-db-ppds

%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 4.0-40.20140403
- 为 Magic 3.0 重建

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-39.20130604
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 04 2013 Jiri Popelka <jpopelka@redhat.com> - 4.0-38.20130604
- Remove some file conflicts (bug #967930)
- Updated to foomatic-db-4.0-20130604

* Tue May 07 2013 Jiri Popelka <jpopelka@redhat.com> - 4.0-37.20130507
- Updated to foomatic-db-4.0-20130507
- Removed old 'Obsoletes: oki4linux'

* Tue Mar 12 2013 Jiri Popelka <jpopelka@redhat.com> - 4.0-36.20130312
- Updated to foomatic-db-4.0-20130312

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-35.20121011
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 11 2012 Jiri Popelka <jpopelka@redhat.com> 4.0-34.20120719
- Updated to foomatic-db-4.0-20121011

* Thu Jul 19 2012 Jiri Popelka <jpopelka@redhat.com> 4.0-33.20120719
- Updated to foomatic-db-4.0-20120719

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-32.20120103
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 24 2012 Tim Waugh <twaugh@redhat.com> 4.0-31.20120103
- Device IDs for:
  - HP DeskJet 720C (bug #797099)
  - Kyocera FS-1118MFP (bug #782377)

* Wed Jan 04 2012 Jiri Popelka <jpopelka@redhat.com> 4.0-30.20120103
- Updated to foomatic-db-4.0-20120103
- spec modernized
- Device IDs for:
  - Brother MFC-8840D (#678065)
  - HP LaserJet M1522nf MFP (#745499)
  - Lexmark C453 (#770169)

* Tue Jun 14 2011 Tim Waugh <twaugh@redhat.com> 4.0-29.20110614
- Updated to foomatic-db-4.0-20110614.

* Mon Feb 21 2011 Tim Waugh <twaugh@redhat.com> 4.0-28.20110221
- Updated to foomatic-db-4.0-20110221.
- No longer need hpijs data.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-27.20101123
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Tim Waugh <twaugh@redhat.com> 4.0-26.20101123
- Rebuilt to pick up postscriptdriver tags now that python-cups
  provides the machinery for this.
- Build requires cups so that configure knows where to put PPDs.

* Wed Jan 19 2011 Jiri Popelka <jpopelka@redhat.com> 4.0-25.20101123
- Removed Brother P-touch (bug #560610, comment #10)

* Mon Dec 06 2010 Jiri Popelka <jpopelka@redhat.com> 4.0-24.20101123
- The pycups requirement is now python-cups.

* Mon Dec 06 2010 Jiri Popelka <jpopelka@redhat.com> 4.0-23.20101123
- Device IDs for:
  - HP Deskjet D4100 (bug #658091)
  - HP Color LaserJet CM4730 MFP (bug #658838)
  - HP LaserJet 4050/4100/4350/5100/8000/P3005 (bug #659041)
  - HP Color LaserJet 2500/3700/4550/4650/4700/5550 (bug #659042)

* Tue Nov 23 2010 Jiri Popelka <jpopelka@redhat.com> 4.0-22.20101123
- Updated to foomatic-db-4.0-20101123 (bug #655238).
- Device ID for Canon iR 3225 (bug #651500).

* Wed Nov 03 2010 Jiri Popelka <jpopelka@redhat.com> 4.0-21.20100819
- Remove wrong Device ID for Canon iR 3170C (bug #617493).

* Fri Aug 20 2010 Jiri Popelka <jpopelka@redhat.com> 4.0-20.20100819
- Removed printer/Samsung-CLP-300|315.xml (bug #625505).
- Removed references to foo2oak-z1.

* Thu Aug 19 2010 Jiri Popelka <jpopelka@redhat.com> 4.0-19.20100819
- Updated to foomatic-db-4.0-20100819, foomatic-db-hpijs-20090901.tar.gz
- Device ID for Canon iR 3170C (bug #617493).

* Mon Jul 12 2010 Jiri Popelka <jpopelka@redhat.com> 4.0-18.20100204
- Moved COPYING file to ppds sub-package.

* Mon May 17 2010 Tim Waugh <twaugh@redhat.com> 4.0-17.20100204
- Don't ship backup files.

* Sun May 16 2010 Tim Waugh <twaugh@redhat.com> 4.0-16.20100204
- Device IDs for another 1302 Ricoh PPDs.

* Thu May  6 2010 Tim Waugh <twaugh@redhat.com> 4.0-15.20100204
- Device IDs for:
  - HP Color LaserJet 2605dn (bug #583909).
  - HP DeskJet F300 (bug #585644).
  - HP OfficeJet 6200 (bug #215063).
  - HP PSC 1400 (bug #586381).
  - Ricoh Aficio MP C3500 (bug #589527).
  - Ricoh Aficio SP C420DN (bug #589533).

* Fri Apr 16 2010 Tim Waugh <twaugh@redhat.com> 4.0-14.20100204
- Device IDs for:
  - Canon BJC-4100 (bug #583060)
  - HP Color LaserJet 3800 (bug #581936).
  - HP DeskJet D2300 (bug #580341).
  - HP DeskJet F2100 (bug #579245).
  - HP OfficeJet 7300 (bug #577897).
  - Lexmark E120 (bug #577881).
  - HP DeskJet 1280 (bug #577870).
  - HP PhotoSmart 7400 (bug #577866).
  - Brother HL-2140 (bug #577863).
  - HP OfficeJet 6200 (bug #215063).
  - HP PSC 2400 (bug #188419).

* Fri Mar 26 2010 Tim Waugh <twaugh@redhat.com> 4.0-13.20100204
- Device IDs for HP PhotoSmart 2570, HP DeskJet 959C and HP OfficeJet
  Pro K550 (bug #577280, bug #577293, bug #577296).

* Thu Mar 25 2010 Tim Waugh <twaugh@redhat.com> 4.0-12.20100402
- Fixed missing units in driver margins (bug #576370).

* Fri Mar 19 2010 Tim Waugh <twaugh@redhat.com> 4.0-11.20100402
- Device ID for Kyocera Mita FS-1020D (bug #575063).

* Thu Feb  4 2010 Tim Waugh <twaugh@redhat.com> 4.0-10.20100402
- Rebuild for postscriptdriver tags.

* Thu Feb  4 2010 Tim Waugh <twaugh@redhat.com> 4.0-9.20100402
- Updated to foomatic-db-4.0-20100402.

* Fri Dec  4 2009 Tim Waugh <twaugh@redhat.com> 4.0-8.20091126
- Added foomatic-db-hpijs tarball back in.

* Thu Nov 26 2009 Tim Waugh <twaugh@redhat.com> 4.0-7.20091126
- Updated to foomatic-db-4.0-20091126 (bug #538994).

* Thu Aug 20 2009 Tim Waugh <twaugh@redhat.com> 4.0-6.20090819
- Removed references to foo2slx and foo2hiperc (bug #518267).

* Wed Aug 19 2009 Tim Waugh <twaugh@redhat.com> 4.0-5.20090819
- Updated to foomatic-db-4.0-20090819.
- Removed deprecated foomatic-db-hpijs tarball.
- Use buildroot macro throughout.

* Tue Aug 18 2009 Tim Waugh <twaugh@redhat.com> 4.0-4.20090702
- Use stcolor driver for Epson Stylus Color 200 (bug #513676).

* Mon Aug 17 2009 Tim Waugh <twaugh@redhat.com> 4.0-3.20090702
- License for ppds sub-package should include GPLv2+.
- Ship COPYING file in main package.
- Added filesystem sub-package for directory ownership.

* Mon Aug  3 2009 Tim Waugh <twaugh@redhat.com> 4.0-2.20090702
- Move foomatic-db-ppds symlink to ppds sub-package.
- Use sed instead of perl in raster PPDs (bug #512739).
- Removed code to convert old-style printer IDs (there are none).
- Ship README file.

* Mon Aug  3 2009 Tim Waugh <twaugh@redhat.com> 4.0-1.20090702
- Split database out from main foomatic package.

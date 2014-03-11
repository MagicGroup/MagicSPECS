Summary:	Clean up and pretty-print HTML/XHTML/XML
Name:		tidyp
Version:	1.02
Release:	7%{?dist}
License:	W3C
Group:		Applications/Text
Url:		http://www.tidyp.com/
Source0:	http://github.com/downloads/petdance/tidyp/tidyp-%{version}.tar.gz
Patch0:		tidy-outfile-raw.patch
Patch1:		tidyp-cflags.patch
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
Requires:	libtidyp%{?_isa} = %{version}-%{release}

%description
tidyp is a fork of tidy on SourceForge. The library name is "tidyp", and the
command-line tool is also "tidyp" but all internal API stays the same.

%package -n libtidyp
Summary:	Shared libraries for tidyp
Group:		System Environment/Libraries

%description -n libtidyp
Shared libraries for tidyp.

%package -n libtidyp-devel
Summary:	Development files for libtidyp
Group:		Development/Libraries
Requires:	libtidyp%{?_isa} = %{version}-%{release}

%description -n libtidyp-devel
Development files for libtidyp.

%prep
%setup -q

# Fix mangling of output file names (#725651)
# Sent upstream: https://github.com/petdance/tidyp/pull/18
%patch0 -p1

# Remove unwanted CFLAGS
%patch1 -p1

# Fix permissions for debuginfo
chmod -x src/{mappedio.*,version.h}

# Fix timestamp order to avoid trying to re-run autotools
touch aclocal.m4
find . -name Makefile.in -exec touch {} \;
touch configure

%build
%configure --disable-static --disable-dependency-tracking
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%check
make check

%clean
rm -rf %{buildroot}

%post -n libtidyp -p /sbin/ldconfig

%postun -n libtidyp -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc ChangeLog README
%{_bindir}/tidyp

%files -n libtidyp
%defattr(-,root,root,-)
%{_libdir}/libtidyp-%{version}.so.0*

%files -n libtidyp-devel
%defattr(-,root,root,-)
%{_includedir}/tidyp/
%{_libdir}/libtidyp.so
%exclude %{_libdir}/libtidyp.la

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.02-7
- 为 Magic 3.0 重建

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> 1.02-6
- rebuilt for gcc 4.7 in Rawhide

* Thu Aug 11 2011 Paul Howarth <paul@city-fan.org> 1.02-5
- fix mangling of output file names (#725651)

* Wed Feb  9 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.02-4
- rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 Jesse Keating <jkeating@redhat.com> 1.02-3
- rebuilt for gcc bug (#634757)

* Fri Jul 23 2010 Paul Howarth <paul@city-fan.org> 1.02-2
- re-jig for Fedora submission
- add ChangeLog and README as %%doc
- upstream URL now http://www.tidyp.com/
- drop obsolete of old libtidyp versions in main package

* Mon May 10 2010 Paul Howarth <paul@city-fan.org> 1.02-1
- update to 1.02
  - metatag check fixed
  - missing files for "make check" included
- drop upstreamed metatag patch
- fix dist tag for RHEL-6 Beta
- touch autotools-generated files in order to prevent attempted
  re-running of autotools at build time

* Mon Apr 26 2010 Paul Howarth <paul@city-fan.org> 1.00-1
- update to 1.00
  - removed -Wextra compiler flag for gcc, incompatible with older versions
  - added "check" and "tags" make targets
  - removed commented-out code
- add %%check section, using test data from upstream git since it was omitted
  from the distribution tarball
- drop upstreamed parts of patches
- merge autotools patch into cflags patch
- add patch to update "generator" metatag properly

* Mon Mar  1 2010 Paul Howarth <paul@city-fan.org> 0.99-2
- main package renamed to tidyp, as per upstream
- new subpackage libtidyp (same split as tidy in Fedora)
- upstream has now provided a proper tarball, with pre-built configure script,
  so rework build system patches and drop autotools buildreqs
- reworked upstream tarball no longer includes docs

* Wed Feb 17 2010 Paul Howarth <paul@city-fan.org> 0.99-1
- libtidyp forked from tidy
- add patches to autotools build to make it work more sanely

* Tue Dec  8 2009 Paul Howarth <paul@city-fan.org> 0.99.0-20.20091203.1
- 20091203 snapshot
- spec housecleaning
- tidy erroneously removed whitespace, causing mangled text (#481350)

* Fri Jul 31 2009 Paul Howarth <paul@city-fan.org> 0.99.0-19.20070615.1
- rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar  3 2009 Paul Howarth <paul@city-fan.org> 0.99.0-18.20070615.1
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Paul Howarth <paul@city-fan.org> 0.99.0-17.20070615.1
- respin (gcc 4.3.0)

* Mon Aug 28 2007 Paul Howarth <paul@city-fan.org> 0.99.0-16.20070615.1
- respin (BuildID)

* Fri Aug 24 2007 Paul Howarth <paul@city-fan.org> 0.99.0-15.20070615.1
- use standard shortname "WSC" for license tag

* Tue Jul 10 2007 Paul Howarth <paul@city-fan.org> 0.99.0-13.20070615.1
- 15th June 2007 snapshot

* Mon Jun 25 2007 Paul Howarth <paul@city-fan.org> 0.99.0-12.20070228.1
- upstream has stopped releasing tarballs and advocates CVS snapshots
  instead
- 28th February 2007 snapshot
- run setup.sh in %%prep rather than %%build
- fileio.h no longer included in -devel package

* Fri Sep 15 2006 Paul Howarth <paul@city-fan.org> 0.99.0-10.20051026
- add dist tag

* Tue Jun 20 2006 Paul Howarth <paul@city-fan.org> 0.99.0-9.20051026.4
- libtidy-devel depends on libtidy, not tidy

* Mon Jan 23 2006 Paul Howarth <paul@city-fan.org> 0.99.0-9.20051026
- Update source to 26 October 2005 version
- Bring back libtidy as per Fedora Extras package
- Never strip binaries

* Fri Oct 21 2005 Paul Howarth <paul@city-fan.org> 0.99.0-6.20051020
- Drop obsoletes/provides for libtidy-progs, which didn't work anyway
- Update to 051020 releases of both src and docs
- Remove buildroot unconditionally in %%clean and %%install
- Don't use macros for pathnames in build-time commands, hardcode them instead
- Wrap %%description at 80 columns

* Tue Aug  9 2005 Paul Howarth <paul@city-fan.org> 0.99.0-6.20050803
- Clean up doc generation
- Build quickref.html
- Strip binaries if we're not making a debuginfo package

* Tue Aug  9 2005 Paul Howarth <paul@city-fan.org> 0.99.0-5.20050803
- Update to 050803 and docs to 050705
- Rename packages *again* to be compatible with Fedora Extras

* Sun Jun  2 2005 Paul Howarth <paul@city-fan.org> 0.99.0-5.20050531
- Update to 050531 version
- Incorporate documentation, version 050502
- Rename/reversion package for Fedora Extras compatibility
- Exclude libtidy.la, not needed

* Tue Feb 01 2005 Paul Howarth <paul@city-fan.org>
- Update to 050120 version

* Wed Oct 27 2004 Paul Howarth <paul@city-fan.org>
- Update to 041026 version

* Tue Jul 20 2004 Paul Howarth <paul@city-fan.org>
- Update to 040706 version

* Thu May 13 2004 Paul Howarth <paul@city-fan.org>
- Initial RPM build

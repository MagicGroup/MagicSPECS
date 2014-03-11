Name:		fdupes
Summary:	Finds duplicate files in a given set of directories
Version:	1.51
Release:	3%{?dist}
License:	MIT
Group:		Applications/File
URL:		https://code.google.com/p/fdupes/
Source0:	https://fdupes.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:        macros.fdupes

Patch0:		fdupes-1.51-destdir.patch
# http://bugs.debian.org/353789
Patch1:		fdupes-1.50-typo.patch
# Fix CVE
Patch2:         fdupes-1.51-check-permissions.patch


%description
FDUPES is a program for identifying duplicate files residing within specified
directories.


%prep
%setup -q -n %{name}-%{version}
%patch2 -p1 -b .cve
%patch0 -p1 -b .destdir
%patch1 -p1 -b .typo


%build
make %{?_smp_mflags} COMPILER_OPTIONS="%{optflags}"


%check
./%{name} testdir
./%{name} --omitfirst testdir
./%{name} --recurse testdir
./%{name} --size testdir


%install
make install INSTALL="%{__install} -p" \
             BIN_DIR=%{_bindir} \
             MAN_BASE_DIR=%{_mandir} \
             DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -m 0644 %{SOURCE1} %{buildroot}%{_rpmconfigdir}/macros.d/


%files
%doc CHANGES CONTRIBUTORS README TODO
%doc %{_mandir}/man1/%{name}.1*
%{_bindir}/%{name}
%{_rpmconfigdir}/macros.d/macros.fdupes


%changelog
* Sun Jan 19 2014 Ville Skyttä <ville.skytta@iki.fi> - 1.51-3
- Move macros to %%{_rpmconfigdir}/macros.d.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.51-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Richard Shaw <hobbes1069@gmail.com> - 1.51-1
- Update to latest upstream release.
- Fixes security bugs BZ#865591 & 865592.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.50-0.7.PR2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.50-0.6.PR2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Richard Shaw <hobbes1069@gmail.com> - 1.50-0.5.PR2
- Add RPM macro.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.50-0.4.PR2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.50-0.3.PR2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.50-0.2.PR2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Feb 01 2009 Debarshi Ray <rishi@fedoraproject.org> - 1.50-0.1.PR2
- Version bump to 1.50 PR2.
  * Added --noprompt, --recurse and --summarize options
  * Now sorts duplicates (old to new) for consistent order when listing or
    deleting duplicate files.
  * Now tests for early matching of files, which should help speed up the
    matching process when large files are involved.
  * Added warning whenever a file cannot be deleted.
  * Fixed bug where some files would not be closed after failure.
  * Fixed bug where confirmmatch() function wouldn't always deal properly with
    zero-length files.
  * Fixed bug where progress indicator would not be cleared when no files were
    found.
- Inclusion of string.h now added by upstream.
- Added patch to fix file comparisons from Debian. (Debian BTS #213385)
- Added patch to enable large file support on 32-bit systems from Debian.
  (Debian BTS #447601)
- Added patch to fix typo in the online manual page from Debian. (Debian BTS
  #353789)

* Tue Feb 19 2008 Release Engineering <rel-eng@fedoraproject.org> - 1.40-12
- Autorebuild for gcc-4.3.

* Thu Dec 27 2007 Debarshi Ray <rishi@fedoraproject.org> - 1.40-11
- Fixed Makefile to preserve timestamps using 'cp -p'.

* Thu Nov 29 2007 Debarshi Ray <rishi@fedoraproject.org> - 1.40-10
- Release bumped to overcome spurious build.

* Sun Nov 25 2007 Debarshi Ray <rishi@fedoraproject.org> - 1.40-9
- Initial build. Imported SPEC from Rawhide.
- Fixed Makefile to use DESTDIR correctly.
- Fixed sources to include string.h.

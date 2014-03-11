Summary: A Hebrew spell checker
Name: hspell
Version: 1.1
Release: 6%{?dist}
URL: http://hspell.ivrix.org.il
Source: http://hspell.ivrix.org.il/hspell-%{version}.tar.gz
License: GPLv2
Group: Applications/Text
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: zlib-devel hunspell-devel
Patch0: hspell-1.0.sharedlib.patch

%description
Hspell is a Hebrew SPELLer and morphological analyzer. It provides a mostly
spell-like interface (gives the list of wrong words in the input text), but can
also suggest corrections (-c). It also provides a true morphological analyzer
(-l), that prints all known meanings of a Hebrew string.

%package devel
Summary: Library and include files for Hspell, the hebrew spell checker
Group: Applications/Text
Requires: %{name} = %{version}-%{release}

%description devel
Library and include files for applications that want to use Hspell.

%package static
Summary: Satic Library for Hspell, the hebrew spell checker
Group: Applications/Text
Requires: %{name}-devel = %{version}-%{release}

%description static
Satic Library for applications that want to use Hspell.

%package -n hunspell-he
Summary: Hebrew hunspell dictionaries
Group: Applications/Text
Requires: hunspell

%description -n hunspell-he
Hebrew hunspell dictionaries.

%prep
%setup -q
%patch0 -p1 -b .sharedlib.patch
/usr/bin/iconv -f hebrew -t utf8 -o WHATSNEW WHATSNEW

%build
%configure --enable-fatverb --enable-linginfo
make CFLAGS="$RPM_OPT_FLAGS" STRIP=:
make hunspell
cat >> hunspell/new_he.aff << EOF
MAP 10
MAP ךכח
MAP םמ
MAP ןנ
MAP ףפ
MAP ץצ
MAP כק
MAP אע # for English
MAP גה # for Russian
MAP צס # for Arabic
MAP חכר # for French
EOF

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
#rm -f $RPM_BUILD_ROOT/%{_libdir}/libhspell.a

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p hunspell/new_he.dic $RPM_BUILD_ROOT/%{_datadir}/myspell/he_IL.dic
cp -p hunspell/new_he.aff $RPM_BUILD_ROOT/%{_datadir}/myspell/he_IL.aff

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE README WHATSNEW COPYING
%{_bindir}/hspell
%{_bindir}/hspell-i
%{_bindir}/multispell
%{_libdir}/libhspell.so.0
%{_mandir}/man1/hspell.1*
%{_datadir}/hspell/

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/libhspell.so
%{_mandir}/man3/hspell.3*

%files static
%defattr(-,root,root)
%{_libdir}/libhspell.a

%files -n hunspell-he
%defattr(-,root,root,-)
%doc LICENSE
%{_datadir}/myspell/*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.1-6
- 为 Magic 3.0 重建

* Mon Dec 12 2011 Liu Di <liudidi@gmail.com> - 1.1-5
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan  9 2010 Dan Kenigsberg <danken@cs.technion.ac.il> - 1.1-3
- Rebuild with proper hunspell-devel dependency

* Fri Jan  1 2010 Dan Kenigsberg <danken@cs.technion.ac.il> - 1.1-2
- Rebase to upstream version 1.1 and fix spec typos.

* Thu Dec 31 2009 Dan Kenigsberg <danken@cs.technion.ac.il> - 1.1-1
- Rebase to upstream version 1.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 1.0-11
- Fix Patch0:/%%patch mismatch.

* Thu Jul 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0-10
- fix license tag

* Wed May 14 2008 Caolan McNamara <caolanm@redhat.com> - 1.0-9
- Resolves: rhbz#313231 build hspell.so instead of a .a

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0-8
- Autorebuild for GCC 4.3

* Tue May 22 2007 Dan Kenigsberg <danken@cs.technion.ac.il> 1.0-7
- Move the hunspell-he dictionaries into hspell package (Bug #240696).
  Mostly applying Caolan McNamara's patch #155078.
* Sun Feb 11 2007 Dan Kenigsberg <danken@cs.technion.ac.il> 1.0-6
- Use gzip -n to exclude MTIME from compressed data and resolve bug #228171
* Tue Sep 11 2006 Dan Kenigsberg <danken@cs.technion.ac.il> 1.0-5
- Rebuild for Fedora Extras 6
* Sun Jul  9 2006 Dan Kenigsberg <danken@cs.technion.ac.il> 1.0-4
- bump version to mend upgrade path. Bug #197125
* Sat May 20 2006 Dan Kenigsberg <danken@cs.technion.ac.il> 1.0-3
- do not strip the binary, create useful defuginfo package (Bug #192437).
* Sun May 15 2006 Dan Kenigsberg <danken@cs.technion.ac.il> 1.0-2
- new upstream release.
- Hebrew description converted to utf8.
* Tue Feb 28 2006 Dan Kenigsberg <danken@cs.technion.ac.il> 0.9-7
- Rebuild for Fedora Extras 5
* Mon Sep 26 2005 Dan Kenigsberg <danken@cs.technion.ac.il> 0.9-6
- Add the text of the GPL to the binary package. It seems that I'll do anything
  to make my sponsor Tom happy.
* Thu Sep 23 2005 Dan Kenigsberg <danken@cs.technion.ac.il> 0.9-5
- According to Tom's request, distribute the fat version.
- Add short Hebrew description to the devel package.
* Thu Sep 20 2005 Dan Kenigsberg <danken@cs.technion.ac.il> 0.9-4
- Distribute the "slim" flavor, as I suspect it is better suited for the casual
  user (even though I personally enjoy the chubby morphological analizer).
* Mon Sep 19 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.9-3
- minor spec file cleanups, eliminate "fat" variant
* Thu Sep 15 2005 Dan Kenigsberg <danken@cs.technion.ac.il> 0.9-2
- version 0.9, some magic to silence rpmlint
* Fri Jun  4 2004 Dan Kenigsberg <danken@cs.technion.ac.il> 0.8-1
- Some cleanups, and a devel package
* Fri Dec 20 2003 Dan Kenigsberg <danken@cs.technion.ac.il> 0.7-1
- Changes for version 0.7
* Tue Jul 29 2003 Dan Kenigsberg <danken@cs.technion.ac.il> 0.6-1
- Tiny changes for the C frontend
* Fri May  2 2003 Dan Kenigsberg <danken@cs.technion.ac.il> 0.5-1
- create the "fat" variant
* Mon Feb 17 2003 Dan Kenigsberg <danken@cs.technion.ac.il> 0.3-2
- The release includes only the compressed database.
- Added signature, and some other minor changes.
* Sun Jan  5 2003 Tzafrir Cohen <tzafrir@technion.ac.il> 0.2-1
- Initial build.

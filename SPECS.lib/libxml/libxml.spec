Name:		libxml
Summary:	Old XML library for Gnome-1 application compatibility
Summary(zh_CN.UTF-8): Gnome-1 应用程序兼容的旧 XML 库
Epoch:		1
Version:	1.8.17
Release:	34%{?dist}
License:	LGPLv2+ or W3C
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:		http://veillard.com/XML/
Source:		ftp://xmlsoft.org/libxml/old/libxml-%{version}.tar.gz
Patch0:		libxml-1.8.17-CAN-2004-0110.patch
Patch1:		libxml-1.8.17-ficora-245608.patch
Patch2:		libxml-1.8.17-CVE-2011-1944.patch
Patch10:	libxml-1.8.17-open-mode.patch
Patch11:	libxml-1.8.17-multiarch.patch
Patch12:	libxml-1.8.17-declarations.patch
Patch13:	libxml-1.8.17-ppc64-config.patch
Patch14:	libxml-1.8.17-utf8.patch
Patch15:	libxml-1.8.17-xpath.patch
Patch16:	libxml-1.8.17-aarch64-config.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)

%description
This library allows old Gnome-1 applications to manipulate XML files.

%description -l zh_CN.UTF-8
Gnome-1 应用程序兼容的旧 XML 库。

%package devel
Summary:	Libraries, includes, etc. to build old libxml-based applications
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name}%{?_isa} = %{epoch}:%{version}-%{release}, pkgconfig

%description devel
Libraries, includes, etc. to build old libxml-based applications.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

# fix CVE-2004-0110 & CVE-2004-0989 (arbitrary code execution via a long URL)
%patch0 -p1

# fix CVE-2009-2414 (stack consumption DoS vulnerabilities)
# fix CVE-2009-2416 (use-after-free DoS vulnerabilities)
%patch1 -p0

# fix CVE-2011-1944 (heap-based buffer overflow by adding new namespace node to
# an existing nodeset or merging nodesets)
%patch2 -p1

# open() with O_CREAT must have 3 arguments
%patch10 -p1

# make xml-config script arch-independent for multiarch compatibility
%patch11 -p1

# silence warnings about implicit function declarations
%patch12 -p1 -b .decl

# fix ppc64 builds
%patch13 -p1

# recode ChangeLog as UTF-8
%patch14 -p1

# fix segfault and regressions in xpath tests
%patch15 -p1

# fix config.guess and config.sub to support build on aarch64 (#925948)
%patch16

%build
export CFLAGS="%{optflags} -Werror-implicit-function-declaration"
%configure --disable-static
# Makefile doesn't work with %%{_smp_mflags}
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} INSTALL="install -p" install

# hack to get /usr/include/gnome-xml/libxml/
if [ -d %{buildroot}/%{prefix}/include/gnome-xml ]; then
	ln -s -f . %{buildroot}/%{_includedir}/gnome-xml/libxml
fi
magic_rpm_clean.sh

%check
make testall

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog README COPYING.LIB TODO
%{_libdir}/libxml.so.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/xml-config
%{_datadir}/gnome-xml/
%{_includedir}/gnome-xml/
%{_libdir}/libxml.so
%{_libdir}/xmlConf.sh
%{_libdir}/pkgconfig/libxml.pc
%exclude %{_libdir}/libxml.la

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1:1.8.17-34
- 为 Magic 3.0 重建

* Fri Aug 08 2014 Liu Di <liudidi@gmail.com> - 1:1.8.17-33
- 为 Magic 3.0 重建

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.17-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 24 2013 Paul Howarth <paul@city-fan.org> 1:1.8.17-31
- fix config.guess and config.sub to support build on aarch64 (#925948)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1:1.8.17-30
- rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1:1.8.17-29
- rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan  5 2012 Paul Howarth <paul@city-fan.org> 1:1.8.17-28
- rebuilt for gcc 4.7

* Fri Jun  3 2011 Paul Howarth <paul@city-fan.org> 1:1.8.17-27
- fix segfault and regressions in xpath tests
- use a patch rather than iconv to fix the ChangeLog encoding

* Thu Jun  2 2011 Paul Howarth <paul@city-fan.org> 1:1.8.17-26
- add patch for CVE-2011-1944 (#709751)
- add %%check section and run regression tests (note that diffs appearing in
  the output do not cause the build to fail)
- nobody else likes macros for commands

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1:1.8.17-25
- rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 12 2009 Paul Howarth <paul@city-fan.org> 1:1.8.17-24
- renumber existing patches to free up low-numbered patches for EL-3 patches
- add patch for CVE-2004-0110 and CVE-2004-0989 (#139090)
- add patch for CVE-2009-2414 and CVE-2009-2416 (#515195, #515205)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1:1.8.17-23
- rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 20 2009 Paul Howarth <paul@city-fan.org> 1:1.8.17-22
- rebuild for %%{_isa} provides/requires

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1:1.8.17-21
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 21 2008 Paul Howarth <paul@city-fan.org> 1:1.8.17-20
- fixes for building with -Werror-implicit-function-declaration and some of the
  compiler warnings
- fix config.guess and config.sub to support build on ppc64

* Wed Feb 13 2008 Paul Howarth <paul@city-fan.org> 1:1.8.17-19
- rebuild with gcc 4.3.0 for Fedora 9

* Fri Oct 26 2007 Paul Howarth <paul@city-fan.org> 1:1.8.17-18
- fix multiarch conflict in xml-config (#342501)
- preserve timestamps for files copied from source to installed package
- re-encode ChangeLog as UTF-8

* Thu Aug 30 2007 Paul Howarth <paul@city-fan.org> 1:1.8.17-17
- rebuild for BuildID inclusion
  (http://fedoraproject.org/wiki/Releases/FeatureBuildId)

* Fri Aug 17 2007 Paul Howarth <paul@city-fan.org> 1:1.8.17-16
- add mode to fix call to open() with O_CREAT and only 2 args
- unexpand tabs in spec
- update license tag

* Mon Sep 11 2006 Paul Howarth <paul@city-fan.org> 1:1.8.17-15
- add release to versioned dependency of libxml-devel on libxml
- drop COPYING file; license is dual W3C/LGPL and the only GPL bits are in the
  build system (e.g. libtool), which is not distributed

* Sat Aug 26 2006 Paul Howarth <paul@city-fan.org> 1:1.8.17-14
- add dist tag
- devel package requires pkgconfig
- update URL to http://veillard.com/XML/
- update source URL
- use Fedora Extras standard buildroot
- own %%{_datadir}/gnome-xml/
- don't include empty NEWS file
- don't include static library or libtool archive
- add note about Makefile being broken with %%{_smp_mflags}
- use make/DESTDIR instead of %%makeinstall
- remove pointless prereq: /sbin/install-info
- cosmetic clean-up of spec file

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1:1.8.17-13.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1:1.8.17-13.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:1.8.17-13.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Feb  9 2005 Daniel Veillard <veillard@redhat.com> 1.8.17-13
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Jun  8 2003 Tim Powers <timp@redhat.com> 1:1.8.17-9.1
- build for RHEL

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epochs where needed.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sun Jan 19 2003 Daniel Veillard <veillard@redhat.com> 1.8.17-7
- apparently there was an old 1.8.17-6 laying around

* Tue Jan 14 2003 Daniel Veillard <veillard@redhat.com> 1.8.17-6
- cleaned up the spec file, rebuild for RawHide

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jan 28 2002 Daniel Veillard <veillard@redhat.com>
- updated to 1.8.17
- made sure the Epoch is set

* Sun Aug 05 2001 Jens Finke <jens@triq.net>
- Merged GPP spec file with spec.in file from CVS.
- Added %%{_datadir}/gnome-xml to devel package to include documentation.
- Added libxml.pc file.

* Wed Jul 18 2001 Gregory Leblanc <gleblanc@cu-portland.edu>
- removed unncessary %%defines 
- made %%setup -quiet
- fixed buildroot
- fixed source line

* Thu Feb 22 2001 Gregory Leblanc <gleblanc@cu-portland.edu>
- fixed macros, removed hard-coded paths, that sort of thing.

* Thu Sep 23 1999 Daniel Veillard <Daniel.Veillard@w3.org>
- corrected the spec file alpha stuff
- switched to version 1.7.1
- Added validation, XPath, nanohttp, removed memory leaks
- Renamed CHAR to xmlChar

* Wed Jun  2 1999 Daniel Veillard <Daniel.Veillard@w3.org>
- Switched to version 1.1: SAX extensions, better entities support, lots of
  bug fixes.

* Sun Oct  4 1998 Daniel Veillard <Daniel.Veillard@w3.org>
- Added xml-config to the package

* Thu Sep 24 1998 Michael Fulbright <msf@redhat.com>
- Built release 0.30

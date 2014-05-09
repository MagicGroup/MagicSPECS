Summary:	Validating XML Parser
Name:		xerces-c
Version:	3.1.1
Release:	5%{?dist}
License:	ASL 2.0
Group:		System Environment/Libraries
URL:		http://xml.apache.org/xerces-c/
Source0:	http://archive.apache.org/dist/xerces/c/3/sources/xerces-c-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	dos2unix

%description 
Xerces-C is a validating XML parser written in a portable
subset of C++. Xerces-C makes it easy to give your application the
ability to read and write XML data. A shared library is provided for
parsing, generating, manipulating, and validating XML
documents. Xerces-C is faithful to the XML 1.0 recommendation and
associated standards: XML 1.0 (Third Edition), XML 1.1 (First
Edition), DOM Level 1, 2, 3 Core, DOM Level 2.0 Traversal and Range,
DOM Level 3.0 Load and Save, SAX 1.0 and SAX 2.0, Namespaces in XML,
Namespaces in XML 1.1, XML Schema, XML Inclusions).


%package	devel
Summary:	Header files, libraries and development documentation for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%package doc
Group:		Documentation
Summary:	Documentation for Xerces-C++ validating XML parser
BuildArch:	noarch

%description doc
Documentation for Xerces-C++.

Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

%prep
%setup -q 
# Copy samples before build to avoid including built binaries in -doc package
mkdir -p _docs
cp -a samples/ _docs/

%build
# --disable-sse2 makes sure explicit -msse2 isn't passed to gcc so
# the binaries would be compatible with non-SSE2 i686 hardware.
# This only affects i686, as on x86_64 the compiler uses SSE2 by default.
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
export CXXFLAGS="$CFLAGS"
%configure --disable-static \
  --disable-pretty-make \
  --disable-sse2
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR="$RPM_BUILD_ROOT"
# Correct errors in encoding
iconv -f iso8859-1 -t utf-8 CREDITS > CREDITS.tmp && mv -f CREDITS.tmp CREDITS
# Correct errors in line endings
pushd doc; dos2unix -k *.xml; popd
# Remove unwanted binaries
rm -rf $RPM_BUILD_ROOT%{_bindir}
# Remove .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/libxerces-c-3.*.so

%files devel
%defattr(-,root,root,-)
%{_libdir}/libxerces-c.so
%{_libdir}/pkgconfig/xerces-c.pc
%{_includedir}/xercesc/

%files doc
%defattr(-,root,root,-)
%doc README LICENSE NOTICE CREDITS doc _docs/*

%changelog
* Wed Apr 30 2014 Liu Di <liudidi@gmail.com> - 3.1.1-5
- 为 Magic 3.0 重建

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Mar 09 2011 Kalev Lember <kalev@smartlink.ee> - 3.1.1-1
- Update to 3.1.1
- Dropped CVE-2009-1885 patch.
- Use dos2unix -k instead of unrecognized option -U
- Removed the multilib conflict workaround as Xerces_autoconf_config.hpp
  no longer contains the conflicting XERCES_SIZEOF_LONG define.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul  9 2010 Jonathan Robie <jrobie@localhost.localdomain> - 3.0.1-20
- Added no-strict-aliasing flag to stop rpmdiff from griping

* Wed May 26 2010 Kalev Lember <kalev@smartlink.ee> 3.0.1-19
- Fix multilib conflict caused by Xerces_autoconf_config.hpp (#595923)

* Fri May 14 2010 Kalev Lember <kalev@smartlink.ee> 3.0.1-18
- Build -doc subpackage as noarch

* Fri May 14 2010 Kalev Lember <kalev@smartlink.ee> 3.0.1-17
- Disable explicit -msse2 to make sure the binaries run on non-SSE2 i686

* Sun Feb 07 2010 Kalev Lember <kalev@smartlink.ee> 3.0.1-16
- Reintroduce a patch for CVE-2009-1885
- Don't build static library
- Use parallel make
- Spec file clean up

* Thu Feb 4 2010 Jonathan Robie <jonathan.robie@redhat.com> 3.0.1-15
- Corrected .spec file

* Wed Feb 3 2010 Jonathan Robie <jonathan.robie@redhat.com> 3.0.1-1
- Move to Xerces 3.0.1.

* Thu Aug  6 2009 Peter Lemenkov <lemenkov@gmail.com> 2.8.0-5
- Fix CVE-2009-1885

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jun 30 2008 Peter Lemenkov <lemenkov@gmail.com> 2.8.0-2
- Spec cleanups ( https://bugzilla.redhat.com/show_bug.cgi?id=435132 )

* Sun Feb 10 2008 Peter Lemenkov <lemenkov@gmail.com> 2.8.0-1
- Ver. 2.8.0

* Sat Nov 25 2006 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-6
- typo fix

* Sat Nov 25 2006 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-5
- fixed some rpmlint warnings

* Fri Nov 24 2006 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-4
- Added samples to docs-package

* Sat Nov 18 2006 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-3
- improvements suggested by Aurelien Bompard

* Sat Oct 14 2006 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-2
- Disabled package 'samples'

* Fri Oct 13 2006 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-1
- initial build for FE

* Fri Jan 06 2006 Dag Wieers <dag@wieers.com> - 2.7.0-1 - 3891/dag
- Cleaned SPEC file.

* Tue Jan 03 2006 Dries Verachtert <dries@ulyssis.org> - 2.7.0-1
- Updated to release 2.7.0.

* Thu Sep 22 2005 C.Lee Taylor <leet@leenx.co.za> 2.6.1-1
- Update to 2.6.1
- Build for FC4 32/64bit

* Sat Aug 20 2005 Che
- initial rpm release

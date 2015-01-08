Name:           xsd
Version:        3.3.0
Release:        16%{?dist}
Summary:        W3C XML schema to C++ data binding compiler

Group:          Development/Tools
# Exceptions permit otherwise GPLv2 incompatible combination with ASL 2.0
License:        GPLv2 with exceptions and ASL 2.0  
URL:            http://www.codesynthesis.com/products/xsd/
Source0:        http://www.codesynthesis.com/download/xsd/3.3/xsd-%{version}-2+dep.tar.bz2
# Sent suggestion to upstream via e-mail 20090707
Patch0:         xsd-3.3.0-xsdcxx-rename.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  m4 boost-devel xerces-c-devel
# Requires:  ace-devel - only needed for applications using
#                        Adaptive Communication Environment (ACE) streams,
#                        enable when Fedora gets ACE packages.
#                        See http://www.cs.wustl.edu/~schmidt/ACE.html and
#                        https://bugzilla.redhat.com/show_bug.cgi?id=450164
Requires:       xerces-c-devel

%description
CodeSynthesis XSD is an open-source, cross-platform W3C XML Schema to
C++ data binding compiler. Provided with an XML instance specification
(XML Schema), it generates C++ classes that represent the given
vocabulary as well as parsing and serialization code.
You can then access the data stored in XML using types and functions
that semantically correspond to your application domain rather than
dealing with intricacies of reading and writing XML.


%package        doc
Group:          Documentation
Summary:        API documentation files for %{name}

%description    doc
This package contains API documentation for %{name}.


%prep
%setup -q -n xsd-%{version}-2+dep
pushd xsd
%patch0 -p1 -b .xsdcxx-rename
popd


%build

# Default GCC on EL-5 will fail on this code with internal
# compiler error when debugging symbol generation is requested with -g
# Reducing debug level to 1 will "fix" this problem. A better way would
# be to use gcc-44, but old versions of boost headers do not compile 
# with it (https://svn.boost.org/trac/boost/ticket/2069).
# Also boost-1.33.1 on those systems does not have boost_system library
# thus we need to disable explicit linking against it.

%if 0%{?el5}
make verbose=1 CXXFLAGS="$RPM_OPT_FLAGS -g1" BOOST_LINK_SYSTEM=n
%else
make verbose=1 CXXFLAGS="$RPM_OPT_FLAGS"
%endif


%install
rm -rf $RPM_BUILD_ROOT
rm -rf apidocdir

%if 0%{?el5}
make install_prefix="$RPM_BUILD_ROOT%{_prefix}" BOOST_LINK_SYSTEM=n install
%else
make install_prefix="$RPM_BUILD_ROOT%{_prefix}" install
%endif

# Split API documentation to -doc subpackage.
mkdir apidocdir
mv $RPM_BUILD_ROOT%{_datadir}/doc/xsd/*.{xhtml,css} apidocdir/
mv $RPM_BUILD_ROOT%{_datadir}/doc/xsd/cxx/ apidocdir/
mv $RPM_BUILD_ROOT%{_datadir}/doc/xsd/ docdir/

# Convert to utf-8.
for file in docdir/NEWS; do
    mv $file timestamp
    iconv -f ISO-8859-1 -t UTF-8 -o $file timestamp
    touch -r timestamp $file
done

# Rename binary to xsdcxx to avoid conflicting with mono-web package.
# Sent suggestion to upstream via e-mail 20090707
# they will consider renaming in 4.0.0
mv $RPM_BUILD_ROOT%{_bindir}/xsd $RPM_BUILD_ROOT%{_bindir}/xsdcxx
mv $RPM_BUILD_ROOT%{_mandir}/man1/xsd.1 $RPM_BUILD_ROOT%{_mandir}/man1/xsdcxx.1

# Remove duplicate docs.
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/libxsd

# Remove Microsoft Visual C++ compiler helper files.
rm -rf $RPM_BUILD_ROOT%{_includedir}/xsd/cxx/compilers

# Remove redundant PostScript files that rpmlint grunts about not being UTF8
# See: https://bugzilla.redhat.com/show_bug.cgi?id=502024#c27
# for Boris Kolpackov's explanation about those
find apidocdir -name "*.ps" | xargs rm -f
# Remove other unwanted crap
find apidocdir -name "*.doxygen" \
            -o -name "makefile" \
            -o -name "*.html2ps" | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc docdir/*
%{_bindir}/xsdcxx
%{_includedir}/xsd/
%{_mandir}/man1/xsdcxx.1*

%files doc
%defattr(-,root,root,-)
%doc apidocdir/*


%changelog
* Mon Dec 29 2014 Liu Di <liudidi@gmail.com> - 3.3.0-16
- 为 Magic 3.0 重建

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 3.3.0-15
- Rebuild for Boost-1.53.0

* Sun Aug 12 2012 Rex Dieter <rdieter@fedoraproject.org> 3.3.0-14
- xsd-3.3.0-2+dep 

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.0-12
- Update to xsd-3.3.0-1+dep upstream tarball, which includes the gcc 4.7 patch

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-11
- Rebuilt for c++ ABI breakage

* Thu Jan 19 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 3.3.0-10
- Add xsd-3.3.0-gcc47.patch (Fix mass rebuild FTBFS).

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 26 2011 Thomas Spura <tomspur@fedoraproject.org> - 3.3.0-8
- rebuild for https://fedoraproject.org/wiki/Features/F17Boost148

* Fri Jul 22 2011 Antti Andreimann <Antti.Andreimann@mail.ee> - 3.3.0-7
- Rebuilt for boost 1.47.0

* Wed Apr 06 2011 Kalev Lember <kalev@smartlink.ee> - 3.3.0-6
- Rebuilt for boost 1.46.1 soname bump

* Thu Mar 10 2011 Kalev Lember <kalev@smartlink.ee> - 3.3.0-5
- Rebuilt with xerces-c 3.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 06 2011 Thomas Spura <tomspur@fedoraproject.org> - 3.3.0-3
- rebuild for new boost (thanks Petr Machata for the fix)

* Mon Aug 02 2010 Antti Andreimann <Antti.Andreimann@mail.ee> 3.3.0-2
- Rebuild for new boost

* Sun Jun 20 2010 Antti Andreimann <Antti.Andreimann@mail.ee> 3.3.0-1
- Updated to version 3.3.0
- Implemented a workaround for gcc segfault on el5

* Sun Feb 07 2010 Caolán McNamara <caolanm@redhat.com> - 3.2.0-7
- Rebuild for xerces soname bump

* Fri Jan 22 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 3.2.0-6
- Rebuild for Boost soname bump

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 07 2009 Antti Andreimann <Antti.Andreimann@mail.ee> 3.2.0-4
- Removed redundant PostScript files from the doc package

* Mon Jul 06 2009 Antti Andreimann <Antti.Andreimann@mail.ee> 3.2.0-3
- Added ACE homepage to SPEC file comments
- Added verbose=1 to MAKEFLAGS so compiler flags could be
  verified from build logs.

* Mon Jul 04 2009 Antti Andreimann <Antti.Andreimann@mail.ee> 3.2.0-2
- Changed License tag to clarify which exceptions we are talking about

* Wed May 20 2009 Antti Andreimann <Antti.Andreimann@mail.ee> 3.2.0-1
- Initial RPM release.

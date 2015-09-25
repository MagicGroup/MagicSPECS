Name:           xqilla
Version:        2.3.0
Release:        7%{?dist}
Summary:        XQuery and XPath 2.0 library, built on top of Xerces-C

License:        ASL 2.0
URL:            http://xqilla.sourceforge.net/HomePage
Source0:        http://downloads.sourceforge.net/xqilla/XQilla-%{version}.tar.gz
Source1:        xqilla.1
# since header xqc.h is provided by xqc
Patch0:         xqilla-2.2.4-use-system-xqc.h.patch

BuildRequires:  xerces-c-devel >= 3.0.1 
BuildRequires:  xqc
BuildRequires:  doxygen graphviz

%description
XQilla is an XQuery and XPath 2.0 implementation written in C++ and based
on Xerces-C. It implements the DOM 3 XPath API, as well as having it's own
more powerful API. It conforms to the W3C proposed recommendation of XQuery
and XPath 2.0.

%package        devel
Summary:        XQilla is an XQuery and XPath 2.0 library, built on top of Xerces-C
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       xerces-c-devel%{?_isa} >= 3.0.1
Requires:       xqc

%description    devel
XQilla is an XQuery and XPath 2.0 implementation written in C++ and based
on Xerces-C. It implements the DOM 3 XPath API, as well as having it's own
more powerful API. It conforms to the W3C proposed recommendation of XQuery
and XPath 2.0.

%package        doc
Summary:        XQilla documentation
Group:          Documentation
BuildArch:      noarch

%description    doc
simple-api and dom3-api documentation for XQilla.

%prep
%setup -qn XQilla-%{version}
%patch0 -p1 -b .xqc

%build
# ensure that xqc.h is not used
rm -f ./include/xqc.h
%configure \
  --disable-static \
  --with-xerces=%{_prefix}

# Avoid lib64 rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}
make docs

%install
# force timestamp preservation when using install program
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -name '*.la' -exec rm -f '{}' ';'
install -D -p -m0664 %{SOURCE1} %{buildroot}/%{_mandir}/man1/%{name}.1

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc ChangeLog LICENSE
%{_bindir}/xqilla
%{_libdir}/libxqilla.so.*
%{_mandir}/man1/%{name}.1.*

%files devel
%{_libdir}/libxqilla.so
%{_includedir}/xqilla/

%files doc
%doc docs/dom3-api/ docs/simple-api/ LICENSE


%changelog
* Fri Sep 25 2015 Liu Di <liudidi@gmail.com> - 2.3.0-7
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.3.0-5
- Rebuilt for GCC 5 C++11 ABI change

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Apr 13 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 2.3.0-1
- upstream 2.3.0
- spec cleanup

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 28 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 2.2.4-5
- fix FTBFS with GCC 4.7 (RHBZ #817274)

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-4
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Aug 05 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 2.2.4-2
- revive xqilla from deprecated
- add man page from debian for xqilla command-line tool
- do not install bundled xqc.h and Requires: xqc

* Thu Mar 10 2011 Kalev Lember <kalev@smartlink.ee> - 2.2.4-1
- Update to 2.2.4
- Added a patch to fix build with GCC 4.6

* Thu Mar 10 2011 Kalev Lember <kalev@smartlink.ee> - 2.2.3-10
- Rebuilt with xerces-c 3.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri May 14 2010 Kalev Lember <kalev@smartlink.ee> - 2.2.3-8
- Require fully versioned main package for -devel subpackage
- Don't build static library
- Removed library Requires which are automatically picked up by rpm
- Removed spurious BR autoconf automake libtool
- Build -doc subpackage as noarch
- Install documentation with %%doc macro
- Use %%{_prefix} instead of hardcoding /usr
- Use parallel make
- Various other spec file clean ups

* Mon Mar  8 2010 Jonathan Robie <jrobie@localhost.localdomain> - 2.2.3-7
- Removed static library, per Fedora packaging guidelines.

* Mon Feb  8 2010 Jonathan Robie <jrobie@localhost.localdomain> - 2.2.3-6
- Fixed rpath problem detected by rpmlint

* Fri Feb  5 2010 Jonathan Robie <jrobie@localhost.localdomain> - 2.2.3-3
- Move to version 2.2.3, using Xerces 3.0.1

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-0.7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 14 2009 Robert Scheck <robert@fedoraproject.org> 2.1.3-0.6
- Added a few #include lines needed to build properly with g++ 4.4

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-0.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan  7 2009 Milan Zazrivec <mzazrivec@redhat.com> 2.1.3-0.4
- fixed requirements for xqilla-devel package

* Tue Dec  2 2008 Milan Zazrivec <mzazrivec@redhat.com 2.1.3-0.3
- fix for bz #473997 - xqilla : Unowned directories

* Fri Aug 29 2008 Milan Zazrivec <mzazrivec@redhat.com> 2.1.3-0.2
- Rebased XQilla to latest upstream version 2.1.3
- Fixed files section in spec (documentation was included twice)

* Fri Feb 29 2008 Milan Zazrivec <mzazrivec@redhat.com> 2.0.0-5
- Create xqilla-doc package for xqilla documentation

* Wed Feb 20 2008 Milan Zazrivec <mzazrivec@redhat.com> - 2.0.0-4
- Fix Requires: value for xqilla-devel

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.0-3
- Autorebuild for GCC 4.3

* Tue Feb 19 2008 Milan Zazrivec <mazrivec@redhat.com> 2.0.0-2
- Included Xerces-C 2.8.0 sources
- Add missing #include <cstring> where needed (g++ 4.3 changes)

* Thu Jan 10 2008 Milan Zazrivec <mzazrivec@redhat.com> 2.0.0-1
- Removed src/mapm/mapm_mt.cpp
- Added modified mapm_mt.c, taken from MAPM library ver. 4.9.5
- Added parallel make

* Tue Jan 08 2008 Milan Zazrivec <mzazrivec@redhat.com> 2.0.0-0
- Initial packaging of version 2.0.0

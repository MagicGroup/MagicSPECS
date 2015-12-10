Summary: A library for supporting Open Financial Exchange (OFX)
Name: libofx
Version: 0.9.9
Release: 6%{?dist}
URL: http://libofx.sourceforge.net/
Group:	System Environment/Libraries
License: GPLv2+
Source: http://downloads.sourceforge.net/libofx/%{name}-%{version}.tar.gz
Patch0: fix-ftbfs-gcc4.7.diff

BuildRequires: opensp-devel
BuildRequires: curl-devel
BuildRequires: libxml++-devel

%description
This is the LibOFX library.  It is a API designed to allow applications to
very easily support OFX command responses, usually provided by financial
institutions.  See http://www.ofx.net/ofx/default.asp for details and
specification. 

%package -n ofx
Summary: Tools for manipulating OFX data
Group: Applications/Productivity
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n ofx
The ofx package contains tools for manipulating OFX data from the
command line; they are often used when testing libofx.

%package devel
Summary: Development files needed for accessing OFX data
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The libofx-devel contains the header files and libraries necessary
for building applications that use libofx.

%prep
%setup -q
%patch0 -p1 -b .gcc47

rm -rf ./doc/ofx_sample_files/CVS
chmod 644 ./doc/ofx_sample_files/*

%build
%configure --with-opensp-libs=%{_libdir} --disable-static --disable-rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*.la $RPM_BUILD_ROOT%{_datadir}/doc

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README totest.txt
%{_libdir}/libofx.so.*
%{_datadir}/libofx/

%files -n ofx
%defattr(-,root,root)
%{_bindir}/ofx*
%{_mandir}/man1/ofx*

%files devel
%defattr(-,root,root)
%doc doc/html doc/ofx_sample_files
%{_includedir}/libofx/
%{_libdir}/pkgconfig/libofx.pc
%{_libdir}/libofx.so

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 0.9.9-6
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.9.9-5
- 为 Magic 3.0 重建

* Wed Jul 23 2014 Liu Di <liudidi@gmail.com> - 0.9.9-4
- 更新到 0.9.9

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.9.5-2
- enumerate %%files a bit, so abi bumps aren't a surprise
- tighten subpkg deps via %%_isa
- -devel: drop Requires: opensp-devel

* Mon Jul 09 2012 Bill Nottingham <notting@redhat.com> - 0.9.5-1
- update to 0.9.5 (#838473)

* Sat Apr 28 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.9.4-4
- Add patch to fix FTBFS on gcc 4.7

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-3
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Apr 19 2011 Bill Nottingham <notting@redhat.com> - 0.9.4-1
- update to 0.9.4

* Mon Feb 14 2011 Bill Nottingham <notting@redhat.com> - 0.9.2-1
- update to 0.9.2

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar  5 2009 Bill Nottingham <notting@redhat.com> - 0.9.1-1
- update to 0.9.1
- remove xml++ support - we've never built it

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep  9 2008 Bill Nottingham <notting@redhat.com> - 0.9.0-1
- update to 0.9.0

* Thu Feb 14 2008 Bill Nottingham <notting@redhat.com> - 0.8.3-5
- fix build with gcc-4.3
- add patch for other account types (#415961)

* Wed Oct 10 2007 Bill Nottingham <notting@redhat.com> - 0.8.3-4
- rebuild for buildid

* Fri Aug  3 2007 Bill Nottingham <notting@redhat.com>
- tweak license tag

* Tue Jan  9 2007 Bill Nottingham <notting@redhat.com> - 0.8.3-3
- update to 0.8.3
- add in (not used) xml++ support pending upstream
- add opensp-devel buildreq, remove INSTALL
- split off binaries into ofx package

* Mon Jan  8 2007 Bill Nottingham <notting@redhat.com> - 0.8.2-3
- spec tweaks

* Mon Aug 28 2006 Bill Nottingham <notting@redhat.com> - 0.8.2-1
- update to 0.8.2

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.8.0-3.1
- rebuild

* Tue Jul 11 2006 Bill Nottingham <notting@redhat.com> - 0.8.0-3
- own %%{_datadir}/libofx (#169336)

* Mon May 15 2006 Brian Pepple <bdpepple@ameritech.net> - 0.8.0-2.3
- Add BR for curl-devel.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.8.0-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.8.0-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan  6 2006 Nalin Dahyabhai <nalin@redhat.com> 0.8.0-2
- rebuild

* Tue Dec 20 2005 Bill Nottingham <notting@redhat.com> 0.8.0-1
- update to 0.8.0

* Tue Dec 13 2005 Tim Waugh <twaugh@redhat.com> 0.7.0-4
- Build requires: openjade-devel -> opensp-devel.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon May 23 2005 Bill Nottingham <notting@redhat.com> 0.7.0-3
- remove static libs

* Tue Mar  8 2005 Bill Nottingham <notting@redhat.com> 0.7.0-2
- fix build with gcc4

* Wed Feb  9 2005 Bill Nottingham <notting@redhat.com> 0.7.0-1
- update to 0.7.0

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com> 0.6.6-2
- rebuilt
- Add gcc 3.4 patch

* Fri Mar 12 2004 Bill Nottingham <notting@redhat.com> 0.6.6-1
- split off from gnucash, adapt upstream spec, add -devel package

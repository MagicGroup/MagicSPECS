Name:           libnetfilter_conntrack
Version:        1.0.4
Release:        3%{?dist}
Summary:        Netfilter conntrack userspace library
Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://netfilter.org
Source0:        http://netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libnfnetlink-devel >= 1.0.1, pkgconfig, kernel-headers, libmnl-devel >= 1.0.3

%description
libnetfilter_conntrack is a userspace library providing a programming 
interface (API) to the in-kernel connection tracking state table.

%package        devel
Summary:        Netfilter conntrack userspace library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}, libnfnetlink-devel >= 1.0.1
Requires:	kernel-headers

%description    devel
libnetfilter_conntrack is a userspace library providing a programming
interface (API) to the in-kernel connection tracking state table.

%prep
%setup -q

# (valid for 1.0.3, may break newer releases)
# Remove outdated files that confuse various helper scripts.
rm compile config.guess config.sub depcomp install-sh ltmain.sh missing

%build
%configure --disable-static --disable-rpath

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/libnetfilter_conntrack
%{_includedir}/libnetfilter_conntrack/*.h

%changelog
* Fri Apr 18 2014 Liu Di <liudidi@gmail.com> - 1.0.4-3
- 为 Magic 3.0 重建

* Fri Apr 18 2014 Liu Di <liudidi@gmail.com> - 1.0.4-2
- 为 Magic 3.0 重建

* Thu Aug  8 2013 Paul P. Komkoff Jr <i@stingr.net> - 1.0.4-1
- new upstream version

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 24 2013 Paul P. Komkoff Jr <i@stingr.net> - 1.0.3-1
- new upstream version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 30 2012 Paul P. Komkoff Jr <i@stingr.net> - 1.0.2-1
- new upstream version

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 18 2012 Paul P. Komkoff Jr <i@stingr.net> - 1.0.1-1
- new upstream version

* Sat Mar 17 2012 Paul P. Komkoff Jr <i@stingr.net> - 1.0.0-1
- new upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Apr  3 2011 Paul P. Komkoff Jr <i@stingr.net> - 0.9.1-1
- new upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 19 2010 Paul P. Komkoff Jr <i@stingr.net> - 0.9.0-1
- new upstream version

* Wed Jan 20 2010 Paul P. Komkoff Jr <i@stingr.net> - 0.0.101-1
- new upstream version

* Mon Sep 28 2009 Paul P. Komkoff Jr <i@stingr.net> - 0.0.100-1
- new upstream version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.99-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.99-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 13 2009 Paul P. Komkoff Jr <i@stingr.net> - 0.0.99-1
- new upstream version

* Sun Oct 26 2008 Paul P. Komkoff Jr <i@stingr.net> - 0.0.97-1
- new upstream version

* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.0.96-3
- Fix Patch0:/%%patch mismatch.

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.0.96-2
- fix license tag

* Wed Jul 16 2008 Paul P. Komkoff Jr <i@stingr.net> - 0.0.96-1
- grab new upstream version
- use bundled header again

* Sat Feb 23 2008 Paul P. Komkoff Jr <i@stingr.net> - 0.0.89-0.1.svn7356
- new version from upstream svn, with new api
- use system headers instead of bundled

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.0.82-3
- Autorebuild for GCC 4.3

* Tue Feb 19 2008 Paul P. Komkoff Jr <i@stingr.net> - 0.0.82-2
- fix build with a new glibc

* Sun Jan 20 2008 Paul P. Komkoff Jr <i@stingr.net> - 0.0.82-1
- new upstream version

* Thu Aug 30 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.0.81-1
- new upstream version

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.0.80-2
- Rebuild for selinux ppc32 issue.

* Thu Jul 19 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.0.80-1
- new upstream version

* Wed May 30 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.0.75-1
- new upstream version

* Sun Mar 25 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.0.50-4
- grab ownership of some directories

* Mon Mar 19 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.0.50-3
- include libnfnetlink-devel into -devel deps

* Sat Mar 17 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.0.50-2
- new way of handling rpaths (as in current packaging guidelines)

* Sun Feb 11 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.0.50-1
- upstream version 0.0.50

* Fri Sep 15 2006 Paul P. Komkoff Jr <i@stingr.net>
- rebuilt

* Wed Jul 12 2006 Felipe Kellermann <stdfk@terra.com.br> - 0.0.31-1
- Adds pkgconfig to devel files.
- Version 0.0.31.

* Mon May  8 2006 Paul P Komkoff Jr <i@stingr.net> - 0.0.30-2
- Include COPYING in %%doc

* Sun Mar 26 2006 Paul P Komkoff Jr <i@stingr.net> - 0.0.30-1
- Preparing for submission to fedora extras

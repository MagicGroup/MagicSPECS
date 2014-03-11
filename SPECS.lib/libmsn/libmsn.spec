
Name:		libmsn
Summary:	Library for connecting to the MSN Messenger service
Version:	4.2.1
Release:	4%{?dist}

Group:		System Environment/Libraries
License:	GPLv2
URL:		http://sourceforge.net/projects/libmsn/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch0:		libmsn-4.2.1-unistd.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	cmake
BuildRequires:	pkgconfig(libssl)	
BuildRequires:	pkgconfig

%description
Libmsn is a reusable, open-source, fully documented library for connecting to
the MSN Messenger service.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .unistd


%build

mkdir -p %{_target_platform}
pushd %{_target_platform} 
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}
make install/fast -C %{_target_platform} DESTDIR=%{buildroot}


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README COPYING THANKS
%{_bindir}/msntest
%{_libdir}/libmsn.so.0*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libmsn.so
%{_libdir}/pkgconfig/libmsn.pc
%{_includedir}/msn/


%changelog
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-3
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 05 2011 Rex Dieter <rdieter@fedoraproject.org> 4.2.1-1
- 4.2.1
- BR: pkgconfig(libssl)

* Wed Nov 23 2011 Rex Dieter <rdieter@fedoraproject.org> 4.2-3
- -devel: drop hard/manual openssl-dep, handled better via pkgconfig deps now

* Fri Nov 18 2011 Rex Dieter <rdieter@fedoraproject.org> 4.2-2
- /usr/include/msn/soap.h: fatal error: xmlParser.h: No such file (#755127)

* Wed Nov 09 2011 John5342 <john5342 at, fedoraproject.org> 4.2-1
- Rebase to new upstream version
- Drop patches (they were already both upstream waiting for this new release)
- No real changes in this version since we already carried all patches except the version change

* Wed Nov 09 2011 John5342 <john5342 at, fedoraproject.org> 4.1-4
- Back port a patch to fix redirects

* Fri Aug 12 2011 Rex Dieter <rdieter@fedoraproject.org> 4.1-3
- -devel: use %%{?_isa}
- -devel: drop hard-coded pkgconfig dep, should be automatic now

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 5 2010 John5342 <john5342 at, fedoraproject.org> - 4.1-1
- libmsn-4.1

* Sat Nov 14 2009 John5342 <john5342 at, fedoraproject.org> - 4.0-1
- 4.0 final

* Sat Sep 19 2009 John5342 <john5342 at, fedoraproject.org> - 4.0-0.15.beta8
- 4.0 beta 8 (fixes #524318)

* Tue Aug 25 2009 Tomas Mraz <tmraz@redhat.com> - 4.0-0.14.beta7
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-0.13.beta7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Lukáš Tinkl <ltinkl@redhat.com> 4.0-0.12.beta7
- 4.0 beta 7

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-0.11.beta4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 24 2009 John5342 <john5342 at, fedoraproject.org> 4.0-0.10.beta4
- libmsn-4.0-beta4

* Fri Jan 23 2009 Rex Dieter <rdieter@fedoraproject.org> 4.0-0.9.beta2
- revert use of (tm)

* Fri Jan 23 2009 Rex Dieter <rdieter@fedoraproject.org> 4.0-0.8.beta2
- remove pkgconfig hack/workaround

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> 4.0-0.7.beta2
- rebuild with new openssl

* Fri Jan 09 2009 Rex Dieter <rdieter@fedoraproject.org> 4.0-0.6.beta2
- pkgconfig patch to workaround bug #479493

* Fri Jan 09 2009 Rex Dieter <rdieter@fedoraproject.org> 4.0-0.5.beta2
- -devel: Requires: openssl-devel

* Fri Jan 09 2009 Rex Dieter <rdieter@fedoraproject.org> 4.0-0.4.beta2
- libmsn-4.0-beta2

* Thu Dec 11 2008 John5342 <john5342 at, fedoraproject.org> 4.0-0.3.beta1
- Left docs out of devel package
- Added (tm) to MSN

* Wed Dec 10 2008 John5342 <john5342 at, fedoraproject.org> 4.0-0.2.beta1
- Removed questionable trademarks in description and summary

* Wed Dec 10 2008 John5342 <john5342 at, fedoraproject.org> 4.0-0.1.beta1
- Initial package

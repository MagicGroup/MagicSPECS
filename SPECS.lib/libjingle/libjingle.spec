Name:           libjingle
Version:        0.6.14
Release:        5%{?dist}
Summary:        GoogleTalk implementation of Jingle
Group:          System Environment/Libraries
License:        BSD
URL:            http://code.google.com/apis/talk/libjingle/
Source0:        http://libjingle.googlecode.com/files/%{name}-%{version}.zip
# Use Makefiles, dammit.
Patch0:		libjingle-0.6.14-build-sanity.patch
# talk/base/basictypes.h and talk/base/logging.h must be included 
# before any header with __BEGIN_DECLS, notably, sys/types.h
Patch1:		libjingle-0.5.1-C-linkage-fix.patch
# We need <cstdlib> for NULL.
Patch2:		libjingle-0.5.8-NULL-fix.patch
# In file included from /usr/include/fcntl.h:41:0,
#                 from physicalsocketserver.cc:37:
#/usr/include/bits/stat.h:91:21: error: field 'st_atim' has incomplete type
#/usr/include/bits/stat.h:92:21: error: field 'st_mtim' has incomplete type
#/usr/include/bits/stat.h:93:21: error: field 'st_ctim' has incomplete type
# FIX: Include <time.h> first.
Patch3:		libjingle-0.5.8-statfix.patch
# md5.h had a typedef for uint32 that did not match the one in basictypes.h
Patch4:		libjingle-0.5.1-uint32-fix.patch
# thread.cc: In static member function ‘static bool talk_base::Thread::SleepMs(int)’:
# thread.cc:199:19: error: aggregate ‘timespec ts’ has incomplete type and cannot be defined
# thread.cc:202:34: error: ‘nanosleep’ was not declared in this scope
# This happens because a local header is included before time.h
Patch5:		libjingle-0.5.1-timefix.patch
# unixfilesystem.cc wouldn't compile.
Patch6:		libjingle-0.5.1-unixfilesystemfix.patch
# Google seems to love to be stupid with headers.
# Especially when they're in "third_party" code.
# Hardcoding paths in include files is dumb.
Patch7:		libjingle-0.5.8-system-expat.patch
Patch8:		libjingle-0.5.8-system-srtp.patch
# Fix devicemanager.cc to compile
Patch9:		libjingle-0.6.14-devicemanager-fix.patch
# Fix v4llookup.cc to compile
Patch10:	libjingle-0.5.8-v4llookup-fix.patch
# Fix type and definition conflicts with Chromium
Patch11:        libjingle-0.6.6-fixconflict.patch
# Make sure linux.h/linux.cc pulls in config.h for LINUX define
Patch14:	libjingle-0.5.8-config-linux.patch
# Fix 0.5.2 compilation
Patch16:	libjingle-0.6.6-compilefix.patch
# Fix missing cstdlib for size_t
Patch17:	libjingle-0.6.0-size_t.patch
# Fix obsolete macro usage
Patch18:	libjingle-0.5.8-fixmacro.patch
# Gcc 4.7.0 no longer includes unistd.h by default
Patch20:	libjingle-0.6.6-unistd.patch

BuildRequires:	libtool, autoconf, automake
BuildRequires:	openssl-devel
BuildRequires:	expat-devel
BuildRequires:	libsrtp-devel
BuildRequires:  alsa-lib-devel
BuildRequires:	pkgconfig 
BuildRequires:	kernel-headers
# Really, we only need libudev-devel.
BuildRequires:	systemd-devel
BuildRequires:	gtk2-devel
BuildRequires:	libXrender-devel, libXcomposite-devel

ExclusiveArch:	%{ix86} x86_64 %{arm}

%description
Libjingle is Google Talk's implementation of Jingle and Jingle-Audio
(proposed extensions to XMPP) to interoperate with Google Talk's
peer-to-peer and voice calling capabilities.

In addition, it is a P2P (peer-to-peer) and RTC (real-time communication) 
stack that builds on XMPP. If you don't need any P2P or RTC, you can use any 
XMPP stack. If you do, then you might want to use libjingle. In fact, you 
can even use libjingle on top of another XMPP stack. 

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:	pkgconfig
Requires:	openssl-devel
Requires:	expat-devel
Requires:	libsrtp-devel
Requires:	gtk2-devel
Requires:	libXrender-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1 -b .SANITY
%patch1 -p1 -b .linkage
%patch2 -p1 -b .NULL
%patch3 -p1 -b .statfix
%patch4 -p1 -b .uint32
%patch5 -p1 -b .timefix
%patch6 -p1 -b .unixfilesystem
%patch7 -p1 -b .system-expat
%patch8 -p1 -b .system-srtp
%patch9 -p1 -b .alsa
%patch10 -p1 -b .v4lfix
%patch11 -p1 -b .fixconflict
%patch14 -p1 -b .config
%patch16 -p1 -b .compilefix
%patch17 -p1 -b .size_t
%patch18 -p1 -b .fixmacro
%patch20 -p1 -b .unistd

touch NEWS ChangeLog
autoreconf -i

rm -rf talk/base/time.h

%build
%configure --disable-static
# Remove rpath.
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog
%{_bindir}/relayserver
%{_bindir}/stunserver
%{_libdir}/*.so.*


%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}-0.6/
%{_libdir}/*.so
%{_libdir}/pkgconfig/jingle*-0.6.pc


%changelog
* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 0.6.14-5
- 为 Magic 3.0 重建

* Tue Jun 24 2014 Liu Di <liudidi@gmail.com> - 0.6.14-4
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  2 2012 Tom Callaway <spot@fedoraproject.org> - 0.6.14-2
- use new BR for libudev

* Mon Jun 11 2012 Tom Callaway <spot@fedoraproject.org> - 0.6.14-1
- update to 0.6.14

* Sun Apr  1 2012 Dan Horák <dan[at]danny.cz> - 0.6.10-3
- set ExclusiveArch

* Wed Mar 21 2012 Tom Callaway <spot@fedoraproject.org> - 0.6.10-2
- resolve patch confusion

* Mon Feb 13 2012 Tom Callaway <spot@fedoraproject.org> - 0.6.10-1
- update to 0.6.10

* Thu Jan  5 2012 Tom Callaway <spot@fedoraproject.org> - 0.6.6-1
- update to 0.6.6

* Tue Sep 27 2011 Tom Callaway <spot@fedoraproject.org> - 0.6.0-2
- fix phone bits up
- properly bump to 0.6

* Tue Sep 27 2011 Tom Callaway <spot@fedoraproject.org> - 0.6.0-1
- update to 0.6.0

* Tue Jul 26 2011 Tom Callaway <spot@fedoraproject.org> - 0.5.8-1
- update to 0.5.8
- merge Google's unpublished Chromium 14 changes

* Wed Mar 30 2011 Tom Callaway <spot@fedoraproject.org> - 0.5.2-1
- update to 0.5.2
- merge Google's unpublished Chromium 12 changes

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Tom Callaway <spot@fedoraproject.org> - 0.5.1-4
- fix linux.h so that LINUX define is pulled in from config.h

* Fri Dec 10 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.5.1-3
- apply change from Chromium to make qname threadsafe

* Fri Dec 10 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.5.1-2
- fix build to properly install config.h
- fix 64bit issues
- fix conflicts with Chromium

* Fri Nov 19 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.5.1-1
- update to 0.5.1

* Tue Aug 25 2009 Tomas Mraz <tmraz@redhat.com> - 0.3.12-6
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar  2 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.3.12-4
- Add patch to fix gcc-4.4.0 errors.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.3.12-2
- rebuild with new openssl

* Wed Sep 17 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.3.12-1
- Update to 0.3.12.
- Add hack to remove rpath.
- Update source url.
- Drop gcc patch. Fixed upstream.
- Drop expat-devel BR.  Not needed anymore.
- Drop *.pc files no longer available.

* Sun Mar 16 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.3.11-8
- Add patch to fix build w/ gcc4.3.

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.3.11-7
- Autorebuild for GCC 4.3

* Fri Feb  8 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.3.11-6
- Rebuild for gcc-4.3.

* Wed Dec  5 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.3.11-5
- rebuild for new libssl.so.6/libcrypto.so.6

* Tue Aug 28 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.3.11-4
- Rebuild for expat 2.0.

* Tue Aug 21 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.3.11-3
- Rebuild.

* Wed Jun 27 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.3.11-2
- Update URL.

* Fri May 18 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.3.11-1
- Update 0.3.11.

* Mon Sep  4 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.3.10-1
- Initial FE spec.

#
# spec file for meanwhile - sametime client library
#

Name:		meanwhile
Summary:	Lotus Sametime Community Client library
Summary(zh_CN.UTF-8): Lotus Sametime 通信客户端库
License:	LGPLv2+
Group:		Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
Version:	1.1.0
Release:	8%{?dist}
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# cvs -d:pserver:anonymous@meanwhile.cvs.sourceforge.net:/cvsroot/meanwhile login
# [hit return for the password]
# cvs -d:pserver:anonymous@meanwhile.cvs.sourceforge.net:/cvsroot/meanwhile co -d meanwhile-1.1.0 -r meanwhile_v1_1_0 meanwhile
# cd meanwhile-1.1.0
# ./autogen.sh
# make dist
Source:		meanwhile-%{version}.tar.gz
Patch0:         %{name}-crash.patch
Patch1:         %{name}-fix-glib-headers.patch
Patch2:         %{name}-file-transfer.patch
Patch3:         %{name}-status-timestamp-workaround.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1037196
Patch4:         %{name}-format-security-fix.patch

URL:		http://meanwhile.sourceforge.net
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: glib2-devel, doxygen

%description
The heart of the Meanwhile Project is the Meanwhile library, providing the
basic Lotus Sametime session functionality along with the core services;
Presence Awareness, Instant Messaging, Multi-user Conferencing, Preferences
Storage, Identity Resolution, and File Transfer. This extensible client
interface allows additional services to be added to a session at runtime,
allowing for simple integration of future service handlers such as the user
directory and whiteboard and screen-sharing.

%description -l zh_CN.UTF-8
Lotus Sametime 通信客户端库。

%package devel
Summary: Header files, libraries and development documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: glib2-devel

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary: Documentation for the Meanwhile library
Summary(zh_CN.UTF-8): %{name} 的文档
Group: Applications/Internet
Group(zh_CN.UTF-8): 文档
License: GFDL

%description doc
Documentation for the Meanwhile library

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q
%patch0 -p0 -b .crash
%patch1 -p1 -b .fix-glib-headers
%patch2 -p1 -b .file-transfer
%patch3 -p1 -b .status-timestamp-workaround
%patch4 -p1 -b .format-security-fix

%build
autoreconf -fisv
%configure --enable-doxygen
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall}
# Remove the latex documentation.  Nobody reads it, it installs a font for
# some unknown reason, and people have to build it themselves.  Dumb.
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-doc-%{version}/latex
rm -rf $RPM_BUILD_ROOT%{_libdir}/libmeanwhile.a
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog COPYING README TODO INSTALL LICENSE NEWS
%{_libdir}/libmeanwhile.so.*

%files devel
%defattr(-, root, root, -)
%{_includedir}/meanwhile/
%exclude %{_libdir}/libmeanwhile.la
%{_libdir}/libmeanwhile.so
%{_libdir}/pkgconfig/meanwhile.pc

%files doc
%defattr(-, root, root, -)
%{_datadir}/doc/%{name}-doc-%{version}/

%changelog
* Fri Aug 22 2014 Liu Di <liudidi@gmail.com> - 1.1.0-8
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.1.0-7
- 为 Magic 3.0 重建

* Sun Dec 18 2011 Liu Di <liudidi@gmail.com> - 1.1.0-6
- 为 Magic 3.0 重建

* Fri Nov 18 2011 Josh Boyer <jwboyer@gmail.com> 1.1.0-5
- Fix glib.h build issues (rhbz 750023)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 29 2010 Josh Boyer <jwboyer@gmail.com> - 1.1.0-4
- Remove libmeanwhile.a (#556084)

* Tue Jan 12 2010 Dan Winship <danw@redhat.com> - 1.1.0-3
- Fix Source tag to indicate a CVS snapshot build.
- Resolves: #554446

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Josh Boyer <jwboyer@gmail.com> - 1.1.0-1
- Update to meanwhile_v1_1_0 branch from upstream CVS.  Fixes bug 490088

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Josh Boyer <jwboyer@gmail.com> - 1.0.2-9
- Kill the latex stuff from the doc subpackage

* Thu Aug 28 2008 Josh Boyer <jwboyer@gmail.com> - 1.0.2-8
- Add patch to fix crash when server removes contact list

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.2-7
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.2-6
- Autorebuild for GCC 4.3

* Fri Aug 03 2007 - jwboyer@jdub.homelinux.org 1.0.2-5
- Update license field

* Fri May 4 2007 - jwboyer@jdub.homelinux.org 1.0.2-4
- Rebuild for F7 to pick up ppc64

* Sun Aug 27 2006 - jwboyer@jdub.homelinux.org 1.0.2-3
- Bump for FE6 rebuild

* Tue Feb 14 2006 - jwboyer@jdub.homelinux.org 1.0.2-2
- Bump for FE5 rebuild

* Tue Jan 3 2006 - jwboyer@jdub.homelinux.org 1.0.2-1
- Update to latest release
- Fixes crash when merging buddy list with server

* Fri Dec 16 2005 - jwboyer@jdub.homelinux.org 1.0.1-1
- Update to latest release
- Fixes mpi conflict with mozilla-nss

* Wed Dec 14 2005 - jwboyer@jdub.homelinux.org 1.0.0-1
- Update to latest release
- gmp and gmp-devel are no longer required since meanwhile uses mpi now

* Sat Oct 29 2005 - jwboyer@jdub.homelinux.org 0.5.0-1
- Update to latest release

* Wed Jun 15 2005 - jwboyer@jdub.homelinux.org 0.4.2-2
- Bump release for rebuild against latest development

* Tue May 31 2005 - jwboyer@jdub.homelinux.org 0.4.2-1
- Update to latest version
- Fix typo in last changelog

* Tue May 24 2005 - jwboyer@jdub.homelinux.org 0.4.1-2
- Updates from review comments

* Mon May 23 2005 - jwboyer@jdub.homelinux.org 0.4.1-1
- Initial package, adapted from spec file by Dag Wieers

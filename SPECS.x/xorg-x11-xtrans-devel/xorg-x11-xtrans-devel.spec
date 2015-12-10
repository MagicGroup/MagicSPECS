# NOTE: This package contains only C source and header files and pkg-config
# *.pc files, and does not contain any ELF binaries or DSOs, so we disable
# debuginfo generation.
%define debug_package %{nil}

Summary: X.Org X11 developmental X transport library
Summary(zh_CN.UTF-8): X.Org X11 X transport 开发库
Name: xorg-x11-xtrans-devel
Version:	1.3.5
Release:	5%{?dist}
License: MIT
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.x.org
BuildArch: noarch

Source0: http://xorg.freedesktop.org/archive/individual/lib/xtrans-%{version}.tar.bz2

# Fedora specific patch
Patch1: xtrans-1.0.3-avoid-gethostname.patch

BuildRequires: pkgconfig
BuildRequires: xorg-x11-util-macros

%description
X.Org X11 developmental X transport library

%description -l zh_CN.UTF-8
X.Org X11 X transport 开发库。

%prep
%setup -q -n xtrans-%{version}
%patch1 -p1 -b .my-name-is-unix

%build

# yes, this looks horrible, but it's to get the .pc file in datadir
%configure --libdir=%{_datadir} \
	   --docdir=%{_docdir}/%{name}-%{version}-%{release}
# Running 'make' not needed.

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%dir %{_includedir}/X11
%dir %{_includedir}/X11/Xtrans
%{_includedir}/X11/Xtrans/Xtrans.c
%{_includedir}/X11/Xtrans/Xtrans.h
%{_includedir}/X11/Xtrans/Xtransint.h
%{_includedir}/X11/Xtrans/Xtranslcl.c
%{_includedir}/X11/Xtrans/Xtranssock.c
%{_includedir}/X11/Xtrans/Xtransutil.c
%{_includedir}/X11/Xtrans/transport.c
%{_datadir}/aclocal/xtrans.m4
%{_datadir}/pkgconfig/xtrans.pc
%dir %{_docdir}/%{name}-%{version}-%{release}
%{_docdir}/%{name}-%{version}-%{release}/xtrans.*

%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 1.3.5-5
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 1.3.5-4
- 为 Magic 3.0 重建

* Tue Oct 27 2015 Liu Di <liudidi@gmail.com> - 1.3.5-3
- 为 Magic 3.0 重建

* Mon Oct 26 2015 Liu Di <liudidi@gmail.com> - 1.3.5-2
- 更新到 1.3.5

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 09 2012 Adam Jackson <ajax@redhat.com> 1.2.7-1
- xtrans 1.2.7 (#806309)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 09 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.6-1
- xtrans 1.2.6

* Sat Sep 25 2010 Parag Nemade <paragn AT fedoraproject.org> - 1.2.2-5
- Merge-review cleanup (#226656)

* Mon Aug 03 2009 Adam Jackson <ajax@redhat.com> 1.2.2-4
- Un-Requires xorg-x11-filesystem

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 09 2008 Adam Jackson <ajax@redhat.com> 1.2.2-1
- xtrans 1.2.2
- Move to BuildArch: noarch.

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.2.1-2
- Fix license tag.

* Wed Jul 02 2008 Adam Jackson <ajax@redhat.com> 1.2.1-1
- xtrans 1.2.1

* Tue May 06 2008 Bill Nottingham <notting@redhat.com> 1.1-2
- xtrans-1.1-abstract.patch: Don't worry about making /tmp/.X11-unix
  (or failure to do so) if you're using an abstract socket (#445303)

* Wed Mar 05 2008 Adam Jackson <ajax@redhat.com> 1.1-1
- xtrans 1.1

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.3-6
- Autorebuild for GCC 4.3

* Mon Oct 01 2007 Adam Jackson <ajax@redhat.com> 1.0.3-5
- xtrans-1.0.3-avoid-gethostname.patch: Don't trust gethostname() output
  when building networkIds for AF_UNIX sockets.  Fixes application launch
  delays and failures when dhclient changes your hostname from under you.

* Thu Sep 20 2007 Adam Jackson <ajax@redhat.com> 1.0.3-4
- Fix a bug in automatic port generation for abstract sockets.  Fixes fast
  user switching, among other things.

* Fri Aug 24 2007 Adam Jackson <ajax@redhat.com> 1.0.3-3
- Abstract sockets for PF_UNIX.

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> 1.0.3-2
- Don't install INSTALL

* Fri Jan 05 2007 Adam Jackson <ajax@redhat.com> 1.0.3-1
- Update to 1.0.3

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-1.1
- rebuild

* Mon Jul 10 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-1.fc6
- Update to xtrans-1.0.1
- Remove xtrans-1.0.0-setuid.diff as it is included in 1.0.1

* Tue Jun 20 2006 Mike A. Harris <mharris@redhat.com> 1.0.0-4
- Added xtrans-1.0.0-setuid.diff to fix potential security issue (#195555)
- Use setup -n instead of -c, and remove extraneous calls to cd from build
  and install sections.
- Use "make install DESTDIR=$RPM_BUILD_ROOT" instead of makeinstall macro.
- Added "AUTHORS ChangeLog COPYING INSTALL NEWS README" to doc macro.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Mike A. Harris <mharris@redhat.com> 1.0.0-3
- Bump and rebuild.

* Fri Dec 23 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-2
- Bump and rebuild.

* Thu Dec 15 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Update to xtrans-1.0.0 from X11R7 RC4 release.

* Tue Nov 22 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-2
- Add "Requires(pre): xorg-x11-filesystem >= 0.99.2-3" to avoid bug (#173384).

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Update to xtrans-0.99.2 from X11R7 RC2 release.

* Thu Oct 20 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Update to xtrans-0.99.1 from X11R7 RC1 release.
- This package contains only C source and header files and pkg-config
  *.pc files, and does not contain any ELF binaries or DSOs, so we disable
  debuginfo generation.

* Sun Oct 02 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-2
- Use Fedora-Extras style BuildRoot tag
- Add tarball URL

* Mon Aug 22 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-1
- Initial build.

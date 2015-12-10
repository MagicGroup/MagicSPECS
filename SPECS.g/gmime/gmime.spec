Name:           gmime
Version:	2.6.20
Release:        4%{?dist}
Summary:        Library for creating and parsing MIME messages
Summary(zh_CN.UTF-8): 创建和解析 MIME 信息的库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
# Files in examples/, src/ and tests/ are GPLv2+
License:        LGPLv2+ and GPLv2+
URL:            http://spruce.sourceforge.net/gmime/
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://download.gnome.org/sources/gmime/%{majorver}/gmime-%{version}.tar.xz

BuildRequires:  glib2-devel >= 2.18.0
BuildRequires:  gpgme-devel
BuildRequires:  libgpg-error-devel
BuildRequires:  zlib-devel >= 1.2.1.1
BuildRequires:  gettext-devel, gtk-doc
BuildRequires:  automake autoconf

Patch3: gmime-2.5.8-gpg-error.patch

# mono available only on selected architectures
%ifarch %ix86 x86_64 ia64 armv4l sparcv9 alpha s390x ppc ppc64
%define buildmono 1
%else
%define buildmono 0
%endif
%if 0%{?rhel} >= 6
%define buildmono 0
%endif

%if 0%buildmono
BuildRequires:  mono-devel gtk-sharp2-gapi
BuildRequires:  gtk-sharp2-devel >= 2.4.0
%endif

%description
The GMime suite provides a core library and set of utilities which may be
used for the creation and parsing of messages using the Multipurpose
Internet Mail Extension (MIME).

%description -l zh_CN.UTF-8
创建和解析 MIME 信息的库。

%package        devel
Summary:        Header files to develop libgmime applications
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       glib2-devel

%description    devel
The GMime suite provides a core library and set of utilities which may be
used for the creation and parsing of messages using the Multipurpose
Internet Mail Extension (MIME). The devel-package contains header files
to develop applications that use libgmime.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%if 0%buildmono
%package        sharp
Summary:        Mono bindings for gmime
Summary(zh_CN.UTF-8): %{name} 的 Mono 绑定
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       gtk-sharp2

%description    sharp
The GMime suite provides a core library and set of utilities which may be
used for the creation and parsing of messages using the Multipurpose
Internet Mail Extension (MIME). The devel-package contains support 
for developing mono applications that use libgmime.

%description sharp -l zh_CN.UTF-8
%{name} 的 Mono 绑定。
%endif

%prep
%setup -q
%patch3 -p1 -b .gpg-error

%build
autoreconf -fisv
MONO_ARGS="--enable-mono=no"
%if 0%buildmono
export MONO_SHARED_DIR=%{_builddir}/%{?buildsubdir}
MONO_ARGS="--enable-mono"
%endif
# Don't conflict with sharutils.
%configure $MONO_ARGS --program-prefix=%{name} --disable-static

# Deal with rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# Omit unused direct shared library dependencies.
sed --in-place --expression 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}

%install
export MONO_SHARED_DIR=%{_builddir}/%{?buildsubdir}
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING README TODO
%{_libdir}/lib*.so.*

%files devel
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/gmime-2.6.pc
%{_includedir}/gmime-2.6
%{_datadir}/gtk-doc/html/gmime-2.6
%{_libdir}/girepository-1.0/GMime-2.6.typelib
%{_datadir}/gir-1.0/GMime-2.6.gir
%{_datadir}/vala/vapi/gmime-2.6.*

%if 0%buildmono
%files sharp
%{_libdir}/pkgconfig/gmime-sharp-2.6.pc
/usr/lib/mono/gac/gmime-sharp
/usr/lib/mono/gmime-sharp-2.6
%{_datadir}/gapi-2.0/gmime-api.xml
%endif

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 2.6.20-4
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 2.6.20-3
- 为 Magic 3.0 重建

* Sun Apr 06 2014 Liu Di <liudidi@gmail.com> - 2.6.20-2
- 更新到 2.6.20

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 2.6.11-2
- 为 Magic 3.0 重建

* Sat Oct 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.6.11-1
- Update to 2.6.11

* Tue Jul 31 2012 Richard Hughes <hughsient@gmail.com> - 2.6.10-1
- Update to 2.6.10

* Tue Jul 24 2012 Kalev Lember <kalevlember@gmail.com> - 2.6.9-1
- Update to 2.6.9, sync with the f17 branch

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 27 2012 Tomas Bzatek <tbzatek@redhat.com> - 2.6.4-1
- Update to 2.6.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 02 2011 Christian Krause <chkr@fedoraproject.org> - 2.6.1-2
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Tue Nov 22 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.6.1-1
- Update to 2.6.1

* Tue Jun 14 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.5.8-1
- Update to 2.5.8

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Dan Horák <dan[at]danny.cz> - 2.5.1-3
- sync the architecture list with the mono package

* Thu Oct 28 2010 Christian Krause <chkr@fedoraproject.org> - 2.5.1-2
- Rebuilt against Mono 2.8

* Wed Feb 10 2010 Bastien Nocera <bnocera@redhat.com> 2.5.1-1
- Update to 2.5.1

* Wed Nov 18 2009 Julian Sikorski <belegdol@fedoraproject.org> - 2.4.11-2
- Enabled rpath removal, got confirmation that it should be safe now

* Wed Nov 18 2009 Julian Sikorski <belegdol@fedoraproject.org> - 2.4.11-1
- Updated to 2.4.11
- Adjusted the license tag (fixes RH bug #522630)
- Got rid of rpath issue properly (but left disabled, need to confirm why chrpath was dropped in the first place)

* Mon Oct 26 2009 Dennis Gilmore <dennis@ausil.us> - 2.4.7-3
- build mono support on s390 and s390x
- exclude mono support on sparc64

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 18 2009 Matthias Clasen <mclasen@redhat.com> - 2.4.7-1
- Update to 2.4.7

* Mon May 25 2009 Xavier Lamien <laxaathom@fedoraprojet.org> - 2.4.3-5
- Build arch ppc64.
- Fix uu??code binaries.

* Tue Mar 31 2009 Debarshi Ray <rishi@fedoraproject.org> - 2.4.3-4
- Merge review feedback (#225808)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.4.3-2
- Update to 2.4.3

* Fri Oct 24 2008 Xavier Lamien <lxtnow@gmail.com> - 2.2.23-2
- Fix Strong name check.

* Mon Sep 15 2008 Matthias Clasen <mclasen@redhat.com> - 2.2.23-1
- Update to 2.2.23
- Drop static libraries from -devel

* Tue May 27 2008 Matthias Clasen <mclasen@redhat.com> - 2.2.21-1
- Update to 2.2.21

* Sun May  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.2.19-1
- Update to 2.2.19
- Fix source url

* Thu Mar 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.2.18-1
- Update to 2.2.18

* Tue Feb 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.2.17-1
- Update to 2.2.17

* Wed Feb  6 2008 Matthias Clasen <mclasen@redhat.com> - 2.2.16-1
- Update to 2.2.16

* Tue Jan 08 2008 - Bastien Nocera <bnocera@redhat.com> - 2.2.15-1
- Update to 2.2.15

* Sun Dec 16 2007 Matthias Clasen  <mclasen@redhat.com> 2.2.12-1
- Update to 2.2.12

* Tue Nov 13 2007 Matthias Clasen  <mclasen@redhat.com> 2.2.11-1
- Update to 2.2.11

* Fri Oct 12 2007 Matthias Clasen  <mclasen@redhat.com> 2.2.10-5
- Don't export unnamespaced internal symbols (#216434)

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.2.10-4
- Rebuild for selinux ppc32 issue.

* Fri Aug 03 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info>
- Update License field due to the "Licensing guidelines changes"

* Wed Jul 25 2007 Jesse Keating <jkeating@redhat.com> - 2.2.10-2
- Rebuild for RH #249435

* Mon Jul 23 2007 Matthias Clasen <mclasen@redhat.com> - 2.2.10-1
- Update to 2.2.10

* Sun Jul 08 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.2.9-3
- there is no mono for ppc64 as well

* Fri Jul 06 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.2.9-2
- build stuff depending on mono on all archs except those where
  we know there is no mono (fixes alpha, #246437)

* Tue May 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.2.9-1
- Update to 2.2.9

* Mon May 21 2007 Matthias Clasen <mclasen@redhat.com> - 2.2.8-1
- Update to 2.2.8

* Tue Feb  6 2007 Alexander Larsson <alexl@redhat.com> - 2.2.3-5
- Fix build with new automake (#224157)

* Thu Oct 12 2006 Alexander Larsson <alexl@redhat.com> - 2.2.3-4
- Bump glib requirement to 2.6 (#209565)

* Tue Sep  5 2006 Alexander Larsson <alexl@redhat.com> - 2.2.3-3
- fix gmime-config multilib conflict (#205208)

* Sat Aug 19 2006 Matthias Clasen <mclasen@redhat.com> - 2.2.3-2
- Rebuild

* Fri Aug 18 2006 Alexander Larsson <alexl@redhat.com> - 2.2.3-1
- Upgrade to 2.2.3
- Use the new mono libdir

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Fri Jun  9 2006 Alexander Larsson <alexl@redhat.com> - 2.2.1-2
- Disable mono parts on s390* as mono doesn't build on s390 atm

* Tue May 23 2006 Alexander Larsson <alexl@redhat.com> - 2.2.1-1
- Update to 2.2.1
- Fix multilib -devel conflict by using pkg-config in gmime-config (#192675)

* Tue Feb 28 2006 Karsten Hopp <karsten@redhat.de> 2.1.19-4
- BuildRequires: gtk-sharp2 on mono archs only

* Sun Feb 12 2006 Christopher Aillon <caillon@redhat.com> - 2.1.19-3
- Rebuild

* Tue Feb  7 2006 Jesse Keating <jkeating@redhat.com> - 2.1.19-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Christopher Aillon <caillon@redhat.com> - 2.1.19-2
- Rebuild

* Sun Jan 22 2006 Alexander Larsson <alexl@redhat.com> - 2.1.19-1
- Update to 2.1.19 (needed by beagle 0.2.0)

* Thu Jan 19 2006 Alexander Larsson <alexl@redhat.com> 2.1.17-3
- Build on s390x

* Mon Jan  9 2006 Alexander Larsson <alexl@redhat.com> 2.1.17-2
- build gmime-sharp conditionally on mono arches

* Mon Jan  9 2006 Alexander Larsson <alexl@redhat.com> - 2.1.17-1
- Move from Extras to Core, Update to 2.1.17, add gmime-sharp subpackage

* Wed Aug 10 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.1.15-1
- Update to 2.1.15
- Use dist

* Wed May 18 2005 Colin Charles <colin@fedoraproject.org> - 2.1.9-5
- bump release, request build on ppc

* Thu Mar 31 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.1.9-4
- add dep glib2-devel for pkgconfig in -devel package

* Mon Oct 18 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:2.1.9-0.fdr.3
- Remove ldconfig from Requires pre and post

* Mon Oct 18 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:2.1.9-0.fdr.2
- BR zlib-devel
- Don't ship empty news file
- Fixes to the files section
- Change ldconfig in post* calls to -p /sbin/ldconfig


* Sun Oct 17 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:2.1.9-0.fdr.1
- Initial RPM release.

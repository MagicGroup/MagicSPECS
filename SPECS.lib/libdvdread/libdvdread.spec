Name:           libdvdread
Version: 4.9.9
Release:        2%{?dist}
Summary:        A library for reading DVD video discs based on Ogle code
Summary(zh_CN.UTF-8): 基于 Ogle 代码读取 DVD 视频光盘的库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        GPLv2+
Source0:        http://dvdnav.mplayerhq.hu/releases/libdvdread-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# dvdread-config: use pkg-config instead of hard-coded 

%description
libdvdread provides a simple foundation for reading DVD video disks.
It provides the functionality that is required to access many DVDs.

%description -l zh_CN.UTF-8
基于 Ogle 代码读取 DVD 视频光盘的库。

%package        devel
Summary:        Development files for libdvdread
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
libdvdread provides a simple foundation for reading DVD video disks.
It provides the functionality that is required to access many DVDs.

This package contains development files for libdvdread.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure \
 --disable-static 

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/libdvdread.so.*

%files devel
%defattr(-,root,root,-)
%doc TODO
%{_includedir}/dvdread
%{_libdir}/libdvdread.so
%{_libdir}/pkgconfig/dvdread.pc

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 4.9.9-2
- 为 Magic 3.0 重建

* Tue Jul 15 2014 Liu Di <liudidi@gmail.com> - 4.9.9-1
- 更新到 4.9.9

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.2.0-2
- 为 Magic 3.0 重建

* Sun Oct 09 2011 Dominik Mierzejewski <rpm@greysector.net> 4.2.0-1
- updated to 4.2.0 release

* Mon Apr 11 2011 Dominik Mierzejewski <rpm@greysector.net> 4.1.4-0.4.svn1226
- updated to SVN r1226
- dropped obsolete endianness check patch

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.4-0.3.svn1188
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 12 2009 Dominik Mierzejewski <rpm@greysector.net> 4.1.4-0.2.svn1188
- updated to SVN r1188 (rhbz#540155)

* Sun Sep 27 2009 Dominik Mierzejewski <rpm@greysector.net> 4.1.4-0.1.svn1183
- updated to SVN r1183
- simplified multilib patch
- fixed endianness issues (rhbz#442508)
- added some docs

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.1.3-3
- fix multilib conflict (#477687)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep 09 2008 Dominik Mierzejewski <rpm@greysector.net> 4.1.3-1
- update to 4.1.3 final

* Sun Aug 31 2008 Dominik Mierzejewski <rpm@greysector.net> 4.1.3-0.3.rc1
- update to 4.1.3rc1
- fix include path

* Thu Jul 17 2008 Dominik Mierzejewski <rpm@greysector.net> 4.1.3-0.2
- resurrect package from new upstream

* Sun Jan 27 2008 Dominik Mierzejewski <rpm@greysector.net> 0.9.7-4
- fix missing <inttypes.h> include (bug 428910)

* Wed Aug 29 2007 Dominik Mierzejewski <rpm@greysector.net> 0.9.7-3
- rebuild for BuildID
- update license tag

* Wed Nov 26 2006 Dominik Mierzejewski <rpm@greysector.net> 0.9.7-2
- Rebuild.

* Fri Oct  6 2006 Dams <anvil[AT]livna.org> - 0.9.7-1
- Updated to 0.9.7

* Wed Sep 20 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.9.6-2
- Rebuild.

* Sun Jul 23 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.9.6-1
- 0.9.6.
- Specfile cleanup.

* Thu Mar 16 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.9.4-4
- Fix linking with libdl on x86_64.
- Don't ship static libs.
- Build with dependency tracking disabled.
- Convert specfile and docs to UTF-8.
- Improve package descriptions.

* Thu Mar 16 2006 Dams <anvil[AT]livna.org> - 0.9.4-3
- We BuildConflicting libdvdcss-devel at build time

* Mon Mar 13 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> 0.9.4-2 
- Drop Epoch completely

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field
- drop Epoch

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Thu Apr  3 2003 Marius Johndal <mariuslj at ifi.uio.no> 0:0.9.4-0.fdr.1
- Initial Fedora RPM release.

* Mon Mar 31 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat Linux 9.
- Exclude .la file.

* Sun Feb 16 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 0.9.4.

* Thu Sep 26 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Updated to the latest cvs release.
- Rebuilt for Red Hat Linux 8.0.
- Updated URLs.

* Mon May 27 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 0.9.3.

* Wed May 15 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Fixed the libdvdcss.so.0/1/2 problem again.

* Thu May  2 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Back to using libdvdcss 1.1.1, now it's all merged and fine.
- Rebuilt against Red Hat Linux 7.3.
- Added the %{?_smp_mflags} expansion.

* Sat Jan 12 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Reverted back to using libdvdcss 0.0.3.ogle3 since it works MUCH better
  than 1.0.x. Doh!

* Tue Nov 13 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt against libdvdcss 1.0.0 (added a patch).

* Mon Oct 29 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Spec file cleanup and fixes.

* Thu Oct 11 2001 Martin Norbäck <d95mback@dtek.chalmers.se>
- Updated to version 0.9.2

* Tue Sep 25 2001 Martin Norbäck <d95mback@dtek.chalmers.se>
- Added small patch to fix the ldopen of libdvdcss

* Tue Sep 18 2001 Martin Norbäck <d95mback@dtek.chalmers.se>
- Updated to version 0.9.1

* Fri Sep 14 2001 Martin Norbäck <d95mback@dtek.chalmers.se>
- Split into normal and devel package

* Thu Sep 6 2001 Martin Norbäck <d95mback@dtek.chalmers.se>
- Updated to version 0.9.0

* Tue Jul 03 2001 Martin Norbäck <d95mback@dtek.chalmers.se>
- initial version



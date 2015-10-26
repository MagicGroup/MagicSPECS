%global ivtv_version 1.1.2

Name:           xorg-x11-drv-ivtv
Version:        1.2.0
Release:        0.12%{?dist}
Summary:        Xorg X11 ivtv video driver
Summary(zh_CN.UTF-8): Xorg X11 ivtv 显卡驱动

Group:          User Interface/X Hardware Support
Group(zh_CN.UTF-8): 用户界面/X 硬件支持
License:        MIT
URL:            http://ivtvdriver.org
Source0:        http://dl.ivtvdriver.org/xf86-video-ivtv/archive/1.1.x/xf86-video-ivtv-%{ivtv_version}.tar.gz
Source1:        ivtv-compat-api.h
Patch0:         xf86-video-ivtv-1.1.2-svn20120804.patch
Patch1:		ivtv-1.1.2-mibstore.patch

ExcludeArch: s390 s390x

BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: xorg-x11-proto-devel
Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)
Requires:  ivtv-firmware
Obsoletes: ivtv_xdriver < %{version}

%description
X.Org X11 ivtv video driver.

%description -l zh_CN.UTF-8
Xorg X11 ivtv 显卡驱动。

%prep
%setup -q -n xf86-video-ivtv-%{ivtv_version}
%patch0 -p1
%patch1 -p1

install -pm 0644 %{SOURCE1} src/compat-api.h


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/ivtv_drv.la


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog README
%{_libdir}/xorg/modules/drivers/ivtv_drv.so


%changelog
* Mon Oct 26 2015 Liu Di <liudidi@gmail.com> - 1.2.0-0.12
- 为 Magic 3.0 重建

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 1.2.0-0.11
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 1.2.0-0.10
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 1.2.0-0.9
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 1.2.0-0.8
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 1.2.0-0.7
- ABI rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-0.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.0-0.5
- require xorg-x11-server-devel, not -sdk

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.0-0.4
- ABI rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> 1.2.0-0.2
- ABI rebuild

* Sat Aug 04 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-0.1
- Update to svn trunk 20120803

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.1.2-9
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.1.2-8
- ABI rebuild

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.1.2-7
- ABI rebuild

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.1.2-6
- Rebuild for server 1.12

* Wed Nov 09 2011 ajax <ajax@redhat.com> - 1.1.2-5
- ABI rebuild

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 1.1.2-4
- Rebuild for xserver 1.11 ABI

* Mon Feb 28 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.2-3
- Rebuilt for new Xorg ABI

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.2-1
- Update to 1.1.2

* Thu Dec 02 2010 Adam Jackson <ajax@redhat.com> 1.1.1-4
- Really rebuild for new Xorg

* Sun Nov 28 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.1.1-3
- Rebuild for new Xorg

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 1.1.1-2
- Add ABI requires magic (#542742)

* Sun Nov 15 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1
- Remove upstreamed patch

* Thu Nov 12 2009 Adam Jackson <ajax@redhat.com> 1.1.0-6
- ExcludeArch: s390 s390x

* Wed Nov 11 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.1.0-5
- Switch to upstream patch.

* Tue Oct 20 2009 kwizart < kwizart at gmail.com > - 1.1.0-3
- Rebuild for F-12
- Add xf86-video-ivtv-1.1.0-Xextproto71.patch to fix new Xorg

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May  7 2009 kwizart < kwizart at gmail.com > - 1.1.0-1
- Update to 1.1.0 (development)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar  6 2008 kwizart < kwizart at gmail.com > - 1.0.1-2
- Add back xf86-video-ivtv-1.0.1-pagesize.patch

* Thu Mar  6 2008 kwizart < kwizart at gmail.com > - 1.0.1-1
- Update to 1.0.1 (final)

* Thu Mar  6 2008 kwizart < kwizart at gmail.com > - 1.0.1-0.2
- Add xf86-video-ivtv-1.0.1-pagesize.patch

* Wed Mar  5 2008 kwizart < kwizart at gmail.com > - 1.0.1-0.1
- Backport the libpciaccess support from pre 1.0.1

* Tue Feb 19 2008 kwizart < kwizart at gmail.com > - 1.0.0-3
- Fix for libpciaccess support

* Mon Feb 18 2008 kwizart < kwizart at gmail.com > - 1.0.0-2
- Bump for Fedora introduction.

* Mon Oct 22 2007 kwizart < kwizart at gmail.com > - 1.0.0-1
- Initial package.

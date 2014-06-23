%global _hardened_build 1

Name:           slim
Version:        1.3.6
Release:        4%{?dist}
Summary:        Simple Login Manager
Summary(zh_CN.UTF-8): 简单的登录管理器
Group:          User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
License:        GPLv2+
URL:            http://slim.berlios.de/
Source0:        http://download.berlios.de/slim/%{name}-%{version}.tar.gz
# stolen from xdm
Source1:        %{name}.pam
# adapted from debian to use freedesktop
Source2:        slim-update_slim_wmlist
Source3:        slim-dynwm
Source4:        slim-fedora.txt
# logrotate entry (see bz#573743)
Source5:        slim.logrotate.d
Source6:        slim-tmpfiles.conf
Source7:        slim.service
# Fedora-specific patches
Patch1:         slim-1.3.3-fedora.patch

BuildRequires:  libXmu-devel libXft-devel libXrender-devel
BuildRequires:  libpng-devel libjpeg-devel freetype-devel fontconfig-devel
BuildRequires:  pkgconfig gettext pam-devel cmake
BuildRequires:  xwd xterm freeglut-devel libXrandr-devel
Requires:       xwd xterm /sbin/shutdown
Requires:       %{_sysconfdir}/pam.d
# we use 'include' in the pam file, so
Requires:       pam >= 0.80
# for anaconda yum
Provides:       service(graphical-login)

BuildRequires:    systemd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description
SLiM (Simple Login Manager) is a graphical login manager for X11.
It aims to be simple, fast and independent from the various
desktop environments.
SLiM is based on latest stable release of Login.app by Per Lidén.

In the distribution, slim may be called through a wrapper, slim-dynwm,
which determines the available window managers using the freedesktop
information and modifies the slim configuration file accordingly,
before launching slim.

%description -l zh_CN.UTF-8
简单的登录管理器。

%prep
%setup -q

%patch1 -p0 -b .fedora
cp -p %{SOURCE4} README.Fedora

%build
CXXFLAGS="%{optflags}" cmake -DUSE_PAM=yes -DCMAKE_INSTALL_PREFIX=%{_prefix} .
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'
install -p -m755 %{SOURCE2} %{buildroot}%{_bindir}/update_slim_wmlist
install -p -m755 %{SOURCE3} %{buildroot}%{_bindir}/%{name}-dynwm
chmod 0644 %{buildroot}%{_sysconfdir}/%{name}.conf
install -d -m755 %{buildroot}%{_sysconfdir}/pam.d
install -p -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/%{name}
mkdir -p %{buildroot}%{_localstatedir}/run/%{name}
# install logrotate entry
install -m0644 -D %{SOURCE5} %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}

%if 0%{?fedora} >= 15
install -p -D %{SOURCE6} %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf
%endif

mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE7} %{buildroot}%{_unitdir}/%{name}.service

# Fix lib dir according to bits of system
mkdir -p %{buildroot}/%{_libdir}/
mv %{buildroot}/usr/lib/lib%{name}.so* %{buildroot}/%{_libdir}/ | :
# rm garbage from instaler
rm %{buildroot}/lib/systemd/system/%{name}.service
# devel .so
rm %{buildroot}/%{_libdir}/lib%{name}.so
magic_rpm_clean.sh

%post
/sbin/ldconfig
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
/sbin/ldconfig
%systemd_postun

%files
%doc COPYING ChangeLog README* THEMES TODO
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/logrotate.d/%{name}
%ghost %dir %{_localstatedir}/run/%{name}
%{_bindir}/%{name}*
%{_bindir}/update_slim_wmlist
%{_mandir}/man1/%{name}*.1*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/themes/
%{_unitdir}/%{name}.service
%{_libdir}/lib%{name}.so.%{version}

%if 0%{?fedora} >= 15
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%endif

%changelog
* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.3.6-4
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.3.6-3
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Nov 16 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 1.3.6-1
- Update to 1.3.6 (bz#1030423)
- Add libslim.so.%%{version}
- Add BR libXrandr-devel

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.3.5-4
- Perl 5.18 rebuild

* Fri Apr 26 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 1.3.5-3
- Harden build - bz#954324

* Thu Feb 7 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 1.3.5-2
- Update to 1.3.5.
- Fix typo in changelog
- Replace $RPM_BUILD_ROOT by %%{buildroot}
- rm garbage from installer /usr/usr/lib/systemd/system/slim.service
- Remove libpng patch.

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 1.3.4-2
- rebuild due to "jpeg8-ABI" feature drop

* Fri Nov 9 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 1.3.4-1
- Update to 1.3.4 version by Globe Trotter request (bz#868594).
- Add Patch0 to fix libpng1.5 incompatability..

* Sun Aug 12 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 1.3.3-5
- Display Manager Rework - https://fedoraproject.org/wiki/Features/DisplayManagerRework (bz#846152).
    Thanks to Lennart Poettering <lpoetter@redhat.com>

* Sun Aug 12 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 1.3.3-4
- Add BR freeglut-devel to fix FBFS on Fedora 18.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 6 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 1.3.3-2
- Update to 1.3.3 version by request bz#800254
- Step to cmake build system.
- Drop libpng and make patches.
- Rebase to new version Fedora patch.

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-11
- Rebuilt for c++ ABI breakage

* Thu Jan 26 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 1.3.2-10
- Add Patch slim-1.3.2-libpng-version.patch to fix FBFS in rawhide.
- Fix bz#717774

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.3.2-8
- Rebuild for new libpng

* Sun Jul 24 2011 Pavel Zhukov <landgraf@fedoraproject.org> - 1.3.2-7
- Rebuild for Rawhide

* Wed Jun 01 2011 Jan Kaluza <jkaluza@redhat.com> - 1.3.2-6
- fix #708693 - added tmfiles.d config to create /var/run/slim directory

* Tue Mar 01 2011 Petr Sabata <psabata@redhat.com> - 1.3.2-5
- General spec cleanup
- Moved slim-dynwm to a separate source file
- Patches renamed
- Buildroot removed

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 24 2010 Petr Sabata <psabata@redhat.com> - 1.3.2-3
- /var/run/slim is now ghost'd, rhbz#656689

* Tue Aug 31 2010 Petr Sabata <psabata@redhat.com> - 1.3.2-2
- slim-update_wm_list script modification, rhbz#581518

* Sun Aug 22 2010 Lorenzo Villani <lvillani@binaryhelix.net> - 1.3.2-1
- New upstream version 1.3.2
- Drop slim-1.3.1-usexwd.patch (folded into 02-slim-1.3.2-fedora.patch)
- Drop slim-1.3.1-curdir.patch (folded into 02-slim-1.3.2-fedora.patch)
- Drop slim-1.3.1-strtol.patch (merged upstream)
- Drop slim-1.3.1-remove.patch (merged upstream)
- Drop slim-1.3.1-gcc44.patch (merged upstream)
- Drop slim-1.3.1-CVE-2009-1756.patch (merged upstream)
- Drop slim-1.3.1-fix-insecure-mcookie-generation.patch (merged upstream)

* Tue Mar 30 2010 Lorenzo Villani <lvillani@binaryhelix.net> - 1.3.1-13
- Missing /var/run/slim (Fix bz#573284)

* Mon Mar 29 2010 Lorenzo Villani <lvillani@binaryhelix.net> - 1.3.1-12
- Add logrotate.d file to work-around bz#573743

* Fri Feb 19 2010 Lorenzo Villani <lvillani@binaryhelix.net> - 1.3.1-11
- Refresh slim-1.3.1-selinux.patch to include fix for bz#561095

* Tue Dec 22 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 1.3.1-9
- Fix CVE-2009-1756 (bugzilla: 544024)
- Fix MIT insecure cookie generation (patch from Debian)
- Fix build with GCC 4.4

* Sat Oct 10 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 1.3.1-8
- Fix BZ #518068

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 21 2009 Anders F Bjorklund <afb@users.sourceforge.net> 1.3.1-6
- exclude current directory from default_path in slim.conf (#505359)

* Sat Feb 28 2009 Anders F Bjorklund <afb@users.sourceforge.net> 1.3.1-5
- provide service(graphical-login) for anaconda yuminstall (#485789)

* Sun Feb 22 2009 Anders F Bjorklund <afb@users.sourceforge.net> 1.3.1-4
- Add header for remove(3)

* Wed Feb 04 2009 Anders F Bjorklund <afb@users.sourceforge.net> 1.3.1-3
- use small "default_blue" background, instead of large compat "default"

* Wed Oct 15 2008 Marco Pesenti Gritti <mpg@redhat.com>  1.3.1-2
- Enable pam_selinux

* Thu Oct 09 2008 Marco Pesenti Gritti <mpg@redhat.com>  1.3.1-1
- Update to 1.3.1

* Sun Oct 05 2008 Anders F Bjorklund <afb@users.sourceforge.net> 1.3.0-7
- add compat req (#465631)

* Wed Sep 24 2008 Anders F Bjorklund <afb@users.sourceforge.net> 1.3.0-6
- fix patch fuzz

* Fri May 16 2008 Anders F Bjorklund <afb@users.sourceforge.net> 1.3.0-5
- all the images are now in desktop-backgrounds-basic

* Fri Feb 22 2008 Anders F Bjorklund <afb@users.sourceforge.net> 1.3.0-4
- add header for strtol(3)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.0-3
- Autorebuild for GCC 4.3

* Sat Jan 19 2008 Anders F Bjorklund <afb@users.sourceforge.net> 1.3.0-2
- rebuild

* Mon Aug  6 2007 Anders F Bjorklund <afb@users.sourceforge.net> 1.3.0-1
- version upgrade

* Mon Aug  6 2007 Anders F Bjorklund <afb@users.sourceforge.net> 1.2.6-6
- require system-logos instead of fedora-logos (#250365)

* Tue May 22 2007 Anders F Bjorklund <afb@users.sourceforge.net> 1.2.6-5
- make sure to own datadir slim parent too

* Mon May 21 2007 Anders F Bjorklund <afb@users.sourceforge.net> 1.2.6-4
- use desktop background, instead of slim
- leave (unused) pam files in the package

* Mon May 14 2007 Anders F Bjorklund <afb@users.sourceforge.net>
- clean up spec file
- correct README user

* Sun May 13 2007 Anders F Bjorklund <afb@users.sourceforge.net> 1.2.6-3
- use slim background instead of default
- added more build dependencies / -devel
- add "README.Fedora"
- patch issue display

* Wed May 09 2007 Anders F Bjorklund <afb@users.sourceforge.net>
- clean up spec file
- noreplace slim.conf

* Tue May 08 2007 Anders F Bjorklund <afb@users.sourceforge.net> 1.2.6-2
- fixed source URL
- added libXft-devel
- removed xrdb dependency (left from wdm)
- added xwd dependency (for screenshots)

* Sun May 06 2007 Anders F Bjorklund <afb@users.sourceforge.net> 1.2.6-1
- initial package
- adopted wdm spec

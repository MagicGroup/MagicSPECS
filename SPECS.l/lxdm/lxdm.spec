# Review at https://bugzilla.redhat.com/show_bug.cgi?id=540034

%{!?_unitdir: %global _unitdir %{_prefix}/lib/systemd/system/}

%global git_snapshot 0

%if 0%{?git_snapshot}
%global git_rev cf9b2cbb7be8ec1a01530d1f37b7d6f48f0e5fd0
%global git_date 20100921
%global git_short %(echo %{git_rev} | cut -c-8)
%global git_version %{git_date}git%{git_short}
%endif

# Source0 was generated as follows: 
# git clone git://lxde.git.sourceforge.net/gitroot/lxde/%{name}
# cd %{name}
# git archive --format=tar --prefix=%{name}/ %{git_short} | bzip2 > %{name}-%{?git_version}.tar.bz2

Name:           lxdm
Version:	0.5.3
Release:	2%{?dist}
Summary:        Lightweight X11 Display Manager
Summary(zh_CN.UTF-8): 轻量级的 X11 登录管理器

Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:        GPLv2+ and LGPLv2+
URL:            http://lxde.org

%if 0%{?git_snapshot}
Source0:        %{name}-%{?git_version}.tar.bz2
%else
Source0:        http://downloads.sourceforge.net/sourceforge/lxde/%{name}-%{version}.tar.xz
%endif

# systemd service file and preset
Source1:        lxdm.service
Source2:        lxdm.preset

# Fedora pam setting
Source10:		pam.lxdm

# Shell script to create tarball from git scm
Source100:      create-tarball-from-git.sh

## Patches needing discussion with the upstream

## Distro specific patches ##

# Distro artwork, start on vt1
Patch50:        lxdm-0.4.1-config.patch
Patch60:        lxdm-0.5.1-ssh-agent-on-start.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  pkgconfig(gtk+-2.0) >= 2.12.0
BuildRequires:  iso-codes-devel
BuildRequires:  ConsoleKit-devel
BuildRequires:  pam-devel
BuildRequires:  intltool >= 0.40.0
Requires:       pam
Requires:       /sbin/shutdown
# needed for anaconda to boot into runlevel 5 after install
Provides:       service(graphical-login) = lxdm

BuildRequires:  systemd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd


%description
LXDM is the future display manager of LXDE, the Lightweight X11 Desktop 
environment. It is designed as a lightweight alternative to replace GDM or 
KDM in LXDE distros. It's still in very early stage of development.

%description -l zh_CN.UTF-8
LXDE 下的一个轻量级的登录管理器，类似 GDM 或 KDM。

%prep
%setup -q %{?git_version:-n %{name}}
%patch50 -p1 -b .config
%patch60 -p1 -b .ssh_agent

sed -i.reset data/lxdm.conf.in \
	-e '\@reset@s|^.*$|reset=1|' 

install -cpm 644  %{SOURCE10} pam/lxdm

cat << EOF > tempfiles.lxdm.conf
d %{_localstatedir}/run/%{name} 0755 root root
EOF

%build
%{?git_version:sh autogen.sh}
%configure \
	--disable-silent-rules \
	--disable-consolekit \
	%{nil}
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'
magic_rpm_clean.sh
%find_lang %{name}

# these files are not in the package, but should be owned by lxdm 
touch %{buildroot}%{_sysconfdir}/%{name}/xinitrc
mkdir -p %{buildroot}%{_localstatedir}/run/%{name}
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}
touch %{buildroot}%{_localstatedir}/lib/%{name}.conf

install -Dpm 644 tempfiles.lxdm.conf %{buildroot}%{_prefix}/lib/tmpfiles.d/lxdm.conf

install -Dpm 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -m644 -p -D %{SOURCE2} %{buildroot}%{_unitdir}-preset/83-fedora-lxdm.preset


%post
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service


%postun
%systemd_postun


%files -f %{name}.lang
# FIXME a%description -l zh_CN.UTF-8 ChangeLog and NEWS if not empty
%doc AUTHORS COPYING README TODO gpl-2.0.txt lgpl-2.1.txt
%dir %{_sysconfdir}/%{name}
%ghost %config(noreplace,missingok) %{_sysconfdir}/%{name}/xinitrc
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/%{name}/Xsession
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/%{name}/LoginReady
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/%{name}/PostLogin
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/%{name}/PostLogout
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/%{name}/PreLogin
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/%{name}/PreReboot
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/%{name}/PreShutdown
%config %{_sysconfdir}/%{name}/lxdm.conf
%config(noreplace) %{_sysconfdir}/pam.d/%{name}

%{_bindir}/%{name}-config
%{_sbindir}/%{name}
%{_sbindir}/lxdm-binary
%{_libexecdir}/lxdm-greeter-gtk
%{_libexecdir}/lxdm-greeter-gdk
%{_libexecdir}/lxdm-numlock
%{_libexecdir}/lxdm-session
%{_datadir}/%{name}/

%config(noreplace) %{_prefix}/lib/tmpfiles.d/lxdm.conf

%{_unitdir}/lxdm.service
%{_unitdir}-preset/83-fedora-lxdm.preset

%ghost %dir %{_localstatedir}/run/%{name}

%dir %{_localstatedir}/lib/%{name}
%ghost %{_localstatedir}/lib/%{name}.conf

%changelog
* Fri Jan 29 2016 Liu Di <liudidi@gmail.com> - 0.5.3-2
- 为 Magic 3.0 重建

* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 0.4.1-7
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.4.1-6
- 为 Magic 3.0 重建

* Mon Jun 23 2014 Liu Di <liudidi@gmail.com> - 0.4.1-5
- 为 Magic 3.0 重建

* Fri Sep 07 2012 Adam Williamson <awilliam@redhat.com> - 0.4.1-4
- ship a systemd preset for lxdm (#855470)
- add After: livesys-late.service to the service file, testing of other
  DMs indicated this is needed for lives

* Tue Aug 07 2012 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.1-3
- Move tmpfiles configuration to new location (#840186)
- Ship systemd service file for Fedora >= 18 (#846148)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 21 2012 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.1-1
- Update to 0.4.1 (#758480), fixes #596360, #635897, #652697, #683728, #758480
  and #758484
- Fix softlock bug causing 100% CPU (#767861, #794478)
- Fix SELinux problem with xauth (#635897)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.3.0-5
- Rebuild for new libpng

* Wed Feb 16 2011 Adam Williamson <awilliam@redhat.com> - 0.3.0-4
- add background.patch from upstream: change X parameter -nr to
  -background (fixes #661600)
- rediff config.patch to account for background.patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 28 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.0-2
- Mark files in /var/run as %%ghost (#656618)

* Thu Sep 30 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.0-1
- Update to 0.3.0

* Wed Sep 29 2010 jkeating - 0.3.0-0.2.20100921gitcf9b2cbb
- Rebuilt for gcc bug 634757

* Mon Sep 21 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.0-0.1.20100921gitcf9b2cbb
- Update to GIT snapshot of 20100921 (fixes #635396)

* Tue May 18 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.0-4
- Fix env XAUTHORITY bug

* Sun May 16 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.0-3
- Fix permissions of /var/run/lxdm
- Add patches to fix some env settings
- Add --debug option

* Sun May 09 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.0-2
- Patch for SELinux problems (#564320)

* Wed May 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0

* Sat Apr 17 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.0-0.3.20100405gitd65ce94
- Adjustments for recent Goddard artwork changes

* Tue Apr 06 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.0-0.2.20100405gitd65ce94
- Fix ownership of scripts in /etc/lxdm

* Mon Apr 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.0-0.1.20100405gitd65ce94
- Update to git release cb858f7
- New BuildRequires pam-devel
- Bump version to 0.2.0

* Wed Mar 11 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.1-0.2.20100303gite4f7b39
- Make sure lxdm.conf gets updated to avoid login problems

* Wed Mar 03 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.1-0.1.20100303gite4f7b39
- Update to git release e4f7b39 (fixes #564995)
- Fix SELinux problems (#564320)

* Wed Feb 24 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.1-0.1.20100223gitdf819fd
- Update to latest git
- BR iso-codes-devel
- Don't hardcode tty1 in the source, use lxdm.conf instead

* Fri Jan 08 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.0-1
- Update to 0.1.0
- Change license to GPLv2+ and LGPLv2+
- Use tty1 by default
- PAM fixes for SELinux (#552885)

* Mon Nov 16 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.3-0.2.20091116svn2145
- Review fixes

* Mon Nov 16 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.3-0.1.20091116svn2145
- Update to SVN release 2145

* Thu Nov 05 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.3-0.1.20091105svn2132
- Update to SVN release 2132

* Sat Oct 31 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.3-0.1.20091031svn2100
- Update to SVN release 2100

* Tue Oct 20 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.3-0.1.20091020svn2082
- Update to SVN release 2082

* Fri Sep 18 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.2-1
- Initial Fedora package

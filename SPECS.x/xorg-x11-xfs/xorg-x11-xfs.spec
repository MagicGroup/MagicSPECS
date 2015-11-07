%global uid 43
%global username xfs

# Component versions
%define xfsinfo 1.0.5
%define fslsfonts 1.0.5
%define fstobdf 1.0.6
%define showfont 1.0.5

Summary:    X.Org X11 xfs font server
Summary(zh_CN.UTF-8): X.Org X11 xfs 字体服务
Name:       xorg-x11-xfs
Version:    1.1.4
Release:    5%{?dist}
Epoch:      1
License:    MIT
URL:        http://www.x.org

Source0:    http://www.x.org/pub/individual/app/xfs-%{version}.tar.bz2
Source1:    http://www.x.org/pub/individual/app/xfsinfo-%{xfsinfo}.tar.bz2
Source2:    http://www.x.org/pub/individual/app/fslsfonts-%{fslsfonts}.tar.bz2
Source3:    http://www.x.org/pub/individual/app/fstobdf-%{fstobdf}.tar.bz2
Source4:    http://www.x.org/pub/individual/app/showfont-%{showfont}.tar.bz2
Source10:   xfs.service
Source11:   xfs.init
Source12:   xfs.config
Source13:   xfs.tmpfiles

BuildRequires:  xorg-x11-font-utils >= 1.1
BuildRequires:  libtool
BuildRequires:  pkgconfig(libfs)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xfont) >= 1.4.5
BuildRequires:  pkgconfig(xorg-macros)
BuildRequires:  pkgconfig(xtrans)

BuildRequires: systemd

Provides:   xfs = %{version}
Provides:   xfsinfo = %{xfsinfo}
Provides:   fslsfonts = %{fslsfonts}
Provides:   fslsfonts = %{fslsfonts}
Provides:   fstobdf = %{fstobdf}
Provides:   showfont = %{showfont}

Requires(pre):  shadow-utils

Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd

%description
X.Org X11 xfs font server.

%description -l zh_CN.UTF-8
X.Org X11 xfs 字体服务。

%package utils
Summary:    X.Org X11 font server utilities
Summary(zh_CN.UTF-8): X.Org X11 字体服务工具
#Requires: %{name} = %{version}-%{release}

%description utils
X.Org X11 font server utilities.

%description utils -l zh_CN.UTF-8
X.Org X11 字体服务工具。

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4

%build

# Build all apps
{
   for app in * ; do
      pushd $app
      case $app in
         xfs-*)
            autoreconf -vif
            %configure
            # export CFLAGS='-DDEFAULT_CONFIG_FILE="/etc/X11/fs/config"'
            make configdir=%{_sysconfdir}/X11/fs
            ;;
         *)
            autoreconf -vif
            %configure
            make %{?_smp_mflags}
            ;;
      esac

      popd
   done
}

%install
# Install all apps
{
   for app in * ; do
      pushd $app
      case $app in
         xfs-*)
            %make_install configdir=%{_sysconfdir}/X11/fs
            ;;
         *)
            %make_install
            ;;
      esac
      popd
   done
}

# Install the Red Hat xfs config file and initscript
install -D -p -m 644 %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/X11/fs/config

# Systemd unit files
mkdir -p %{buildroot}%{_unitdir}
install -p -m 644 -D %{SOURCE10} %{buildroot}%{_unitdir}/xfs.service
install -p -m 644 -D %{SOURCE13} %{buildroot}%{_tmpfilesdir}/xfs.conf

%pre
getent group %username >/dev/null || groupadd -g %uid -r %username &>/dev/null || :
getent passwd %username >/dev/null || useradd -u %uid -r -s /sbin/nologin \
    -d %{_sysconfdir}/X11/fs -M -c 'X Font Server' -g %username %username &>/dev/null || :
exit 0

%post
%systemd_post xfs.service

%preun
%systemd_preun xfs.service

%postun
%systemd_postun_with_restart xfs.service

%files
%doc xfs-%{version}/COPYING
%{_bindir}/xfs
%dir %{_sysconfdir}/X11/fs
# NOTE: We intentionally override the upstream default config file location
# during build.
# FIXME: Create patch for the following, and submit it upstream.
# Check if this is still relevent:  set configdir=$(sysconfdir) in Makefile.am
# and if so, submit patch upstream to fix.
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/X11/fs/config
%{_mandir}/man1/xfs.1*
%{_unitdir}/xfs.service
%{_tmpfilesdir}/xfs.conf

%files utils
%doc xfs-%{version}/COPYING
%{_bindir}/fslsfonts
%{_bindir}/fstobdf
%{_bindir}/showfont
%{_bindir}/xfsinfo
%{_mandir}/man1/fslsfonts.1*
%{_mandir}/man1/fstobdf.1*
%{_mandir}/man1/showfont.1*
%{_mandir}/man1/xfsinfo.1*

%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 1:1.1.4-5
- 为 Magic 3.0 重建

* Tue Oct 27 2015 Liu Di <liudidi@gmail.com> - 1:1.1.4-4
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 08 2015 Simone Caronni <negativo17@gmail.com> - 1:1.1.4-2
- Clean up SPEC file, fix rpmlint warnings.
- Rewrite completely init script and install logic completely according to
  packaging guidelines.
- Add systemd files (starting Fedora 22 / RHEL 8).
- Remove upgrade stuff (~2005/2006).
- xfsinfo 1.0.5
- fslsfonts 1.0.5
- fstobdf 1.0.6
- showfont 1.0.5

* Thu Aug 28 2014 Hans de Goede <hdegoede@redhat.com> - 1:1.1.4-1
- xfs 1.1.4 (rhbz#952216)
- xfsinfo 1.0.4
- fslsfonts 1.0.4
- fstobdf 1.0.5
- showfont 1.0.4

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 09 2014 Adam Jackson <ajax@redhat.com> 1.1.3-1
- xfs 1.1.3 plus new fontproto compat
- Pre-F12 changelog trim

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 23 2012 Adam Jackson <ajax@redhat.com> 1.1.2-1
- xfs 1.1.2

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 05 2011 Adam Jackson <ajax@redhat.com> 1.1.1-3
- xfs.init: Redact calls to chkfontpath (#665746)
- Remove some monolith-to-modular upgrade path leftovers

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 02 2010 Peter Hutterer <peter.hutterer@redhat.com> 1:1.1.1-1
- xfs 1.1.1
- xfsinfo 1.0.3
- fslsfonts 1.0.3
- fstobdf 1.0.4
- showfont 1.0.3

* Thu Jul 08 2010 Adam Jackson <ajax@redhat.com> 1:1.0.5-8
- Install a COPYING for -utils too
- Remove some XFree86 compat oh my goodness how was that still there.

* Fri Mar 05 2010 Matěj Cepl <mcepl@redhat.com> - 1:1.0.5-7
- Fixed bad directory ownership of /etc/X11

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

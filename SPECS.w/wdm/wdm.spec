Name:           wdm
Version:        1.28
Release:        14%{?dist}
Summary:        WINGs Display Manager
Summary(zh_CN.UTF-8): WINGs 会话管理器

Group:          User Interface/X
Group(zh_CN.UTF-8):	用户界面/X
# many MIT source files from xdm, and GPLv2+ from Wings
License:        GPLv2+
URL:            http://voins.program.ru/wdm/
Source0:        http://voins.program.ru/wdm/wdm-%{version}.tar.bz2
# stolen from xdm
Source1:        %{name}.pam
# adapted from debian to use freedesktop
Source2:        wdm-update_wdm_wmlist
# record and reuse previous session before launching generic Xsession
Source3:        wdm-Xsession
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# debian patch modified to remove the configure patching
#Patch0:         http://ftp.debian.org/debian/pool/main/w/wdm/wdm_1.28-2.1.diff.gz
Patch0:         wdm_1.28-2.1.diff
# use fedora background/icon and match gdm default config
Patch1:         wdm-1.28-fedora.patch
# fix failsafe path and insecure use of /tmp
Patch2:         wdm-1.28-failsafe_tmp.patch
# fix reconfiguration script
Patch3:         wdm-1.28-reconf.patch

#Patch4:         wdm-1.28-ck.patch

BuildRequires:  WINGs-devel gettext pam-devel
BuildRequires:  libXt-devel libXmu-devel
BuildRequires:  xrdb xterm /sbin/shutdown
Requires:       xrdb xterm /sbin/shutdown
Requires:       %{_sysconfdir}/pam.d
# we don't want to have new files, we reuse the kdm/xdm files
Requires:       xdm xorg-x11-xinit
# we use 'include' in the pam file, so
Requires:       pam >= 0.80
# reuse the images
#Requires:       desktop-backgrounds-basic

%description
wdm combines the functions of a graphical display manager identifying 
and authenticating a user on a system with some of the functions of a 
session manager in selecting and starting a window manager. Optionally, 
wdm can shutdown (reboot or halt) the system.

wdm is a modification of XFree86's xdm package for graphically handling 
authentication and system login. Most of xdm has been preserved 
(XFree86 4.2.1.1) with the Login interface based on a WINGs. Tom 
Rothamel's "external greet" interface (see AUTHORS) was used to 
communicate wdm with wdmLogin. 

In the distribution, wdm may be called through a wrapper, wdm-dynwm, 
which determines the available window managers using the freedesktop 
information and modifies the wdm-config configuration file accordingly, 
before launching wdm.

%description -l zh_CN.UTF-8
一个会话管理器。

%prep
%setup -q
%patch0 -p1
#%patch1 -p1 -b .fedora
%patch2 -p1 -b .failsafe_tmp
%patch3 -p1 -b .reconf
#%patch4 -p1 -b .ck

%build

export DEF_SERVER='%{_bindir}/X -nolisten tcp'
#export CFLAGS="$RPM_OPT_FLAGS `pkg-config --cflags ck-connector` -DUSE_CONSOLEKIT"
#export LDFLAGS="`pkg-config --libs ck-connector`"

%configure \
   --with-pamdir=%{_sysconfdir}/pam.d \
   --with-logdir=%{_localstatedir}/log \
   --with-runlockdir=%{_localstatedir}/run \
   --with-wdmdir=%{_sysconfdir}/wdm \
   --with-nlsdir=%{_datadir}/locale \
   --with-fakehome=%{_localstatedir}/run/wdm \
   --with-gfxdir=%{_datadir}/pixmaps/wdm \
   --with-defuserpath='/bin:%{_bindir}' \
   --with-defsystempath='/sbin:%{_sbindir}:/bin:%{_bindir}' \
   --disable-selinux \
   --enable-aafont 


make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

install -p -m755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/update_wdm_wmlist

# do a wdm wrapper which updates the window manager list before
# launching wdm
cat > $RPM_BUILD_ROOT%{_bindir}/wdm-dynwm << EOF
#!/bin/sh
update_wdm_wmlist
wdm "\$@"
EOF

chmod 0755 $RPM_BUILD_ROOT%{_bindir}/wdm-dynwm

# move the reconfiguration script to _bindir
mv $RPM_BUILD_ROOT%{_sysconfdir}/wdm/wdmReconfig $RPM_BUILD_ROOT%{_bindir}

chmod 0644 $RPM_BUILD_ROOT%{_sysconfdir}/wdm/wdm-config

install -p -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/wdm

# remove old X session script, and old XFree86 session script
rm $RPM_BUILD_ROOT%{_sysconfdir}/wdm/Xsession.orig
rm $RPM_BUILD_ROOT%{_sysconfdir}/wdm/Xsession.XFree86

# use xdm/kdm files 
# first rename wdm files
for file in Xaccess Xsession Xsetup_0 GiveConsole TakeConsole; do
mv $RPM_BUILD_ROOT%{_sysconfdir}/wdm/$file $RPM_BUILD_ROOT%{_sysconfdir}/wdm/$file.wdm
done

# then use symlinks or wrapper
# calls /etc/X11xinit/Xsession
install -p -m755 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/wdm/Xsession
ln -s ../X11/xdm/Xaccess $RPM_BUILD_ROOT%{_sysconfdir}/wdm/Xaccess
ln -s ../X11/xdm/Xsetup_0 $RPM_BUILD_ROOT%{_sysconfdir}/wdm/Xsetup_0
ln -s ../X11/xdm/GiveConsole $RPM_BUILD_ROOT%{_sysconfdir}/wdm/GiveConsole
ln -s ../X11/xdm/TakeConsole $RPM_BUILD_ROOT%{_sysconfdir}/wdm/TakeConsole
ln -s ../X11/xdm/Xsession $RPM_BUILD_ROOT%{_sysconfdir}/wdm/Xsession.xorg
magic_rpm_clean.sh
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog* NEWS README* TODO NASA_image_guideline.html 
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pam.d/wdm
%dir %{_sysconfdir}/wdm/
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/wdm/wdm-config
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/wdm/wdm-config.in
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/wdm/Xresources
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/wdm/Xservers
%config %{_sysconfdir}/wdm/GiveConsole.wdm
%config %{_sysconfdir}/wdm/TakeConsole.wdm
%config %{_sysconfdir}/wdm/Xaccess.wdm
%config %{_sysconfdir}/wdm/Xclients
%config %{_sysconfdir}/wdm/Xclients.in
%config %{_sysconfdir}/wdm/Xservers.fs
%config %{_sysconfdir}/wdm/Xservers.ws
%config %{_sysconfdir}/wdm/Xsession
%config %{_sysconfdir}/wdm/Xsession.wdm
%config %{_sysconfdir}/wdm/Xsetup_0.wdm
# links
%config %{_sysconfdir}/wdm/GiveConsole
%config %{_sysconfdir}/wdm/TakeConsole
%config %{_sysconfdir}/wdm/Xaccess
%config %{_sysconfdir}/wdm/Xsession.xorg
%config %{_sysconfdir}/wdm/Xsetup_0
%{_bindir}/wdm*
%{_bindir}/update_wdm_wmlist
%{_mandir}/man1/wdm*.1*
%{_datadir}/pixmaps/wdm/
%dir %{_localstatedir}/run/wdm


%changelog
* Mon Oct 19 2015 Liu Di <liudidi@gmail.com> - 1.28-14
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.28-13
- 为 Magic 3.0 重建



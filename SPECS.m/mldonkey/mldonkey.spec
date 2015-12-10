%define _notuse_dependency_tracking %{nil}

Name:		mldonkey
Version: 3.1.5
Release: 3%{?dist}
Summary:	Client for several P2P networks
Summary(zh_CN.UTF-8): P2P 网络的客户端
License:	GPLv2+
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:	mldonkey-gui.desktop
Source8:	mldonkey_df_monitor.crond
Source9:	mldonkey_df_monitor.sh
Source11:	mldonkey.logrotate
Source12:	mldonkey.service
#Patch1:		mldonkey-0001-Init-script-enhancements.patch
Patch2:		mldonkey-0002-Fix-DSO-linking.patch
Patch3:		mldonkey-3.0.3-gcc47.patch
URL:		http://mldonkey.sourceforge.net
Group:		Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if 0%{?el5}
BuildRequires:	ocaml >= 3.09.3
BuildRequires:	camlp4
%else
BuildRequires:	ocaml >= 3.10.0
BuildRequires:	ocaml-camlp4-devel
%endif
%if 0%{?fedora}%{?el6}
BuildRequires:	ocaml-lablgtk-devel >= 2.10.0
BuildRequires:	desktop-file-utils
BuildRequires:	gtk2-devel >= 2.4.0
BuildRequires:	librsvg2-devel >= 2.4.0
%endif
BuildRequires:	zlib-devel
BuildRequires:	bzip2-devel
BuildRequires:	ncurses-devel
%if 0%{?el5}
BuildRequires:	file
%else
BuildRequires:	file-devel
%endif
ExcludeArch:     sparc64 s390 s390x

Requires:	logrotate
# for kill_mldonkey
Requires:	perl(LWP::UserAgent)
# for mldonkey_command
Requires:	nc


%description
MLDonkey is a door to the 'donkey' network, a decentralized network used to
exchange big files on the Internet. It is written in a wonderful language,
called Objective-Caml, and present most features of the basic Windows donkey
client, plus some more:
  - It should work on most UNIX-compatible platforms.
  - You can remotely command your client, either by telnet (port 4000),
    by a WEB browser (http://localhost:4080), or with a classical client
    interface (see http://www.nongnu.org/mldonkey)
  - You can connect to several servers, and each search will query all the
    connected servers.
  - You can select mp3s by bitrates in queries (useful ?).
  - You can select the name of a downloaded file before moving it to your
    incoming directory.
  - You can have several queries in the graphical user interface at the same
    time.
  - You can remember your old queries results in the command-line interface.
  - You can search in the history of all files you have seen on the network.

It can also access other peer-to-peer networks:
- BitTorrent
- Fasttrack
- FileTP (wget-clone)
- DC++

%description -l zh_CN.UTF-8
P2P 网络的客户端，支持 edonkey 协议和 BitTorrent, Fasttrack, FileTP, DC++ 等。


%if 0%{?fedora}%{?el6}
%package gui
Summary:	Graphical frontend for mldonkey based on GTK
Summary(zh_CN.UTF-8): 基于 GTK 的 mldonkey 的图形界面
Group:		Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
Requires:	hicolor-icon-theme
# TODO requirement for mldonkey_previewer
# Requires:	mplayer


%description gui
The GTK interface for mldonkey provides a convenient way of managing
all mldonkey operations. It gives details about conected servers,
downloaded files, friends and lets one search for files in a pleasing
way.

%description gui -l zh_CN.UTF-8
基于 GTK 的 mldonkey 的图形界面。
%endif


%package server
Summary:	Enables mldonkey as a system daemon
Summary(zh_CN.UTF-8): 使 mldonkey 做为系统服务启动
Group:		System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
Requires:	%{name} = %{version}-%{release}
# Necessary for mldonkey_df_monitor.sh
Requires:	mailx
Requires(pre):	/usr/sbin/useradd
#Requires(post): /sbin/chkconfig
#Requires(preun):/sbin/chkconfig
#Requires(preun):/sbin/service
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units


%description server
Contains init and configs to launch mldonkey as a service.

NOTE: by default incoming dir is located in %{_localstatedir}/lib/mldonkey/incoming
and temp dir in %{_localstatedir}/lib/cache/mldonkey. Mlondkey is launched
with the mldonkey user (created after installation).

NOTE: If you are using a password for your mldonkey, you need to specify
it in your %{_sysconfdir}/sysconfig/mldonkey, because mldonkey now stores
it encrypted.

%description server -l zh_CN.UTF-8
使 mldonkey 做为系统服务启动。

%package -n konqueror-mldonkey-ed2k-support
Summary:	Easy way to download a ed2k-link from Konqueror
Summary(zh_CN.UTF-8): 在 Konqueror 中简单下载 ed2k 链接
Group:		User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Requires:	perl(LWP::UserAgent)
Requires:	kdelibs4


%description -n konqueror-mldonkey-ed2k-support
This package contains tool which gives you an easy way to add an ed2k-link
(like ed2k://|file|filename.exe|21352658|72b0b287cab7d875ccc1d89ebe910b9g|)
with a single click to your mldonkey download queue.
You need to edit %{_sysconfdir}/sysconfig/mldonkey_submit

%description -n konqueror-mldonkey-ed2k-support -l zh_CN.UTF-8
在 Konqueror 中简单下载 ed2k 链接。

#%package -n mozilla-mldonkey-ed2k-support
#Summary:	Easy way to download a ed2k-link from Mozilla/Firefox
#Group:		User Interface/Desktops
# TODO should it require firefox?


#%description -n mozilla-mldonkey-ed2k-support
#This package contains tool which gives you an easy way to add an ed2k-link
#(like ed2k://|file|filename.exe|21352658|72b0b287cab7d875ccc1d89ebe910b9g|)
#with a single click within Mozilla/Firefox to your mldonkey download queue.
#The tool is a .xpi file to import into mozilla. The file is located in
#%{_datadir}/%name


%prep
%setup -q
#%patch1 -p1 -b .fedora
%if 0%{?fedora}
%patch2 -p1 -b .DSO_linking
#%patch3 -p1 -b .gcc47
%endif
# Let's make rpmlint happy
sed -i 's|\r||g' distrib/ed2k_submit/README.MLdonkeySubmit
sed -i 's|\r||g' docs/slavanap.txt

iconv -f iso8859-1 -t UTF-8 docs/gnutella.txt > docs/gnutella.utf8 && mv docs/gnutella.{utf8,txt}
iconv -f iso8859-1 -t UTF-8 distrib/Authors.txt > distrib/Authors.utf8 && mv distrib/Authors.{utf8,txt}

chmod 644 src/utils/lib/fst_hash.c
chmod 644 src/networks/fasttrack/fst_crypt_ml.c


%build
%configure --enable-pthread --disable-option-checking \
%if 0%{?fedora}%{?el6}
           --enable-ocamlver=%(rpm -q --qf '%%{version}' ocaml) \
           --enable-gui=newgui2 \
%else
           --enable-ocamlver=3.09.3 \
           --disable-gui \
%endif
           --disable-gd


make depend
# Does not support parallel builds
make
make utils


%install
rm -rf $RPM_BUILD_ROOT
DONT_GPRINTIFY=1
export DONT_GPRINTIFY
make DESTDIR=$RPM_BUILD_ROOT install

# core
install -p -m 755 distrib/mldonkey_command $RPM_BUILD_ROOT%{_bindir}/mldonkey_command
install -p -m 755 distrib/kill_mldonkey $RPM_BUILD_ROOT%{_bindir}/kill_mldonkey

# utils
for util in copysources mld_hash get_range svg_converter subconv; do
	install -p -m 755 $util $RPM_BUILD_ROOT%{_bindir}/$util ;
done
# in order to avoid conflicts with rb_libtorrent (see bz# 484885, 484884)
install -p -m 755 make_torrent $RPM_BUILD_ROOT%{_bindir}/mldonkey_make_torrent

%if 0%{?fedora}%{?el6}
# gui
install -p -m 755 mlguistarter $RPM_BUILD_ROOT%{_bindir}/mlguistarter

# install preview utility
install -p -m 755 distrib/mldonkey_previewer $RPM_BUILD_ROOT%{_bindir}/mldonkey_previewer

# menu and pixmaps
install packages/rpm/mldonkey-icon-16.png -D -m 644 $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/mldonkey.png
install packages/rpm/mldonkey-icon-32.png -D -m 644 $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/mldonkey.png
install packages/rpm/mldonkey-icon-48.png -D -m 644 $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/mldonkey.png
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/pixmaps
ln -s ../icons/hicolor/48x48/apps/mldonkey.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/mldonkey.png
desktop-file-install --vendor fedora --dir $RPM_BUILD_ROOT%{_datadir}/applications --copy-generic-name-to-name %{SOURCE1}
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop
%endif

# Send email when mldonkey runs out of allowed disk space
install -D -p -m 755 %{SOURCE9} $RPM_BUILD_ROOT%{_sbindir}/mldonkey_df_monitor.sh
sed -i 's,/var,%{_localstatedir},g;
        s,/etc/init.d,%{_initrddir},g;
        s,/etc,%{_sysconfdir},g' $RPM_BUILD_ROOT%{_sbindir}/mldonkey_df_monitor.sh

install -D -p -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/mldonkey_df_monitor
sed -i 's,/usr/sbin,%{_sbindir},g' $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/mldonkey_df_monitor

# create directory for storing log-file
install -d -m 755 $RPM_BUILD_ROOT%{_localstatedir}/log/mldonkey

# install logrotate script for  /var/log/mldonkey/mldonkey.log
install -D -p -m 644 %{SOURCE11} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/mldonkey
sed -i 's,/var,%{_localstatedir},g' $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/mldonkey

# install init-scipt
#install -D -p -m 755 packages/rpm/mldonkey.init $RPM_BUILD_ROOT%{_initrddir}/mldonkey
#sed -e 's,/etc/init.d,%{_initrddir},g;
#        s,/etc,%{_sysconfdir},g;
#        s,/var,%{_localstatedir},g' $RPM_BUILD_ROOT%{_initrddir}/mldonkey
install -D -p -m 644 %{SOURCE12} $RPM_BUILD_ROOT/%{_unitdir}/mldonkey.service

# Create necessary directories for server
install -d -m 755 $RPM_BUILD_ROOT%{_localstatedir}/cache/mldonkey
install -d -m 755 $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/incoming
install -d -m 755 $RPM_BUILD_ROOT%{_localstatedir}/run/%{name}

# create downloads.ini
echo -e \
"temp_directory = \"%{_localstatedir}/cache/mldonkey\"\n"\
"incoming_directory = \"%{_localstatedir}/lib/%{name}/incoming\"\n"\
%if 0%{?fedora}%{?el6}
"mldonkey_gui = \"%{_bindir}/mlgui\"\n"\
%endif
"mldonkey_bin = \"%{_bindir}/mldonkey\"\n"\
"log_file = \"%{_localstatedir}/log/mldonkey/mldonkey.log\"\n"\
> $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/downloads.ini

# Install sysconfig file
install -D -p -m 644 packages/rpm/mldonkey.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/mldonkey
sed -i 's,/var,%{_localstatedir},g' $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/mldonkey

# ed2k for konqueror support
install -p -m 755 distrib/ed2k_submit/mldonkey_submit $RPM_BUILD_ROOT%{_bindir}/mldonkey_submit
install -p -m 644 distrib/ed2k_submit/mldonkey $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/mldonkey_submit
sed -i 's,myusername,,;s,mypassword,,' $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/mldonkey_submit
install -D -p -m 644 distrib/ed2k_submit/ed2k.protocol  $RPM_BUILD_ROOT%{_datadir}/services/ed2k.protocol

# ed2k for mozilla support
# TODO should we unpack it into FF's plugins directory?
#install -D -p -m 644 distrib/ed2k_mozilla/mldonkey_protocol_handler-2.2.xpi $RPM_BUILD_ROOT%{_datadir}/%{name}/mldonkey_protocol_handler-2.2.xpi
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%pre server
/usr/sbin/useradd -r -d %{_localstatedir}/lib/%{name} \
                  -c "MlDonkey service" -s /bin/bash mldonkey 2>/dev/null || :


%post server
#if [ "$1" == "1" ]; then
#	/sbin/chkconfig --add mldonkey || :
#fi
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi



%preun server
#if [ "$1" == "0" ]; then
#	/sbin/service mldonkey stop >/dev/null 2>&1 || :
#	/sbin/chkconfig --del mldonkey || :
#fi
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable mldonkey.service > /dev/null 2>&1 || :
    /bin/systemctl stop mldonkey.service > /dev/null 2>&1 || :
fi

%postun server
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart mldonkey.service >/dev/null 2>&1 || :
fi

%triggerun -- mldonkey-server < 3.0.3-5
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply httpd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save mldonkey >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del mldonkey >/dev/null 2>&1 || :
/bin/systemctl try-restart mldonkey.service >/dev/null 2>&1 || :


%files
%defattr(-,root,root)
%doc Copying.txt distrib/Authors.txt distrib/Bugs.txt distrib/ChangeLog distrib/Developers.txt
%doc docs
%{_bindir}/mlnet
%{_bindir}/mldonkey_command
%{_bindir}/kill_mldonkey
%{_bindir}/copysources
%{_bindir}/get_range
%{_bindir}/mldonkey_make_torrent
%{_bindir}/mlbt
%{_bindir}/mld_hash
%{_bindir}/mldc
%{_bindir}/mlgnut
%{_bindir}/mldonkey
%{_bindir}/mlslsk
%{_bindir}/subconv
%{_bindir}/svg_converter


%if 0%{?fedora}%{?el6}
%files gui
%defattr(-,root,root)
%doc Copying.txt distrib/Authors.txt distrib/Bugs.txt distrib/ChangeLog distrib/Developers.txt
%{_bindir}/mlbt+gui
%{_bindir}/mldc+gui
%{_bindir}/mldonkey+gui
%{_bindir}/mldonkey_gui
%{_bindir}/mldonkey_previewer
%{_bindir}/mlgnut+gui
%{_bindir}/mlgui
%{_bindir}/mlguistarter
%{_bindir}/mlnet+gui
%{_bindir}/mlslsk+gui
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/16x16/apps/mldonkey.png
%{_datadir}/icons/hicolor/32x32/apps/mldonkey.png
%{_datadir}/icons/hicolor/48x48/apps/mldonkey.png
%{_datadir}/pixmaps/mldonkey.png
%endif


%files server
%defattr(-,root,root)
%doc Copying.txt
%config(noreplace) %{_sysconfdir}/sysconfig/mldonkey
%config(noreplace) %{_sysconfdir}/cron.d/mldonkey_df_monitor
#%%attr(755,root,root) %%{_initrddir}/mldonkey
%attr(755,root,root) %{_unitdir}/mldonkey.service
%config(noreplace) %{_sysconfdir}/logrotate.d/mldonkey
%{_sbindir}/mldonkey_df_monitor.sh
%attr(750,mldonkey,mldonkey) %dir %{_localstatedir}/log/mldonkey
%attr(750,mldonkey,mldonkey) %dir %{_localstatedir}/cache/mldonkey
%attr(750,mldonkey,mldonkey) %dir %{_localstatedir}/lib/mldonkey
%attr(755,mldonkey,mldonkey) %dir %{_localstatedir}/run/mldonkey
%attr(770,mldonkey,mldonkey) %dir %{_localstatedir}/lib/mldonkey/incoming
%config(noreplace) %{_localstatedir}/lib/mldonkey/downloads.ini


#%files -n mozilla-mldonkey-ed2k-support
#%defattr(-,root,root)
#%doc Copying.txt
#%{_datadir}/%{name}/mldonkey_protocol_handler-2.2.xpi


%files -n konqueror-mldonkey-ed2k-support
%defattr(-,root,root)
%doc Copying.txt distrib/ed2k_submit/README.MLdonkeySubmit
%config(noreplace) %{_sysconfdir}/sysconfig/mldonkey_submit
%{_bindir}/mldonkey_submit
%{_datadir}/services/ed2k.protocol


%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 3.1.5-3
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 3.1.5-2
- 为 Magic 3.0 重建

* Fri Oct 17 2014 Liu Di <liudidi@gmail.com> - 3.1.5-1
- 更新到 3.1.5

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 15 2012 Jon Ciesla <limburgher@gmail.com> - 3.0.3-5
- Migrate to systemd, BZ 789784.
- gcc47 patch.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 3.0.3-3
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 13 2010 Peter Lemenkov <lemenkov@gmail.com> 3.0.3-1
- Ver. 3.0.3
- Fixed rhbz #616128
- Fixed rhbz #589261 (forced log to syslog)

* Thu Aug 12 2010 Peter Lemenkov <lemenkov@gmail.com> 3.0.2-2
- Fixed rhbz #623627

* Fri Jun 11 2010 Peter Lemenkov <lemenkov@gmail.com> 3.0.2-1
- Ver. 3.0.2

* Mon Mar 15 2010 Peter Lemenkov <lemenkov@gmail.com> 3.0.1-2
- Disable probing for GUI libraries in EPEL
- Fixed DSO linking with newest GCC

* Tue Jan 26 2010 Peter Lemenkov <lemenkov@gmail.com> 3.0.1-1
- Ver. 3.0.1
- Greatly changed init-script
- Disabled GUI for EPEL

* Tue Sep 22 2009 Dennis Gilmore <dennis@ausil.us> - 3.0.0-3
- ExlcudeArch sparc64 s390 s390x since they dont have ocaml

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Mar 14 2009 Peter Lemenkov <lemenkov@gmail.com> 3.0.0-1
- Ver. 3.0.0
- Dropped patch1

* Thu Feb 26 2009 Richard W.M. Jones <rjones@redhat.com> - 2.9.7-4
- Fix remote arbitrary file disclosure via a GET request with more
  than one leading / (slash) character in the filename (rhbz#487132).

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Peter Lemenkov <lemenkov@gmail.com> 2.9.7-2
- Fixed bz# 484884

* Sun Feb  8 2009 Peter Lemenkov <lemenkov@gmail.com> 2.9.7-1
- Ver. 2.9.7

* Mon Jan 26 2009 Peter Lemenkov <lemenkov@gmail.com> 2.9.6-3
- Temporarily disable mozilla support

* Sat Dec  6 2008 Peter Lemenkov <lemenkov@gmail.com> 2.9.6-2
- Fixed installation of sysconfig-file

* Mon Aug 25 2008 Peter Lemenkov <lemenkov@gmail.com> 2.9.6-1
- Ver. 2.9.6

* Mon Jun 23 2008 Peter Lemenkov <lemenkov@gmail.com> 2.9.5-1
- Ver. 2.9.5

* Sun Jan 27 2008 Peter Lemenkov <lemenkov@gmail.com> 2.9.3-1
- Ver. 2.9.3

* Sun Jan 13 2008 Peter Lemenkov <lemenkov@gmail.com> 2.9.2-2
- Correct BR for perl modules
- More robust iconv usage
- Fixed desktop file
- Changed BR for scriplets

* Sun Nov  4 2007 Peter Lemenkov <lemenkov@gmail.com> 2.9.2-1
- Ver. 2.9.2
- BR ocaml >= 3.10.0
- BR lablgtk > 2.10.0

* Tue Sep 25 2007 Peter Lemenkov <lemenkov@gmail.com> 2.9.1-1
- Ver. 2.9.1
- converted two non-UTF8 text-files

* Sun Aug 19 2007 Peter Lemenkov <lemenkov@gmail.com> 2.9.0-2
- fixed License tag as required in Fedora

* Sun Aug  5 2007 Peter Lemenkov <lemenkov@gmail.com> 2.9.0-1
- Added shadow-utils as required
- Ver. 2.9.0
- Disabled Gnutella/G2 (unmaintained)
- Added BR file-devel (for libmagic)

* Wed Jun  6 2007 Peter Lemenkov <lemenkov@gmail.com> 2.8.7-1
- Ver. 2.8.7
- Added DC++ back

* Sun May 20 2007 Peter Lemenkov <lemenkov@gmail.com> 2.8.5-6
- Splitted ed2k-support to mozilla-mldonkey-ed2k-support and
  konqueror-mldonkey-ed2k-support

* Sun May 13 2007 Peter Lemenkov <lemenkov@gmail.com> 2.8.5-5
- Fixed bug #1421

* Sat May  5 2007 Peter Lemenkov <lemenkov@gmail.com> 2.8.5-4
- Fixed file conflicts
- Removed soulseek support (broken)

* Sat May  5 2007 Peter Lemenkov <lemenkov@gmail.com> 2.8.5-3
- Removed mysterious Requires kdelibs

* Fri May  4 2007 Peter Lemenkov <lemenkov@gmail.com> 2.8.5-2
- Added BR ncurses-devel

* Mon Apr 23 2007 Peter Lemenkov <lemenkov@gmail.com> 2.8.5-1
- version 2.8.5
- graphical stats disabled (temporarily?), see bug #1191
- mlchat removed from upstream

* Sun May 21 2006 Aurelien Bompard <gauret[AT]free.fr> 2.7.6-1
- version 2.7.6

* Mon Apr 17 2006 Aurelien Bompard <gauret[AT]free.fr> 2.7.5-1
- version 2.7.5

* Wed Mar 15 2006 Aurelien Bompard <gauret[AT]free.fr> 2.7.3-1
- version 2.7.3
- drop patch 0 & patch 1 (applied upstream)

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Fri Dec 02 2005 Aurelien Bompard <gauret[AT]free.fr> 2.7.0-0.lvn.2
- patch init script to add condrestart
- use condrestart in logrotate

* Sun Nov 20 2005 Aurelien Bompard <gauret[AT]free.fr> 2.7.0-0.lvn.1
- version 2.7.0
- fix logrotate file

* Mon Sep 05 2005 Aurelien Bompard <gauret[AT]free.fr> 2.6.4-0.lvn.1
- version 2.6.4

* Mon Aug 22 2005 Aurelien Bompard <gauret[AT]free.fr> 2.6.3-0.lvn.1
- version 2.6.3

* Thu Aug 11 2005 Aurelien Bompard <gauret[AT]free.fr> 2.6.2-0.lvn.1
- version 2.6.2

* Wed Aug 10 2005 Aurelien Bompard <gauret[AT]free.fr> 2.6.1-0.lvn.1
- version 2.6.1
- don't start initscript on boot by default

* Fri Jul 22 2005 Aurelien Bompard <gauret[AT]free.fr> 2.6.0-0.lvn.1
- update to 2.6.0
- drop explicit Epoch

* Mon Jun 27 2005 Aurelien Bompard <gauret[AT]free.fr> 0:2.5.30.16-0.lvn.1
- version 2.5.30.16
- add missing scriptlets requirements
- don't remove the mldonkey user on uninstall
- init script: sync with upstream
- sysconfig file: sync with upstream
- start script: sync with upstream

* Sun Feb 13 2005 Aurelien Bompard <gauret[AT]free.fr> 0:2.5.28-0.lvn.1
- version 2.5.28
- enable gui
- disable direct-connect (broken at the moment)

* Wed Aug 04 2004 Aurelien Bompard <gauret[AT]free.fr> 0:2.5.22-0.lvn.1
- version 2.5.22
- get ready for the new gui based on GTK2
  (upstream says "still a little buggy", and it does not build yet)

* Thu May 06 2004 Aurelien Bompard <gauret[AT]free.fr> 0:2.5.21-0.lvn.1
- version 2.5.21 (bugfix again...)

* Tue May 04 2004 Aurelien Bompard <gauret[AT]free.fr> 0:2.5.20-0.lvn.1
- version 2.5.20 (bugfix)

* Mon May 03 2004 Aurelien Bompard <gauret[AT]free.fr> 0:2.5.19-0.lvn.1
- version 2.5.19

* Sun Apr 25 2004 Aurelien Bompard <gauret[AT]free.fr> 0:2.5.18-0.lvn.1
- version 2.5.18

* Mon Mar 08 2004 Aurelien Bompard <gauret[AT]free.fr> 0:2.5.16-0.lvn.1
- update to version 2.5.16
- new subconv tool to convert movie subtitles

* Mon Mar 01 2004 Aurelien Bompard <gauret[AT]free.fr> 0:2.5.12-0.lvn.1
- Initial Fedora package, ported from Mandrake/PLF

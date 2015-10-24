#global checkout 20130722git65169c9
Name:           x2goserver
Version:        4.0.1.19
Release:        4%{?dist}
Summary:        X2Go Server
Summary(zh_CN.UTF-8): X2Go 服务器

Group:          Applications/Communications
Group(zh_CN.UTF-8): 应用程序/通信
License:        GPLv2+
URL:            http://www.x2go.org
Source0:        http://code.x2go.org/releases/source/%{name}/%{name}-%{version}.tar.gz
# git clone git://code.x2go.org/x2goserver
# cd x2goserver
# git archive --prefix=x2goserver-4.1.0.0-20130722git65169c9/ 65169c9d65b117802e50631be0bbd719163d969e | gzip > ../x2goserver-4.1.0.0-20130722git65169c9.tar.gz
#Source0:        %{name}/%{name}-%{version}-%{checkout}.tar.gz
Source1:        x2gocleansessions.service
Source2:        x2gocleansessions.init

Patch1:		x2goserver-4.0.1.19-magic.patch

BuildRequires:  desktop-file-utils
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  man2html-core
BuildRequires:  systemd
# So XSESSIONDIR gets linked
BuildRequires:  xorg-x11-xinit
# For x2goruncommand - for now
Requires:       bc
# For x2goshowblocks
Requires:       lsof
# For netstat in x2goresume-session
Requires:       net-tools
Requires:       openssh-server
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# We need a database
Requires:       perl(DBD::SQLite)
# For killall in x2gosuspend-session
Requires:       psmisc
# For x2godbadmin
Requires:       pwgen
# For printing, file-sharing
Requires:       sshfs
# For /etc/sudoers.d
Requires:       sudo
Requires:       x2goagent >= 3.5.0.25
Requires:       xorg-x11-fonts-misc
Requires:       xorg-x11-xauth
Requires(pre):  shadow-utils
Requires(post): grep
Requires(post): perl(DBD::SQLite)
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
# Provide upstream path from upstream rpms
# http://bugs.x2go.org/cgi-bin/bugreport.cgi?bug=755
Obsoletes:      x2goserver-extensions < %{version}-%{release}

%{?perl_default_filter}

%description
X2Go is a server based computing environment with
    - session resuming
    - low bandwidth support
    - session brokerage support
    - client side mass storage mounting support
    - audio support
    - authentication by smartcard and USB stick

This package contains the main daemon and tools for X2Go server-side session
administrations.


%description -l zh_CN.UTF-8
X 的远程服务.

%package fmbindings
Summary:        X2Go Server file manager bindings
Summary(zh_CN.UTF-8): %{name} 的文件管理组件
Requires:       %{name} = %{version}-%{release}
Requires:       xdg-utils
Group:          Applications/Communications
Group(zh_CN.UTF-8): 应用程序/通信

%description fmbindings
X2Go is a server based computing environment with
    - session resuming
    - low bandwidth support
    - session brokerage support
    - client side mass storage mounting support
    - audio support
    - authentication by smartcard and USB stick

This package contains generic MIME type information
for X2Go's local folder sharing. It can be used with all
freedesktop.org compliant desktop shells.

However, this package can be superseded by other, more specific
destkop binding components, if installed and being used with the
corresponding desktop shell:
    - under LXDE by x2golxdebindings
    - under GNOMEv2 by x2gognomebindings
    - under KDE4 by plasma-widget-x2go
    - under MATE by x2gomatebindings


%description fmbindings -l zh_CN.UTF-8
%{name} 的文件管理组件。

%package printing
Summary:        X2Go Server printing support
Summary(zh_CN.UTF-8): %{name} 的打印支持
Requires:       %{name} = %{version}-%{release}
Group:          Applications/Communications
Group(zh_CN.UTF-8): 应用程序/通信

%description printing
The X2Go Server printing package provides client-side printing support for
X2Go.

This package has to be installed on X2Go servers that shall be able to pass
X2Go print jobs on to the X2Go client.

This package co-operates with the cups-x2go CUPS backend. If CUPS server and
X2Go server are hosted on different machines, then make sure you install
this package on the X2Go server(s) (and the cups-x2go package on the CUPS
server).
%description printing -l zh_CN.UTF-8
%{name} 的打印支持。


%package xsession
Summary:        X2Go Server Xsession runner
Summary(zh_CN.UTF-8): %{name} 的 X 会话运行器
Requires:       %{name} = %{version}-%{release}
# Symlinks to xinit files
Requires:       xorg-x11-xinit
Group:          Applications/Communications
Group(zh_CN.UTF-8): 应用程序/通信

%description xsession
X2Go is a server based computing environment with
   - session resuming
   - low bandwidth support
   - session brokerage support
   - client side mass storage mounting support
   - audio support
   - authentication by smartcard and USB stick

This X2Go server add-on enables Xsession script handling
when starting desktop sessions with X2Go.

Amongst others the parsing of Xsession scripts will
enable desktop-profiles, ssh-agent startups, gpgagent
startups and many more Xsession related features on
X2Go session login automagically.

%description xsession -l zh_CN.UTF-8
%{name} 的 X 会话运行器。

%prep
%setup -q
%patch1 -p1

# Set path
find -type f | xargs sed -i -r -e '/^LIBDIR=/s,/lib/,/%{_lib}/,'
sed -i -e 's,/lib/,/%{_lib}/,' x2goserver/bin/x2gopath
sed -i -e 's/\t$(MAKE) -C x2goserver-compat/#\t$(MAKE) -C x2goserver-compat/g' Makefile
sed -i -e 's/\t$(MAKE) -C x2goserver-pyhoca/#\t$(MAKE) -C x2goserver-pyhoca/g' Makefile
# Don't try to be root
sed -i -e 's/-o root -g root//' */Makefile


%build
export PATH=%{_qt4_bindir}:$PATH
make CFLAGS="%{optflags} -fPIC" %{?_smp_mflags} PERL_INSTALLDIRS=vendor PREFIX=%{_prefix}


%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}

# Make symbolic link relative (xsession - disabled for now)
#rm %{buildroot}%{_sysconfdir}/x2go/Xresources
#ln -s ../X11/Xresources %{buildroot}%{_sysconfdir}/x2go/

# Remove placeholder files
rm %{buildroot}%{_libdir}/x2go/extensions/*.d/.placeholder

# x2gouser homedir, state dir
mkdir -p %{buildroot}%{_sharedstatedir}/x2go
# Create empty session file for %%ghost
touch %{buildroot}%{_sharedstatedir}/x2go/x2go_sessions

# Printing spool dir
mkdir -p %{buildroot}%{_localstatedir}/spool/x2goprint

# System.d session cleanup script
mkdir -p %{buildroot}%{_unitdir}
install -pm0644 %SOURCE1 %{buildroot}%{_unitdir}

desktop-file-validate %{buildroot}%{_datadir}/applications/x2gofm.desktop
chmod 440 %{buildroot}%{_sysconfdir}/sudoers.d/x2goserver

%pre
getent group x2gouser >/dev/null || groupadd -r x2gouser
getent passwd x2gouser >/dev/null || \
    useradd -r -g x2gouser -d /var/lib/x2go -s /sbin/nologin \
    -c "x2go" x2gouser
exit 0

%post
# Initialize the session database
[ ! -s %{_sharedstatedir}/x2go/x2go_sessions ] &&
  egrep "^backend=sqlite.*" /etc/x2go/x2gosql/sql >/dev/null 2>&1 &&
  %{_sbindir}/x2godbadmin --createdb >/dev/null 2>&1 || :

%systemd_post x2gocleansessions.service

%preun
%systemd_preun x2gocleansessions.service

%postun
%systemd_postun x2gocleansessions.service

%post fmbindings
touch --no-create %{_datadir}/mime/packages &> /dev/null || :
/usr/bin/update-desktop-database &>/dev/null || :

%postun fmbindings
/usr/bin/update-desktop-database &>/dev/null || :
if [ $1 -eq 0 ] ; then
        /bin/touch --no-create %{_datadir}/mime/packages &> /dev/null || :
        /usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
fi

%posttrans fmbindings
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :

%pre printing
getent group x2goprint >/dev/null || groupadd -r x2goprint
getent passwd x2goprint >/dev/null || \
    useradd -r -g x2goprint -d /var/spool/x2goprint -s /sbin/nologin \
    -c "x2go" x2goprint
exit 0


%files
%doc ChangeLog COPYING
%config(noreplace) %{_sysconfdir}/logcheck
%config(noreplace) %{_sysconfdir}/sudoers.d/x2goserver
%dir %{_sysconfdir}/x2go/
%config(noreplace) %{_sysconfdir}/x2go/x2go_logout
%config(noreplace) %{_sysconfdir}/x2go/x2go_logout.d/
%config(noreplace) %{_sysconfdir}/x2go/x2goagent.options
%config(noreplace) %{_sysconfdir}/x2go/x2goserver.conf
%config(noreplace) %{_sysconfdir}/x2go/x2gosql/
%{_bindir}/x2go*
%exclude %{_bindir}/x2gofm
%exclude %{_bindir}/x2goprint
%dir %{_libdir}/x2go
%{_libdir}/x2go/extensions
%{_libdir}/x2go/x2gosqlitewrapper.pl
%attr(02755,root,x2gouser) %{_libdir}/x2go/x2gosqlitewrapper
%{_libdir}/x2go/x2gochangestatus
%{_libdir}/x2go/x2gocreatesession
%{_libdir}/x2go/x2godbwrapper.pm
%{_libdir}/x2go/x2gogetagent
%{_libdir}/x2go/x2gogetagentstate
%{_libdir}/x2go/x2gogetdisplays
%{_libdir}/x2go/x2gogetports
%{_libdir}/x2go/x2gogetstatus
%{_libdir}/x2go/x2goinsertport
%{_libdir}/x2go/x2goinsertsession
%{_libdir}/x2go/x2golistsessions_sql
%{_libdir}/x2go/x2gologlevel
%{_libdir}/x2go/x2gologlevel.pm
%{_libdir}/x2go/x2goutils.pm
%{_libdir}/x2go/x2goresume
%{_libdir}/x2go/x2gormforward
%{_libdir}/x2go/x2gormport
%{_libdir}/x2go/x2gosuspend-agent
%{_libdir}/x2go/x2gosyslog
%{_sbindir}/x2go*
%{_mandir}/man5/x2go*.5*
%{_mandir}/man8/x2go*.8*
%exclude %{_mandir}/man8/x2gofm.8*
%exclude %{_mandir}/man8/x2goprint.8*
%dir %{_datadir}/x2go/
%dir %{_datadir}/x2go/versions
%{_datadir}/x2go/versions/VERSION.x2goserver
%{_datadir}/x2go/versions/VERSION.x2goserver-extensions
%dir %{_datadir}/x2go/x2gofeature.d
%{_datadir}/x2go/x2gofeature.d/x2goserver.features
%{_datadir}/x2go/x2gofeature.d/x2goserver-extensions.features
%attr(0775,root,x2gouser) %dir %{_sharedstatedir}/x2go/
%ghost %attr(0660,root,x2gouser) %{_sharedstatedir}/x2go/x2go_sessions
%{_unitdir}/x2gocleansessions.service

%files fmbindings
%{_bindir}/x2gofm
%{_datadir}/applications/x2gofm.desktop
%{_datadir}/mime/packages/sshfs-x2go.xml
%{_datadir}/x2go/versions/VERSION.x2goserver-fmbindings
%{_datadir}/x2go/x2gofeature.d/x2goserver-fmbindings.features
%{_mandir}/man8/x2gofm.8*

%files printing
%{_bindir}/x2goprint
%{_datadir}/x2go/versions/VERSION.x2goserver-printing
%{_datadir}/x2go/x2gofeature.d/x2goserver-printing.features
%attr(0700,x2goprint,x2goprint) %{_localstatedir}/spool/x2goprint
%{_mandir}/man8/x2goprint.8*

%files xsession
%{_sysconfdir}/x2go/xinitrc.d
%{_sysconfdir}/x2go/Xclients.d
%{_sysconfdir}/x2go/Xresources
%config(noreplace) %{_sysconfdir}/x2go/Xsession
%{_datadir}/x2go/x2gofeature.d/x2goserver-xsession.features
%{_datadir}/x2go/versions/VERSION.x2goserver-xsession


%changelog
* Wed Oct 21 2015 Liu Di <liudidi@gmail.com> - 4.0.1.19-4
- 为 Magic 3.0 重建

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 4.0.1.19-3
- 为 Magic 3.0 重建

* Sun Mar 01 2015 Liu Di <liudidi@gmail.com> - 4.0.1.19-2
- 为 Magic 3.0 重建

* Tue Feb 24 2015 Orion Poplawski <orion@cora.nwra.com> - 4.0.1.19-1
- Update to 4.0.1.19
- Drop Xsession and path patches fixed upstream

* Mon Jan 26 2015 Orion Poplawski <orion@cora.nwra.com> - 4.0.1.18-6
- Obsolete x2goserver-extensions to provide upgrade path from upstream rpms

* Thu Jan 8 2015 Orion Poplawski <orion@cora.nwra.com> - 4.0.1.18-5
- Fix local desktop sharing breakage (bug #1180303)

* Tue Dec 9 2014 Orion Poplawski <orion@cora.nwra.com> - 4.0.1.18-4
- Apply upstream fix for issue with Xsession aborting

* Fri Oct 24 2014 Orion Poplawski <orion@cora.nwra.com> - 4.0.1.18-3
- Do not require x2goserver-xession, do not ship feature file in main package

* Fri Oct 24 2014 Orion Poplawski <orion@cora.nwra.com> - 4.0.1.18-2
- Require x2goserver-xession

* Mon Oct 06 2014 Orion Poplawski <orion@cora.nwra.com> - 4.0.1.18-1
- Update to 4.0.1.18

* Fri Oct 03 2014 Orion Poplawski <orion@cora.nwra.com> - 4.0.1.17-1
- Update to 4.0.1.17



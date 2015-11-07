#global prerelease	rc1

## Fedora Extras specific customization below...
%bcond_without		fedora
%bcond_with		upstart
%bcond_without		systemd
%bcond_with		sysv
%bcond_without		tmpfiles
%bcond_without		unrar
%bcond_without		noarch
%bcond_without		bytecode
##

%global _hardened_build	1

%ifnarch s390 s390x
%global have_ocaml	1
%else
%global have_ocaml	0
%endif

%global username	clamupdate
%global homedir		%_var/lib/clamav
%global freshclamlog	%_var/log/freshclam.log
%global milteruser	clamilt
%global milterlog	%_var/log/clamav-milter.log
%global milterstatedir	%_var/run/clamav-milter
%global pkgdatadir	%_datadir/%name

%global scanuser	clamscan
%global scanstatedir	%_var/run/clamd.scan

%{?with_noarch:%global noarch	BuildArch:	noarch}
%{!?_unitdir:%global _unitdir /lib/systemd/system}
%{!?_initrddir:%global _initrddir /etc/rc.d/init.d}
%{!?release_func:%global release_func() %%{?prerelease:0.}%1%%{?prerelease:.%%prerelease}%%{?dist}}
%{!?apply:%global  apply(p:n:b:) %patch%%{-n:%%{-n*}} %%{-p:-p %%{-p*}} %%{-b:-b %%{-b*}} \
%nil}
%{!?systemd_reqs:%global systemd_reqs \
Requires(post):		 /bin/systemctl\
Requires(preun):	 /bin/systemctl\
Requires(postun):	 /bin/systemctl\
%nil}
%{!?systemd_install:%global systemd_install()\
%post %1\
%systemd_post %2 \
%preun %1\
%systemd_preun %2 \
%postun %1\
%systemd_postun_with_restart %2 \
%nil}


Summary:	End-user tools for the Clam Antivirus scanner
Name:		clamav
Version:	0.98.7
Release:	5%{?dist}
License:	%{?with_unrar:proprietary}%{!?with_unrar:GPLv2}
Group:		Applications/File
URL:		http://www.clamav.net
%if 0%{?with_unrar:1}
Source0:	http://download.sourceforge.net/sourceforge/clamav/%name-%version%{?prerelease}.tar.gz
%else
# Unfortunately, clamav includes support for RAR v3, derived from GPL
# incompatible unrar from RARlabs. We have to pull this code out.
# tarball was created by
#  make clean-sources NAME=clamav VERSION=<version> TARBALL=clamav-<version>.tar.gz TARBALL_CLEAN=clamav-<version>-norar.tar.xz
Source0:	%name-%version%{?prerelease}-norar.tar.xz
%endif
# To download the *.cvd, go to http://www.clamav.net and use the links
# there (I renamed the files to add the -version suffix for verifying).
Source10:	http://db.local.clamav.net/main-55.cvd
Source11:	http://db.local.clamav.net/daily-20394.cvd

Patch24:	clamav-0.92-private.patch
Patch26:	clamav-0.98.5-cliopts.patch
Patch27:	clamav-0.98-umask.patch
# https://bugzilla.redhat.com/attachment.cgi?id=403775&action=diff&context=patch&collapsed=&headers=1&format=raw
Patch29:	clamav-0.98.6-jitoff.patch
# https://llvm.org/viewvc/llvm-project/llvm/trunk/lib/ExecutionEngine/JIT/Intercept.cpp?r1=128086&r2=137567
Patch30:	llvm-glibc.patch
BuildRoot:	%_tmppath/%name-%version-%release-root
Requires:	clamav-lib = %version-%release
Requires:	data(clamav)
BuildRequires:	zlib-devel bzip2-devel gmp-devel curl-devel
BuildRequires:	ncurses-devel openssl-devel libxml2-devel
BuildRequires:	%_includedir/tcpd.h
%{?with_bytecode:BuildRequires:	bc tcl groff graphviz}
%if %{have_ocaml}
%{?with_bytecode:BuildRequires:	ocaml}
%endif

%package filesystem
Summary:	Filesystem structure for clamav
Group:		Applications/File
Provides:	user(%username)  = 4
Provides:	group(%username) = 4
# Prevent version mix
Conflicts:	%name < %version-%release
Conflicts:	%name > %version-%release
Requires(pre):  shadow-utils
%{?noarch}

%package lib
Summary:	Dynamic libraries for the Clam Antivirus scanner
Group:		System Environment/Libraries
Requires:	data(clamav)

%package devel
Summary:	Header files and libraries for the Clam Antivirus scanner
Group:		Development/Libraries
Source100:	clamd-gen
Requires:	clamav-lib        = %version-%release
Requires:	clamav-filesystem = %version-%release

%package data
Summary:	Virus signature data for the Clam Antivirus scanner
Group:		Applications/File
Requires(pre):		clamav-filesystem = %version-%release
Requires(postun):	clamav-filesystem = %version-%release
Provides:		data(clamav) = full
Conflicts:		data(clamav) < full
Conflicts:		data(clamav) > full
%{?noarch}

%package data-empty
Summary:	Empty data package for the Clam Antivirus scanner
Group:		Applications/File
Provides:	data(clamav) = empty
Conflicts:	data(clamav) < empty
Conflicts:	data(clamav) > empty
%{?noarch}

%package update
Summary:	Auto-updater for the Clam Antivirus scanner data-files
Group:		Applications/File
Source200:	freshclam-sleep
Source201:	freshclam.sysconfig
Source202:	clamav-update.crond
Source203:	clamav-update.logrotate
Requires:	clamav-filesystem = %version-%release
Requires:	crontabs
Requires(pre):		/etc/cron.d
Requires(postun):	/etc/cron.d
Requires(post):		%__chown %__chmod
Requires(post):		group(%username)

%package server
Summary:	Clam Antivirus scanner server
Group:		System Environment/Daemons
Source2:	clamd.sysconfig
Source3:	clamd.logrotate
Source5:	clamd-README
Source7:	clamd.SERVICE.init
Source8:	clamav-notify-servers
Requires:	data(clamav)
Requires:	clamav-filesystem = %version-%release
Requires:	clamav-lib        = %version-%release
Requires:	nc coreutils

%if 0%{?with_sysv:1}
%package server-sysvinit
Summary:	SysV initscripts for clamav server
Group:		System Environment/Daemons
Provides:	init(clamav-server) = sysv
Requires:	clamav-server = %version-%release
Requires(pre):		%_initrddir
Requires(postun):	%_initrddir
Provides:	clamav-server-sysv = %version-%release
Obsoletes:	clamav-server-sysv < %version-%release
Source520:	clamd-wrapper
%{?noarch}
%endif

%package server-systemd
Summary:	Systemd initscripts for clamav server
Group:		System Environment/Daemons
Provides:	init(clamav-server) = systemd
Requires:	clamav-server = %version-%release
Source530:	clamd@.service
%{?systemd_reqs}
%{?noarch}


%package scanner
Summary:	Clamav scanner daemon
Group:		System Environment/Daemons
Requires:	init(clamav-scanner)
Provides:	user(%scanuser)  = 49
Provides:	group(%scanuser) = 49
Requires:	clamav-server = %version-%release
%{?noarch}

# Remove me after EOL of RHEL5
%if 0%{?with_sysv:1}
%package scanner-sysvinit
Summary:	SysV initscripts for clamav scanner daemon
Group:		System Environment/Daemons
Provides:	init(clamav-scanner) = sysv
Requires:	clamav-server-sysvinit = %version-%release
Requires:	clamav-scanner = %version-%release
Requires(pre):		%_initrddir
Requires(postun):	%_initrddir initscripts
Requires(post):		chkconfig
Requires(preun):	chkconfig initscripts
%{?noarch}
%endif

# Remove me after EOL of RHEL6
%package scanner-upstart
Summary:	Upstart initscripts for clamav scanner daemon
Group:		System Environment/Daemons
Source410:	clamd.scan.upstart
Provides:	init(clamav-scanner) = upstart
Requires:	clamav-scanner = %version-%release
Requires(pre):		/etc/init
Requires(post):		/usr/bin/killall
Requires(preun):	/sbin/initctl
%{?noarch}

%package scanner-systemd
Summary:	Systemd initscripts for clamav scanner daemon
Group:		System Environment/Daemons
Source430:	clamd@scan.service
Provides:	init(clamav-scanner) = systemd
Requires:	clamav-scanner = %version-%release
Requires:	clamav-server-systemd = %version-%release
%{?systemd_reqs}
%{?noarch}

%package milter
Summary:	Milter module for the Clam Antivirus scanner
Group:		System Environment/Daemons
Source300:	README.fedora
Requires:	init(clamav-milter)
BuildRequires:	sendmail-devel
Provides:	user(%milteruser)  = 5
Provides:	group(%milteruser) = 5
Requires(post):	coreutils
Requires(pre):  shadow-utils

Provides:	milter(clamav) = sendmail
Provides:	milter(clamav) = postfix

Provides:	clamav-milter-core = %version-%release
Obsoletes:	clamav-milter-core < %version-%release
Provides:	clamav-milter-sendmail = %version-%release
Obsoletes:	clamav-milter-sendmail < %version-%release

# Remove me after EOL of RHEL5
%if 0%{?with_sysv:1}
%package milter-sysvinit
Summary:	SysV initscripts for the clamav sendmail-milter
Group:		System Environment/Daemons
Source320:	clamav-milter.sysv
Provides:	init(clamav-milter) = sysvinit
Requires:	clamav-milter = %version-%release
Requires(post):		user(%milteruser) clamav-milter
Requires(preun):	user(%milteruser) clamav-milter
Requires(pre):		%_initrddir
Requires(postun):	%_initrddir initscripts
Requires(post):		chkconfig
Requires(preun):	chkconfig initscripts
Provides:		clamav-milter-sysv = %version-%release
Obsoletes:		clamav-milter-sysv < %version-%release
%{?noarch}
%endif

# Remove me after EOL of RHEL6
%package milter-upstart
Summary:	Upstart initscripts for the clamav sendmail-milter
Group:		System Environment/Daemons
Source310:	clamav-milter.upstart
Provides:	init(clamav-milter) = upstart
Requires:	clamav-milter = %version-%release
Requires(pre):		/etc/init
Requires(post):		/usr/bin/killall
Requires(preun):	/sbin/initctl
%{?noarch}

%package milter-systemd
Summary:	Systemd initscripts for the clamav sendmail-milter
Group:		System Environment/Daemons
Source330:	clamav-milter.systemd
Provides:	init(clamav-milter) = systemd
Requires:	clamav-milter = %version-%release
%{?systemd_reqs}
%{?noarch}


%description
Clam AntiVirus is an anti-virus toolkit for UNIX. The main purpose of this
software is the integration with mail servers (attachment scanning). The
package provides a flexible and scalable multi-threaded daemon, a command
line scanner, and a tool for automatic updating via Internet. The programs
are based on a shared library distributed with the Clam AntiVirus package,
which you can use with your own software. The virus database is based on
the virus database from OpenAntiVirus, but contains additional signatures
(including signatures for popular polymorphic viruses, too) and is KEPT UP
TO DATE.

%description filesystem
This package provides the filesystem structure and contains the
user-creation scripts required by clamav.

%description lib
This package contains dynamic libraries shared between applications
using the Clam Antivirus scanner.

%description devel
This package contains headerfiles and libraries which are needed to
build applications using clamav.

%description data
This package contains the virus-database needed by clamav. This
database should be updated regularly; the 'clamav-update' package
ships a corresponding cron-job. This package and the
'clamav-data-empty' package are mutually exclusive.

Use -data when you want a working (but perhaps outdated) virus scanner
immediately after package installation.

Use -data-empty when you are updating the virus database regulary and
do not want to download a >5MB sized rpm-package with outdated virus
definitions.


%description data-empty
This is an empty package to fulfill inter-package dependencies of the
clamav suite. This package and the 'clamav-data' package are mutually
exclusive.

Use -data when you want a working (but perhaps outdated) virus scanner
immediately after package installation.

Use -data-empty when you are updating the virus database regulary and
do not want to download a >5MB sized rpm-package with outdated virus
definitions.


%description update
This package contains programs which can be used to update the clamav
anti-virus database automatically. It uses the freshclam(1) utility for
this task. To activate it, uncomment the entry in /etc/cron.d/clamav-update.

%description server
ATTENTION: most users do not need this package; the main package has
everything (or depends on it) which is needed to scan for virii on
workstations.

This package contains files which are needed to execute the clamd-daemon.
This daemon does not provide a system-wide service. Instead of, an instance
of this daemon should be started for each service requiring it.

See the README file how this can be done with a minimum of effort.


%if 0%{?with_sysv:1}
%description server-sysvinit
SysV initscripts template for the clamav server
%endif

%description server-systemd
Systemd template for the clamav server


%description scanner
This package contains a generic system wide clamd service which is
e.g. used by the clamav-milter package.

%if 0%{?with_sysv:1}
%description scanner-sysvinit
The SysV initscripts for clamav-scanner.
%endif

%description scanner-upstart
The Upstart initscripts for clamav-scanner.

%description scanner-systemd
The systemd initscripts for clamav-scanner.


%description milter
This package contains files which are needed to run the clamav-milter.

%if 0%{?with_sysv:1}
%description milter-sysvinit
The SysV initscripts for clamav-milter.
%endif

%description milter-upstart
The Upstart initscripts for clamav-milter.

%description milter-systemd
The systemd initscripts for clamav-scanner.

## ------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}%{?prerelease}

%apply -n24 -p1 -b .private
%apply -n26 -p1 -b .cliopts
%apply -n27 -p1 -b .umask
%apply -n29 -p1 -b .jitoff
%apply -n30 -p1
%{?apply_end}

install -p -m0644 %SOURCE300 clamav-milter/

mkdir -p libclamunrar{,_iface}
%{!?with_unrar:touch libclamunrar/{Makefile.in,all,install}}

sed -ri \
    -e 's!^#?(LogFile ).*!#\1/var/log/clamd.<SERVICE>!g' \
    -e 's!^#?(LocalSocket ).*!#\1/var/run/clamd.<SERVICE>/clamd.sock!g' \
    -e 's!^(#?PidFile ).*!\1/var/run/clamd.<SERVICE>/clamd.pid!g' \
    -e 's!^#?(User ).*!\1<USER>!g' \
    -e 's!^#?(AllowSupplementaryGroups|LogSyslog).*!\1 yes!g' \
    -e 's! /usr/local/share/clamav,! %homedir,!g' \
    etc/clamd.conf.sample

sed -ri \
    -e 's!^#?(UpdateLogFile )!#\1!g;' \
    -e 's!^#?(LogSyslog).*!\1 yes!g' \
    -e 's!(DatabaseOwner *)clamav$!\1%username!g' etc/freshclam.conf.sample


## ------------------------------------------------------------

%build
CFLAGS="$RPM_OPT_FLAGS -Wall -W -Wmissing-prototypes -Wmissing-declarations -std=gnu99"
export LDFLAGS='-Wl,--as-needed'
# HACK: remove me...
export FRESHCLAM_LIBS='-lz'
# IPv6 check is buggy and does not work when there are no IPv6 interface on build machine
export have_cv_ipv6=yes
%configure \
	--disable-static \
	--disable-rpath \
	--disable-silent-rules \
	--disable-clamav \
	--with-user=%username \
	--with-group=%username \
	--with-libcurl=%{_prefix} \
	--with-dbdir=/var/lib/clamav \
	--enable-milter \
	--enable-clamdtop \
	%{!?with_bytecode:--disable-llvm} \
	%{!?with_unrar:--disable-unrar}

# TODO: check periodically that CLAMAVUSER is used for freshclam only


# build with --as-needed and disable rpath
sed -i \
	-e 's! -shared ! -Wl,--as-needed\0!g'					\
	-e '/sys_lib_dlsearch_path_spec=\"\/lib \/usr\/lib /s!\"\/lib \/usr\/lib !/\"/%_lib /usr/%_lib !g'	\
	libtool


make %{?_smp_mflags}


## ------------------------------------------------------------

%install
rm -rf "$RPM_BUILD_ROOT" _doc*
make DESTDIR="$RPM_BUILD_ROOT" install

function smartsubst() {
	local tmp
	local regexp=$1
	shift

	tmp=$(mktemp /tmp/%name-subst.XXXXXX)
	for i; do
		sed -e "$regexp" "$i" >$tmp
		cmp -s $tmp "$i" || cat $tmp >"$i"
		rm -f $tmp
	done
}


install -d -m 0755 \
	$RPM_BUILD_ROOT%_sysconfdir/{mail,clamd.d,logrotate.d} \
	$RPM_BUILD_ROOT%_tmpfilesdir \
	$RPM_BUILD_ROOT%_var/{log,run} \
	$RPM_BUILD_ROOT%milterstatedir \
	$RPM_BUILD_ROOT%pkgdatadir/template \
	$RPM_BUILD_ROOT%_initrddir \
	$RPM_BUILD_ROOT%homedir \
	$RPM_BUILD_ROOT%scanstatedir

rm -f	$RPM_BUILD_ROOT%_sysconfdir/clamd.conf.sample \
	$RPM_BUILD_ROOT%_libdir/*.la


touch $RPM_BUILD_ROOT%homedir/daily.cld
touch $RPM_BUILD_ROOT%homedir/main.cld

install -D -m 0644 -p %SOURCE10		$RPM_BUILD_ROOT%homedir/main.cvd
install -D -m 0644 -p %SOURCE11		$RPM_BUILD_ROOT%homedir/daily.cvd

## prepare the server-files
install -D -m 0644 -p %SOURCE2		_doc_server/clamd.sysconfig
install -D -m 0644 -p %SOURCE3		_doc_server/clamd.logrotate
%if 0%{?with_sysv:1}
install -D -m 0755 -p %SOURCE7		_doc_server/clamd.init
%endif
install -D -m 0644 -p %SOURCE5		_doc_server/README
install -D -m 0644 -p etc/clamd.conf.sample	_doc_server/clamd.conf

%if 0%{?with_sysv:1}
install -m 0644 -p %SOURCE520		$RPM_BUILD_ROOT%pkgdatadir/
%endif
install -m 0755 -p %SOURCE100		$RPM_BUILD_ROOT%pkgdatadir/
cp -pa _doc_server/*			$RPM_BUILD_ROOT%pkgdatadir/template

%if 0%{?with_sysv:1}
smartsubst 's!/usr/share/clamav!%pkgdatadir!g' $RPM_BUILD_ROOT%pkgdatadir/clamd-wrapper
%endif
install -D -p -m 0644 %SOURCE530        $RPM_BUILD_ROOT%_unitdir/clamd@.service


## prepare the update-files
install -D -m 0644 -p %SOURCE203	$RPM_BUILD_ROOT%_sysconfdir/logrotate.d/clamav-update
install -D -m 0755 -p %SOURCE8		$RPM_BUILD_ROOT%_sbindir/clamav-notify-servers
touch $RPM_BUILD_ROOT%freshclamlog

install -D -p -m 0755 %SOURCE200	$RPM_BUILD_ROOT%pkgdatadir/freshclam-sleep
install -D -p -m 0644 %SOURCE201	$RPM_BUILD_ROOT%_sysconfdir/sysconfig/freshclam
install -D -p -m 0600 %SOURCE202	$RPM_BUILD_ROOT%_sysconfdir/cron.d/clamav-update
mv -f $RPM_BUILD_ROOT%_sysconfdir/freshclam.conf{.sample,}

smartsubst 's!webmaster,clamav!webmaster,%username!g;
	    s!/usr/share/clamav!%pkgdatadir!g;
	    s!/usr/bin!%_bindir!g;
            s!/usr/sbin!%_sbindir!g;' \
   $RPM_BUILD_ROOT%_sysconfdir/cron.d/clamav-update \
   $RPM_BUILD_ROOT%pkgdatadir/freshclam-sleep


### The scanner stuff
sed -e 's!<SERVICE>!scan!g;s!<USER>!%scanuser!g' \
    etc/clamd.conf.sample > $RPM_BUILD_ROOT%_sysconfdir/clamd.d/scan.conf

%if 0%{?with_sysv:1}
sed -e 's!<SERVICE>!scan!g;' $RPM_BUILD_ROOT%pkgdatadir/template/clamd.init \
    > $RPM_BUILD_ROOT%_initrddir/clamd.scan
%endif

install -D -p -m 0644 %SOURCE410 $RPM_BUILD_ROOT%_sysconfdir/init/clamd.scan.conf
install -D -p -m 0644 %SOURCE430 $RPM_BUILD_ROOT%_unitdir/clamd@scan.service

cat << EOF > $RPM_BUILD_ROOT%_tmpfilesdir/clamd.scan.conf
d %scanstatedir 0710 %scanuser %scanuser
EOF

touch $RPM_BUILD_ROOT%scanstatedir/clamd.{sock,pid}


### The milter stuff
sed -r \
    -e 's!^#?(User).*!\1 %milteruser!g' \
    -e 's!^#?(AllowSupplementaryGroups|LogSyslog) .*!\1 yes!g' \
    -e 's! /tmp/clamav-milter.socket! %milterstatedir/clamav-milter.socket!g' \
    -e 's! /var/run/clamav-milter.pid! %milterstatedir/clamav-milter.pid!g' \
    -e 's! /tmp/clamav-milter.log! %milterlog!g' \
    etc/clamav-milter.conf.sample > $RPM_BUILD_ROOT%_sysconfdir/mail/clamav-milter.conf

install -D -p -m 0644 %SOURCE310 $RPM_BUILD_ROOT%_sysconfdir/init/clamav-milter.conf
%if 0%{?with_sysv:1}
install -D -p -m 0755 %SOURCE320 $RPM_BUILD_ROOT%_initrddir/clamav-milter
%endif
install -D -p -m 0644 %SOURCE330 $RPM_BUILD_ROOT%_unitdir/clamav-milter.service

cat << EOF > $RPM_BUILD_ROOT%_tmpfilesdir/clamav-milter.conf
d %milterstatedir 0710 %milteruser %milteruser
EOF

rm -f $RPM_BUILD_ROOT%_sysconfdir/clamav-milter.conf.sample
touch $RPM_BUILD_ROOT{%milterstatedir/clamav-milter.{socket,pid},%milterlog}

%{!?with_upstart:  rm -rf $RPM_BUILD_ROOT%_sysconfdir/init}
%{!?with_systemd:  rm -rf $RPM_BUILD_ROOT%_unitdir}
%{!?with_sysv:     rm -f  $RPM_BUILD_ROOT%_initrddir/*}
%{!?with_sysv:     rm -rf $RPM_BUILD_ROOT%_var/run/*/*.pid}
%{!?with_tmpfiles: rm -rf $RPM_BUILD_ROOT%_tmpfilesdir}

%if 0%{?with_sysv:1}
# keep clamd-wrapper in every case because it might be needed by other
# packages
ln -s %pkgdatadir/clamd-wrapper		$RPM_BUILD_ROOT%_initrddir/clamd-wrapper
%endif

## ------------------------------------------------------------

%check
make check

## ------------------------------------------------------------

%clean
rm -rf "$RPM_BUILD_ROOT"

## ------------------------------------------------------------

%pre filesystem
getent group %{username} >/dev/null || groupadd -r %{username}
getent passwd %{username} >/dev/null || \
    useradd -r -g %{username} -d %{homedir} -s /sbin/nologin \
    -c "Clamav database update user" %{username}
exit 0


%pre scanner
getent group %{scanuser} >/dev/null || groupadd -r %{scanuser}
getent passwd %{scanuser} >/dev/null || \
    useradd -r -g %{scanuser} -d / -s /sbin/nologin \
    -c "Clamav scanner user" %{scanuser}
exit 0


%{?with_tmpfiles:
%post scanner
%{?with_systemd:/bin/systemd-tmpfiles --create %_tmpfilesdir/clamd.scan.conf || :}}


%post server-systemd
test "$1" != "1" || /bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun server-systemd
/bin/systemctl daemon-reload >/dev/null 2>&1 || :


%if 0%{?with_sysv:1}
%post scanner-sysvinit
/sbin/chkconfig --add clamd.scan

%preun scanner-sysvinit
test "$1" != 0 || %_initrddir/clamd.scan stop &>/dev/null || :
test "$1" != 0 || /sbin/chkconfig --del clamd.scan

%postun scanner-sysvinit
test "$1"  = 0 || %_initrddir/clamd.scan condrestart >/dev/null || :
%endif


%post scanner-upstart
/usr/bin/killall -u %scanuser clamd 2>/dev/null || :

%preun scanner-upstart
test "$1" != "0" || /sbin/initctl -q stop clamd.scan || :


%systemd_install scanner-systemd clamd@scan.service


%post update
test -e %freshclamlog || {
	touch %freshclamlog
	%__chmod 0664 %freshclamlog
	%__chown root:%username %freshclamlog
	! test -x /sbin/restorecon || /sbin/restorecon %freshclamlog
}

%triggerin update -- %name-update < 0.97.3-1704
# remove me after F19
! test -x /sbin/restorecon || /sbin/restorecon %freshclamlog &>/dev/null || :


%triggerin milter -- clamav-scanner
# Add the milteruser to the scanuser group; this is required when
# milter and clamd communicate through local sockets
/usr/sbin/groupmems -g %scanuser -a %milteruser &>/dev/null || :

%pre milter
getent group %{milteruser} >/dev/null || groupadd -r %{milteruser}
getent passwd %{milteruser} >/dev/null || \
    useradd -r -g %{milteruser} -d %{milterstatedir} -s /sbin/nologin \
    -c "Clamav Milter user" %{milteruser}
exit 0


%post milter
test -e %milterlog || {
	touch %milterlog
	chmod 0620             %milterlog
	chown root:%milteruser %milterlog
	! test -x /sbin/restorecon || /sbin/restorecon %milterlog
}
%{?with_systemd:/bin/systemd-tmpfiles --create %_tmpfilesdir/clamav-milter.conf || :}


%triggerin milter -- %name-milter < 0.97.3-1704
# remove me after F19
! test -x /sbin/restorecon || /sbin/restorecon %milterlog &>/dev/null || :


%if 0%{?with_sysv:1}
%post milter-sysvinit
/sbin/chkconfig --add clamav-milter

%preun milter-sysvinit
test "$1" != 0 || %_initrddir/clamav-milter stop &>/dev/null || :
test "$1" != 0 || /sbin/chkconfig --del clamav-milter

%postun milter-sysvinit
test "$1"  = 0 || %_initrddir/clamav-milter condrestart >/dev/null || :
%endif


%post milter-upstart
/usr/bin/killall -u %milteruser clamav-milter 2>/dev/null || :

%preun milter-upstart
test "$1" != "0" || /sbin/initctl -q stop clamav-milter || :


%systemd_install milter-systemd clamav-milter.service


%post   lib -p /sbin/ldconfig
%postun lib -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS BUGS COPYING ChangeLog FAQ NEWS README UPGRADE
%doc docs/*.pdf
%_bindir/*
%_mandir/man[15]/*
%exclude %_bindir/clamav-config
%exclude %_bindir/freshclam
%exclude %_mandir/*/freshclam*

## -----------------------

%files lib
%defattr(-,root,root,-)
%_libdir/*.so.*

## -----------------------

%files devel
%defattr(-,root,root,-)
%_includedir/*
%_libdir/*.so
%pkgdatadir/template
%pkgdatadir/clamd-gen
%_libdir/pkgconfig/*
%_bindir/clamav-config

## -----------------------

%files filesystem
%attr(-,%username,%username) %dir %homedir
%attr(-,root,root)           %dir %pkgdatadir

## -----------------------

%files data
%defattr(-,%username,%username,-)
# use %%config to keep files which were updated by 'freshclam'
# already. Without this tag, they would be overridden with older
# versions whenever a new -data package is installed.
%config %verify(not size md5 mtime) %homedir/*.cvd


%files data-empty
%defattr(-,%username,%username,-)
%ghost %attr(0664,%username,%username) %homedir/*.cvd


## -----------------------

%files update
%defattr(-,root,root,-)
%_bindir/freshclam
%_mandir/*/freshclam*
%pkgdatadir/freshclam-sleep
%config(noreplace) %verify(not mtime)    %_sysconfdir/freshclam.conf
%config(noreplace) %verify(not mtime)    %_sysconfdir/logrotate.d/*
%config(noreplace) %_sysconfdir/cron.d/clamav-update
%config(noreplace) %_sysconfdir/sysconfig/freshclam

%ghost %attr(0664,root,%username) %verify(not size md5 mtime) %freshclamlog
%ghost %attr(0664,%username,%username) %homedir/*.cld


## -----------------------

%files server
%defattr(-,root,root,-)
%doc _doc_server/*
%_mandir/man[58]/clamd*
%_sbindir/*
%dir %_sysconfdir/clamd.d

%exclude %_sbindir/*milter*
%exclude %_mandir/man8/clamav-milter*


%if 0%{?with_sysv:1}
%files server-sysvinit
%defattr(-,root,root,-)
%_initrddir/clamd-wrapper
%pkgdatadir/clamd-wrapper
%endif

%if 0%{?with_systemd:1}
%files server-systemd
 %defattr(-,root,root,-)
 %_unitdir/clamd@.service
%endif

## -----------------------

%files scanner
%defattr(-,root,root,-)
%config(noreplace) %_sysconfdir/clamd.d/scan.conf
%ghost %scanstatedir/clamd.sock

%if 0%{?with_tmpfiles:1}
  %_tmpfilesdir/clamd.scan.conf
  %ghost %dir %attr(0710,%scanuser,%scanuser) %scanstatedir
%else
  %dir %attr(0710,%scanuser,%scanuser) %scanstatedir
%endif

%if 0%{?with_sysv:1}
%files scanner-sysvinit
  %attr(0755,root,root) %config %_initrddir/clamd.scan
  %ghost %scanstatedir/clamd.pid
%endif

%if 0%{?with_upstart:1}
%files scanner-upstart
  %defattr(-,root,root,-)
  %config(noreplace) %_sysconfdir/init/clamd.scan*
%endif

%if 0%{?with_systemd:1}
%files scanner-systemd
  %defattr(-,root,root,-)
  %_unitdir/clamd@scan.service
%endif

## -----------------------

%files milter
%defattr(-,root,root,-)
%doc clamav-milter/README.fedora
%_sbindir/*milter*
%_mandir/man8/clamav-milter*
%config(noreplace) %_sysconfdir/mail/clamav-milter.conf
%ghost %attr(0620,root,%milteruser) %verify(not size md5 mtime) %milterlog
%ghost %milterstatedir/clamav-milter.socket

%if 0%{?with_tmpfiles:1}
  %_tmpfilesdir/clamav-milter.conf
  %ghost %dir %attr(0710,%milteruser,%milteruser) %milterstatedir
%else
  %dir %attr(0710,%milteruser,%milteruser) %milterstatedir
%endif

%if 0%{?with_sysv:1}
%files milter-sysvinit
  %defattr(-,root,root,-)
  %config %_initrddir/clamav-milter
  %ghost %milterstatedir/clamav-milter.pid
%endif

%if 0%{?with_upstart:1}
%files milter-upstart
  %defattr(-,root,root,-)
  %config(noreplace) %_sysconfdir/init/clamav-milter*
%endif

%if 0%{?with_systemd:1}
%files milter-systemd
  %defattr(-,root,root,-)
  %_unitdir/clamav-milter.service
%endif


%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.98.7-5
- 为 Magic 3.0 重建

* Fri Sep 18 2015 Liu Di <liudidi@gmail.com> - 0.98.7-4
- 为 Magic 3.0 重建

* Tue Jun 30 2015 Robert Scheck <robert@fedoraproject.org> - 0.98.7-3
- Move /etc/tmpfiles.d/ to /usr/lib/tmpfiles.d/ (#1126595)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Robert Scheck <robert@fedoraproject.org> - 0.98.7-1
- Upgrade to 0.98.7 and updated daily.cvd (#1217014)

* Tue Mar 10 2015 Adam Jackson <ajax@redhat.com> 0.98.6-2
- Drop sysvinit subpackages in F23+

* Thu Jan 29 2015 Robert Scheck <robert@fedoraproject.org> - 0.98.6-1
- Upgrade to 0.98.6 and updated daily.cvd (#1187050)

* Wed Nov 19 2014 Robert Scheck <robert@fedoraproject.org> - 0.98.5-2
- Corrected summary of clamav-server-systemd package (#1165672)

* Wed Nov 19 2014 Robert Scheck <robert@fedoraproject.org> - 0.98.5-1
- Upgrade to 0.98.5 and updated daily.cvd (#1138101)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 21 2014 Robert Scheck <robert@fedoraproject.org> - 0.98.4-1
- Upgrade to 0.98.4 and updated daily.cvd (#1111811)
- Add build requirement to libxml2 for DMG, OpenIOC and XAR

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 10 2014 Robert Scheck <robert@fedoraproject.org> - 0.98.3-1
- Upgrade to 0.98.3 and updated daily.cvd (#1095614)
- Avoid automatic path detection breakage regarding curl
- Added build requirement to openssl-devel for hasing code
- Added clamsubmit to main package

* Wed Jan 15 2014 Robert Scheck <robert@fedoraproject.org> - 0.98.1-1
- Upgrade to 0.98.1 and updated daily.cvd (#1053400)

* Wed Oct 09 2013 Dan Horák <dan[at]danny.cz> - 0.98-2
- Use fanotify from glibc instead of the limited hand-crafted version

* Sun Oct 06 2013 Robert Scheck <robert@fedoraproject.org> - 0.98-1
- Upgrade to 0.98 and updated main.cvd and daily.cvd (#1010168)

* Wed Aug 07 2013 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.97.8-4
- Add a missing requirement on crontabs to spec file
- Fix RHBZ#988605

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 2 2013 Nick Bebout <nb@fedoraproject.org> - 0.97.8-1
- Update to 0.97.8

* Wed Apr 10 2013 Jon Ciesla <limburgher@gmail.com> - 0.97.7-2
- Migrate from fedora-usermgmt to guideline scriptlets.

* Sat Mar 23 2013 Nick Bebout <nb@fedoraproject.org> - 0.97.7-1
- Update to 0.97.7

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97.6-1901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Sep 22 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.6-1900
- updated to 0.97.6
- use %%systemd macros

* Tue Aug 14 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.5-1900
- disabled upstart support

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97.5-1801
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.5-1800
- updated to 0.97.5
- CVE-2012-1457: allows to bypass malware detection via a TAR archive
  entry with a length field that exceeds the total TAR file size
- CVE-2012-1458: allows to bypass malware detection via a crafted
  reset interval in the LZXC header of a CHM file
- CVE-2012-1459: allows to bypass malware detection via a TAR archive
  entry with a length field corresponding to that entire entry, plus
  part of the header of the next entry
- ship local copy of virus database; it was removed by accident from
  0.97.5 tarball
- removed sysv compat stuff

* Fri Apr 13 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.4-1801
- build with -fPIE

* Fri Mar 16 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.4-1800
- updated to 0.97.4

* Sun Feb  5 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.3-1703
- fixed SELinux restorecon invocation
- added trigger to fix SELinux contexts of logfiles created by old
  packages
- fixed build with recent gcc/glibc toolchain

* Sat Jan 21 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.3-1703
- rewrote clamav-notify-servers to be init system neutral
- set PrivateTmp systemd option (#782488)

* Sun Jan  8 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.3-1702
- set correct SELinux context for logfiles generated in %%post (#754555)
- create systemd tmpfiles in %%post
- created -server-systemd subpackage providing a clamd@.service template
- made script in -scanner-systemd an instance of clamd@.service

* Tue Oct 18 2011 Nick Bebout <nb@fedoraproject.org> - 0.97.3-1700
- updated to 0.97.3
- CVE-2011-3627 clamav: Recursion level crash fixed in v0.97.3

* Thu Aug  4 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.2-1700
- moved sysv wrapper script into -sysv subpackage
- start systemd services after network.target and nss-lookup.target

* Tue Jul 26 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.2-1600
- updated to 0.97.2
- CVE-2011-2721 Off-by-one error by scanning message hashes (#725694)
- fixed systemd scripts and their installation

* Thu Jun  9 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.1-1600
- updated to 0.97.1
- fixed Requires(preun) vs. Requires(postun) inconsistency

* Sat Apr 23 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97-1601
- fixed tmpfiles.d syntax (#696812)

* Sun Feb 20 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97-1600
- updated to 0.97
- rediffed some patches

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96.5-1503
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan  8 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96.5-1502
- fixed signal specifier in clamd-wrapper (#668131, James Ralston)

* Fri Dec 24 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96.5-1501
- added systemd init scripts which obsolete to old sysvinit ones
- added tmpfiles.d/ descriptions

* Sat Dec  4 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96.5-1500
- updated to 0.96.5
- CVE-2010-4260 Multiple errors within the processing of PDF files can
  be exploited to e.g. cause a crash.
- CVE-2010-4261 An off-by-one error within the "icon_cb()" function
  can be exploited to cause a memory corruption.

* Sun Oct 31 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96.4-1500
- updated to 0.96.4
- execute 'make check' (#640347) but ignore errors for now because
  four checks are failing on f13

* Wed Sep 29 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96.3-1501
- lowered stop priority of sysv initscripts (#629435)

* Wed Sep 22 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96.3-1500
- updated to 0.96.3
- fixes CVE-2010-0405 in shipped bzlib.c copy

* Sun Aug 15 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96.2-1500
- updated to 0.96.2
- rediffed patches
- removed the -jit-disable patch which is replaced upstream by a more
  detailed configuration option.

* Wed Aug 11 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de>
- removed old %%trigger which renamed the 'clamav' user- and groupnames
  to 'clamupdate'
- use 'groupmems', not 'usermod' to add a user to a group because
  'usermod' does not work when user does not exist in local /etc/passwd

* Tue Jul 13 2010 Dan Horák <dan[at]danny.cz> - 0.96.1-1401
- ocaml not available (at least) on s390(x)

* Tue Jun  1 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96.1-1400
- updated to 0.96.1
- rediffed patches

* Sat May 29 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 0.96.1403
- CVE-2010-1639 Clam AntiVirus: Heap-based overflow, when processing malicious PDF file(s)

* Wed Apr 21 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96-1402
- updated to final 0.96
- applied upstream patch which allows to disable JIT compiler (#573191)
- build JIT compiler again
- disabled JIT compiler by default
- removed explicit 'pkgconfig' requirements in -devel (#533956)

* Sat Mar 20 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96-0.1401.rc1
- do not build the bytecode JIT compiler for now until it can be disabled
  at runtime (#573191)

* Thu Mar 11 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96-1400.rc1
- updated to 0.96rc1
- added some BRs

* Sun Dec  6 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.95.3-1301
- updated -upstart to upstart 0.6.3

* Sat Nov 21 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de>
- adjusted chkconfig positions for clamav-milter (#530101)
- use %%apply instead of %%patch

* Thu Oct 29 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.95.3-1300
- updated to 0.95.3

* Sun Sep 13 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de>
- conditionalized build of noarch subpackages to ease packaging under RHEL5

* Sun Aug  9 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.95.2-5
- modified freshclam configuration to log by syslog by default
- disabled LocalSocket option in sample configuration
- fixed clamav-milter sysv initscript to use bash interpreter and to
  be disabled by default

* Sat Aug  8 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.95.2-4
- renamed 'clamav' user/group to 'clamupdate'
- add the '%milteruser' user to the '%scanuser' group when the -scanner
  subpackage is installed

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 11 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.95.2-1
- updated to 0.95.2

* Sun Apr 19 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.95.1-3
- fixed '--without upstart' operation

* Wed Apr 15 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.95.1-2
- added '%%bcond_without upstart' conditional to ease skipping of
  -upstart subpackage creation e.g. on EL5 systems
- fixed Provides/Obsoletes: typo in -milter-sysvinit subpackage which
  broke update path

* Fri Apr 10 2009 Robert Scheck <robert@fedoraproject.org> - 0.95.1-1
- Upgrade to 0.95.1 (#495039)

* Wed Mar 25 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.95-1
- updated to final 0.95
- added ncurses-devel (-> clamdtop) BR
- enforced IPv6 support

* Sun Mar  8 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.95-0.1.rc1
- updated to 0.95rc1
- added -upstart subpackages
- renamed -sysv to -sysvinit to make -upstart win the default dep resolving
- reworked complete milter stuff
- added -scanner subpackage which contains a preconfigured daemon
  (e.g. for use by -milter)
- moved %%changelog entries from 2006 and before into ChangeLog-rpm.old

* Wed Feb 25 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.94.2-3
- made some subpackages noarch
- fixed typo in SysV initscript which removes 'touch' file (#473513)

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.94.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 02 2008 Robert Scheck <robert@fedoraproject.org> - 0.94.2-1
- Upgrade to 0.94.2 (#474002)

* Wed Nov 05 2008 Robert Scheck <robert@fedoraproject.org> - 0.94.1-1
- Upgrade to 0.94.1

* Sun Oct 26 2008 Robert Scheck <robert@fedoraproject.org> - 0.94-1
- Upgrade to 0.94 (SECURITY), fixes #461461:
- CVE-2008-1389 Invalid memory access in the CHM unpacker
- CVE-2008-3912 Out-of-memory NULL pointer dereference in mbox/msg
- CVE-2008-3913 Memory leak in code path in freshclam's manager.c
- CVE-2008-3914 Multiple file descriptor leaks on the code paths

* Sun Jul 13 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.93.3-1
- updated to 0.93.3; another fix for CVE-2008-2713 (out-of-bounds read
  on petite files)
- put pid instead of pgrp into pidfile of clamav-milter (bz #452359)
- rediffed patches

* Tue Jun 17 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.93.1-1
- updated to 0.93.1
- rediffed -path patch
- CVE-2008-2713 Invalid Memory Access Denial Of Service Vulnerability

* Mon Apr 14 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.93-1
- updated to final 0.93
- removed daily.inc + main.inc directories; they are now replaced by
  *.cld containers
- trimmed down MAILTO list of cronjob to 'root' again; every well
  configured system has an alias for this recipient

* Wed Mar 12 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.93-0.1.rc1
- moved -milter scriptlets into -milter-core subpackage
- added a requirement on the milteruser to the -milter-sendmail
  subpackage (reported by Bruce Jerrick)

* Tue Mar  4 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.93-0.0.rc1
- updated to 0.93rc1
- fixed rpath issues

* Mon Feb 11 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.92.1-1
- updated to 0.92.1

* Tue Jan  1 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.92-6
- redisabled unrar stuff completely by using clean sources
- splitted -milter subpackage into pieces to allow use without sendmail
  (#239037)

* Tue Jan  1 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.92-5
- use a better way to disable RPATH-generation (needed for '--with
  unrar' builds)

* Mon Dec 31 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.92-4
- added a README.fedora to the milter package (#240610)
- ship original sources again; unrar is now licensed correctly (no more
  stolen code put under GPL). Nevertheless, this license is not GPL
  compatible, and to allow libclamav to be used by GPL applications,
  unrar is disabled by a ./configure switch.
- use pkg-config in clamav-config to emulate --cflags and --libs
  operations (fixes partly multilib issues)
- registered some more auto-updated files and marked them as %%ghost

* Fri Dec 21 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.92-3
- updated to 0.92 (SECURITY):
- CVE-2007-6335 MEW PE File Integer Overflow Vulnerability

* Mon Oct 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.91.2-3
- remove RAR decompression code from source tarball because of
  legal problems (resolves 334371)
- correct license tag

* Mon Sep 24 2007 Jesse Keating <jkeating@redhat.com> - 0.91.2-2
- Bump release for upgrade path.

* Sat Aug 25 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.91.2-1
- updated to 0.91.2 (SECURITY):
- CVE-2007-4510 DOS in RTF parser
- DOS in html normalizer
- arbitrary command execution by special crafted recipients in
  clamav-milter's black-hole mode
- fixed an open(2) issue

* Tue Jul 17 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.91.1-0
- updated to 0.91.1

* Thu Jul 12 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.91-1
- updated to 0.91

* Thu May 31 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.90.3-1
- updated to 0.90.3
- BR tcpd.h instead of tcp_wrappers(-devel) to make it build both
  in FC6- and F7+

* Fri Apr 13 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.90.2-1
- [SECURITY] updated to 0.90.2; fixes CVE-2007-1745, CVE-2007-1997

* Fri Mar  2 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.90.1-2
- BR 'tcp_wrappers-devel' instead of plain 'tcp_wrappers'

* Fri Mar  2 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.90.1-1
- updated to 0.90.1
- updated %%doc list

* Sun Feb 18 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.90-1
- updated to final 0.90
- removed -visibility patch since fixed upstream

* Sun Feb  4 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.90-0.3.rc3
- build with -Wl,-as-needed and cleaned up pkgconfig file
- removed old hack which forced installation of freshclam.conf; related
  check was removed upstream
- removed static library
- removed %%changelog entries from before 2004

* Sat Feb  3 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.90-0.2.rc3
- updated to 0.90rc3
- splitted mandatory parts from the data-file into a separate -filesystem
  subpackage
- added a -data-empty subpackage to allow a setup where database is
  updated per cron-job and user does not want to download the large
  -data package with outdated virus definitations (#214949)
- %%ghost'ed the files downloaded by freshclam

Name:           munin
Version:        2.0.25
Release:        2%{?dist}
Summary:        Network-wide graphing framework (grapher/gatherer)

Group:          System Environment/Daemons
License:        GPLv2
URL:            http://munin-monitoring.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        http://downloads.sourceforge.net/sourceforge/munin/%{name}-%{version}.tar.gz
Source10:       http://downloads.sourceforge.net/sourceforge/munin/%{name}-%{version}.tar.gz.sha256sum
Source1:        munin-1.2.4-sendmail-config
Source2:        munin-1.2.5-hddtemp_smartctl-config
Source3:        munin-node.logrotate
Source4:        munin.logrotate
Source6:        munin-1.2.6-postfix-config
Source7:        munin-1.4.5-df-config
Source8:        munin-node.service
Source9:        %{name}.conf
Source11:       munin-node.service-privatetmp
# BZ#747663 http://munin-monitoring.org/ticket/1155
Source12:       cpuspeed.in.rev1243
Source13:       linux-init.d_munin-asyncd.in
Source14:       munin-asyncd.service
Source15:       munin-fcgi-html.service
Source16:       munin-fcgi-graph.service
Source17:       munin.cron.d
Source18:       munin-node.rc
Source19:       httpd_munin-cgi.conf
Source20:       Makefile.config-dist
Source21:       nginx_munin.conf
Source22:       munin-fcgi-html.rc
Source23:       munin-fcgi-graph.rc
Source24:       munin-2.0.9-amavis-config

#Patch1:         munin-1.4.6-restorecon.patch
#Patch2:         munin-1.4.2-fontfix.patch
Patch4:         munin-2.0.4-Utils-cluck.patch
Patch5:         acpi-2.0.5.patch
#Patch6:         munin-2.0.7-http_loadtime.patch
#Patch7:         munin-2.0-defect-1213.patch
#Patch8:         munin-2.0.2-defect-1245-LimitsOld.pm-notify_alias.patch
Patch9:         munin-2.0.8-cgitmp.patch
# BZ# 877116 Patch using '&' in the URLs instead of '&amp;' in HTMLConfig
Patch10:        munin-2.0.9_HTMLConfig.pm.patch

BuildArch:      noarch

%if 0%{?fedora} > 20
BuildRequires:  /usr/bin/hostname
%else
BuildRequires:  /bin/hostname
%endif
BuildRequires:  perl >= 5.8
%if 0%{?rhel} > 6 || 0%{?fedora} > 12
BuildRequires:  perl(Directory::Scratch)
%endif
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Net::Server)
BuildRequires:  perl(Net::SNMP)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::MockModule)
BuildRequires:  perl(Test::MockObject)
#BuildRequires:  perl(Test::Perl::Critic) >= 1.096 ## Not packaged
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(Net::SSLeay)
BuildRequires:  perl(HTML::Template)
BuildRequires:  perl(LWP::UserAgent)
# Work-around for koji
%if 0%{?rhel} > 6 || 0%{?fedora} > 16
BuildRequires:  perl-Carp
%endif
# RHEL6+ BuildRequires:  perl(Log::Log4perl) >= 1.18
%if 0%{?rhel} > 5 || 0%{?fedora} > 11
BuildRequires:  perl(Log::Log4perl) >= 1.18
%else
BuildRequires:  perl(Log::Log4perl)
%endif
Requires(pre):  shadow-utils
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# Munin server requires
Requires:       logrotate
Requires:       perl >= 5.8
Requires:       perl(CGI::Fast)
Requires:       perl(FCGI)
Requires:       perl(Digest::MD5)
Requires:       perl(File::Copy::Recursive)
Requires:       perl(Getopt::Long)
Requires:       perl(HTML::Template)
Requires:       perl(IO::Socket::INET6)
Requires:       perl(Net::Server)
Requires:       perl(Net::SNMP)
Requires:       perl(Net::SSLeay)
Requires:       perl(Params::Validate)
Requires:       perl(RRDs)
Requires:       perl(Storable)
Requires:       perl(Text::Balanced)
Requires:       perl(DateTime)
Requires:       perl(Time::HiRes)
Requires:       perl(Taint::Runtime)
Requires:       sysstat
Requires:       crontabs
# BZ#913111 : Removed because it pulls boa .. and no clean way to prefer apache.
#Requires:       webserver

# SystemD
%if 0%{?rhel} > 6 || 0%{?fedora} > 15
BuildRequires:  systemd-units
%endif

# Munin node requires
%if 0%{?rhel} > 6
#Requires:       perl(Cache::Memcached)
#Requires:       perl(Carp::Always)
# This one is in fact optional, only needed for cidr_allow in munin-node,
# which is documented in the manual page. Not present in el7.
#Requires:       perl(Net::CIDR)
%else
Requires:       perl(Cache::Memcached)
Requires:       perl(Carp::Always)
Requires:       perl(Net::CIDR)
%endif
Requires:       perl(Crypt::DES)
Requires:       perl(Digest::HMAC)
Requires:       perl(Digest::SHA1)
Requires:       perl(Net::Server)
Requires:       perl(Net::Server::Fork)
Requires:       perl(Net::SNMP)
Requires:       perl(Net::SSLeay)
Requires:       perl(Time::HiRes)
# mysql plugin requires perl(Cache::Cache)
Requires:       perl(Cache::Cache)

# Munin node java monitor requires
#Requires:       java-jmx # rhel<5
BuildRequires:  java-devel
BuildRequires:  jpackage-utils
%if 0%{?rhel} > 6
# RHEL7 does not have mx4j
#BuildRequires:  mx4j
%else
BuildRequires:  mx4j
%endif

# CGI requires
# RHEL6+ Requires:       dejavu-sans-mono-fonts


%description
Munin is a highly flexible and powerful solution used to create graphs
of virtually everything imaginable throughout your network, while still
maintaining a rattling ease of installation and configuration.

This package contains the grapher/gatherer. You will only need one instance of
it in your network. It will periodically poll all the nodes in your network
it's aware of for data, which it in turn will use to create graphs and HTML
pages, suitable for viewing with your graphical web browser of choice.

Munin is written in Perl, and relies heavily on Tobi Oetiker's excellent
RRDtool.

Creaete a munin web user after installing:
htpasswd -bc /etc/munin/munin-htpasswd MUNIN_WEB_USER PASSWORD


%package node
Group:          System Environment/Daemons
Summary:        Network-wide graphing framework (node)
BuildArch:      noarch
Requires:       %{name}-common = %{version}
Requires:       perl-Net-Server
Requires:       perl-Net-CIDR
Requires:       procps >= 2.0.7
Requires:       sysstat, /usr/bin/which, hdparm
Requires:       perl(LWP::UserAgent)
Requires(pre):  shadow-utils
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service

%description node
Munin is a highly flexible and powerful solution used to create graphs
of virtually everything imaginable throughout your network, while still
maintaining a rattling ease of installation and configuration.

This package contains node software. You should install it on all the nodes
in your network. It will know how to extract all sorts of data from the
node it runs on, and will wait for the gatherer to request this data for
further processing.

It includes a range of plugins capable of extracting common values such as
cpu usage, network usage, load average, and so on. Creating your own plugins
which are capable of extracting other system-specific values is very easy,
and is often done in a matter of minutes. You can also create plugins which
relay information from other devices in your network that can't run Munin,
such as a switch or a server running another operating system, by using SNMP
or similar technology.

Munin is written in Perl, and relies heavily on Tobi Oetiker's excellent
RRDtool.

%package async
Group:          System Environment/Daemons
Summary:        Network-wide graphing framework (asynchronous client tools)
BuildArch:      noarch
Requires:       %{name}-node = %{version}

%description async
Munin is a highly flexible and powerful solution used to create graphs of
virtually everything imaginable throughout your network, while still
maintaining a rattling ease of installation and configuration.

This package contains the tools necessary for setting up an asynchronous
client / spooling system.

See documentation for setup instructions:
https://munin.readthedocs.org/en/latest/node/async.html


%package common
Group:          System Environment/Daemons
Summary:        Network-wide graphing framework (common files)
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description common
Munin is a highly flexible and powerful solution used to create graphs
of virtually everything imaginable throughout your network, while still
maintaining a rattling ease of installation and configuration.

This package contains common files that are used by both the server (munin)
and node (munin-node) packages.


%package java-plugins
Group:          System Environment/Daemons
Summary:        java-plugins for munin
Requires:       %{name}-node = %{version}
BuildArch:      noarch
Requires:       jpackage-utils

%description java-plugins
java-plugins for munin-node.

Install this sub-package for the jmx node plugin.

%package ruby-plugins
Group:          System Environment/Daemons
Summary:        ruby-plugins for munin
Requires:       %{name}-node = %{version}
BuildArch:      noarch

%description ruby-plugins
ruby-plugins for munin-node.

Install this sub-package for the tomcat node plugin.


# BZ# 861816 munin-2.x CGI support is broken without manual hacks
%package cgi
Group:          System Environment/Daemons
Summary:        Network-wide graphing framework (cgi files for apache)
BuildArch:      noarch
Requires:       %{name}-common = %{version}
Requires:       mod_fcgid

%description cgi
Munin package uses cron by default.  This package contains the CGI files that
can generate HTML and graphs dynamically. This enables munin to scale better
for a master with many nodes.

See documentation for setup instructions:
http://munin-monitoring.org/wiki/CgiHowto2
http://munin.readthedocs.org/en/latest/example/webserver/apache-virtualhost.html

QUICK-HOWTO:
sed -i 's/\(.*\)_strategy.*/\1_strategy cgi/' /etc/munin/munin.conf
htpasswd -bc /etc/munin/munin-htpasswd MUNIN_WEB_USER PASSWORD
for svc in httpd munin-node ; do
  service $svc stop
  chkconfig $svc on
  service $svc start
done

# BZ# 905241
%package nginx
Group:          System Environment/Daemons
Summary:        Network-wide graphing framework (cgi files for nginx)
BuildArch:      noarch
Requires:       %{name}-common = %{version}
Requires:       spawn-fcgi

%description nginx
Munin package uses cron by default.  This package contains the CGI files that
can generate HTML and graphs dynamically. This enables munin to scale better
for a master with many nodes.

QUICK-HOWTO:
sed -i 's/\(.*\)_strategy.*/\1_strategy cgi/;s/#cgiurl_graph/cgiurl_graph/' /etc/munin/munin.conf
for svc in munin-fcgi-graph munin-fcgi-html nginx ; do
  service $svc stop
  chkconfig $svc on
  service $svc start
done

%package netip-plugins
Group:          System Environment/Daemons
Summary:        Network-wide graphing framework (dhcpd3 and ntp plugins)
BuildArch:      noarch
Requires:       %{name}-common = %{version}

%description netip-plugins
Munin plugins that require Net::IP.  This is only dhcpd3 and ntp currently.


%prep
%setup -q -n munin-%{version}

%if 0%{?rhel} < 6 && 0%{?fedora} < 11
install -c %{SOURCE12} ./plugins/node.d.linux/cpuspeed.in
%endif

%if 0%{?rhel} > 6
# This one relies on Cache::Memcached, which is not shipped with el7
rm -f plugins/node.d/memcached_.in
%endif

%patch4 -p0
%patch5 -p0
#% patch7 -p1
%patch9 -p1
%patch10 -p1
install -c %{SOURCE13} ./resources/

# Create Makefile.config-dist
install -c %{SOURCE20} .
sed -i -e 's,^PERLSITELIB := \(.*\),PERLSITELIB := %{perl_vendorlib},;' Makefile.config-dist


%build
%if 0%{?rhel} > 6
export  CLASSPATH=plugins/javalib/org/munin/plugin/jmx:$CLASSPATH
%else
export  CLASSPATH=plugins/javalib/org/munin/plugin/jmx:$(build-classpath mx4j):$CLASSPATH
%endif
make    CONFIG=Makefile.config-dist

# Convert to utf-8
for file in Announce-2.0 COPYING ChangeLog Checklist HACKING.pod README RELEASE UPGRADING UPGRADING-1.4; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done

# Fix the wrong FSF address
for FILE in plugins/node.d.linux/tcp.in COPYING plugins/node.d.linux/bonding_err_.in; do
  sed -i 's|59 Temple Place.*Suite 330, Boston, MA *02111-1307|51 Franklin St, Fifth Floor, Boston, MA 02110-1301|g' $FILE
done


%install
rm -rf ${buildroot}

## Node
%if 0%{?rhel} > 6
export  CLASSPATH=plugins/javalib/org/munin/plugin/jmx:$CLASSPATH
%else
export  CLASSPATH=plugins/javalib/org/munin/plugin/jmx:$(build-classpath mx4j):$CLASSPATH
%endif
make    CONFIG=Makefile.config-dist \
        DESTDIR=%{buildroot} \
%if 0%{?rhel} > 7 || 0%{?fedora} > 19
        DOCDIR=%{buildroot}%{_docdir}/%{name} \
%else
        DOCDIR=%{buildroot}%{_docdir}/%{name}-%{version} \
%endif
        JAVALIBDIR=%{buildroot}%{_datadir}/java \
        MANDIR=%{buildroot}%{_mandir} \
        PREFIX=%{buildroot}%{_prefix} \
        USER=nobody GROUP=nobody \
        install

# Remove fonts
rm %{buildroot}%{_datadir}/munin/DejaVuSans*.ttf

# install logrotate scripts
mkdir -p %{buildroot}/etc/logrotate.d
install -m 0644 %{SOURCE3} %{buildroot}/etc/logrotate.d/munin-node
install -m 0644 %{SOURCE4} %{buildroot}/etc/logrotate.d/munin

# BZ#821912 - Move .htaccess to apache config to allow easier user-access changes.
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
sed -e 's/# </</g' %{buildroot}/var/www/html/munin/.htaccess > %{buildroot}%{_sysconfdir}/httpd/conf.d/munin.conf
echo "ScriptAlias /munin-cgi/munin-cgi-graph /var/www/cgi-bin/munin-cgi-graph" >> \
  %{buildroot}%{_sysconfdir}/httpd/conf.d/munin.conf
rm %{buildroot}/var/www/html/munin/.htaccess

# install cron script
mkdir -p %{buildroot}/etc/cron.d
install -m 0644 %{SOURCE17} %{buildroot}/etc/cron.d/munin

# BZ# 908711
mv %{buildroot}/usr/share/munin/munin-asyncd %{buildroot}/usr/sbin/munin-asyncd

# SystemD
%if 0%{?rhel} > 6 || 0%{?fedora} > 15
mkdir -p %{buildroot}/lib/systemd/system
%endif
# Fedora 17 and higer uses privatetmp
%if 0%{?fedora} == 16
install -m 0644 %{SOURCE8} %{buildroot}/lib/systemd/system/munin-node.service
install -m 0644 %{SOURCE14} %{buildroot}/lib/systemd/system/munin-asyncd.service
install -m 0644 %{SOURCE15} %{buildroot}/lib/systemd/system/munin-fcgi-html.service
install -m 0644 %{SOURCE16} %{buildroot}/lib/systemd/system/munin-fcgi-graph.service
%endif
%if 0%{?rhel} > 6 || 0%{?fedora} > 16
install -m 0644 %{SOURCE11} %{buildroot}/lib/systemd/system/munin-node.service
install -m 0644 %{SOURCE14} %{buildroot}/lib/systemd/system/munin-asyncd.service
install -m 0644 %{SOURCE15} %{buildroot}/lib/systemd/system/munin-fcgi-html.service
install -m 0644 %{SOURCE16} %{buildroot}/lib/systemd/system/munin-fcgi-graph.service
%endif
mkdir -p %{buildroot}/var/lib/munin/spool

# install tmpfiles.d entry
%if 0%{?rhel} > 6 || 0%{?fedora} > 14
mkdir -p %{buildroot}%{_sysconfdir}/tmpfiles.d
install -m 0644 %{SOURCE9} %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf
%endif

# Fedora 15 and rhel use sysvinit / upstart
%if (0%{?rhel} > 4 && 0%{?rhel} <= 6) || 0%{?fedora} == 15
mkdir -p %{buildroot}/etc/rc.d/init.d
cat %{SOURCE18} | sed -e 's/2345/\-/' > %{buildroot}/etc/rc.d/init.d/munin-node
chmod 755 %{buildroot}/etc/rc.d/init.d/munin-node
install -m 0755 %{SOURCE13} %{buildroot}/etc/rc.d/init.d/munin-asyncd
install -m 0755 %{SOURCE22} %{buildroot}/etc/rc.d/init.d/munin-fcgi-html
install -m 0755 %{SOURCE23} %{buildroot}/etc/rc.d/init.d/munin-fcgi-graph
%endif

# Fix default config file
sed -i '
  s,/etc/munin/munin-conf.d,/etc/munin/conf.d,;
  s,#html_strategy.*,html_strategy cron,;
  s,#graph_strategy.*,graph_strategy cron,;
  s,#cgiurl_graph,cgiurl_graph,;
  ' %{buildroot}/etc/munin/munin.conf
mkdir -p %{buildroot}/etc/munin/conf.d
mkdir -p %{buildroot}/etc/munin/plugin-conf.d
mkdir -p %{buildroot}/etc/munin/node.d
mkdir -p %{buildroot}/etc/munin/plugin-node.d

# install config for sendmail under fedora
install -m 0644 %{SOURCE1} %{buildroot}/etc/munin/plugin-conf.d/sendmail

# install config for hddtemp_smartctl
install -m 0644 %{SOURCE2} %{buildroot}/etc/munin/plugin-conf.d/hddtemp_smartctl

# install logrotate scripts
install -m 0644 %{SOURCE3} %{buildroot}/etc/logrotate.d/munin-node
install -m 0644 %{SOURCE4} %{buildroot}/etc/logrotate.d/munin
%if 0%{?fedora} > 15 || 0%{?rhel} > 6
echo 'Using SU directive for logrotate.d'
%else
# Fedora >= 16 requires 'su' directive.
echo 'Commenting out SU directive for logrotate.d'
sed -i 's/su /#su /' %{buildroot}/etc/logrotate.d/munin-node
sed -i 's/su /#su /' %{buildroot}/etc/logrotate.d/munin
%endif

# install config for postfix under fedora
install -m 0644 %{SOURCE6} %{buildroot}/etc/munin/plugin-conf.d/postfix

# install df config to exclude fses we shouldn't try and monitor
install -m 0644 %{SOURCE7} %{buildroot}/etc/munin/plugin-conf.d/df

# Install amavis config file to set MUNIN_MKTEMP env
install -m 0644 %{SOURCE24} %{buildroot}/etc/munin/plugin-conf.d/amavis

# Append for BZ# 746083
cat - >> %{buildroot}/etc/munin/plugin-conf.d/munin-node <<EOT.node
[diskstats]
user munin

[iostat_ios]
user munin
EOT.node

# http://munin-monitoring.org/ticket/808
cat - >> %{buildroot}/etc/munin/plugin-conf.d/fw_ <<EOT.fw
[fw_*]
user root
EOT.fw

# Preload static html files
mkdir -p %{buildroot}/var/www/html/munin/
cp -r %{buildroot}/etc/munin/static %{buildroot}/var/www/html/munin/

# Remove plugins that are missing deps
rm %{buildroot}/usr/share/munin/plugins/sybase_space

# Create DBDIRNODE
mkdir -p %{buildroot}/var/lib/munin-node/plugin-state

# Create for BZ 786030
touch %{buildroot}/var/lib/munin/plugin-state/yum.state

# Create CGI tmpdir space
mkdir -p %{buildroot}/var/lib/munin/cgi-tmp/munin-cgi-graph

# BZ# 881689 - Fix config file so that it no longer references the build host
sed -i 's/^\[.*/\[localhost\]/' %{buildroot}/etc/munin/munin.conf

# BZ# 885422 Move munin-node logs to /var/log/munin-node/
mkdir -p %{buildroot}/var/log/munin-node
sed -i -e '
  s,^log_file .*,log_file /var/log/munin-node/munin-node.log,;
  s,^#host_name .*,host_name localhost.localdomain,;
  ' %{buildroot}/etc/munin/munin-node.conf

# Create sample fcgi config files
mkdir -p %{buildroot}/etc/sysconfig %{buildroot}/etc/httpd/conf.d
cp %{SOURCE19} %{buildroot}/etc/httpd/conf.d/munin-cgi.conf
mkdir -p %{buildroot}/etc/nginx/conf.d
cp %{SOURCE21} %{buildroot}/etc/nginx/conf.d/munin.conf

# Create sample htpasswd file
touch %{buildroot}/etc/munin/munin-htpasswd

# Fix munin-check to report more accurately
sed -i -e '
  s,nobody,munin,;
  s,owner_ok /var/log/munin .*,owner_ok /var/log/munin apache,;
  s,owner_ok /var/lib/munin .*,owner_ok /var/lib/munin munin,;
  s,owner_ok /var/lib/munin/plugin-state .*,owner_ok /var/lib/munin/plugin-state root,;
  ' %{buildroot}/usr/bin/munin-check


%clean
rm -rf %{buildroot}


#
# node package scripts
#
# adding because of f17.
%pre common
/usr/bin/getent group munin >/dev/null || \
  /usr/sbin/groupadd -r munin
/usr/bin/getent passwd munin >/dev/null || \
  /usr/sbin/useradd -r -g munin -d /var/lib/munin -s /sbin/nologin \
    -c "Munin user" munin
exit 0

%pre node
/usr/bin/getent group munin >/dev/null || \
  /usr/sbin/groupadd -r munin
/usr/bin/getent passwd munin >/dev/null || \
  /usr/sbin/useradd -r -g munin -d /var/lib/munin -s /sbin/nologin \
    -c "Munin user" munin
exit 0

%pre cgi
#why this? search for BUG above
chown apache /var/log/munin
exit 0

%post node
%if 0%{?rhel} > 6 || 0%{?fedora} > 15
  %if 0%{?systemd_post:1}
    %systemd_post munin-node.service
  %else
    if [ $1 -eq 1 ] ; then
      # Initial installation
      /bin/systemctl daemon-reload >/dev/null 2>&1 || :
    fi
  %endif
%else
  # sysvinit only in f15 and older and epel
  /sbin/chkconfig --add munin-node
%endif
# Only run configure on a new install, not an upgrade.
if [ "$1" = "1" ]; then
     /usr/sbin/munin-node-configure --shell 2> /dev/null | sh >& /dev/null || :
fi

%post async
%if 0%{?rhel} > 6 || 0%{?fedora} > 15
  %if 0%{?systemd_post:1}
    %systemd_post munin-asyncd.service
  %else
    if [ $1 -eq 1 ] ; then
      # Initial installation
      /bin/systemctl daemon-reload >/dev/null 2>&1 || :
    fi
  %endif
%else
  # sysvinit only in f15 and older and epel
  /sbin/chkconfig --add munin-asyncd
%endif

%preun node
%if 0%{?rhel} > 6 || 0%{?fedora} > 15
# Newer installs use systemd
  %if 0%{?systemd_preun:1}
    %systemd_preun munin-node.service
  %else
    if [ "$1" = 0 ]; then
      /bin/systemctl --no-reload disable munin-node.service >/dev/null 2>&1 || :
      /bin/systemctl stop munin-node.service >/dev/null 2>&1 || :
    fi
  %endif
%else
# Older installs use sysvinit / upstart
if [ "$1" = 0 ]; then
  service munin-node stop &>/dev/null || :
  /sbin/chkconfig --del munin-node
fi
%endif

%preun nginx
%if 0%{?rhel} > 6 || 0%{?fedora} > 15
# Newer installs use systemd
  %if 0%{?systemd_preun:1}
    for svc in fcgi-html fcgi-graph ; do
      %systemd_preun munin-${svc}.service
    done
  %else
    if [ "$1" = 0 ]; then
      for svc in fcgi-html fcgi-graph ; do
        /bin/systemctl --no-reload disable munin-${svc}.service >/dev/null 2>&1 || :
        /bin/systemctl stop munin-${svc}.service >/dev/null 2>&1 || :
      done
    fi
  %endif
%else
# Older installs use sysvinit / upstart
if [ "$1" = 0 ]; then
  for svc in fcgi-html fcgi-graph; do
    service munin-${svc} stop &>/dev/null || :
    /sbin/chkconfig --del munin-${svc}
  done
fi
%endif

%postun node
if [ "$1" = "0" ]; then
  [ -d %{_sysconfdir}/munin/plugins ] && \
    find %{_sysconfdir}/munin/plugins/ -maxdepth 1 -type l -print0 | \
      xargs -0 rm || :
fi

%triggerun node -- munin-node < 1.4.7-2
mv -f %{_sysconfdir}/munin/plugins %{_sysconfdir}/munin/plugins.bak || :

%triggerpostun node -- munin-node < 1.4.7-2
mv -f %{_sysconfdir}/munin/plugins.bak %{_sysconfdir}/munin/plugins || :


#
# main package scripts
#
%pre
/usr/bin/getent group munin >/dev/null || \
  /usr/sbin/groupadd -r munin
/usr/bin/getent passwd munin >/dev/null || \
  /usr/sbin/useradd -r -g munin -d /var/lib/munin -s /sbin/nologin \
    -c "Munin user" munin
exit 0


%files
%defattr(-,root,root)
%doc %{_mandir}/man1/munindoc*
%doc %{_mandir}/man1/munin-sched*
%doc %{_mandir}/man3/Munin::Master*
%doc %{_mandir}/man5/munin.conf*
%doc %{_mandir}/man8/munin*
%dir %{_sysconfdir}/munin
%dir %{_sysconfdir}/munin/conf.d
%dir %{_sysconfdir}/munin/static
%dir %{_sysconfdir}/munin/templates
%dir %{_sysconfdir}/munin/templates/partial
%dir %{_datadir}/munin
%dir %{_datadir}/munin/plugins
#BUG. User apache does not necessarily exists when installing package munin
#since httpd is not required. it matters if httpd is later installed and
#the munin graph or html cgi programs are used - they log here.
#this is fixed with %%pre cgi, but if user tries to use the cgi programs
#without the cgi package, it's tough luck.
#proper fix may be to create the apache user in pre, but I'm not gonna do it.
%dir %attr(0775,apache,munin) /var/log/munin
%dir %attr(0775,root,munin) /var/lib/munin/plugin-state
%attr(0755,munin,munin) %dir /var/www/html/munin
%attr(0755,munin,munin) %dir /var/www/html/munin/static
%attr(0755,root,munin) /var/www/cgi-bin/munin-cgi-graph
%attr(0755,root,munin) /var/www/cgi-bin/munin-cgi-html
%attr(0644,munin,munin) /var/www/html/munin/static/*
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/cron.d/munin
%config(noreplace) %{_sysconfdir}/httpd/conf.d/munin.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/munin
%config(noreplace) %{_sysconfdir}/munin/munin.conf
%config(noreplace) %{_sysconfdir}/munin/munin-htpasswd
%config(noreplace) %{_sysconfdir}/munin/static/*
%config(noreplace) %{_sysconfdir}/munin/templates/partial/*.tmpl
%config(noreplace) %{_sysconfdir}/munin/templates/*.tmpl
%attr(0755,root,root) %{_bindir}/munin-check
%attr(0755,root,root) %{_bindir}/munin-cron
%attr(0755,root,root) %{_bindir}/munindoc
%attr(0755,root,root) %{_sbindir}/munin-sched
%{_datadir}/munin/munin-datafile2storable
%{_datadir}/munin/munin-graph
%{_datadir}/munin/munin-html
%{_datadir}/munin/munin-limits
%{_datadir}/munin/munin-storable2datafile
%{_datadir}/munin/munin-update
%{perl_vendorlib}/Munin/Master/*.pm


%files node
%defattr(-,root,root)
%doc %{_mandir}/man1/munin-node*
%doc %{_mandir}/man1/munin-run*
%doc %{_mandir}/man3/Munin::Common*
%doc %{_mandir}/man3/Munin::Node*
%doc %{_mandir}/man3/Munin::Plugin*
%doc %{_mandir}/man5/munin-node*
%dir %{_sysconfdir}/munin/node.d
%dir %{_sysconfdir}/munin/plugins
%dir %{_sysconfdir}/munin
%dir %{_datadir}/munin
%dir %attr(-,munin,munin) /var/lib/munin
%dir %attr(0775,nobody,munin) /var/lib/munin-node/plugin-state
%dir %attr(0755,root,root) /var/log/munin-node
%config(noreplace) %{_sysconfdir}/logrotate.d/munin-node
%config(noreplace) %{_sysconfdir}/munin/munin-node.conf
%config(noreplace) %{_sysconfdir}/munin/plugin-conf.d/amavis
%config(noreplace) %{_sysconfdir}/munin/plugin-conf.d/df
%config(noreplace) %{_sysconfdir}/munin/plugin-conf.d/fw_
%config(noreplace) %{_sysconfdir}/munin/plugin-conf.d/hddtemp_smartctl
%config(noreplace) %{_sysconfdir}/munin/plugin-conf.d/munin-node
%config(noreplace) %{_sysconfdir}/munin/plugin-conf.d/postfix
%config(noreplace) %{_sysconfdir}/munin/plugin-conf.d/sendmail
%if 0%{?rhel} > 6 || 0%{?fedora} > 15
/lib/systemd/system/munin-node.service
%else
%{_sysconfdir}/rc.d/init.d/munin-node
%endif
%attr(0755,root,root) %{_sbindir}/munin-run
%attr(0755,root,root) %{_sbindir}/munin-node
%attr(0755,root,root) %{_sbindir}/munin-node-configure
%attr(-,munin,munin) /var/lib/munin/plugin-state/yum.state
%exclude %{_datadir}/munin/plugins/dhcpd3
%exclude %{_datadir}/munin/plugins/jmx_
%exclude %{_datadir}/munin/plugins/ntp_
%exclude %{_datadir}/munin/plugins/tomcat_
%{_datadir}/munin/plugins/
%{perl_vendorlib}/Munin/Node
%{perl_vendorlib}/Munin/Plugin*


%files async
%defattr(-,root,root)
%{_sbindir}/munin-asyncd
%{_datadir}/munin/munin-async
%dir /var/lib/munin/spool
%if 0%{?rhel} > 6 || 0%{?fedora} > 15
/lib/systemd/system/munin-asyncd.service
%else
%{_sysconfdir}/rc.d/init.d/munin-asyncd
%endif


%files common
%defattr(-,root,root)
%doc Announce-2.0 COPYING ChangeLog Checklist HACKING.pod README RELEASE UPGRADING UPGRADING-1.4
%dir %{perl_vendorlib}/Munin
%dir %attr(-,munin,munin) %{_localstatedir}/run/%{name}/
%if 0%{?rhel} > 6 || 0%{?fedora} > 14
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%endif
%{perl_vendorlib}/Munin/Common


%files java-plugins
%defattr(-,root,root)
%{_datadir}/java/munin-jmx-plugins.jar
%{_datadir}/munin/plugins/jmx_


%files ruby-plugins
%defattr(-,root,root)
%{_datadir}/munin/plugins/tomcat_


%files cgi
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/munin-cgi.conf
%if 0%{?rhel} > 6 || 0%{?fedora} > 15
/lib/systemd/system/munin-fcgi-html.service
/lib/systemd/system/munin-fcgi-graph.service
%endif
%attr(0755,root,root) %dir /var/lib/munin/cgi-tmp
%attr(0755,apache,apache) %dir /var/lib/munin/cgi-tmp/munin-cgi-graph


%files nginx
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/nginx/conf.d/munin.conf
%if 0%{?rhel} > 6 || 0%{?fedora} > 15
/lib/systemd/system/munin-fcgi-html.service
/lib/systemd/system/munin-fcgi-graph.service
%else
%{_sysconfdir}/rc.d/init.d/munin-fcgi-html
%{_sysconfdir}/rc.d/init.d/munin-fcgi-graph
%endif


%files netip-plugins
%defattr(-,root,root)
%{_datadir}/munin/plugins/dhcpd3
%{_datadir}/munin/plugins/ntp_


%changelog
* Thu Jan 01 2015 Liu Di <liudidi@gmail.com> - 2.0.25-2
- 为 Magic 3.0 重建

* Tue Nov 25 2014 "D. Johnson" <fenris02@fedoraproject.org> - 2.0.25-1
- Upstream released 2.0.25

* Sun Oct 26 2014 "D. Johnson" <fenris02@fedoraproject.org> - 2.0.24-1
- Upstream released 2.0.24

* Sat Oct 18 2014 "D. Johnson" <fenris02@fedoraproject.org> - 2.0.23-1
- Upstream released 2.0.23

* Fri Oct 17 2014 "D. Johnson" <fenris02@fedoraproject.org> - 2.0.22-1
- Upstream released 2.0.22

* Tue Oct 07 2014 "D. Johnson" <fenris02@fedoraproject.org> - 2.0.21-8
- BZ# 1149948 - munin-async pid file in /var/run rather than /var/run/munin

* Mon Sep 15 2014 Petr Pisar <ppisar@redhat.com> - 2.0.21-6
- Build against perl 5.20

* Sun Sep 14 2014 "D. Johnson" <fenris02@fedoraproject.org> - 2.0.21-6
- Add amavis plugin config defaults

* Sun Sep 07 2014 "D. Johnson" <fenris02@fedoraproject.org> - 2.0.21-5
- BZ# 1114857 - munin-2.0.21-2.fc21 FTBFS: No Package found for java-1.7.0-devel
- re-merge earlier commit for epel7

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.21-4
- Perl 5.20 rebuild

* Fri Aug 01 2014 "D. Johnson" <fenris02@fedoraproject.org> - 2.0.21-3
- Default to a localhost name to prevent munin-node from complaining

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 28 2014 Lubomir Rintel <lkundrak@v3.sk> - 2.0.21-1.1
- mx4j is not a build time dependency
- RHEL 7 Actually uses systemd too
- No Net::CIDR in el7
- No Cache::Memcached in el7
- Carp::Always is not actually required

* Fri Apr 25 2014 "D. Johnson" <fenris02@fedoraproject.org> - 2.0.21-1
- Upstream released 2.0.21

* Fri Mar 28 2014 "D. Johnson" <fenris02@fedoraproject.org> - 2.0.20-1
- Upstream released 2.0.20
- BZ# 1082162: munin-asyncd doesn't get added to chkconfig

* Wed Mar 26 2014 D. Johnson <fenris02@fedoraproject.org> - 2.0.19-2
- BZ# 1081254: Start asyncd after node
- BZ# 1028075: munin-node doesn't get added to chkconfig

* Sun Dec 08 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.19-1
- Upstream to 2.0.19

* Sun Dec 08 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.18-2
- Modifying hostname require for f21

* Sat Dec 07 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.18-1
- BZ# 1037890,1037889,1037888: CVE-2013-6359

* Tue Sep 24 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.17-6
- Move Net::IP plugins to a subpackage for dep handling

* Fri Aug 16 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.17-5
- BZ# 993985: munin possibly affected by F-20 unversioned docdir change

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Aug 01 2013 Petr Pisar <ppisar@redhat.com> - 2.0.17-3
- Perl 5.18 rebuild

* Sat Jul 27 2013 Jóhann B. Guðmundsson <johannbg@fedoraproject.org> - 2.0.17-2
- BZ# 989080 Add a missing requirement on crontabs to spec file

* Sat Jul 20 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.17-1
- Upstream release 2.0.17

* Tue Jun 04 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.16-1
- Upstream released 2.0.16

* Sat Jun 01 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.15-1
- Upstream released 2.0.15

* Wed May 22 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.14-2
- Corrected bugid 905241 references

* Sat May 11 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.14-1
- Upstream released 2.0.14

* Fri Apr 26 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.13-1
- Upstream released 2.0.13

* Thu Apr 4 2013 Viljo Viitanen <viljo.viitanen@iki.fi> - 2.0.12-4
- BZ #905241 add nginx cgi package, removed unnecessary services from apache
  cgi package

* Mon Apr 01 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.12-3
- Add fw_ default config

* Sun Mar 24 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.12-2
- BZ# 917002 minor edits for asyncd

* Fri Mar 22 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.12-1
- Upstream release 2.0.12

* Sat Mar 09 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.11.1-3
- Update systemd scriptlets

* Fri Feb 22 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.11.1-2
- BZ# 913111 Removed R:webserver because it pulls boa .. and no clean way to
  prefer apache.
- BZ# 917002 munin-asyncd should wait for munin-node

* Sat Feb 09 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.11.1-1
- Upstream version 2.0.11.1

* Thu Feb 07 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.11-4
- BZ# 908711 munin-async: wrong path in init script

* Wed Feb 06 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.11-3
- Split out tomcat plugin to remove ruby dep from node.

* Mon Feb 04 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.11-2
- BZ# 907369 revert HTMLOld.pm patch

* Sun Feb 03 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.11-1
- Upstream release 2.0.11

* Mon Jan 21 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.10-2
- BZ# 896644 Wrong path to munin jar in jmx plugin

* Wed Jan 09 2013 D. Johnson <fenris02@fedoraproject.org> - 2.0.10-1
- Update to 2.0.10
- BZ# 891940,892377 Only stop/restart services provided by sub-package, not deps.
- BZ# 881689 Fix config file so that it no longer references the build host
- BZ# 877116 Patch using '&' in the URLs instead of '&amp;' in HTMLConfig

* Fri Dec 21 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.9-4
- Use Makefile.config-dist instead of sed.
- BZ# 890246,890247 "su" directive is not used in epel5/6 logrotate

* Sun Dec 09 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.9-3
- Add documentation links for async
- BZ# 885422 Move munin-node logs to /var/log/munin-node/
- BZ# 877166 Convert '&' to '&amp;' in HTMLConfig.pm for validation

* Thu Dec 06 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.9-2
- Require: LWP::UserAgent for plugins
- BZ# 861816 Add simplified files for switching to FCGI
- BZ# 880505 Change logrotate files to include su directive

* Thu Dec 06 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.9-1
- Update to 2.0.9

* Fri Nov 30 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.8-3
- BZ# 880505 munin logrotate permissions fix.

* Tue Nov 13 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.8-2
- Added cgitmp patch c/o Diego Elio Pettenò <flameeyes@flameeyes.eu>
- BZ# 861816 Add sample files for switching to FCGI

* Sun Nov 11 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.8-1
- Upstream to 2.0.8

* Sun Nov 04 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.7-6
- minor CGI permission fixes

* Sun Nov 04 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.7-5
- BZ# 872891 Re-add config file option to use conf.d/ instead of munin-conf.d/

* Fri Oct 26 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.7-4
- more CGI files to correct cgi-bin/
- BZ# 871967 Upstream 1235, Munin: unknown states on services for LimitsOld.pm
- BZ# 861816 Create CGI sub-package for dynamic graphing

* Fri Oct 19 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.7-3
- BZ# 859956 Minor fedora/rhel build macro fixes
- BZ# 861148 Upstream 1213, Incorrect child count in worker threads for GraphOld.pm and HTMLOld.pm

* Sun Oct 14 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.7-2
- Do not use 'env' for #! lines.
- Require: perl-Taint-Runtime to prevent warnings

* Sun Oct 07 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.7-1
- Upstream to 2.0.7
- BZ# 850401 Use systemd_preun when available (f18)
- BZ# 863490 [patch] http_load plugin uses wrong time command
- BZ# 862469 Move asyncd init files to asyncd subpackage

* Tue Sep 11 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.6-3
- Upstream removed dists/redhat/

* Sat Sep 08 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.6-2
- node: remove File::Path as it is no longer needed.
- added DBDIRNODE for munin-node.

* Fri Aug 31 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.6-1
- BZ# 851375 Replace @@GOODSH@@ in epel init scripts
- BZ# 849831,849834 CVE-2012-3512 munin: insecure state file handling, munin->root privilege [fedora-all]

* Mon Aug 20 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.5-3
- rebuilt for epel

* Tue Aug 14 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.5-2
- Added munin-asyncd init files

* Tue Aug 14 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.5-1
- Updated to 2.0.5
- BZ# 603344 / upstream 1180, ACPI thermal information changed with 3.x kernels

* Tue Aug 07 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.4-3
- BZ# 823533 "hddtemp_smartctl plugin has a bug" - upstream patched
- BZ# 825820 Munin memcache plugin requires "perl(Cache::Memcached)"
- BZ# 834055 Munin updates changing permissions, conflicts with what munin-check does
- BZ# 812893,812894,839786,840496 - updated to munin2

* Sun Aug 05 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.4-2
- Changing permissions on html directories to minimize cron messages.

* Sat Aug 04 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.4-1
- updated to 2.0.4
- backported el6 packaging items

* Tue Jul 24 2012 fenris02@fedoraproject.org - 2.0.3-1
- Adjust default conf.d entry.
- updated to 2.0.3

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 19 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.2-2
- fixed conflicts

* Sat Jul 14 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.2-1
- updated to 2.0.2

* Thu Jun 07 2012 D. Johnson <fenris02@fedoraproject.org> - 2.0.0-1
- initial 2.0 release

* Fri May 18 2012 D. Johnson <fenris02@fedoraproject.org> - 1.4.7-5
- BZ# 822992 Including GCTime.java.patch
- BZ# 747663 Include older cpuspeed.in for older kernels
- BZ# 822894 Requires: perl-Net-CIDR
- BZ# 746083 Append user=munin for munin-node plugins
- BZ# 821912 Move htaccess to httpd/conf.d/munin.conf for easier administration

* Sun May 13 2012 Kevin Fenzi <kevin@scrye.com> - 1.4.7-4
- Fix ownership on /var/run/munin. Fixes bug #821204

* Tue Apr 24 2012 Kevin Fenzi <kevin@scrye.com> - 1.4.7-3
- A better for for 811867 with triggers.
- Fix directory conflict. Fixes bug #816340
- Fix path in java plugin. Fixes bug #816570

* Sun Apr 15 2012 Kevin Fenzi <kevin@scrye.com> - 1.4.7-2
- Fix node postun from messing up plugins on upgrade. Works around bug #811867

* Wed Mar 14 2012 D. Johnson <fenris02@fedoraproject.org> - 1.4.7-1
- updated for 1.4.7 release

* Wed Feb 22 2012 Kevin Fenzi <kevin@scrye.com> 1.4.6-8
- Build against java-1.7.0 now. Fixes bug #796345

* Tue Jan 31 2012 D. Johnson <fenris02@fedoraproject.org> - 1.4.6-7
- Create state file for yum-plugin. Fixes BZ #786030.

* Fri Jan 20 2012 Kevin Fenzi <kevin@scrye.com> - 1.4.6-6
- Add PrivateTmp=true to systemd unit file. Fixes bug #782512
- Change logrotate to use munin user. Fixes bug #771017

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-5.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.6-4.3
- Rebuild for java 1.6.0 downgrade (fesco ticket 663)

* Sat Aug 27 2011 Kevin Fenzi <kevin@scrye.com> - 1.4.6-4.1
- Add patch to run restorecon in the sysvinit script.
- This doesn't matter on f16+

* Sat Aug 20 2011 D. Johnson <fenris02@fedoraproject.org> - 1.4.6-4
- fix tmpfiles.d file for f15 (BZ# 731181)

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.4.6-3
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.4.6-2
- Perl mass rebuild

* Fri Jul 08 2011 D. Johnson <fenris02@fedoraproject.org> - 1.4.6-1
- update to 1.4.6

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.5-13
- Perl mass rebuild

* Wed Jun 15 2011 D. Johnson <fenris02@fedoraproject.org> - 1.4.5-12
- Use tmpfiles.d instead of ExecStartPre
- Add patch for noSuchObject errors (BZ# 712245)

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.5-11
- Perl 5.14 mass rebuild

* Wed Jun  1 2011 D. Johnson <fenris02@fedoraproject.org> - 1.4.5-10
- Fixes http://munin-monitoring.org/ticket/887

* Mon May 30 2011 D. Johnson <fenris02@fedoraproject.org> - 1.4.5-9
- Native systemd service file for munin-node (BZ# 699275)

* Tue Feb 08 2011 Kevin Fenzi <kevin@tummy.com> - 1.4.5-8
- Fix issue with uppercase node names returning no data. Fixes #673263

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 05 2010 Kevin Fenzi <kevin@tummy.com> - 1.4.5-6
- Adjust the df fix to include all the right fses

* Thu Nov 25 2010 Kevin Fenzi <kevin@tummy.com> - 1.4.5-5
- Exclude some fses from df plugin. fixes #601410

* Wed Aug 11 2010 Todd Zullinger <tmz@pobox.com> - 1.4.5-4.1
- Move jmx_ plugin to java-plugins package

* Wed Jul 07 2010 Kevin Fenzi <kevin@tummy.com> - 1.4.5-4
- Move docs to common subpackage to make sure COPYING is installed.

* Sat Jul 03 2010 Kevin Fenzi <kevin@tummy.com> - 1.4.5-3
- Add /etc/munin/node.d dir

* Sat Jun 12 2010 Kevin Fenzi <kevin@tummy.com> - 1.4.5-2
- Add /etc/munin/conf.d/ dir

* Sat Jun 05 2010 Kevin Fenzi <kevin@tummy.com> - 1.4.5-1
- Update to 1.4.5

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.4.4-2
- Mass rebuild with perl-5.12.0

* Mon Mar 01 2010 Kevin Fenzi <kevin@tummy.com> - 1.4.4-1
- Update to 1.4.4
- Add more doc files. Fixes bug #563824
- fw_forwarded_local fixed upstream in 1.4.4. Fixes bug #568500

* Sun Jan 17 2010 Kevin Fenzi <kevin@tummy.com> - 1.4.3-2
- Fix owner on state files.
- Add some BuildRequires.
- Make munin-node-configure only run on install, not upgrade. bug 540687

* Thu Dec 31 2009 Kevin Fenzi <kevin@tummy.com> - 1.4.3-1
- Update to 1.4.3

* Thu Dec 17 2009 Ingvar Hagelund <ingvar@linpro.no> - 1.4.2-1
- New upstream release
- Removed upstream packaged fonts
- Added a patch that makes rrdtool use the system bitstream vera fonts on
  rhel < 6 and fedora < 11

* Fri Dec 11 2009 Ingvar Hagelund <ingvar@linpro.no> - 1.4.1-3
- More correct fedora and el versions for previous font path fix
- Added a patch that fixes a quoting bug in GraphOld.pm, fixing fonts on el4

* Wed Dec 09 2009 Ingvar Hagelund <ingvar@linpro.no> - 1.4.1-2
- Remove jmx plugins when not supported (like on el4 and older fedora)
- Correct font path on older distros like el5, el4 and fedora<11

* Fri Dec 04 2009 Kevin Fenzi <kevin@tummy.com> - 1.4.1-1
- Update to 1.4.1

* Sat Nov 28 2009 Kevin Fenzi <kevin@tummy.com> - 1.4.0-1
- Update to final 1.4.0 version

* Sat Nov 21 2009 Kevin Fenzi <kevin@tummy.com> - 1.4.0-0.1.beta
- Update to beta 1.4.0 version.
- Add common subpackage for common files.

* Sun Nov 08 2009 Kevin Fenzi <kevin@tummy.com> - 1.4.0-0.1.alpha
- Initial alpha version of 1.4.0

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 24 2009 Andreas Thienemann <andreas@bawue.net> - 1.2.6-8
- Updated dependencies to better reflect plugin requirements
- Added hddtemp_smartctl patch to only scan for standby state on /dev/[sh]d? devices.

* Sat Jan 17 2009 Kevin Fenzi <kevin@tummy.com> - 1.2.6-7
- Adjust font requires for new dejavu-sans-mono-fonts name (fixes #480463)

* Mon Jan 12 2009 Kevin Fenzi <kevin@tummy.com> - 1.2.6-6
- Fix to require the correct font

* Sun Jan 11 2009 Kevin Fenzi <kevin@tummy.com> - 1.2.6-5
- Switch to using dejavu-fonts instead of bitstream-vera

* Sun Jan 04 2009 Kevin Fenzi <kevin@tummy.com> - 1.2.6-4
- Require bitstream-vera-fonts-sans-mono for Font (fixes #477428)

* Mon Aug 11 2008 Kevin Fenzi <kevin@tummy.com> - 1.2.6-3
- Move Munin/Plugin.pm to the node subpackage (fixes #457403)

* Sat Jul 12 2008 Kevin Fenzi <kevin@tummy.com> - 1.2.6-2
- Apply postfix patch (fixes #454159)
- Add perl version dep and remove unneeded perl-HTML-Template (fixes #453923)

* Fri Jun 20 2008 Kevin Fenzi <kevin@tummy.com> - 1.2.6-1
- Upgrade to 1.2.6

* Tue May 20 2008 Kevin Fenzi <kevin@tummy.com> - 1.2.5-5
- Rebuild for new perl

* Wed Dec 26 2007 Kevin Fenzi <kevin@tummy.com> - 1.2.5-4
- Add patch to fix ampersand and degrees in plugins (fixes #376441)

* Fri Nov 30 2007 Kevin Fenzi <kevin@tummy.com> - 1.2.5-3
- Removed unnneeded plugins.conf file (fixes #288541)
- Fix license tag.
- Fix ip_conntrack monitoring (fixes #253192)
- Switch to new useradd guidelines.

* Tue Mar 27 2007 Kevin Fenzi <kevin@tummy.com> - 1.2.5-2
- Fix directory ownership (fixes #233886)

* Tue Oct 17 2006 Kevin Fenzi <kevin@tummy.com> - 1.2.5-1
- Update to 1.2.5
- Fix HD stats (fixes #205042)
- Add in logrotate scripts that seem to have been dropped upstream

* Sun Aug 27 2006 Kevin Fenzi <kevin@tummy.com> - 1.2.4-10
- Rebuild for fc6

* Tue Jun 27 2006 Kevin Fenzi <kevin@tummy.com> - 1.2.4-9
- Re-enable snmp plugins now that perl-Net-SNMP is available (fixes 196588)
- Thanks to Herbert Straub <herbert@linuxhacker.at> for patch.
- Fix sendmail plugins to look in the right place for the queue

* Sat Apr 22 2006 Kevin Fenzi <kevin@tummy.com> - 1.2.4-8
- add patch to remove unneeded munin-nagios in cron.
- add patch to remove buildhostname in munin.conf (fixes #188928)
- clean up prep section of spec.

* Fri Feb 24 2006 Kevin Fenzi <kevin@scrye.com> - 1.2.4-7
- Remove bogus Provides for perl RRDs (fixes #182702)

* Thu Feb 16 2006 Kevin Fenzi <kevin@tummy.com> - 1.2.4-6
- Readded old changelog entries per request
- Rebuilt for fc5

* Sat Dec 24 2005 Kevin Fenzi <kevin@tummy.com> - 1.2.4-5
- Fixed ownership for /var/log/munin in node subpackage (fixes 176529)

* Wed Dec 14 2005 Kevin Fenzi <kevin@tummy.com> - 1.2.4-4
- Fixed ownership for /var/lib/munin in node subpackage

* Wed Dec 14 2005 Kevin Fenzi <kevin@tummy.com> - 1.2.4-3
- Fixed libdir messup to allow builds on x86_64

* Mon Dec 12 2005 Kevin Fenzi <kevin@tummy.com> - 1.2.4-2
- Removed plugins that require Net-SNMP and Sybase

* Tue Dec  6 2005 Kevin Fenzi <kevin@tummy.com> - 1.2.4-1
- Inital cleanup for fedora-extras

* Thu Apr 21 2005 Ingvar Hagelund <ingvar@linpro.no> - 1.2.3-4
- Fixed a bug in the iostat plugin

* Wed Apr 20 2005 Ingvar Hagelund <ingvar@linpro.no> - 1.2.3-3
- Added the missing /var/run/munin

* Tue Apr 19 2005 Ingvar Hagelund <ingvar@linpro.no> - 1.2.3-2
- Removed a lot of unecessary perl dependencies

* Mon Apr 18 2005 Ingvar Hagelund <ingvar@linpro.no> - 1.2.3-1
- Sync with svn

* Tue Mar 22 2005 Ingvar Hagelund <ingvar@linpro.no> - 1.2.2-5
- Sync with release of 1.2.2
- Add some nice text from the suse specfile
- Minimal changes in the header
- Some cosmetic changes
- Added logrotate scripts (stolen from debian package)

* Sun Feb 01 2004 Ingvar Hagelund <ingvar@linpro.no>
- Sync with CVS. Version 1.0.0pre2

* Sun Jan 18 2004 Ingvar Hagelund <ingvar@linpro.no>
- Sync with CVS. Change names to munin.

* Fri Oct 31 2003 Ingvar Hagelund <ingvar@linpro.no>
- Lot of small fixes. Now builds on more RPM distros

* Wed May 21 2003 Ingvar Hagelund <ingvar@linpro.no>
- Sync with CVS
- 0.9.5-1

* Tue Apr  1 2003 Ingvar Hagelund <ingvar@linpro.no>
- Sync with CVS
- Makefile-based install of core files
- Build doc (only pod2man)

* Thu Jan  9 2003 Ingvar Hagelund <ingvar@linpro.no>
- Sync with CVS, auto rpmbuild

* Thu Jan  2 2003 Ingvar Hagelund <ingvar@linpro.no>
- Fix spec file for RedHat 8.0 and new version of lrrd

* Wed Sep  4 2002 Ingvar Hagelund <ingvar@linpro.no>
- Small bugfixes in the rpm package

* Tue Jun 18 2002 Kjetil Torgrim Homme <kjetilho@linpro.no>
- new package

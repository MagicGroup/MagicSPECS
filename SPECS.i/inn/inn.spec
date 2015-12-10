%global _hardened_build 1

Summary: The InterNetNews system, an Usenet news server
Summary(zh_CN.UTF-8): InterNetNews 系统，一个新闻组服务器
Name: inn
Version: 2.6.0
Release: 0.rc1.1%{?dist}.5
#see LICENSE file for details
License: GPLv2+ and BSD and MIT and Public Domain
Group: System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
URL: https://www.isc.org/software/INN/
Source0: ftp://ftp.isc.org/isc/inn/testing/inn-%{version}rc1.tar.gz
Source2: inn-default-distributions
Source10: inn-faq.tar.gz
Source20: innd.service
Source21: innd-expire.service
Source22: innd-expire.timer
Source23: innd-nntpsend.service
Source24: innd-nntpsend.timer
Source25: innd-rnews.service
Source26: innd-rnews.timer
Patch1:  inn-2.6.0-rh.patch
Patch6: inn-2.5.2.posix.patch
Patch7: inn-2.4.3.warn.patch
Patch8: inn-2.4.2-makedbz.patch
Patch10: inn-2.6.0-doc.patch
Patch13: inn-2.5.0-chown.patch
Patch14: inn-redhat_build.patch
patch17: inn-2.5.2-pconf.patch
Patch19: inn-2.5.4-docrun.patch
BuildRequires: python db4-devel byacc krb5-devel pam-devel e2fsprogs-devel perl
BuildRequires: perl(ExtUtils::Embed) flex systemd-units
Requires(pre): shadow-utils
Requires: grep, coreutils, sed
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: bash >= 2.0
Requires(post): systemd-units inews
Requires(preun): systemd-units
Requires(postun): systemd-units

# XXX white out bogus perl requirement for now
Provides: perl(::usr/lib/innshellvars.pl) = %{version}-%{release}

Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
INN (InterNetNews) is a complete system for serving Usenet news and/or
private newsfeeds.  INN includes innd, an NNTP (NetNews Transport
Protocol) server, and nnrpd, a newsreader that is spawned for each
client.  Both innd and nnrpd vary slightly from the NNTP protocol, but
not in ways that are easily noticed.

Install the inn package if you need a complete system for serving and
reading Usenet news.  You may also need to install inn-devel, if you
are going to use a separate program which interfaces to INN, like
newsgate or tin.

%description -l zh_CN.UTF-8
新闻组服务器。

%package devel
Summary: The INN (InterNetNews) library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: inn = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}

%description devel
The inn-devel package contains the INN (InterNetNews) library, which
several programs that interface with INN need in order to work (for
example, newsgate and tin).

If you are installing a program which must interface with the INN news
system, you should install inn-devel.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package -n inews
Summary: Sends Usenet articles to a local news server for distribution
Summary(zh_CN.UTF-8): 发送 Usenet 的文章到本地新闻服务器
Group: System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务

%description -n inews
The inews program is used by some news programs (for example, inn and
trn) to post Usenet news articles to local news servers.  Inews reads
an article from a file or standard input, adds headers, performs some
consistency checks and then sends the article to the local news server
specified in the inn.conf file.

Install inews if you need a program for posting Usenet articles to
local news servers.

%description -n inews -l zh_CN.UTF-8
发送 Usenet 的文章到本地新闻服务器。

%package libs
Summary: Libraries provided by INN
Summary(zh_CN.UTF-8): %{name} 的运行库
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统

%description libs
This package contains dynamic libraries provided by INN project

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%pre
getent group news >/dev/null || groupadd -g 13 -r news
getent passwd news >/dev/null || \
useradd -r -u 9 -g news -d /etc/news  \
-c "News server user" news
exit 0

%prep
%setup -q -n inn-%{version}rc1
%patch1 -p1 -b .rh
%patch6 -p1 -b .posix
%patch7 -p1 -b .warn
%patch8 -p1 -b .makedbz
%patch10 -p1 -b .docx
%patch13 -p1 -b .chown
%patch14 -p1 -b .redhat_build

%patch17 -p1 -b .pfix
# %patch19 -p1 -b .docrun

perl -pi -e 's/su news/su -m news/' ./INSTALL
perl -pi -e 's/LOCK_READ/LLOCK_READ/' `find . -type f`
perl -pi -e 's/LOCK_WRITE/LLOCK_WRITE/' `find . -type f`

%build
export DEFINE_INN_FLAGS="-D_XOPEN_SOURCE=600 -D_BSD_SOURCE -DHAVE_ET_COM_ERR_H -DHAVE_SSIZE_T"
export CFLAGS="$RPM_OPT_FLAGS $DEFINE_INN_FLAGS -fno-strict-aliasing -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"

%ifarch s390 s390x sparc sparcv9 sparc64
export CFLAGS="$CFLAGS -fPIC"
%else
export CFLAGS="$CFLAGS -fpic"
%endif

%configure --bindir=%{_libexecdir}/news \
  --sysconfdir=%{_sysconfdir}/news --exec-prefix=%{_libexecdir}/news \
  --with-log-dir=/var/log/news --with-spool-dir=/var/spool/news\
  --with-db-dir=%{_sharedstatedir}/news --with-run-dir=/run/news \
  --with-etc-dir=%{_sysconfdir}/news --with-tmp-dir=%{_sharedstatedir}/news/tmp \
  --with-perl --enable-shared --enable-uucp-rnews \
  --with-libperl-dir=%{perl_vendorlib} \
  --enable-pgp-verify --with-sendmail=/usr/sbin/sendmail \
  --with-news-user=news --with-news-group=news --with-news-master=news \
  --enable-ipv6 --with-http-dir=%{_sharedstatedir}/news/http \
  --enable-libtool --disable-static --with-pic

# Don't hardcode rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make # %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/news/http
make install DESTDIR=$RPM_BUILD_ROOT

# -- Install man pages needed by suck et al.
mkdir -p $RPM_BUILD_ROOT%{_includedir}/inn

for f in clibrary.h config.h
do
    install -p -m 0644 ./include/$f $RPM_BUILD_ROOT%{_includedir}/inn
done
for f in defines.h system.h libinn.h storage.h options.h dbz.h
do
    install -p -m 0644 ./include/inn/$f $RPM_BUILD_ROOT%{_includedir}/inn
done

touch     $RPM_BUILD_ROOT%{_sharedstatedir}/news/subscriptions
chmod 644 $RPM_BUILD_ROOT%{_sharedstatedir}/news/subscriptions

install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sharedstatedir}/news/distributions

mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -p -m 0644 %{SOURCE20} $RPM_BUILD_ROOT%{_unitdir}

install -p -m 0644 %{SOURCE21} $RPM_BUILD_ROOT%{_unitdir}
install -p -m 0644 %{SOURCE22} $RPM_BUILD_ROOT%{_unitdir}

install -p -m 0644 %{SOURCE23} $RPM_BUILD_ROOT%{_unitdir}
install -p -m 0644 %{SOURCE24} $RPM_BUILD_ROOT%{_unitdir}

install -p -m 0644 %{SOURCE25} $RPM_BUILD_ROOT%{_unitdir}
install -p -m 0644 %{SOURCE26} $RPM_BUILD_ROOT%{_unitdir}

tar xf %{SOURCE10}
mv inn.html FAQ.html

touch $RPM_BUILD_ROOT%{_sharedstatedir}/news/history
#LD_LIBRARY_PATH=$RPM_BUILD_ROOT/usr/lib $RPM_BUILD_ROOT/usr/bin/makedbz -i \
# -f $RPM_BUILD_ROOT/var/lib/news/history
#chmod 644 $RPM_BUILD_ROOT/var/lib/news/*

cat > $RPM_BUILD_ROOT%{_sysconfdir}/news/.profile <<EOF
PATH=/bin:%{_bindir}:%{_libexecdir}/news
export PATH
EOF

#Fix perms in sample directory to avoid bogus dependencies
find samples -name "*.in" -exec chmod a-x {} \;

# we get this from cleanfeed
rm -f $RPM_BUILD_ROOT%{_libexecdir}/news/filter/filter_innd.pl

mkdir -p $RPM_BUILD_ROOT%{_bindir}
ln -sf %{_libexecdir}/news/inews $RPM_BUILD_ROOT%{_bindir}/inews
ln -sf %{_libexecdir}/news/rnews $RPM_BUILD_ROOT%{_bindir}/rnews

# Remove unwanted files
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.a

# Documentation is installed via rpm %%doc directive
rm -rf $RPM_BUILD_ROOT/usr/doc/

# Use tmpfiles.d to create /var/run/news
install -d $RPM_BUILD_ROOT%{_tmpfilesdir}
cat <<EOF >$RPM_BUILD_ROOT%{_tmpfilesdir}/inn.conf
D %{_localstatedir}/run/news 0755 news news -
EOF
install -d -m 0755 $RPM_BUILD_ROOT%{_localstatedir}/run/news
magic_rpm_clean.sh

%post
su -m news -c '/usr/libexec/news/makedbz -i -o'

umask 002
touch /var/log/news/news.notice
touch /var/log/news/news.crit
touch /var/log/news/news.err
chown -R news:news /var/log/news*

%systemd_post innd.service

%systemd_post innd-expire.timer
%systemd_post innd-nntpsend.timer
%systemd_post innd-rnews.timer

systemctl start innd-expire.timer
systemctl start innd-nntpsend.timer
systemctl start innd-rnews.timer

%post libs -p /sbin/ldconfig

%triggerin -- rsyslog
if [ -f /etc/rsyslog.conf ]; then
  if ! grep -q INN /etc/rsyslog.conf; then
    sed 's/mail.none;/mail.none;news.none;/' < /etc/rsyslog.conf > /etc/rsyslog.conf.inn
    mv /etc/rsyslog.conf.inn /etc/rsyslog.conf

    echo '' \
       >> /etc/rsyslog.conf
    echo '#' \
       >> /etc/rsyslog.conf
    echo '# INN' \
       >> /etc/rsyslog.conf
    echo '#' \
       >> /etc/rsyslog.conf
    echo 'news.=crit                                        /var/log/news/news.crit'   >> /etc/rsyslog.conf
    echo 'news.=err                                         /var/log/news/news.err'    >> /etc/rsyslog.conf
e    echo 'news.notice                                       /var/log/news/news.notice' >> /etc/rsyslog.conf
    echo 'news.=debug                                       /var/log/news/news.debug' >> /etc/rsyslog.conf

    fi
  if [ -f /var/run/rsyslogd.pid ]; then
    kill -HUP `cat /var/run/rsyslogd.pid` 2> /dev/null ||:
  fi
fi

%triggerin -- sysklogd
if [ -f /etc/syslog.conf ]; then
  if ! grep -q INN /etc/syslog.conf; then
    sed 's/mail.none;/mail.none;news.none;/' < /etc/syslog.conf > /etc/syslog.conf.inn
    mv /etc/syslog.conf.inn /etc/syslog.conf

    echo '' \
       >> /etc/syslog.conf
    echo '#' \
       >> /etc/syslog.conf
    echo '# INN' \
       >> /etc/syslog.conf
    echo '#' \
       >> /etc/syslog.conf
    echo 'news.=crit                                        /var/log/news/news.crit'   >> /etc/syslog.conf
    echo 'news.=err                                         /var/log/news/news.err'    >> /etc/syslog.conf
    echo 'news.notice                                       /var/log/news/news.notice' >> /etc/syslog.conf
    fi
  if [ -f /var/run/syslogd.pid ]; then
    kill -HUP `cat /var/run/syslogd.pid` 2> /dev/null ||:
  fi
fi

%preun
%systemd_preun innd.service

%systemd_preun innd-expire.service
%systemd_preun innd-nntpsend.service
%systemd_preun innd-rnews.service

%systemd_preun innd-expire.timer
%systemd_preun innd-nntpsend.timer
%systemd_preun innd-rnews.timer

if [ $1 = 0 ]; then
    if [ -f /var/lib/news/history.dir ]; then
       rm -f /var/lib/news/history.*
    fi
fi

%postun
%systemd_postun_with_restart innd.service

%systemd_postun_with_restart innd-expire.timer
%systemd_postun_with_restart innd-nntpsend.timer
%systemd_postun_with_restart innd-rnews.timer

%postun libs -p /sbin/ldconfig

%files
%defattr(0755,news,news,-)
%{_bindir}/rnews
%defattr(0755,root,root,-)
# /etc config files plus config
%{_unitdir}/innd.service
%{_unitdir}/innd-expire.service
%{_unitdir}/innd-expire.timer
%{_unitdir}/innd-nntpsend.service
%{_unitdir}/innd-nntpsend.timer
%{_unitdir}/innd-rnews.service
%{_unitdir}/innd-rnews.timer
%defattr(-,news,news,-)
# tmpfile.d files
%{_tmpfilesdir}/inn.conf
%dir %{_localstatedir}/run/news
# /etc/news config files
%dir %{_sysconfdir}/news
%config(noreplace) %{_sysconfdir}/news/passwd.nntp
%config(noreplace) %{_sysconfdir}/news/send-uucp.cf
%config(noreplace) %{_sysconfdir}/news/actsync.cfg
%config(noreplace) %{_sysconfdir}/news/motd.innd.sample
%config(noreplace) %{_sysconfdir}/news/motd.nnrpd.sample
%config(noreplace) %{_sysconfdir}/news/expire.ctl
%config(noreplace) %{_sysconfdir}/news/actsync.ign
%config(noreplace) %{_sysconfdir}/news/innreport.conf
%config(noreplace) %{_sysconfdir}/news/distrib.pats
%config(noreplace) %{_sysconfdir}/news/buffindexed.conf
%config(noreplace) %{_sysconfdir}/news/innwatch.ctl
%config(noreplace) %{_sysconfdir}/news/nntpsend.ctl
%config(noreplace) %{_sysconfdir}/news/innfeed.conf
%config(noreplace) %{_sysconfdir}/news/nnrpd.track
%config(noreplace) %{_sysconfdir}/news/control.ctl.local
%config(noreplace) %{_sysconfdir}/news/storage.conf
%config(noreplace) %{_sysconfdir}/news/moderators
%config(noreplace) %{_sysconfdir}/news/news2mail.cf
%config(noreplace) %{_sysconfdir}/news/cycbuff.conf
%config(noreplace) %{_sysconfdir}/news/subscriptions
%config(noreplace) %{_sysconfdir}/news/control.ctl
%config(noreplace) %{_sysconfdir}/news/localgroups
%config(noreplace) %{_sysconfdir}/news/.profile
%config(noreplace) %{_sysconfdir}/news/nocem.ctl
%config(noreplace) %{_sysconfdir}/news/incoming.conf
%config(noreplace) %{_sysconfdir}/news/inn-radius.conf
%config(noreplace) %{_sysconfdir}/news/ovdb.conf
%config(noreplace) %{_sysconfdir}/news/newsfeeds
%config(noreplace) %{_sysconfdir}/news/readers.conf
%config(noreplace) %{_sysconfdir}/news/distributions

%dir %{_sharedstatedir}/news
%config(noreplace) %{_sharedstatedir}/news/active.times
%config(noreplace) %{_sharedstatedir}/news/distributions
%config(noreplace) %{_sharedstatedir}/news/newsgroups
%config(noreplace) %{_sharedstatedir}/news/active
%config(noreplace) %{_sharedstatedir}/news/subscriptions
%config(noreplace) %{_sharedstatedir}/news/history

%config(noreplace) %{_sysconfdir}/news/innshellvars.pl.local
%config(noreplace) %{_sysconfdir}/news/innshellvars.local
%config(noreplace) %{_sysconfdir}/news/innshellvars.tcl.local

%defattr(0755,root,news,-)
%dir %{_libexecdir}/news
%{_libexecdir}/news/controlbatch
%attr(4510,root,news) %{_libexecdir}/news/innbind
%{_libexecdir}/news/docheckgroups
%{_libexecdir}/news/imapfeed
%{_libexecdir}/news/send-nntp
%{_libexecdir}/news/actmerge
%{_libexecdir}/news/ovdb_server
%{_libexecdir}/news/filechan
%{_libexecdir}/news/ninpaths
%{_libexecdir}/news/mod-active
%{_libexecdir}/news/news2mail
%{_libexecdir}/news/innconfval
%{_libexecdir}/news/shlock
%{_libexecdir}/news/nnrpd
%{_libexecdir}/news/controlchan
%{_libexecdir}/news/procbatch
%{_libexecdir}/news/expire
%{_libexecdir}/news/convdate
%{_libexecdir}/news/pullnews
%{_libexecdir}/news/archive
%{_libexecdir}/news/cnfsstat
%{_libexecdir}/news/grephistory
%{_libexecdir}/news/send-ihave
%{_libexecdir}/news/tinyleaf
%{_libexecdir}/news/cvtbatch
%{_libexecdir}/news/expirerm
%{_libexecdir}/news/rc.news
%attr(4550,uucp,news) %{_libexecdir}/news/rnews
%{_libexecdir}/news/innxmit
%{_libexecdir}/news/actsyncd
%{_libexecdir}/news/shrinkfile
%{_libexecdir}/news/makedbz
%{_libexecdir}/news/actsync
%{_libexecdir}/news/pgpverify
%{_libexecdir}/news/inndf
%{_libexecdir}/news/scanlogs
%{_libexecdir}/news/simpleftp
%{_libexecdir}/news/ovdb_init
%{_libexecdir}/news/ctlinnd
%{_libexecdir}/news/innstat
%{_libexecdir}/news/send-uucp
%{_libexecdir}/news/buffchan
%{_libexecdir}/news/perl-nocem
%{_libexecdir}/news/scanspool
%{_libexecdir}/news/expireover
%{_libexecdir}/news/batcher
%{_libexecdir}/news/fastrm
%{_libexecdir}/news/innmail
%{_libexecdir}/news/innxbatch
%{_libexecdir}/news/buffindexed_d
%{_libexecdir}/news/nntpget
%{_libexecdir}/news/cnfsheadconf
%{_libexecdir}/news/ovdb_stat
%{_libexecdir}/news/prunehistory
%{_libexecdir}/news/innreport
%attr(0644,root,news) %{_libexecdir}/news/innreport_inn.pm
%{_libexecdir}/news/getlist
%{_libexecdir}/news/innd
%{_libexecdir}/news/innupgrade
%{_libexecdir}/news/news.daily
%{_libexecdir}/news/sm
%{_libexecdir}/news/innwatch
%{_libexecdir}/news/inncheck
%{_libexecdir}/news/writelog
%{_libexecdir}/news/signcontrol
%{_libexecdir}/news/tdx-util
%{_libexecdir}/news/tally.control
%{_libexecdir}/news/overchan
%{_libexecdir}/news/sendinpaths
%{_libexecdir}/news/makehistory
%{_libexecdir}/news/nntpsend
%{_libexecdir}/news/mailpost
%{_libexecdir}/news/innfeed
%{_libexecdir}/news/ovdb_monitor
%{_libexecdir}/news/sendxbatches

%define filterdir %{_libexecdir}/news/filter
%dir %{filterdir}
%{filterdir}/filter_nnrpd.pl
%{filterdir}/nnrpd_access.pl
%{filterdir}/startup_innd.pl
%{filterdir}/nnrpd_auth.py*
%{filterdir}/nnrpd_access.py*
%{filterdir}/nnrpd_auth.pl
%{filterdir}/INN.py*
%{filterdir}/nnrpd.py*
%{filterdir}/filter_innd.py*
%{filterdir}/nnrpd_dynamic.py*

%define authdir %{_libexecdir}/news/auth
%{authdir}/

%define resolvdir %{authdir}/resolv
%dir %{resolvdir}
%{resolvdir}/domain
%{resolvdir}/ident

%define controldir %{_libexecdir}/news/control
%dir %{controldir}
%{controldir}/version.pl
%{controldir}/ihave.pl
%{controldir}/sendsys.pl
%{controldir}/sendme.pl
%{controldir}/checkgroups.pl
%{controldir}/senduuname.pl
%{controldir}/newgroup.pl
%{controldir}/rmgroup.pl

%define rnewsdir %{_libexecdir}/news/rnews.libexec
%dir %{rnewsdir}
%{rnewsdir}/encode
%{rnewsdir}/gunbatch
%{rnewsdir}/decode
%{rnewsdir}/bunbatch
%{rnewsdir}/c7unbatch

%{_libexecdir}/news/innshellvars.pl
%{_libexecdir}/news/innshellvars
%{_libexecdir}/news/innshellvars.tcl

%attr(0775,root,news) %dir %{_sharedstatedir}/news/http
%{_sharedstatedir}/news/http/innreport.css

%dir %{perl_vendorlib}/INN
%{perl_vendorlib}/INN/Config.pm
%{perl_vendorlib}/INN/Utils/Shlock.pm

%defattr(-,news,news,-)
%dir /var/spool/news
%dir /var/spool/news/archive
%dir /var/spool/news/articles
%attr(0775,news,news) %dir /var/spool/news/incoming
%attr(0775,news,news) %dir /var/spool/news/incoming/bad
%dir /var/spool/news/innfeed
%dir /var/spool/news/outgoing
%dir /var/spool/news/overview
%dir /var/log/news/OLD
%dir %{_sharedstatedir}/news/tmp
%ghost %dir /run/news
%defattr(-,root,root,-)
%{_mandir}/man1/c*.1.gz
%{_mandir}/man1/f*.1.gz
%{_mandir}/man1/g*.1.gz
%{_mandir}/man1/inn*.1.gz
%{_mandir}/man1/n*.1.gz
%{_mandir}/man1/p*.1.gz
%{_mandir}/man1/r*.1.gz
%{_mandir}/man1/s*.1.gz
%{_mandir}/man[58]/*
%defattr(-,root,root,0755)
%doc NEWS README* HACKING ChangeLog CONTRIBUTORS LICENSE INSTALL FAQ.html 
%doc doc/config-design doc/history-innfeed doc/GPL doc/sample-control
%doc doc/config-semantics doc/external-auth TODO doc/hook-python doc/config-syntax
%doc doc/hook-perl doc/history
%doc samples

%files libs
%defattr(-,root,root,-)
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/inn/
%{_includedir}/inn/*
%{_libdir}/lib*.so
%{_mandir}/man3/*

%files -n inews
%defattr(-,root,root,-)
%config(noreplace) %attr(-,news,news) %{_sysconfdir}/news/inn.conf
%{_bindir}/inews
%attr(0755,root,root) %{_libexecdir}/news/inews
%{_mandir}/man1/inews*

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 2.6.0-0.rc1.1.5
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 2.6.0-0.rc1.1.4
- 为 Magic 3.0 重建

* Sun Oct 11 2015 Liu Di <liudidi@gmail.com> - 2.6.0-0.rc1.1.3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-0.rc1.1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.6.0-0.rc1.1.1
- Perl 5.22 rebuild

* Thu May 07 2015 Dan Horák <dan[at]danny.cz> - 2.6.0-0.rc1.1
- workaround ssize_t detection

* Tue Apr 21 2015 Jochen Schmitt <Jochen herr-schmitt de> - 2.6.0-0.rc1
- New upstream release

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.5.4-3
- Perl 5.20 rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 15 2014 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.4-1
- New upstream release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Jan  4 2014 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.3-18
- User systemd scriptlets rpm macros for timers

* Thu Jan  2 2014 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.3-17
- Add a delay for the systemd timers on boot
- Avoid warning when stopping timers during update
- Stricter Req. in inn-devel subpackage

* Sun Dec 29 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.3-16
- Additional rework on the systemd timer files

* Sun Dec 29 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.3-15
- Rework ystemd timer handling (#1046960)

* Sat Dec 14 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.3-14
- Fix typo in innd-nntpsend.service (#1043126)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.5.3-12
- Perl 5.18 rebuild

* Tue May 28 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.3-11
- Fix typos in the posix patch (hint from upstream)

* Tue May 21 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.3-10
- Building package with PIE flags (#965502)
- Fix issue with recent pod2man releases

* Sun Feb 24 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.3-9
- Fix name conflict with libradius

* Fri Jan 25 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.3-8
- Timer service units have to been enabled also

* Wed Jan 23 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.3-7
- Using of %%{_tmpfilesdir} instaead of %%{_sysconfdir}/tmpfiles.d/
- Disable SMP build due an SMP-related issue
- Rework for the systemd timers. They will been enabled and started after install

* Tue Jan 22 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.3-6
- Fix some issues with the systemd timer units

* Wed Jan 16 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.3-5
- Migrating from cron to systemd timer
- Change %%doc %%dir into %%doc

* Fri Oct  5 2012 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.3-4
- Introduction of systemd rpm macros

* Tue Sep 11 2012 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.3-3
- New release is SMP compilant

* Tue Sep 11 2012 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.3-2
- Remove inn-2.5.2-hdr.patch

* Thu Sep 06 2012 Ondrej Vasik <ovasik@redhat.com> - 2.5.3-1
- new upstream release 2.5.3

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.5.2-22
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 15 2011 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.2-20
- Redirect both STDOUT and STDERR on cron.hourly

* Sun Nov 13 2011 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.2-19
- Avoid useless messages in cron.hourly (#753581)

* Wed Oct  5 2011 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.2-18
- Unghosting /var/run/news

* Wed Oct  5 2011 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.2-17
- Use tmpfiles.d to create /var/run/news
- Clean up SPEC file 

* Mon Sep 19 2011 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.2-16
- Set PATH for user news to more resticted values

* Mon Sep 19 2011 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.2-15
- Move wrong place assigments in innd.service file

* Thu Sep  1 2011 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.2-14
- Rewrite systemd.service file
- Allow login to news user account

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 2.5.2-13
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 2.5.2-12
- Perl mass rebuild

* Wed Jul 13 2011 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.2-11
- Add Condition to /etc/news/inn.conf in innd.service

* Tue Jul  5 2011 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.2-10
- Fix typo in start-inn

* Sun Jun 26 2011 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.2-9
- Initial migration to native systemd support

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.5.2-8
- Perl mass rebuild

* Tue May 31 2011 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.2-7
- Change /var/run/news to /run/news

* Mon May 30 2011 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.2-6
- Create /var/run/news in innd.init (#708627)
- This release is not SMP compilant

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 11 2010 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.2-4
- Rebuild for python-2.7 (#623322)
- Fix SMP issue in frontends

* Wed Jul 14 2010 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.2-3
- /var/run/news ghosted tmpfs

* Tue Jul  6 2010 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.2-2
- Try to fix a smp issue on innfeed/Makefile

* Mon Jun 28 2010 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.2-1
- New upstream release

* Wed Jun 2 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 2.5.1-5
- Resolves: #597799 - Two typos in /etc/init.d/inn, three typos in /etc/cron.*/inn* in F13
- Resolves: #596580 - Migration from /usr/lib/news/bin to /usr/libexec/news is not complete
- Resolves: #604473 - wrong permissions on /usr/share/doc/inn-2.5.1(Jochen@herr-schmitt.de)
- add patch inn-2.5.1-config-path.patch
- add BuildRequires: flex (Jochen@herr-schmitt.de)

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.5.1-4
- Mass rebuild with perl-5.12.0

* Wed Dec 16 2009 Nikola Pajkovsky <npajkovs@redhta.com> - 2.5.1-3
- rebuild 
- chage licence and remove on rm -f
- drop patches inn-2.4.1.perl.patch and inn-2.4.5-dynlib.patch

* Fri Dec 11 2009 Nikola Pajkovsky <npajkovs@redhat.com> - 2.5.1-2
- #225901 - Merge Review: inn

* Tue Oct 13 2009 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.1-1
- New upstream release

* Mon Sep 14 2009 Nikola Pajkovsky <npajkovs@redhat.com> - 2.5.0-5
- resolved: 511772 - inn/storage.h not self-contained, missing inn/options.h

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Nikola Pajkovsky <npajkovs@redhat.com> 2.5.0-3
- ugly sed script for file section was deleted and rewrite in classic style
- fix init script(does not start correctly and shutdown when pid does not exist when service run)

* Wed Jun 24 2009 Ondrej Vasik <ovasik@redhat.com> - 2.5.0-2
- add support for load average to makehistory(#276061)
- update faq, ship it in %%doc
- fix typo in filelist

* Tue Jun 09 2009 Ondrej Vasik <ovasik@redhat.com> - 2.5.0-1
- new upstream release 2.5.0
- remove applied and adjust modified patches

* Tue May 19 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.6-2
- reflect change in sasl_encode64 abi(null terminator) - #501452

* Wed Mar 11 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.6-1
- new bugfix upstream release 2.4.6
- no strict aliasing, remove pyo/.pyc filters files from list

* Wed Feb 25 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.5-10
- mark /usr/lib/news/lib/innshellvars* as noreplace,
  versioned provide for perl(::/usr/lib/innshellvars.pl)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.5-8
- create user/group news with reserved uidgid numbers

* Wed Jan 13 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.5-7
- fix upstream url

* Mon Dec  1 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.4.5-6
- Rebuild for Python 2.6

* Mon Dec 01 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.5-5
- do own /usr/include/inn in devel package (#473922)

* Tue Nov 25 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.5-4
- package summary tuning

* Fri Aug 29 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.5-3
- patch fuzz clean up

* Fri Jul  7 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.5-2
- do not use static libraries(changes by Jochen Schmitt,#453993)
- own all dirs spawned by inn package(#448088)

* Thu Jul  3 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.5-1
- new upstream release 2.4.5

* Tue Jun 17 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.4-3
- Add news user. fixes bug #437462
* Mon May 19 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.4-2
- add sparc arches to the list for -fPIC(Dennis Gilmore)

* Thu May 15 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.4-1
- new upstream release 2.4.4

* Thu Apr 24 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.3-14
- make /var/spool/news/incoming writable for news group
  (#426760)
- changes because of /sbin/nologin shell for news user

* Wed Apr  9 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.3-13
- few documentation changes because of /sbin/nologin shell 
  for news user (su - news -c <commmand> will not work in 
  that case ) #233738

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.4.3-12
- BuildRequires: perl(ExtUtils::Embed)

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.4.3-11
- add Requires for versioned perl (libperl.so)

* Mon Feb 11 2008 Ondrej Vasik <ovasik@redhat.com> 2.4.3-10
- again added trigger for sysklogd
- rebuild for gcc43

* Wed Jan 16 2008 Ondrej Vasik <ovasik@redhat.com> 2.4.3-9
- do not show annoying fatal log message when nonfatal error 
  eaddrinuse occured in rcreader
- use /etc/rsyslog.conf instead of /etc/syslog.conf

* Mon Jan 07 2008 Ondrej Vasik <ovasik@redhat.com> 2.4.3-8
- initscript changes - review changes caused errors while
  in stop() phase - not known variable NEWSBIN(#401241)
- added url, fixed License tag

* Tue Oct 02 2007 Ondrej Dvoracek <odvorace@redhat.com> 2.4.3-7
- initscript review (#246951)
- added buildrequires for perl-devel and python

* Tue Aug 29 2006 Martin Stransky <stransky@redhat.com> 2.4.3-6
- added dist tag
- added patch from #204371 - innd.init script should use 
  ctlinnd to stop the server

* Mon Jul 17 2006 Jesse Keating <jkeating@redhat.com> - 2.4.3-5
- rebuild

* Wed Jun 21 2006 Martin Stransky <stransky@redhat.com> 2.4.3-4
- enabled ipv6 support

* Wed Jun 07 2006 Karsten Hopp <karsten@redhat.de> 2.4.3-3
- add some buildrequirements (krb5-devel pam-devel e2fsprogs-devel)

* Sun May 28 2006 Martin Stransky <stransky@redhat.com> 2.4.3-2
- file conflicts for inn (#192689)
- added byacc to dependencies (#193402)

* Mon Mar 27 2006 Martin Stransky <stransky@redhat.com> 2.4.3-1
- new upstream

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.4.2-4.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.4.2-4.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Aug 02 2005 Karsten Hopp <karsten@redhat.de> 2.4.2-4
- rebuild with current rpm
- include .pyc and pyo files created by /usr/lib/rpm/brp-python-bytecompile

* Thu Apr  7 2005 Martin Stransky <stransky@redhat.com> 2.4.2-3
- add support for large files

* Mon Mar  7 2005 Martin Stransky <stransky@redhat.com>
- rebuilt

* Tue Jan 11 2005 Martin Stransky <stransky@redhat.com> 2.4.2-1
- fix file conflict between inews and inn packages (#51607)
- update to 2.4.2
- thanks to Jochen Schmitt <Jochen@herr-schmitt.de>

* Thu Dec 23 2004 Martin Stransky <stransky@redhat.com> 2.4.1-2
- fix array overflow / uninitialized pointer (#143592)

* Wed Dec 15 2004 Martin Stransky <stransky@redhat.com> 2.4.1-1
- diff patch (fix obsolete version of diff parameter) #137342
- posix/warnings patch #110825

* Mon Dec 13 2004 Martin Stransky <stransky@redhat.com> 2.4.1-1
- update to INN 2.4.1
- Thanks to Jochen Schmitt <Jochen@herr-schmitt.de>

* Tue Oct  5 2004 Thomas Woerner <twoerner@redhat.com> 2.3.5-11.1
- using runuser instead of su in cronjobs

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 17 2004 Thomas Woerner <twoerner@redhat.com> 2.3.5-10
- compiling server and suid programs PIE

* Tue Apr  6 2004 Thomas Woerner <twoerner@redhat.com> 2.3.5-9
- /etc/rc.d/init.d/innd is owned by root now (#119131)

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com>
- Use ':' instead of '.' as separator for chown.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 29 2004 Thomas Woerner <twoerner@redhat.com> 2.3.5-7
- using db-4.2

* Mon Jul 14 2003 Chip Turner <cturner@redhat.com>
- rebuild for new perl 5.8.1

* Thu Jul 03 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- recompile for other thingy

* Wed Jun 11 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- link against db-4.1  #92420
- use correct optims settings from rpm  #92410
- install with other perms to allow debuginfo stripping #92412

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 30 2003 Ellito Lee <sopwith@redhat.com> 2.3.5-2
- headusage patch for ppc64 etc.

* Sun Mar 30 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- 2.3.5 update

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Jan 17 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to current bug-fix release

* Fri Jan 03 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- do not require cleanfeed  #80124

* Tue Dec 17 2002 Phil Knirsch <pknirsch@redhat.com> 2.3.3-9
- Fixed changelog entries containing percent sections.

* Tue Dec 03 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- do not link against -lelf

* Thu Nov  7 2002 Tim Powers <timp@redhat.com>
- rebuilt to fix unsatisfied dependencies
- pass _target_platform when configuring

* Tue Jul 23 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix cron scripts to use correct paths #69189
- add compat symlinks for rnews/inews into /usr/bin

* Thu Jul 18 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- make check if networking is up more robust in initscript
- move most apps into /usr/lib/news/bin for less namespace pollution

* Tue Jun 18 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add some cvs patches
- crude hack to change LOCK_READ and LOCK_WRITE within INN source code

* Mon May 27 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to inn-2.3.3
- use db4

* Mon Apr 15 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- put /etc/news/inn.conf into the inews subpackage to make a smaller
  client side possible and require inews from the main inn rpm

* Mon Apr 08 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- startup and cron scripts unset LANG and LC_COLLATE to make
  inn more robust   (#60770)
- really link against db3
- inews requires inn #59852

* Thu Feb 28 2002 Elliot Lee <sopwith@redhat.com> 2.3.2-10
- Change db4-devel requirement to db3-devel.
- Use _smp_mflags

* Thu Jan 31 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix #59123

* Wed Jan 30 2002 Jeff Johnson <jbj@redhat.com>
- white out bogus perl requirement for now.
- don't include <db1/ndbm.h> to avoid linking with -ldb1.

* Sat Jan 26 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- change to db4

* Sun Jan 20 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- allow rebuilding by not using newer autoconf, adjust inn patches

* Tue Jul 24 2001 Tim Powers <timp@redhat.com>
- make inews owned by root, not the build system

* Tue Jul 24 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fix badd attr() macro

* Sat Jul 21 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add build req

* Fri Jul 06 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- change perms on inews

* Tue Jun 19 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.3.2

* Wed Feb 14 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add startup script patch by kevin@labsysgrp.com #27421
- inews subpackage does not depend on inn anymore #24439
- fix reload and make some cleanups to the startup script #18076

* Wed Feb 07 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add a "exit 0" to the postun script

* Wed Jan 24 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.3.1
- do not use --enable-tagged-hash
- move tmp dir to /var/lib/news/tmp
- add more docu
- do not call "strip" directly
- remove some of the default files as the ones in INN are ok
- do not req /etc/init.d
- do not attempt an automatic update from previous versions as
  we have to deal with different storage methods
- prepare startup script for translations
- add minimal check into startup for a history file

* Mon Jan 22 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- innreport had wrong perms
- files for the cron-jobs must be owned by root:root

* Tue Aug 29 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- remove cleanfeed sources

* Mon Jul 24 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- fix some perms

* Mon Jul 24 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.2.3
- fixed many perms
- cleaned up complete build process

* Sat Jul 15 2000 Bill Nottingham <notting@redhat.com>
- move initscript back

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jul 10 2000 Bill Nottingham <notting@redhat.com>
- add fix for the verifycancels problem fron Russ Allbery
- turn them off anyways
- fix perms on inews

* Sat Jul  8 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- prereq init.d

* Tue Jun 27 2000 Than Ngo <than@redhat.de>
- /etc/rc.d/init.d -> /etc/init.d
- fix initscript

* Sun Jun 25 2000 Matt Wilson <msw@redhat.com>
- defattr root

* Wed Jun 21 2000 Preston Brown <pbrown@redhat.com>
- fix up some issues with our new gcc compiler (patch 6)
- don't do chown in the install script so we can build as nonroot

* Mon Jun 19 2000 Preston Brown <pbrown@redhat.com>
- FHS mandir

* Tue May 23 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- add inn-2.2.2-rnews.patch which is also accepted in current cvs

* Mon May 22 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- fix stupid bug in rnews cronjob
- enable controlchan in default newsfeeds config
- run "rnews -U" hourly instead of daily

* Fri May 19 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- add bug-fix to batcher from cvs version
- "su news" before starting rnews from cron

* Mon Apr  3 2000 Bill Notttingham <notting@redhat.com>
- arrgh, there is no /usr/lib/news anymore. (#10536)
- pppatch ppport for ppproper ppperl

* Thu Mar 02 2000 Cristian Gafton <gafton@redhat.com>
- remove useless filter_innd.pl so that we will get the cleanfeed one
  instead

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages
- other minor fixes

* Tue Dec 14 1999 Bill Nottingham <notting@redhat.com>
- update to 2.2.2

* Sun Aug 29 1999 Cristian Gafton <gafton@redhat.com>
- version 2.2.1 to fix security problems in previous inn versions
- add the faq back to the source rpm

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging

* Tue Jun 22 1999 Jeff Johnson <jbj@redhat.com>
- fix syntax error in reload (#3636).

* Fri Jun 18 1999 Bill Nottingham <notting@redhat.com>
- don't run by default

* Sun Jun 13 1999 Jeff Johnson <jbj@redhat.com>
- mark /var/lib/news/* as config(noreplace) (#3425)

* Thu Jun 10 1999 Dale Lovelace <dale@redhat.com>
- change su news to su - news (#3331)

* Wed Jun  2 1999 Jeff Johsnon <jbj@redhat.com>
- complete trn->inews->inn dependency (#2646)
- use f_bsize rather than f_frsize when computing blocks avail (#3154).
- increase client timeout to 30 mins (=1800) (#2833).
- add missing includes to inn-devel (#2904).

* Mon May 31 1999 Jeff Johnson <jbj@redhat.com>
- fix owner and permissions on /var/lib/news/.news.daily (#2354).

* Tue Mar 30 1999 Preston Brown <pbrown@redhat.com>
- fixed paths in cron jobs, check to see that innd is enabled

* Fri Mar 26 1999 Preston Brown <pbrown@redhat.com>
- path to makehistory corrected.

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- fixed permissions on rnews for uucp

* Fri Mar 19 1999 Preston Brown <pbrown@redhat.com>
- make sure init scripts get packaged up, fix other minor bugs
- major fixups to innd.conf for denial of service attacks, sanity, etc.
- make sure history gets rebuilt in an upgrade (added to post section)
- many thanks go out to mmchen@minn.net for these suggestions.

* Fri Feb 19 1999 Cristian Gafton <gafton@redhat.com>
- prereq all the stuff we need in the postinstall scripts

* Sat Feb  6 1999 Bill Nottingham <notting@redhat.com>
- strip -x bits from docs/samples (bogus dependencies)

* Thu Sep 03 1998 Cristian Gafton <gafton@redhat.com>
- updated to version 2.1

* Fri Aug 21 1998 Jeff Johnson <jbj@redhat.com>
- innd.init chkconfig entry was incorrect (problem #855)

* Tue Jun 30 1998 Jeff Johnson <jbj@redhat.com>
- susbsys name must be identical to script name (problem #700)

* Mon Jun 29 1998 Bryan C. Andregg <bandregg@redhat.com>
- fixed startinnfeed paths

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- enhanced initscript

* Fri May 01 1998 Cristian Gafton <gafton@redhat.com>
- fixed innfeed patched to be perl-version independent

* Wed Apr 15 1998 Bryan C. Andregg <bandregg@redhat.com>
- fixed sfnet.* entries in control.ctl

* Mon Apr 13 1998 Bryan C. Andregg <bandregg@redhat.com>
- moved cleanfeed to its own package

* Thu Apr 09 1998 Bryan C. Andregg <bandregg@redhat.com>
- added insync patches
- added cleanfeed
- added innfeed

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- abuse buildroot to simplify the file list
- built against Manhattan

* Tue Mar 24 1998 Bryan C. Andregg <bandregg@redhat.com>
- updated to inn 1.7.2
- Added REMEMBER_TRASH and Poison patch

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- updated to inn 1.7
- added chkconfig support to the initscripts
- orginally released as release 2, leving release 1 if a 4.2.x upgrade
  is ever necessary 
- don't start it in any runlevel (by default)
- added inndcomm.h

* Thu Oct 09 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Aug 05 1997 Elliot Lee <sopwith@redhat.com>
- Applied the 1.5.1sec and 1.5.1sec2 patches
- Applied 3 more unoff patches.
- Removed insanity in /etc/cron.hourly/inn-cron-nntpsend, it now
  just runs nntpsend as news.

* Wed Apr 02 1997 Erik Troan <ewt@redhat.com>
- Patch from CERT for sh exploit.
- Changed /usr/ucb/compress reference to /usr/bin/compress

* Mon Mar 17 1997 Erik Troan <ewt@redhat.com>
- Removed inews.1 from main inn package (it's still in the inews packaeg)
- Fixed references to /usr/spoo in sendbatch
- added "-s -" to crosspost line in newsfeeds
- /var/lib/news/active.time is now created as news.news
- /etc/news/nnrp.access and /etc/news/nntpsend.ctl are mode 0440 
- included a better rc script which does a better job of shutting down news
- updated /etc/rc.d/rc.news output look like the rest of our initscripts
- hacked sendbatch df stuff to work on machines w/o a separate /var/spool/news

* Tue Mar 11 1997 Erik Troan <ewt@redhat.com>
- added chmod to make sure rnews is 755
- /etc/news/nnrp.access and /etc/news/nntpsend.ctl are news.news not root.news
  or root.root
- install an empty /var/lib/news/.news.daily as a config file
- added dbz/dbz.h as /usr/include/dbz.h
- added /usr/bin/inews link to /usr/lib/news/inews
- changed INEWS_PATH to DONT -- I'm not sure this is right though
- turned off MMAP_SYNC
- added a ton of man pages which were missing from the filelist
- increased CLIENT_TIMEOUT to (30 * 60)
- added a postinstall to create /var/lib/news/active.times if it doesn't
  already exist
- patched rc.news to start inn w/ -L flag
- pulled news.init into a separate source file rather then creating it through
  a patch
- added /etc/rc.d/rc5.d/S95news to the file list
- remove pid files from /var/lock/news/* on shutdown
- use /var/lock/subsys/news rather then /var/lock/subsys/inn or things
  don't shutdown properly

* Mon Mar 10 1997 Christian 'Dr. Disk' Hechelmann <drdisk@ds9.au.s.shuttle.de>
- changed devel package description to include tin.
- the devel package missed libinn.h
- moved libinn.3 man-page to the devel package
- moved changelog up
- in post some echo statements were messed up. if we put the redirection
  staements in a different line than the echo command we really should use
  a backslash to thell the shell :-)
- in install a chmod line referenced the same directory twice.
- changed inn-1.5.1-redhat.patch: The patch for news.daily had a side effect.
  as EXPIREOVERFLAGS was set to '-a', expireover would break if there were
  articles to be removed, as '-a' can't be used if '-z' is specified...
  Now there is a separate 'eval expireover -a' after the first eval. Dirty
  but works.

* Wed Feb 26 1997 Erik Troan <ewt@redhat.com>
- Added a /usr/bin/rnews symlink to /usr/lib/news/rnews as other programs like
  to use it.

* Tue Feb 25 1997 Elliot Lee <sopwith@cuc.edu>
- Fixed rnews path in /etc/cron.daily/inn-cron-rnews
- Added overview! and crosspost lines to /etc/news/newsfeeds
- Fixed nntpsend.ctl path in /usr/lib/news/bin/nntpsend, and set a saner
  nntpsend.ctl config file.
- Added automated inn.conf 'server: ' line creation in post
- Added misc. patches from ftp.isc.org/isc/inn/unoff-patches/1.5
- Removed -lelf from config.data LIBS
- Made RPM_OPT_FLAGS work.
- Bug in rpm meant that putting post after files made it not run. Moved
  post up.
- Added /etc/cron.hourly/inn-cron-nntpsend to send news every hour.
- Fixed most of the misc permissions/ownership stuff that inncheck
  complained about.

* Wed Feb 19 1997 Erik Troan <ewt@redhat.com>
- Incorporated changes from <drdisk@tilx01.ti.fht-esslingen.de> which fixed
  some paths and restored the cron jobs which disappeared in the 1.5.1
  switch. He also made the whole thing use a buildroot and added some files
  which were missing from the file list.

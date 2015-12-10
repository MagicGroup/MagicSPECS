%define _vararpwatch %{_localstatedir}/lib/arpwatch

Name: arpwatch
Epoch: 14
Version: 2.1a15
Release: 21%{?dist}
Summary: Network monitoring tools for tracking IP addresses on a network
Summary(zh_CN.UTF-8): 在网络中跟踪IP地址的网络监视工具
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
License: BSD with advertising
URL: http://ee.lbl.gov/
Requires(pre): shadow-utils 
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires: /usr/sbin/sendmail
BuildRequires: /usr/sbin/sendmail libpcap-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: ftp://ftp.ee.lbl.gov/arpwatch-%{version}.tar.gz
Source1: arpwatch.service
Source2: arpwatch.sysconfig
# created by:
# wget -O- http://standards.ieee.org/regauth/oui/oui.txt | \
# iconv -f iso8859-1 -t utf8 | massagevendor | bzip2
Source3: ethercodes-20110707.dat.bz2
Patch1: arpwatch-2.1a4-fhs.patch
Patch2: arpwatch-2.1a10-man.patch
Patch3: arpwatch-drop.patch
Patch4: arpwatch-drop-man.patch
Patch5: arpwatch-addr.patch
Patch6: arpwatch-dir-man.patch
Patch7: arpwatch-scripts.patch
Patch8: arpwatch-2.1a15-nolocalpcap.patch
Patch9: arpwatch-2.1a15-bogon.patch
Patch10: arpwatch-2.1a15-extraman.patch
Patch11: arpwatch-exitcode.patch

%description
The arpwatch package contains arpwatch and arpsnmp.  Arpwatch and
arpsnmp are both network monitoring tools.  Both utilities monitor
Ethernet or FDDI network traffic and build databases of Ethernet/IP
address pairs, and can report certain changes via email.

Install the arpwatch package if you need networking monitoring devices
which will automatically keep track of the IP addresses on your
network.

%description -l zh_CN.UTF-8
arpwathc包包含了 arpwatch 和 arpsnmp。Arpwath 和 arpsmp 都是网络监视工具。
工具都能监视以太网或FDDI网络流量，并且建立关于 Ethernet/IP 地址对的数据库。
同时可以通过电子邮件发送这些的更改。
 
如果你需要监视网络设备以便自动保持IP地址安装 arpwatch 包。

%prep
%setup -q

%patch1 -p1 -b .fhs
%patch2 -p1 -b .arpsnmpman
%patch3 -p1 -b .droproot
%patch4 -p0 -b .droprootman
%patch5 -p1 -b .mailuser
%patch6 -p1 -b .dirman
%patch7 -p1 -b .scripts
%patch8 -p1 -b .nolocalpcap
%patch9 -p1 -b .bogon
%patch10 -p1 -b .extraman
%patch11 -p1 -b .exitcode

%build
%configure
make ARPDIR=%{_vararpwatch}

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_vararpwatch}
mkdir -p $RPM_BUILD_ROOT/lib/systemd/system
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig

make DESTDIR=$RPM_BUILD_ROOT install install-man

# prepare awk scripts
perl -pi -e "s/\'/\'\\\'\'/g" *.awk

# and embed them
for i in arp2ethers massagevendor massagevendor-old; do
	cp -f $i $RPM_BUILD_ROOT%{_sbindir}
	for j in *.awk; do
		sed "s/-f\ *\(\<$j\>\)/\'\1\n\' /g" \
			< $RPM_BUILD_ROOT%{_sbindir}/$i \
			| sed "s/$j\$//;tx;b;:x;r$j" \
			> $RPM_BUILD_ROOT%{_sbindir}/$i.x
		mv -f $RPM_BUILD_ROOT%{_sbindir}/$i{.x,}
	done
	chmod 755 $RPM_BUILD_ROOT%{_sbindir}/$i
done

install -p -m644 *.dat $RPM_BUILD_ROOT%{_vararpwatch}
install -p -m644 %{SOURCE1} $RPM_BUILD_ROOT/lib/systemd/system/arpwatch.service
install -p -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/arpwatch
install -p -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_vararpwatch}/ethercodes.dat.bz2
bzip2 -df $RPM_BUILD_ROOT%{_vararpwatch}/ethercodes.dat.bz2

rm -f $RPM_BUILD_ROOT%{_sbindir}/massagevendor-old

%clean
rm -rf $RPM_BUILD_ROOT

%post
/bin/systemctl daemon-reload &> /dev/null
:

%pre
if ! getent group arpwatch &> /dev/null; then
	getent group pcap 2> /dev/null | grep -q 77 &&
		/usr/sbin/groupmod -n arpwatch pcap 2> /dev/null ||
		/usr/sbin/groupadd -g 77 arpwatch 2> /dev/null
fi
if ! getent passwd arpwatch &> /dev/null; then
	getent passwd pcap 2> /dev/null | grep -q 77 &&
		/usr/sbin/usermod -l arpwatch -g 77 \
			-d %{_vararpwatch} pcap 2> /dev/null ||
		/usr/sbin/useradd -u 77 -g 77 -s /sbin/nologin \
			-M -r -d %{_vararpwatch} arpwatch 2> /dev/null
fi
:

%postun
/bin/systemctl daemon-reload &> /dev/null
if [ "$1" -ge 1 ]; then
	/bin/systemctl try-restart arpwatch.service &> /dev/null
fi
:

%preun
if [ "$1" -eq 0 ]; then
	/bin/systemctl --no-reload disable arpwatch.service &> /dev/null
	/bin/systemctl stop arpwatch.service &> /dev/null
fi
:

%files
%defattr(-,root,root)
%doc README CHANGES arpfetch
%{_sbindir}/arpwatch
%{_sbindir}/arpsnmp
%{_sbindir}/arp2ethers
%{_sbindir}/massagevendor
%{_mandir}/man8/*.8*
/lib/systemd/system/arpwatch.service
%config(noreplace) %{_sysconfdir}/sysconfig/arpwatch
%defattr(-,arpwatch,arpwatch)
%dir %{_vararpwatch}
%verify(not md5 size mtime) %config(noreplace) %{_vararpwatch}/arp.dat
%verify(not md5 size mtime) %config(noreplace) %{_vararpwatch}/ethercodes.dat

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 14:2.1a15-21
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 14:2.1a15-20
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 14:2.1a15-18
- 为 Magic 3.0 重建

* Mon Oct 31 2011 Liu Di <liudidi@gmail.com> - 14:2.1a15-17
- 移植到 systemd


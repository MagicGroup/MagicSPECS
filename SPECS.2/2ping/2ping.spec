Name:           2ping
Version:        2.0
Release:        8%{?dist}
Summary:        Bi-directional ping utility
Summary(zh_CN.UTF-8): 双向 ping 工具
License:        GPLv2+
URL:            http://www.finnie.org/software/2ping
Source0:        http://www.finnie.org/software/%{name}/%{name}-%{version}.tar.gz
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Digest::CRC)
Requires:       perl(Digest::MD5)
Requires:       perl(Digest::SHA)
Requires:       perl(IO::Socket::INET6)
BuildArch:      noarch

%description
2ping is a bi-directional ping utility. It uses 3-way pings (akin to TCP SYN, 
SYN/ACK, ACK) and after-the-fact state comparison between a 2ping listener 
and a 2ping client to determine which direction packet loss occurs.

%description -l zh_CN.UTF-8
2ping是一个双向 ping 工具。它采用 3 种方式 ping（即TCP SYN， 
SYN / ACK，ACK），然后通过 2ping 接受者和客户端之间的状态比
较确定哪个方向丢包。

%prep
%setup -q

%build
make EXTRAVERSION=-%{release} %{?_smp_mflags}

%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot}

%files
%doc ChangeLog COPYING README
%{_bindir}/2ping
%{_bindir}/2ping6
%{_mandir}/man8/2ping.8*
%{_mandir}/man8/2ping6.8*

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 2.0-8
- 为 Magic 3.0 重建

* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 2.0-7
- 为 Magic 3.0 重建

* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 2.0-6
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 2.0-5
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 2.0-4
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.0-3
- 为 Magic 3.0 重建

* Mon Jan 27 2014 Liu Di <liudidi@gmail.com> - 2
- 新包

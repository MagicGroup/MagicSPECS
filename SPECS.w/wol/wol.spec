Name:           wol
Version:        0.7.1
Release:        15%{?dist}
Summary:        Wake On Lan client
Summary(zh_CN.UTF-8): 网络唤醒客户端

Group:          Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
License:        GPLv2+
URL:            http://sourceforge.net/projects/wake-on-lan/
Source0:        http://downloads.sourceforge.net/wake-on-lan/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gettext
BuildRequires:  perl-podlators

Requires(post):  /sbin/install-info
Requires(preun): /sbin/install-info

%description
wol implements Wake On LAN functionality in a small program. It wakes up
hardware that is Magic Packet compliant. SecureON is supported by wol too.

%description -l zh_CN.UTF-8
通过网络远程打开计算机。

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}
iconv -f iso8859-1 -t utf-8 ChangeLog > ChangeLog.conv
touch -c -r ChangeLog ChangeLog.conv
mv ChangeLog.conv ChangeLog

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"
rm -f %{buildroot}%{_infodir}/dir
magic_rpm_clean.sh 
%find_lang %{name} || :

%clean
rm -rf %{buildroot}

%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :

%preun
if [ "$1" = 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi

%files 
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_infodir}/%{name}.info.gz
%{_mandir}/man?/*.*
%{_bindir}/%{name}*

%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 0.7.1-15
- 为 Magic 3.0 重建

* Tue Oct 20 2015 Liu Di <liudidi@gmail.com> - 0.7.1-14
- 为 Magic 3.0 重建

* Sat Sep 13 2014 Liu Di <liudidi@gmail.com> - 0.7.1-13
- 为 Magic 3.0 重建

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 01 2013 Fabian Affolter <mail@fabian-affolter.ch> - 0.7.1-10
- BR fixed for building man page

* Tue Feb 19 2013 Fabian Affolter <mail@fabian-affolter.ch> - 0.7.1-9
- Minor spec file updates

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 07 2008 Fabian Affolter <mail@fabian-affolter.ch> - 0.7.1-2
- Fix Source0
- Fix License

* Sat Dec 06 2008 Fabian Affolter <mail@fabian-affolter.ch> - 0.7.1-1
- Initial package for Fedora

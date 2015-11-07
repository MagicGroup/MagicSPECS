Summary: Fast anti-spam filtering by Bayesian statistical analysis
Summary(zh_CN): 使用贝叶斯统计分析的快速反垃圾过滤器
Name: bogofilter
Version: 1.2.4
Release: 3%{?dist}
License: GPLv2
Group: Applications/Internet
Group(zh_CN): 应用程序/互联网
URL: http://bogofilter.sourceforge.net/
Source: http://downloads.sourceforge.net/bogofilter/bogofilter-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: flex libdb-devel gsl-devel
BuildRequires: /usr/bin/iconv

%description
Bogofilter is a Bayesian spam filter.  In its normal mode of
operation, it takes an email message or other text on standard input,
does a statistical check against lists of "good" and "bad" words, and
returns a status code indicating whether or not the message is spam.
Bogofilter is designed with fast algorithms (including Berkeley DB system),
coded directly in C, and tuned for speed, so it can be used for production
by sites that process a lot of mail.

%description -l zh_CN
使用贝叶斯统计分析的快速反垃圾过滤器．

%package bogoupgrade
Summary: Upgrades bogofilter database to current version
Summary(zh_CN): 升级 %name 的数据库到当前版本
Group: Applications/Internet
Group(zh_CN): 应用程序/互联网
Provides: bogoupgrade
Requires: %{name} = %{version}-%{release}

%description bogoupgrade
bogoupgrade is a command to upgrade bogofilter鈥檚 databases from an old
format to the current format. Since the format of the database changes
once in a while, the utility is designed to make the upgrade easy.

bogoupgrade is in an extra package to remove the perl dependency on the
main bogofilter package.

%description -l zh_CN
升级 %name 的数据库到当前版本．

%prep
%setup -q
iconv -f iso-8859-1 -t utf-8 \
 doc/bogofilter-faq-fr.html > doc/bogofilter-faq-fr.html.utf8
%{__mv} -f doc/bogofilter-faq-fr.html.utf8 \
 doc/bogofilter-faq-fr.html

%build
%configure --disable-rpath
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

%{__mv} -f %{buildroot}%{_sysconfdir}/bogofilter.cf.example \
 %{buildroot}%{_sysconfdir}/bogofilter.cf

%{__install} -d -m0755 rpm-doc/xml/ rpm-doc/html/
%{__install} -m644 doc/*.xml rpm-doc/xml/
%{__install} -m644 doc/*.html rpm-doc/html/

%{__chmod} -x contrib/*

%clean
%{__rm} -rf %{buildroot}

%files bogoupgrade
%defattr(-, root, root, 0755)
%{_bindir}/bogoupgrade
%{_mandir}/man1/bogoupgrade*

%files
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING NEWS README* RELEASE.NOTES* TODO bogofilter.cf.example
%doc doc/bogofilter-SA* doc/bogofilter-tuning.HOWTO* doc/integrating* doc/programmer/
%doc rpm-doc/html/ rpm-doc/xml/ contrib
%{_mandir}/man1/bogo*.1*
%{_mandir}/man1/bf_*.1*
%config(noreplace) %{_sysconfdir}/bogofilter.cf
%{_bindir}/bogo*
%{_bindir}/bf_*
%exclude %{_bindir}/bogoupgrade
%exclude %{_mandir}/man1/bogoupgrade*

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.2.4-3
- 为 Magic 3.0 重建

* Wed Mar 05 2014 Liu Di <liudidi@gmail.com> - 1.2.4-2
- 更新到 1.2.4

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.2.2-2
- 为 Magic 3.0 重建

* Thu Nov 03 2011 Liu Di <liudidi@gmail.com> - 1.2.2-1
- 更新到 1.2.2

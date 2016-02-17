Name:           libetpan
Version: 1.6
Release:        6%{?dist}
Summary: Portable, efficient middle-ware for different kinds of mail access
Summary(zh_CN.UTF-8): 不同类型的邮件访问所用的可移植高效中间件

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        BSD
URL:            http://www.etpan.org/
Source0:        https://github.com/dinhviethoa/%{name}/archive/%{version}.tar.gz
Patch0:         libetpan-multiarch.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libdb-devel
BuildRequires:  cyrus-sasl-devel
BuildRequires:  gnutls-devel
BuildRequires:  libcurl-devel expat-devel
BuildRequires:  libtool
BuildRequires:  zlib-devel
BuildRequires:  autoconf automake

%description
The purpose of this mail library is to provide a portable, efficient middle-ware
for different kinds of mail access. When using the drivers interface, the
interface is the same for all kinds of mail access, remote and local mailboxes.

%description -l zh_CN.UTF-8
不同类型的邮件访问所用的可移植高效中间件。

%package        devel
Summary:        Development package for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       gnutls-devel
Requires:       cyrus-sasl-devel
Requires:       libdb-devel
Requires:       expat-devel libcurl-devel
Requires:       zlib-devel

%description    devel
The %{name}-devel package contains the files needed for development
with %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -b.multi

%build
if ! [ -f configure ];then ./autogen.sh;fi
%configure --disable-static --with-gnutls=yes --with-openssl=no
make LIBTOOL=%{_bindir}/libtool %{?_smp_mflags}

cd doc
make doc


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_libdir}/libetpan.{,l}a

touch -r ChangeLog $RPM_BUILD_ROOT%{_bindir}/libetpan-config
iconv -f iso8859-1 -t utf-8 ChangeLog > ChangeLog.conv && mv -f ChangeLog.conv ChangeLog
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYRIGHT NEWS
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/API.html doc/README.html doc/DOCUMENTATION
%{_bindir}/libetpan-config
%{_includedir}/libetpan
%{_includedir}/libetpan.h
%{_libdir}/*.so

%changelog
* Sun Feb 14 2016 Liu Di <liudidi@gmail.com> - 1.6-6
- 为 Magic 3.0 重建

* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 1.6-5
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.6-4
- 更新到 1.6

* Tue Jul 15 2014 Liu Di <liudidi@gmail.com> - 1.5-3
- 更新到 1.5

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1-1
- version upgrade (soname 16.0.0)
- drop upstreamed build fix
- spec cleanup

* Sun Apr 10 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0.1-0.2.20110312cvs
- add BR zlib

* Sat Mar 12 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0.1-0.1.20110312cvs
- upgrade to cvs to fix imap/gmail issues

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue May 11 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0-1
- version upgrade

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.58-1
- version upgrade

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.57-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 21 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.57-1
- version upgrade
- switch to gnutls (fixed upstream)

* Mon Sep 08 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.56-1
- version upgrade

* Tue Jun 17 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.54-1
- version upgrade
- fix #451025

* Mon Feb 11 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> - 0.52-5
- Rebuilt for gcc43

* Sat Jan 05 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.52-4
- fix #342021 multiarch

* Thu Dec 06 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.52-3
- bump

* Mon Nov 19 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.52-2
- bump

* Wed Aug 22 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.52-1
- version upgrade

* Sun Feb 25 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.49-2
- bump

* Wed Jan 17 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.49-1
- version upgrade

* Mon Nov 06 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.48-1
- version upgrade

* Thu Oct 19 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.47-1
- version upgrade

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.46-2
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.46-1
- version upgrade

* Wed Sep 13 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.45-2
- FE6 rebuild

* Thu Mar 23 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.45-1
- version upgrade

* Wed Feb 15 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.42-2
- Rebuild for Fedora Extras 5

* Fri Feb 03 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.42-1
- version upgrade

* Sun Dec 25 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.41-1
- version upgrade

* Thu Nov 17 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.40-1
- version upgrade

* Fri Sep 23 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.39.1-1
- version upgrade

* Sat Aug 13 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.38-4
- add dist tag

* Mon Aug 08 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.38-3
- remove some doc
- build without gnutls

* Sun Jul 31 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.38-2
- add documentation
- add more Requires/BuildRequires
- build with gnutls support

* Sun Jul 31 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.38-1
- Initial Release

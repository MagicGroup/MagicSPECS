
Name:           libpqxx
Summary:        C++ client API for PostgreSQL
Summary(zh_CN.UTF-8): PostgreSQL 的 C++ 客户端 API
Epoch:          1
Version:        4.0.1
Release:        2%{?dist}

License:        BSD
URL:            http://pqxx.org/
Source0:        http://pqxx.org/download/software/libpqxx/libpqxx-%{version}.tar.gz
Source1:        http://pqxx.org/download/software/libpqxx/libpqxx-%{version}.tar.gz.md5sum

Patch3:         libpqxx-2.6.8-multilib.patch

BuildRequires:  postgresql-devel
BuildRequires:  pkgconfig
BuildRequires:  python

%description
C++ client API for PostgreSQL. The standard front-end (in the sense of
"language binding") for writing C++ programs that use PostgreSQL.
Supersedes older libpq++ interface.

%description -l zh_CN.UTF-8
PostgreSQL 的 C++ 客户端 API。

%package devel
Summary:        Development tools for %{name} 
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       postgresql-devel
%description devel
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary: Developer documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文档
BuildArch: noarch
%description doc
%{summary}.

%description doc -l zh_CN.UTF-8
%{name} 的开发文档。


%prep
%setup -q

# fix spurious permissions
chmod -x COPYING

%patch3 -p1 -b .multilib


%build
%configure --enable-shared --disable-static

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

rm -fv %{buildroot}%{_libdir}/lib*.la
magic_rpm_clean.sh

%check 
# FIXME: most/all fail, need already-running postgresql instance?
make %{?_smp_mflags} check ||:


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING NEWS README VERSION
%{_libdir}/libpqxx-4.0.so

%files devel
%doc README-UPGRADE
%{_bindir}/pqxx-config
%{_includedir}/pqxx/
%{_libdir}/libpqxx.so
%{_libdir}/pkgconfig/libpqxx.pc

%files doc
%doc doc/html/*


%changelog
* Mon Jul 28 2014 Liu Di <liudidi@gmail.com> - 1:4.0.1-2
- 为 Magic 3.0 重建

* Tue Jun 24 2014 Rex Dieter <rdieter@fedoraproject.org> 1:4.0.1-1
- 4.0.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2-0.7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Sep 20 2013 Rex Dieter <rdieter@fedoraproject.org> - 1:3.2-0.6
- .spec cleanup
- -doc subpkg
- (re)enable %%check

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2-0.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 01 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1:3.2-0.1
- version upgrade
- upstream fixes for gcc4.6
- fix ftbfs (rhbz#716147)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 1:3.0.2-4
- Epoch: 1
- libpqxx-3.0.2

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 09 2009 Rex Dieter <rdieter@fedoraproject.org> 3.0.0-1
- libpqxx-3.0

* Tue Mar 03 2009 Robert Scheck <robert@fedoraproject.org> - 2.6.8-12
- Rebuilt against libtool 2.2

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Rex Dieter <rdieter@fedoraproject.org> 2.6.8-10
- gcc43 patch
- fix multilib conflicts (#342331)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.6.8-9
- Autorebuild for GCC 4.3

* Sun Dec 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.6.8-8
- cosmetics

* Fri Aug 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.6.8-7
- update Source URL's

* Mon Jun 04 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.6.8-6
- 2.6.9 pulled, revert to 2.6.8 (for koffice)

* Tue May 22 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.6.9-1
- libpqxx-2.6.9

* Wed Dec 06 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.6.8-5
- re-enable visibility patch (bummer, still needed)

* Wed Dec 06 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.6.8-4
- respin for postgresql
- drop visibility patch

* Wed Oct 04 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.6.8-3
- respin

* Wed Sep 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.6.8-1
- fc6+: drop -Werror (for now) 
- include %%check section (not used, by default)

* Fri Sep 15 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> 2.6.7-2
- version upgrade

* Thu Aug 03 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> 2.6.7-1
- version upgrade
- fix #192933

* Mon May 29 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> 2.6.6-1
- version upgrade

* Thu Feb 16 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> 2.5.5-7
- Rebuild for Fedora Extras 5

* Wed Sep 28 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> 2.5.5-6
- fix #169441

* Tue Sep 27 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> 2.5.5-5
- try fc5 build

* Tue Sep 27 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> 2.5.5-4
- version upgrade

* Tue Jul 05 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> 2.5.4-4
- add dist tag

* Fri Jul 01 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> 2.5.4-3
- add postgresql-devel to Requires for devel package
- get rid of -R option in pqxx-config
- don't need BuildRequires perl

* Thu Jun 30 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> 2.5.4-2
- Drop explicit Requires for ldconfig

* Sat Jun 25 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> 2.5.4-1
- Initial Release

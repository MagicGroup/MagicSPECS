Name:    libassuan
Summary: GnuPG IPC library
Summary(zh_CN.UTF-8): GnuPG IPC 库
Version: 2.1.1
Release: 1%{?dist}

# The library is LGPLv2+, the documentation GPLv3+
License: LGPLv2+ and GPLv3+
Source0: ftp://ftp.gnupg.org/gcrypt/libassuan/libassuan-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/libassuan/libassuan-%{version}.tar.bz2.sig
URL:     http://www.gnupg.org/
Group:   System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1:  libassuan-1.0.5-multilib.patch

BuildRequires: gawk
BuildRequires: libgpg-error-devel >= 1.8
BuildRequires: pth-devel

%description
This is the IPC library used by GnuPG 2, GPGME and a few other
packages.

%description -l zh_CN.UTF-8
GnuPG IPC 库。

%package devel 
Summary: GnuPG IPC library 
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Provides: libassuan2-devel = %{version}-%{release}
Provides: libassuan2-devel%{?_isa} = %{version}-%{release}
Requires: pth-devel
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
%description devel 
This is the IPC static library used by GnuPG 2, GPGME and a few other
packages.

This package contains files needed to develop applications using %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%patch1 -p1 -b .multilib


%build
%configure \
  --includedir=%{_includedir}/libassuan2

make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

## Unpackaged files
rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_libdir}/lib*.la
magic_rpm_clean.sh

%check
make check


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel 
/usr/sbin/install-info %{_infodir}/assuan.info %{_infodir}/dir &>/dev/null || :

%preun devel 
if [ $1 -eq 0 ]; then
  /usr/sbin/install-info --delete %{_infodir}/assuan.info %{_infodir}/dir &>/dev/null || :
fi


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING COPYING.LIB NEWS README THANKS TODO
%{_libdir}/libassuan.so.0*

%files devel 
%defattr(-,root,root,-)
%{_bindir}/libassuan-config
%{_includedir}/libassuan2/
%{_libdir}/libassuan.so
%{_datadir}/aclocal/libassuan.m4
%{_infodir}/assuan.info*


%changelog
* Thu Jul 10 2014 Liu Di <liudidi@gmail.com> - 2.1.1-1
- 更新到 2.1.1

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.0.3-2
- 为 Magic 3.0 重建

* Fri Jul 15 2011 Tomáš Mráz <tmraz@redhat.com> 2.0.1-1
- new upstream release

* Thu Apr 14 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-4
- Missing ldconfig calls (#696787)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 10 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.0.0-2
- -devel: Provides: libassuan2-devel

* Tue Jul 27 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.0.0-1
- libassuan-2.0.0 (#573796)

* Thu Dec 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.5-4
- better versioning for Obsoletes
- better (upstreamable) multilib patch

* Thu Dec 17 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.5-3
- Fix license tag - the documentation is GPLv3+

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.5-1
- libassuan-1.0.5

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Apr 03 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.4-3
- multiarch conflicts (#341911)

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.4-2
- respin (gcc43)

* Wed Dec 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.0.4-1
- libassuan-1.0.4
- License: LGPLv2+
- disable useless -debuginfo (static libs only)

* Sun Aug 26 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.0.3-2
- BR: gawk (to reenable pth support)

* Fri Aug 24 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.0.3-1
- libassuan-1.0.3
- License: LGPLv2

* Thu Aug 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.0.2-2
- License: LGPLv3 (clarification, changed from LGPLv2 1.0.1 -> 1.0.2)

* Fri Jul 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.0.2-1
- libassuan-1.0.2
- rename -static -> -devel

* Sat Nov 25 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 1.0.1-1
- libassuan-1.0.1

* Mon Nov 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 1.0.0-1
- libassuan-1.0.0
- rename -devel -> -static (+Obsoletes/Provides: %%name-devel)

* Wed Oct 18 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.9.3-2
- another libassuan.m4 patch

* Tue Oct 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.9.3-1
- 0.9.3
- BR: pth-devel, -devel: Requires: pth-devel

* Wed Oct 04 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.9.2-1
- 0.9.2

* Mon Oct 02 2006 Rex Dieter <rexdieter[AT]users.sf.ne> - 0.9.0-3
- respin

* Tue Sep 26 2006 Rex Dieter <rexdieter[AT]users.sf.net - 0.9.0-2
- -devel: Provides: %%name-static
- 0.9.0

* Mon Aug 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.6.10-3
- fc6 respin

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Mon Jul  4 2005 Michael Schwendt <mschwendt[at]users.sf.net> - 0.6.10-2
- Build PIC only for x86_64.

* Fri Jul  1 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.6.10-1
- 0.6.10, macro patch no longer needed (#162262).

* Sun May  8 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.6.9-4
- rebuilt

* Fri Mar 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.6.9-3
- Fix FC4 build and source URLs.

* Thu Feb  3 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.6.9-2
- Build PIC to fix x86_64 linking.

* Thu Jan 06 2005 Rex Dieter <rexdieter[AT]users.sf.net> - 0.6.9-1
- 0.6.9

* Sat Oct 23 2004 Rex Dieter <rexdieter[AT]users.sf.net> - 0.6.7-0.fdr.3
- *really* fix description this time.

* Fri Oct 22 2004 Rex Dieter <rexdieter[AT]users.sf.net> - 0.6.7-0.fdr.2
- remove "We decided..." part of description
- remove hard-coded .gz info references
- Req(preun)->Preq(postun): /sbin/install-info

* Thu Oct 21 2004 Rex Dieter <rexdieter[AT]users.sf.net> - 0.6.7-0.fdr.1
- cleanup, make presentable.

* Tue Oct 19 2004 Rex Dieter <rexdieter[AT]users.sf.net> - 0.6.7-0.fdr.0
- first try

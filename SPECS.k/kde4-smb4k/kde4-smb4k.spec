%define realname smb4k
Name:		kde4-smb4k
Version:	1.2.1
Release:	2%{?dist}
Summary:	The SMB/CIFS Share Browser for KDE
Summary(zh_CN.UTF-8): KDE下的SMB/CIFS共享浏览器

Group:		Applications/Internet
Group(zh_CN.UTF-8):	应用程序/互联网
License:	GPL
URL:		http://smb4k.sf.net/
Source0:	http://downloads.sourceforge.net/project/smb4k/%{version}/%{realname}-%{version}.tar.xz
Patch1:		smb4k-1.1.2-notrdoc.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	kdelibs4-devel kdebase4-devel gettext
Requires:	samba-client

%description
Smb4K is an SMB/CIFS share browser for KDE. It uses the Samba software suite to
access the SMB/CIFS shares of the local network neighborhood. Its purpose is to
provide a program that's easy to use and has as many features as possible.

%description -l zh_CN.UTF-8
Smb4K是一个KDE下的SMB/CIFS共享浏览器。它使用Samba软件套装来访问本地网上邻居的
SMB/CIFS共享。它的目标是尽可能提供一个容易使用并有许多特性的程序。

%package devel
Summary:	Development files for %{name}
Summary(zh_CN.UTF-8):	%{name}的开发文件
Group:		Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the libraries, include files and other resources
needed to develop applications using %{name}.

%description devel -l zh_CN.UTF-8
这个包包含了使用%{name}开发程序所需要的库，包含文件和其它资源。

%prep
%setup -q -n %{realname}-%{version}
%patch1 -p1

%build
mkdir build
cd build
%{cmake_kde4} -DINSTALL_HEADER_FILES=ON ..
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd build
make install DESTDIR=$RPM_BUILD_ROOT

magic_rpm_clean.sh

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, root)
%doc AUTHORS BUGS ChangeLog COPYING README 
%{kde4_bindir}/*
%{kde4_appsdir}/*
%{kde4_iconsdir}/*
%{kde4_plugindir}/*
%{kde4_libdir}/libsmb4k*so*
%{kde4_libdir}/libkdeinit4_smb4k.so
%{kde4_servicesdir}/plasma-applet-smb4k-qml.desktop
%{kde4_kcfgdir}/*
%{kde4_xdgappsdir}/*.desktop
%{kde4_localedir}/zh_*
%{kde4_dbus_system_servicesdir}/*
%{_sysconfdir}/dbus-1/system.d/*.smb4k.mounthelper.conf
%{kde4_auth_policy_filesdir}/*.smb4k.mounthelper.policy

%files devel
%defattr(-, root, root)
%{kde4_includedir}/*
%{kde4_htmldir}/en/smb4k/*
%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.2.1-2
- 更新到 1.2.1

* Thu Jun 05 2014 Liu Di <liudidi@gmail.com> - 1.1.2-1
- 更新到 1.1.2

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.0-2
- 为 Magic 3.0 重建

* Fri Sep 05 2008 Liu Di <liudidi@gmail.com> - 0.9.7-1mgc
- 更新到 0.9.7

* Fri Jun 13 2008 Liu Di <liudidi@gmail.com> - 0.9.5-1mgc
- 更新到 0.9.5

* Wed Jan 23 2008 Liu Di <liudidi@gmail.com> - 0.9.2-1mgc
- update to 0.9.2

* Wed Jan 10 2007 Liu Di <liudidi@gmail.com> - 0.8.0-1mgc
- update to 0.8.0

* Wed Sep 27 2006 Marcin Garski <mgarski[AT]post.pl> 0.7.3-1
- Updated to version 0.7.3

* Fri Sep 01 2006 Marcin Garski <mgarski[AT]post.pl> 0.7.2-2
- Rebuild for Fedora Core 6
- Spec tweak

* Fri Aug 18 2006 Marcin Garski <mgarski[AT]post.pl> 0.7.2-1
- Updated to version 0.7.2

* Mon Jun 19 2006 Marcin Garski <mgarski[AT]post.pl> 0.7.1-1
- Updated to version 0.7.1
- Drop smb4k-0.6.5-desktop.patch (merged upstream)

* Tue Apr 25 2006 Marcin Garski <mgarski[AT]post.pl> 0.7.0-1
- Updated to version 0.7.0, comment --enable-final

* Tue Apr 18 2006 Marcin Garski <mgarski[AT]post.pl> 0.6.10-1
- Updated to version 0.6.10

* Fri Mar 24 2006 Marcin Garski <mgarski[AT]post.pl> 0.6.9-1
- Updated to version 0.6.9

* Fri Feb 24 2006 Marcin Garski <mgarski[AT]post.pl> 0.6.8-1
- Updated to version 0.6.8

* Fri Feb 17 2006 Marcin Garski <mgarski[AT]post.pl> 0.6.7-4
- Updated smb4k-0.6.8-mount.patch

* Fri Feb 17 2006 Marcin Garski <mgarski[AT]post.pl> 0.6.7-3
- Add support of mount.cifs/umount.cifs (bug #181638)
- Remove smb4k-0.6.5-buff.patch

* Tue Feb 14 2006 Marcin Garski <mgarski[AT]post.pl> 0.6.7-2
- Rebuild

* Wed Feb 08 2006 Marcin Garski <mgarski[AT]post.pl> 0.6.7-1
- Updated to version 0.6.7

* Wed Feb 01 2006 Marcin Garski <mgarski[AT]post.pl> 0.6.5-5
- Fix GCC warnings
- Don't own KDE directories

* Wed Jan 18 2006 Marcin Garski <mgarski[AT]post.pl> 0.6.5-4
- Remove libxml2 from BR
- Add workaround for broken libtool archive (made by Dawid Gajownik)

* Sun Jan 15 2006 Marcin Garski <mgarski[AT]post.pl> 0.6.5-3
- Get rid of desktop-file-utils
- Add --disable-dependency-tracking & --enable-final

* Thu Jan 12 2006 Marcin Garski <mgarski[AT]post.pl> 0.6.5-2
- Add kdebase-devel to BuildRequires

* Wed Jan 11 2006 Marcin Garski <mgarski[AT]post.pl> 0.6.5-1
- Updated to version 0.6.5 && spec cleanup for FE

* Sun Sep 05 2004 Marcin Garski <mgarski[AT]post.pl> 0.4.1a-1.fc2
- Updated to version 0.4.1a

* Thu Aug 31 2004 Marcin Garski <mgarski[AT]post.pl> 0.4.1-1.fc2
- Updated to version 0.4.1

* Wed Jun 02 2004 Marcin Garski <mgarski[AT]post.pl> 0.4.0-3.fc2
- Rebuild for Fedora Core 2

* Thu May 06 2004 Marcin Garski <mgarski[AT]post.pl> 0.4.0-2
- Convert pl.po to UTF-8

* Thu May 06 2004 Marcin Garski <mgarski[AT]post.pl> 0.4.0-1
- Update to 0.4.0

* Wed Jan 21 2004 Marcin Garski <mgarski[AT]post.pl> 0.3.2-1
- Rebuild for Fedora Core 1

* Thu Dec 18 2003 Marcin Garski <mgarski[AT]post.pl> 0.3.1-3
- Cleanup specfile

* Fri Nov 27 2003 Marcin Garski <mgarski[AT]post.pl> 0.3.1-2
- Initial specfile based on specfile by Ian Geiser <geiseri[AT]msoe.edu>

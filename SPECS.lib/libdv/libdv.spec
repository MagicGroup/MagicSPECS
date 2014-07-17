Summary:	Software decoder for DV format video
Summary(zh_CN.UTF-8): DV 格式视频的软件解码器
Name:		libdv
Version:	1.0.0
Release:	5%{?dist}
License:	LGPL
Group:		System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
URL:		http://libdv.sourceforge.net/
Source:		http://dl.sf.net/libdv/libdv-%{version}.tar.gz
Patch1:		libdv-0.104-no-exec-stack.patch
Patch2:		libdv-0.104-pic-fix.patch
Patch4:		libdv-0.104-gtk2.patch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	gtk2-devel
BuildRequires:	libXt-devel, libXv-devel
# Required for the gtk2 patch
BuildRequires:	autoconf, automake, libtool, SDL-devel
ExcludeArch:	s390 s390x

%package	devel
Summary:	Development package for libdv
Summary(zh_CN.UTF-8): libdv的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8):   开发/库
Requires:	%{name} = %{version}-%{release}

%package	tools
Summary:	Basic tools to manipulate Digital Video streams
Summary(zh_CN.UTF-8):	处理数字视频流的基本工具
Group:		Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
Requires:	%{name} = %{version}-%{release}

%description
The Quasar DV codec (libdv) is a software codec for DV video, the
encoding format used by most digital camcorders, typically those that
support the IEEE 1394 (a.k.a. FireWire or i.Link) interface. libdv was
developed according to the official standards for DV video: IEC 61834
and SMPTE 314M.

%description -l zh_CN.UTF-8
Quasar DV 编码(libdv)是一个DV视频的软件编码器，编码格式被大多数数字摄像机
使用，代表性的是支持IEEE 1394（也叫火线或i.Link）接口。libdv是按照DV视频
的官方标准：IEC 61834和SMPTE 314M开发的。

%description tools
This package contains some basic programs to display and encode
digital video streams. This programs uses the Quasar DV codec (libdv),
a software codec for DV video, the encoding format used by most
digital camcorders, typically those that support the IEEE 1394
(a.k.a. FireWire or i.Link) interface.

%description tools -l zh_CN.UTF-8
这个包包含了一些显示和编码数字视频流的基本工具。这些程序使用了Quasar DV
编码器(libdv)，DV视频的软件编码器，编码格式被大多数数字摄像机使用，代表
性的是支持IEEE 1394（也叫火线或i.Link）接口。

%description devel
This package contains development files for libdv.

%description devel -l zh_CN.UTF-8
这个包包含了libdv的开发文件。

%prep
%setup -q
%patch1 -p0 -b .no-exec-stack
#patch2 -p1 -b .pic-fix
#%patch4 -p1 -b .gtk2
# Required for the gtk2 patch
autoreconf -fisv

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
rm $RPM_BUILD_ROOT%{_libdir}/libdv.a
rm $RPM_BUILD_ROOT%{_libdir}/libdv.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING COPYRIGHT ChangeLog
%{_libdir}/libdv.so.*

%files tools
%defattr(-,root,root,-)
%doc README.*
%{_bindir}/dubdv
%{_bindir}/dvconnect
%{_bindir}/encodedv
%{_bindir}/playdv
%{_mandir}/man1/dubdv.1.gz
%{_mandir}/man1/dvconnect.1.gz
%{_mandir}/man1/encodedv.1*
%{_mandir}/man1/playdv.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/libdv/
%{_libdir}/libdv.so
%{_libdir}/pkgconfig/libdv.pc

%changelog
* Tue Jul 15 2014 Liu Di <liudidi@gmail.com> - 1.0.0-5
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.0-4
- 为 Magic 3.0 重建

* Thu Jan 05 2012 Liu Di <liudidi@gmail.com> - 1.0.0-3
- 为 Magic 3.0 重建

* Mon Oct 09 2006 Liu Di <liudidi@gmail.com> - 0.104-2mgc
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:0.104-4.fc6.1
- rebuild

* Wed May 24 2006 Jarod Wilson <jwilson@redhat.com> 0.104-4
- disable PIC patch for now, it reliably causes segfaults on x86

* Sat May 13 2006 Jarod Wilson <jwilson@redhat.com> 0.104-3
- rebuilt against latest X libs

* Tue Mar 07 2006 Warren Togami <wtogami@redhat.com> 0.104-2
- remove instead of exclude static libs

* Wed Feb 15 2006 Matthias Saou <http://freshrpms.net/> 0.104-1
- Update to 0.104 at last (#147311)
- Include no-exec-stack, pic-fix, amd64reloc and gtk2 patches from Gentoo
  and PLD (merge gcc4 fix to the pic-fix patch).
- Now build against gtk2 (thanks to the patch above).
- Exclude static library.

* Mon Feb 13 2006 Paul Nasrat <pnasrat@redhat.com> - 0:0.103-4.3
- Patch to build with gcc 4.1

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0:0.103-4.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0:0.103-4.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 16 2005 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 28 2005 Warren Togami <wtogami@redhat.com> - 0:0.103-3
- gcc4 rebuild

* Sun Feb 06 2005 Warren Togami <wtogami@redhat.com> - 0:0.103-2
- Fix erroneously requiring an executable stack (Nicholas Miell #146590)

* Sun Sep 19 2004 Warren Togami <wtogami@redhat.com> - 0:0.103-1
- upgrade to 0.103

* Sun Jun 20 2004 Jeremy Katz <katzj@redhat.com> - 0:0.102-4
- gtk+ doesn't need to be in the .pc file (committed upstream, reported 
- don't require gtk+-devel for -devel package (unneeded)
  to fedora-devel-list by John Thacker)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun May 30 2004 Warren Togami <wtogami@redhat.com> 0:0.102-2
- Bug #123367 -devel Req gtk+-devel

* Mon Mar 29 2004 Warren Togami <wtogami@redhat.com> 0:0.102-1
- update to 0.102

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 14 2004 Warren Togami <wtogami@redhat.com> 0:0.101-2
- upgrade to 0.101
- spec cleanup
- exclude from mainframes
- GPL -> LGPL

* Sun Apr 27 2003 Dams <anvil[AT]livna.org> 0:0.99-0.fdr.2
- Added post/postun scriptlets

* Fri Apr 25 2003 Dams <anvil[AT]livna.org> 
- Initial build.



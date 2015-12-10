Summary: Library for accessing MusicBrainz servers
Summary(zh_CN.UTF-8): 访问MusicBrainz服务器的库
Name: libmusicbrainz
Version: 2.1.5
Release: 7%{?dist}
License: LGPL
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.musicbrainz.org/
Source0: ftp://ftp.musicbrainz.org/pub/musicbrainz/%{name}-%{version}.tar.gz
BuildRequires: libstdc++-devel
BuildRequires: expat-devel
Patch2: libmusicbrainz-2.1.5-gcc44.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Obsoletes: musicbrainz

%description
The MusicBrainz client library allows applications to make metadata
lookup to a MusicBrainz server, generate signatures from WAV data and
create CD Index Disk ids from audio CD roms.

%description -l zh_CN.UTF-8
MusicBrainz客户端库允许应用程序从MusicBrainz服务器上查询元数据，从WAV
数据生成签名和从音频CD建立CD索引标识。

%package devel
Summary: Headers for developing programs that will use libmusicbrainz
Summary(zh_CN.UTF-8): 使用libmusicbrainz开发程序所需要的头文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: libstdc++-devel
Obsoletes: musicbrainz-devel

%description devel
This package contains the headers that programmers will need to develop
applications which will use libmusicbrainz.

%description devel -l zh_CN.UTF-8
这个包包含了程序员使用libmusicbrainz开发应用程序所需要的头文件。

%prep
%setup -q
%patch2 -p1

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/*.a
magic_rpm_clean.sh

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README TODO
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,0755)
%{_libdir}/pkgconfig/*pc
%{_includedir}/musicbrainz
%{_libdir}/*.so

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 2.1.5-7
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 2.1.5-6
- 为 Magic 3.0 重建

* Tue Jul 22 2014 Liu Di <liudidi@gmail.com> - 2.1.5-5
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.1.5-4
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Liu Di <liudidi@gmail.com> - 2.1.5-3
- 为 Magic 3.0 重建

* Fri Jan 05 2007 Liu Di <liudidi@gmail.com> - 2.1.4-1mgc
- update to 2.1.4

* Fri Sep 15 2006 Liu Di <liudidi@gmail.com> - 2.1.3-1mgc
- update to 2.1.3

* Tue Apr 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.1.1-3
- apply .spec file cleanups from Matthias Saou (#172926)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.1.1-2.1
- bump again for double-long bug on ppc(64)

* Tue Feb  7 2006 Christopher Aillon <caillon@redhat.com> - 2.1.1-2
- Stop shipping the .a file in the main package

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.1.1-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 23 2005 John (J5) Palmieri <johnp@redhat.com> 2.1.1-1
- Update to upstream version 2.1.1
- Removed libmusicbrainz-2.0.2-missing-return.patch
- Removed libmusicbrainz-2.0.2-conf.patch

* Wed Mar 03 2005 John (J5) Palmieri <johnp@redhat.com> 2.0.2-14
- Add patch to fix percision cast error to compile correctly on s390x
 
* Wed Mar 03 2005 John (J5) Palmieri <johnp@redhat.com> 2.0.2-13
- rebuild with gcc 4.0

* Mon Nov 08 2004 Colin Walters <walters@redhat.com> 2.0.2-12
- Add libmusicbrainz-2.0.2-missing-return.patch (bug #137289)

* Thu Oct 07 2004 Colin Walters <walters@redhat.com> 2.0.2-11
- BuildRequire expat-devel

* Tue Sep 28 2004 Colin Walters <walters@redhat.com> 2.0.2-10
- Move .so symlink to -devel package

* Tue Aug 31 2004 Colin Walters <walters@redhat.com> 2.0.2-9
- Add ldconfig calls (bz #131281)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Dec 18 2003 Brent Fox <bfox@redhat.com> 2.0.2-6
- add a BuildPreReq for libstdc++-devel and gcc-c++ (bug #106556)
- add a Requires for libstdc++-devel for libmusicbrainz-devel

* Mon Sep  1 2003 Bill Nottingham <notting@redhat.com>
- Obsoletes musicbrainz-devel too

* Mon Sep  1 2003 Jonathan Blandford <jrb@redhat.com>
- Obsoletes musicbrainz

* Fri Aug 22 2003 Bill Nottingham <notting@redhat.com> 2.0.2-5
- fix autoconf/libtool weirdness, remove exclusivearch

* Fri Aug 22 2003 Brent Fox <bfox@redhat.com> 2.0.2-4
- add ExcludeArch for s390x (something is really broken)

* Fri Aug 22 2003 Brent Fox <bfox@redhat.com> 2.0.2-3
- add ExcludeArch for ppc64

* Fri Aug 22 2003 Brent Fox <bfox@redhat.com> 2.0.2-2
- add ExcludeArch for x86_64 for now

* Thu Aug 21 2003 Brent Fox <bfox@redhat.com> 
- Initial build.



Summary: Library for reading and writing ID3v1 and ID3v2 tags
Summary(zh_CN.UTF-8): 读取和写入 ID3v1 和 ID3v2 标签的库
Name: libid3tag
Version: 0.15.1b
Release: 10%{?dist}
License: GPL
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.underbit.com/products/mad/
Source: ftp://ftp.mars.org/pub/mpeg/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: zlib-devel, gcc-c++
Conflicts: libmad < 0.15.1b

%description
A library for reading and (eventually) writing ID3 tags, both ID3v1 and the
various versions of ID3v2.

%description -l zh_CN.UTF-8
读取和(最终)写入ID3标签的库，同时支持ID3v1和多种版本的ID3v2。

%package devel
Summary: Header and library for developing programs that will use libid3tag
Summary(zh_CN.UTF-8): 使用libid3tag开发程序所需要的头文件和库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}, pkgconfig, zlib-devel

%description devel
A library for reading and (eventually) writing ID3 tags, both ID3v1 and the
various versions of ID3v2.

This package contains the header file as well as the static library needed
to develop programs that will use libid3tag for ID3 tar reading and writing.

%description devel -l zh_CN.UTF-8
读取和(最终)写入ID3标签的库，同时支持ID3v1和多种版本的ID3v2。

这个包包含使用libid3tag开发程序所需要的头文件和静态库。

%prep
%setup

# Create an additional pkgconfig file
%{__cat} > id3tag.pc << EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: id3tag
Description: ID3 tag library
Requires:
Version: %{version}
Libs: -L%{_libdir} -lid3tag -lz
Cflags: -I%{_includedir}
EOF


%build
%configure
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%makeinstall
%{__install} -D -m 644 id3tag.pc %{buildroot}%{_libdir}/pkgconfig/id3tag.pc


%clean
%{__rm} -rf %{buildroot}


%post
/sbin/ldconfig

%postun
/sbin/ldconfig


%files 
%defattr(-, root, root, 0755)
%doc CHANGES COPYING COPYRIGHT CREDITS README TODO
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, 0755)
%{_libdir}/*.a
%exclude %{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*


%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 0.15.1b-10
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.15.1b-9
- 为 Magic 3.0 重建

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 0.15.1b-8
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.15.1b-7
- 为 Magic 3.0 重建

* Sat Jan 07 2012 Liu Di <liudidi@gmail.com> - 0.15.1b-6
- 为 Magic 3.0 重建

* Tue Oct 4 2005 kde <jack@linux.net.cn>
- port to Magic Linux 2.0

* Mon Aug 30 2004 Matthias Saou <http://freshrpms.net/> 0.15.1b-3
- Added missing /sbin/ldconfig calls.

* Tue May 18 2004 Matthias Saou <http://freshrpms.net/> 0.15.1b-2
- Rebuilt for Fedora Core 2.
- Added pkgconfig dependency to the devel package.

* Thu Feb 19 2004 Matthias Saou <http://freshrpms.net/> 0.15.1b-1
- Update to 0.15.1b.

* Sun Nov  2 2003 Matthias Saou <http://freshrpms.net/> 0.15.0b-4
- Rebuild for Fedora Core 1.

* Wed Sep  3 2003 Matthias Saou <http://freshrpms.net/>
- Fixed the -I in the pkgconfig file, thanks to Michael A. Peters.

* Thu Aug 28 2003 Matthias Saou <http://freshrpms.net/>
- Added id3tag.pc required by gstreamer-plugins.
- Added zlib-devel dep to the devel package.

* Mon Jul 21 2003 Matthias Saou <http://freshrpms.net/>
- Added zlib-devel build dep.

* Wed Jun 25 2003 Matthias Saou <http://freshrpms.net/>
- Initial release of 0.15.0b.


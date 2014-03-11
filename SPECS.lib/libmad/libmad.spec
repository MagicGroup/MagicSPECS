# $Id: libmad.spec 4260 2006-03-29 17:04:33Z thias $
# Authority: matthias

Summary: MPEG audio decoding library
Summary(zh_CN.UTF-8): MPEG 音频编码库
Name: libmad
Version: 0.15.1b
Release: 7%{?dist}
License: GPL
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.underbit.com/products/mad/
Source: ftp://ftp.mars.org/pub/mpeg/%{name}-%{version}.tar.gz
Patch1: %{name}-%{version}-gcc44.patch
Patch2: libmad-0.15.1b-mips-fix.patch
Packager: Dries Verachtert <dries@ulyssis.org>
Vendor: Dries RPM Repository http://dries.ulyssis.org/rpm/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gcc-c++
Provides: mad = %{version}-%{release}

%description
MAD (libmad) is a high-quality MPEG audio decoder. It currently supports
MPEG-1 and the MPEG-2 extension to Lower Sampling Frequencies, as well as
the so-called MPEG 2.5 format. All three audio layers (Layer I, Layer II,
and Layer III a.k.a. MP3) are fully implemented.

MAD does not yet support MPEG-2 multichannel audio (although it should be
backward compatible with such streams) nor does it currently support AAC.

%description -l zh_CN.UTF-8
MAD (libman) 是一个高品质的MPEG音频编码器。它当前支持MPEG-1和MPEG-2的低采
样率扩展，也叫MPEG 2.5格式。所有的三层音频（层 I, 层 II和层 III也叫MP3）
已被完全实现。

MAD还不支持MPEG-2 多声道音频（尽管这样的流应该向后兼容），也不支持AAC。

%package devel
Summary: Header and library for developing programs that will use libmad
Summary(zh_CN.UTF-8): 使用libmad开发程序所需要的头文件和库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}, pkgconfig

%description devel
MAD (libmad) is a high-quality MPEG audio decoder. It currently supports
MPEG-1 and the MPEG-2 extension to Lower Sampling Frequencies, as well as
the so-called MPEG 2.5 format. All three audio layers (Layer I, Layer II,
and Layer III a.k.a. MP3) are fully implemented.

This package contains the header file as well as the static library needed
to develop programs that will use libmad for mpeg audio decoding.

%description devel -l zh_CN.UTF-8
MAD (libman) 是一个高品质的MPEG音频编码器。它当前支持MPEG-1和MPEG-2的低采
样率扩展，也叫MPEG 2.5格式。所有的三层音频（层 I, 层 II和层 III也叫MP3）
已被完全实现。

这个包包含了使用libmad进行mpeg音频编码的程序开发所需要的静态库和头文件。

%prep
%setup
%patch1 -p1
%patch2 -p1

# Create an additional pkgconfig file
%{__cat} << EOF > mad.pc
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: mad
Description: MPEG Audio Decoder
Requires:
Version: %{version}
Libs: -L%{_libdir} -lmad -lm
Cflags: -I%{_includedir}
EOF


%build
%configure \
    --disable-dependency-tracking \
    --enable-accuracy \
    --disable-debugging
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%makeinstall
%{__install} -D -p -m 0644 mad.pc %{buildroot}%{_libdir}/pkgconfig/mad.pc


%clean
%{__rm} -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


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
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.15.1b-7
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Liu Di <liudidi@gmail.com> - 0.15.1b-6
- 为 Magic 3.0 重建

* Fri Mar 17 2006 Matthias Saou <http://freshrpms.net/> 0.15.1b-4 #4260
- Release bump to drop the disttag number in FC5 build.

* Mon Aug 30 2004 Matthias Saou <http://freshrpms.net/> 0.15.1b-3
- Added missing /sbin/ldconfig calls.

* Tue May 18 2004 Matthias Saou <http://freshrpms.net/> 0.15.1b-2
- Rebuilt for Fedora Core 2.
- Added pkgconfig dependency to the devel package.

* Thu Feb 19 2004 Matthias Saou <http://freshrpms.net/> 0.15.1b-1
- Update to 0.15.1b.

* Sun Nov  2 2003 Matthias Saou <http://freshrpms.net/> 0.15.0b-3
- Rebuild for Fedora Core 1.

* Thu Aug 28 2003 Matthias Saou <http://freshrpms.net/>
- Added mad.pc required by gstreamer-plugins.

* Mon Mar 31 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.15.0b.
- Split a devel package.

* Mon Mar 31 2003 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 9.
- Added mad provides.

* Fri Sep 27 2002 Matthias Saou <http://freshrpms.net/>
- Rebuild for Red Hat Linux 8.0 (missing because of license issues).
- Spec file cleanup.

* Tue Mar 12 2002 Bill Nottingham <notting@redhat.com> 0.14.2b-3
- ship libid3tag too

* Thu Feb 21 2002 Bill Nottingham <notting@redhat.com>
- rebuild

* Mon Jan 28 2002 Bill Nottingham <notting@redhat.com>
- split libmad off into a separate package


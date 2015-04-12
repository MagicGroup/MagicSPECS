Summary: 	Library for reading and writing Quicktime files
Summary(zh_CN.UTF-8): 读写 QuickTime 文件的库
Name: 		libquicktime
Version:	1.2.4
Release:	6%{?dist}
License:	LGPLv2+
Group: 		System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
URL: 		http://libquicktime.sourceforge.net/
Source0: 	http://downloads.sourceforge.net/libquicktime/%{name}-%{version}.tar.gz
Patch1:		%{name}-1.2.4-ffmpeg55.patch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	libdv-devel
BuildRequires:	libpng-devel libjpeg-devel libGLU-devel
BuildRequires:	libvorbis-devel ffmpeg-devel
BuildRequires:	lame-devel alsa-lib-devel libXt-devel libXaw-devel libXv-devel
BuildRequires:	libdv-devel >= 0.102-4 x264-devel faac-devel faad2-devel
BuildRequires:	libavc1394-devel libraw1394-devel >= 0.9.0-12
BuildRequires:	gtk2-devel >= 2.4.0
BuildRequires:  gettext-devel
BuildRequires:  libtool

%package utils
Summary:	Utilities for working with Quicktime files
Summary(zh_CN.UTF-8): 处理 QuickTime 文件的工具
Group:		Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体

%package devel
Summary:	Development files for libquicktime
Summary(zh_CN.UTF-8): %name 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:	%{name} = %{version}-%{release} zlib-devel pkgconfig

# --------------------------------------------------------------------

%description
Libquicktime is based on the quicktime4linux library with several
enhancements. All 3rd-party libraries were removed from the
sourcetree. Instead, the systemwide installed libraries are detected
by the configure script. All original codecs were moved into
dynamically loadable modules, and new codecs are in
development. Libquicktime is source-compatible with
quicktime4linux. Special API extensions allow access to the codec
registry and more convenient processing of Audio and Video
data. 

%description -l zh_CN.UTF-8
读写 QuickTime 文件的库。

%description utils
Libquicktime is based on the quicktime4linux library with several
enhancements. This package contains utility programs and additional
tools, like a commandline player and a GTK configuration utility which
can configure the parameters of all installed codecs.

%description utils -l zh_CN.UTF-8
处理 QuickTime 文件的工具

%description devel
Libquicktime is based on the quicktime4linux library with several
enhancements. This package contains development files for %{name}.

%description devel -l zh_CN.UTF-8
%name 的开发包。

# --------------------------------------------------------------------

%prep
%setup -q
%patch1 -p1
# regenerate configure to disable rpath
autoreconf -f -i

# --------------------------------------------------------------------

%build
%configure \
	--enable-gpl \
	--disable-rpath \
	--with-cpuflags="$RPM_OPT_FLAGS" \
	--disable-dependency-tracking \
	--without-doxygen \
	--disable-static \
	--with-libdv \
	--enable-libswscale \
%ifarch i686 pentium3 pentium4 athlon x86_64 ia64
	--enable-mmx \
%else
	--disable-mmx
%endif

make %{?_smp_mflags}

# --------------------------------------------------------------------

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT%{_libdir} -type f -a -name \*.la -exec rm {} \;


magic_rpm_clean.sh
#%find_lang %{name}


# --------------------------------------------------------------------

%clean
rm -rf $RPM_BUILD_ROOT

# --------------------------------------------------------------------

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
#%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING README TODO
%{_libdir}/%{name}*.so.*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/lqt_*.so

%files utils
%defattr(-,root,root,-)
%{_bindir}/libquicktime_config
%{_bindir}/lqt_transcode
%{_bindir}/lqtplay
%{_bindir}/lqtremux
%{_bindir}/qt2text
%{_bindir}/qtdechunk
%{_bindir}/qtdump
%{_bindir}/qtinfo
%{_bindir}/qtrechunk
%{_bindir}/qtstreamize
%{_bindir}/qtyuv4toyuv
%{_mandir}/man1/lqtplay.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/lqt/
%{_libdir}/pkgconfig/libquicktime.pc
%{_libdir}/%{name}*.so

# --------------------------------------------------------------------

%changelog
* Mon Mar 30 2015 Liu Di <liudidi@gmail.com> - 1.2.4-6
- 为 Magic 3.0 重建

* Mon Jul 28 2014 Liu Di <liudidi@gmail.com> - 1.2.4-5
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Liu Di <liudidi@gmail.com> - 1.2.4-4
- 为 Magic 3.0 重建

* Thu Jul 04 2013 Liu Di <liudidi@gmail.com> - 1.2.4-3
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.2.3-2
- 为 Magic 3.0 重建



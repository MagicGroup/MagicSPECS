Summary:        MAC: short for Monkey's Audio Codec 
Summary(zh_CN.UTF-8):	MAC: Monkey's Audio Codec的缩写
Name:           mac
Version:        3.99u4b5
License:      LGPL
Group:          Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
Source:         mac-3.99-u4-b5.tar.gz
Patch0:		mac-gcc44.patch
Release:        8%{?dist}
Vendor:         Matthew T. Ashland <email@monkeysaudio.com>,SuperMMX
URL:            http://sourceforge.net/projects/mac-port/
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

%description
Monkey's Audio Codec, a lossless audio codec (almost with the .ape extension).
This is the MAC Linux port.
Since 3.99 update 4 build 4, mac-port has support for big endian platforms,
and has been tested in MAC OSX 10.4, Linux PowerPC and SunOS Sparc,
but need more tests in more OSes and more Platforms.

%description -l zh_CN.UTF-8
Monkey's Audio Codec, 一个无损音频编码器（几乎都带有.ape扩展名）。
这是MAC的Linux移动。
从3.99u4b4开始,mac开始支持许多平台，并在MAC OSX 10.4, Linux PowerPC和SunOS Sparc
上测试过了，不过需要更多平台和OS的测试。

%package        devel
Group:          Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Summary:        Libraries and header files for MAC
Summary(zh_CN.UTF-8): MAC的库和头文件
Requires:       %{name} = %{version}-%{release}

%description devel
Libraries and header files for Monkey's Audio Codec Linux port.

%description devel -l zh_CN.UTF-8
Monkey's Audio Codec Linux移植的库和头文件。

%prep
%setup -q -n mac-3.99-u4-b5
%patch0 -p1

%build
%configure
make  %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=$RPM_BUILD_ROOT install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
[ -d $RPM_BUILD_ROOT ] && rm -rf $RPM_BUILD_ROOT;

%files
%defattr(-,root,root)
%doc README AUTHORS  COPYING ChangeLog TODO INSTALL NEWS
%{_libdir}/lib*
%{_bindir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 3.99u4b5-8
- 为 Magic 3.0 重建

* Fri Aug 08 2014 Liu Di <liudidi@gmail.com> - 3.99u4b5-7
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 3.99u4b5-6
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Liu Di <liudidi@gmail.com> - 3.99u4b5-5
- 为 Magic 3.0 重建

* Tue Oct 10 2006 Liu Di <liudidi@gmail.com> - 3.99u4b5-1mgc
- update to 3.99u4b5

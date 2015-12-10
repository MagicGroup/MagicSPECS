%undefine _hardened_build

Summary: A MPEG-4 encoder
Summary(zh_CN.UTF-8): MPEG-4 编码器
Name: faac
Version: 1.28
Release: 5%{?dist}
License: LGPL
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Source0: %{name}-%{version}.tar.bz2
Patch1:	faac-1.28-gcc4.patch
Url: http://prdownloads.sourceforge.net/faac/faac-1.25.tar.gz?use_mirror=mesh
BuildRequires: autoconf automake libtool faad2-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)


%description
FAAC supports several MPEG-4 object types (LC, LTP, HE AAC, Main, PS) and file formats (raw AAC, MP4, ADTS AAC), multichannel and gapless en/decoding as well as MP4 metadata tags.

%description -l zh_CN.UTF-8
FAAC 支持若干 MPEG-4 对象类型（LC, LTP, HE AAC, Main, PS）和文件格式

%package devel
Summary: Development libs for faac
Summary(zh_CN.UTF-8): faac 的开发库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: faad2-devel

%description devel
Header files and static libraries for faac.

%description -l zh_CN.UTF-8
faac 的头文件和静态库。

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
find . -type f | xargs dos2unix
chmod -R 777 *

%build
./bootstrap
%configure --with-mp4v2
make %{?_smp_mflags} CXXFLAGS="-O3 -pipe" CFLAGS="-O3 -pipe"

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
%{__rm} -f %{buildroot}%{_libdir}/*.la


%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING NEWS README ChangeLog
%{_bindir}/faac
%{_libdir}/libfaac.so.*
%{_mandir}/man1/faac.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 1.28-5
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 1.28-4
- 为 Magic 3.0 重建

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 1.28-3
- 为 Magic 3.0 重建

* Sun Nov 20 2011 Liu Di <liudidi@gmail.com> - 1.28-2
- 为 Magic 3.0 重建

* Fri Nov 09 2007 Liu Di <liudidi@gmail.com> - 1.26-1mgc
- update to 1.26

* Sat Sep 22 2007 kde <athena_star@163.com> - 1.25-1mgc
- Initial build

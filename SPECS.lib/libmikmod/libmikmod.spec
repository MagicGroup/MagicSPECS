Summary: A MOD music file player library
Summary(zh_CN.UTF-8): MOD 音乐文件播放器库
Name: libmikmod
Version: 3.3.7
Release: 3%{?dist}
License: GPLv2 and LGPLv2+
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: esound-devel
URL: http://mikmod.raphnet.net/
Source0: http://downloads.sourceforge.net/project/mikmod/libmikmod/%{version}/libmikmod-%{version}.tar.gz
Patch3:  libmikmod-multilib.patch
Patch4:  libmikmod-autoconf.patch
Patch5:  libmikmod-info.patch

%description
libmikmod is a library used by the mikmod MOD music file player for
UNIX-like systems. Supported file formats include MOD, STM, S3M, MTM,
XM, ULT and IT.

%description -l zh_CN.UTF-8
libmikmod 是 mikmod MOD 音乐文件播放器使用的库。支持的文件格式包括
MOD, STM, S3M, MTM, XM, ULT 和 IT。

%package devel
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary: Header files and documentation for compiling mikmod applications
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name} = %{version}-%{release}
Provides: mikmod-devel = 3.2.2-4
Obsoletes: mikmod-devel < 3.2.2-4

%description devel
This package includes the header files you will need to compile
applications for mikmod.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-%{version}

%build
%configure
make %{?_smp_flags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT%{_infodir}/dir $RPM_BUILD_ROOT%{_libdir}/*.a
find $RPM_BUILD_ROOT | grep "\\.la$" | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%post devel
[ -x /sbin/install-info ] && /sbin/install-info %{_infodir}/mikmod.info %{_infodir}/dir || :

%postun -p /sbin/ldconfig

%postun devel
if [ $1 = 0 ] ; then
	[ -x /sbin/install-info ] && /sbin/install-info  --delete %{_infodir}/mikmod.info %{_infodir}/dir || :
fi

%files
%defattr(-, root, root)
%doc AUTHORS COPYING.LIB COPYING.LESSER NEWS README TODO
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root)
%{_bindir}/*-config
%{_libdir}/*.so
%{_datadir}/aclocal/*
%{_includedir}/*
%{_infodir}/mikmod*
%{_mandir}/man1/libmikmod-config*
%{_libdir}/pkgconfig/libmikmod.pc

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 3.3.7-3
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 3.3.7-2
- 更新到 3.3.7

* Tue Jul 22 2014 Liu Di <liudidi@gmail.com> - 3.3.6-1
- 更新到 3.3.6

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 3.2.0-0.beta2.2
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Liu Di <liudidi@gmail.com> - 3.2.0-0.beta2.1
- 为 Magic 3.0 重建


#  Build from TAR gzip source code with : rpmbuild -ta autoconvert-0.3.14.tar.gz
Name: autoconvert
Summary: autoconvert - Program for converting one chinese language code to another.
Summary(zh_CN.UTF-8): 转换一种中文编码到另一种的程序。
Version: 0.3.16
Release: 8%{?dist}
License: GPL
Group: Applications/Text
Group(zh_CN.UTF-8): 应用程序/文本
Url: http://people.debian.org/~ygh
Source0: http://people.debian.org/~ygh/%{name}-%{version}.tar.gz
Patch1: autoconvert-no-install.patch
Patch2: autoconvert-0.3.16-fix.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
#Prefix: %{_prefix}
#Requires: 
Packager:  kde <jack@linux.net.cn>

%description
Program for converting one chinese language code to another.

%description -l zh_CN.UTF-8
AutoConvert 是一个汉字编码自动识别转换的程序，目前他可以自动识别 GB/Big5/HZ 编码，
可以转换 gb/big5/hz/uni/utf7/utf8 编码。当文本超过 1000 字时，对 GB/Big5 的识别准
确率接近 100%。HZ 识别率也近似 100%。这个程序最初的目的，也是它现在最大用途就是配
合 procmail 对电子邮件进行汉字编码自动转换。

AutoConvert 现在还很简单，不能处理 GB/Big5/HZ 混合编码。

%package devel
Summary: AutoConvert header files.
Summary(zh_CN.UTF-8): AutoConvert 的头文件。
Group: Applications/Tools 
Group(zh_CN.UTF-8): 应用程序/工具

%description devel
AutoConvert header files.

%description devel -l zh_CN.UTF-8
AutonConvert 的头文件。

%prep
%setup

%patch1 -p1
%patch2 -p1

%build
make OPTIMIZE="%{optflags}"


%install
rm -rf $RPM_BUILD_ROOT
#%makeinstall
cd $RPM_BUILD_DIR/%{name}-%{version}
install -D -m 755 autogb $RPM_BUILD_ROOT%{_bindir}/autogb
mkdir -p $RPM_BUILD_ROOT%{_libdir}
#install -m 644 lib/*.so* $RPM_BUILD_ROOT%{_libdir}
install -m 755 lib/libhz.so.0.0 $RPM_BUILD_ROOT%{_libdir}/libhz.so.0.0
install -D -m 755 lib/libhz.a $RPM_BUILD_ROOT%{_libdir}/libhz.a
mkdir -p $RPM_BUILD_ROOT%{_datadir}
install -m 644 contrib/xchat-plugins/*.so* $RPM_BUILD_ROOT%{_datadir}
install -D -m 755 contrib/xchat-plugins/xchat-autogb.so $RPM_BUILD_ROOT%{_datadir}/zh-autoconvert/xchat-autogb.so
install -D -m 755 contrib/xchat-plugins/xchat-autob5.so $RPM_BUILD_ROOT%{_datadir}/zh-autoconvert/xchat-autob5.so
mkdir -p $RPM_BUILD_ROOT%{_includedir}
install -m 644 include/*.h $RPM_BUILD_ROOT%{_includedir}
cd $RPM_BUILD_ROOT%{_bindir}
ln -s autogb autob5
cd $RPM_BUILD_ROOT%{_libdir}
ln -s libhz.so.0.0 libhz.so.0
ln -s libhz.so.0.0 libhz.so 



%clean
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_DIR/%{name}-%{version}


%files
%defattr(-,root,root)
%doc GPL Readme LICENSE
%{_bindir}/auto*
%{_libdir}/libhz.so.*
%{_datadir}/*
%exclude %{_libdir}/debug

%files devel
%defattr(-,root,root)
%{_libdir}/libhz.a
%{_libdir}/libhz.so
%{_includedir}/*.h

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.3.16-6
- 为 Magic 3.0 重建

* Tue Nov 01 2011 Liu Di <liudidi@gmail.com> - 0.3.16-5
- 为 Magic 3.0 重建

* Tue Feb 8 2005 kde <jack@linux.net.cn>
- initialized the first spec file

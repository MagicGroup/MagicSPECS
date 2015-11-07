#  Build from TAR gzip source code with : rpmbuild -ta autoconvert-0.3.14.tar.gz
Name: cconv
Summary: a iconv based simplified-traditional chinese conversion tool 
Summary(zh_CN.UTF-8): 简繁中文转换程序
Version: 0.6.2
Release: 3%{?dist}
License: GPL
Group: Applications/Text
Group(zh_CN.UTF-8): 应用程序/文本
Url: http://code.google.com/p/cconv
Source0: http://cconv.googlecode.com/files/%{name}-%{version}.tar.gz
Patch1:	cconv-0.6.2-fix-libunicode-conflict.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Packager: Liu Di <liudidi@gmail.com>

%description
a iconv based simplified-traditional chinese conversion tool 

%description -l zh_CN.UTF-8
简繁中文转换程序，由于linux下广泛使用的iconv只支持单字一一对应转换，
cconv在iconv的基础上增加了词语转换功能。

%package devel
Summary: %name header files.
Summary(zh_CN.UTF-8): %name 的头文件。
Group: Applications/Tools 
Group(zh_CN.UTF-8): 应用程序/工具

%description devel
%name header files.

%description devel -l zh_CN.UTF-8
%name 的头文件。

%prep
%setup
%patch1 -p1

%build
autoreconf -fisv
%configure
make %{?_smp_mflags} OPTIMIZE="%{optflags}"


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

rm -f %{buildroot}%{_libdir}/lib*.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_DIR/%{name}-%{version}


%files
%defattr(-,root,root)
%{_bindir}/cconv
%{_libdir}/libcconv.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/libcconv.so
%{_libdir}/libcconv.a

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.6.2-3
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.6.2-2
- 为 Magic 3.0 重建

* Fri Nov 04 2011 Liu Di <liudidi@gmail.com> - 0.6.2-1
- 更新到 0.6.2

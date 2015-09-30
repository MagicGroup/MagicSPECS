Name:		SDL_rtf
Version:		0.1.0
Release:		4%{?dist}
Summary:	Simple DirectMedia Layer Rich Text Format (RTF) library
Summary(zh_CN.UTF-8): 简单直接媒体层(SDL)富文本格式(RTF)库
Group:		System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
License:		LGPL
URL:			http://www.libsdl.org/projects/SDL_rtf/
Source0:		http://www.libsdl.org/projects/%{name}/release/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	SDL >= 1.2.4 SDL_ttf freetype
BuildRequires:	SDL-devel >= 1.2.4 SDL_ttf-devel
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	zlib-devel


%description
This library allows you to display simple Rich Text Format (RTF) files in
SDL applications. The RTF format specification is available at:
http://msdn.microsoft.com/library/default.asp?url=/library/en-us/dnrtfspec/html/rtfspec.asp

%description -l zh_CN.UTF-8
这个库允许你在SDL应用程序中显示简单富文本格式(RTF)文件。RTF格式的描述可以下面找到：
http://msdn.microsoft.com/library/default.asp?url=/library/en-us/dnrtfspec/html/rtfspec.asp

%package	devel
Summary:	Files to develop SDL applications which use Rich Text Format (RTF) files
Summary(zh_CN.UTF-8):	SDL_rtf的开发文件
Group:		Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:	%{name} = %{version}-%{release}
Requires:	SDL-devel >= 1.2.4


%description devel
This library allows you to display simple Rich Text Format (RTF) files in
SDL applications.This package provides the libraries, include files and
other resources needed for developing SDL_rtf applications.

%description devel -l zh_CN.UTF-8
这个库允许你在SDL应用程序中显示简单富文本格式(RTF)文件。
这个包包含了开发SDL_rtf应用程序需要的库，包含文件和其它资源。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags} OPTIMIZE="%{optflags}"

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/%{name}-%{version}

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc README CHANGES COPYING
%{_libdir}/lib*.so*


%files devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_includedir}/SDL/*.h


%changelog
* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 0.1.0-4
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.1.0-3
- 为 Magic 3.0 重建

* Tue Jan 31 2006 kde <jack@linux.net.cn> 0.1.0-1mgc
- initial spec file

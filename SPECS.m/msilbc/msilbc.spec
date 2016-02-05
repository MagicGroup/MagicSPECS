%define	major 0
%define libname %name-libs
%define develname %name-devel

Summary:	msiLBC is low bitrate audio codec - plugin for mediastreamer
Summary(zh_CN.UTF-8): msiLBC 是一个低采样率的音频编码，可用在媒体服务插件
Name:		msilbc
Version:	2.1.2
Release:	9%{?dist}
License:	GPL2
Group:  System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:		http://www.linphone.org
Source0:	http://download.savannah.gnu.org/releases/linphone/plugins/sources/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ortp-devel
BuildRequires:	linphone-devel 
BuildRequires:	libilbc-devel

%description
This package supplies the mediastreamer plugin for the iLBC audio
codec, which is necessary to use the codec with Linphone.
iLBC is low bitrate audio codec - plugin for mediastreamer.
Needed to build Google Talk libjingle voice call support with iLBC codec.

%description -l zh_CN.UTF-8
msiLBC 是一个低采样率的音频编码，可用在媒体服务插件。

#--------------------------------------------------------------------
%package -n %{libname}
Summary:	Library files for msiLBC
Summary(zh_CN.UTF-8): %{name} 的动态运行库
Group:  System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description -n	%{libname}
This package supplies the mediastreamer plugin for the iLBC audio
codec, which is necessary to use the codec with Linphone.
iLBC is low bitrate audio codec - plugin for mediastreamer.
Needed to build Google Talk libjingle voice call support with iLBC codec.

%description -n %{libname} -l zh_CN.UTF-8
%{name} 的动态运行库。

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/mediastreamer/plugins/libmsilbc.so.%{major}*


#--------------------------------------------------------------------
%package -n %{develname}
Summary:	Development files for msiLBC library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
This package supplies the mediastreamer plugin for the iLBC audio
codec, which is necessary to use the codec with Linphone.
iLBC is low bitrate audio codec - plugin for mediastreamer.
Needed to build Google Talk libjingle voice call support with iLBC codec.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%files -n %{develname}
%defattr(-,root,root)
%doc README INSTALL AUTHORS COPYING NEWS
%{_libdir}/mediastreamer/plugins/libmsilbc.so
%{_libdir}/mediastreamer/plugins/libmsilbc.la


#--------------------------------------------------------------------
%prep
%setup -q

%build
export ILBC_CFLAGS='%{optflags}'
export ILBC_LIBS='%_libdir'
%configure
%{__make}

%install
rm -rf %{buildroot}
%makeinstall

%clean
rm -rf %{buildroot}




%changelog
* Wed Feb 03 2016 Liu Di <liudidi@gmail.com> - 2.1.2-9
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 2.1.1-8
- 为 Magic 3.0 重建

* Sat Jul 25 2015 Liu Di <liudidi@gmail.com> - 2.1.1-7
- 为 Magic 3.0 重建

* Sat Apr 18 2015 Liu Di <liudidi@gmail.com> - 2.1.1-6
- 更新到 2.1.1

* Thu Jan 01 2015 Liu Di <liudidi@gmail.com> - 2.0.3-6
- 为 Magic 3.0 重建

* Tue Jun 24 2014 Liu Di <liudidi@gmail.com> - 2.0.3-5
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 2.0.3-4
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.0.3-3
- 为 Magic 3.0 重建

* Wed Jan 18 2012 Liu Di <liudidi@gmail.com> - 2.0.3-2
- 为 Magic 3.0 重建

* Wed Apr 06 2011 José Melo <mmodem@mandriva.org> 2.0.3-1mdv2011.0
+ Revision: 650838
- Add missing buildrequire libilbc-devel
- Add missing buildrequire linphone-devel
- Add missing buildrequire ortp-devel
- import msilbc


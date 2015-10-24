%define debug_package %{nil}
Summary: Audio Video Standard of China
Summary(zh_CN.UTF-8): 中国的音频视频标准
Name: xavs
Version: 0.1.51
Release: 5%{?dist}
License: GPL
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://xavs.sourceforge.net/
Source0: %{name}-trunk.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Requires: %{name}-libs = %{version}-%{release}

%description
AVS is the Audio Video Standard of China.  This project aims to
implement high quality AVS encoder and decoder.


%package libs
Summary: Shared libs for %{name}
Summary(zh_CN.UTF-8): %{name} 的共享库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description libs
Shared libraries for %{name}.

%description libs -l zh_CN.UTF-8
%{name} 的动态共享库。

%package static
Summary: Static libs for %{name}
Summary(zh_CN.UTF-8): %{name} 的静态库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description static
Static libraries for %{name}.

%description static -l zh_CN.UTF-8
%{name} 的静态库。

%package devel
Summary: Devel files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
Devel files for %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。

%prep
%setup -q -n trunk

%build
export CFLAGS="%{optflags}"
./configure \
  --bindir=%{_bindir} \
  --libdir=%{_libdir} \
  --includedir=%{_includedir} \
  --enable-pic --enable-shared

%install
rm -rf %{buildroot}
make install \
  DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc doc/*.txt
%{_bindir}/xavs

%files libs
%defattr(-,root,root,-)
%{_libdir}/libxavs.so.*

%files static
%defattr(-,root,root,-)
%{_libdir}/libxavs.a

%files devel
%defattr(-,root,root,-)
%{_libdir}/libxavs.so
%{_includedir}/xavs.h
%{_libdir}/pkgconfig/xavs.pc

%changelog
* Wed Oct 21 2015 Liu Di <liudidi@gmail.com> - 0.1.51-5
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.1.51-4
- 为 Magic 3.0 重建

* Thu Feb 23 2012 Liu Di <liudidi@gmail.com> - 0.1.51-3
- 为 Magic 3.0 重建

* Mon Mar 14 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.1.51-2
- Initial build.


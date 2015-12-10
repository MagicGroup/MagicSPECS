Name: libipt
Version:	1.4.3
Release:	3%{?dist}
Summary: Intel Processor Trace Decoder Library
Summary(zh_CN.UTF-8): Intel 处理器跟踪信息解码库
License: BSD
URL: https://github.com/01org/processor-trace
Source0: https://github.com/01org/processor-trace/archive/v1.4.2.tar.gz
BuildRequires: cmake
ExclusiveArch: %{ix86} x86_64

%description
The Intel Processor Trace (Intel PT) Decoder Library is Intel's reference
implementation for decoding Intel PT.  It can be used as a standalone library
or it can be partially or fully integrated into your tool.

%description -l zh_CN.UTF-8
Intel 处理器跟踪信息解码库。

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%package devel
Summary: Header files and libraries for Intel Processor Trace Decoder Library
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name}%{?_isa} = %{version}-%{release}
ExclusiveArch: %{ix86} x86_64

%description devel
The %{name}-devel package contains the header files and libraries needed to
develop programs that use the Intel Processor Trace (Intel PT) Decoder Library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n processor-trace-%{version}

%build
# -DPTUNIT:BOOL=ON has no effect on ctest.
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DPTUNIT:BOOL=OFF \
       -DFEATURE_THREADS:BOOL=ON \
       -DDEVBUILD:BOOL=ON \
       .
make VERBOSE=1 %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
%global develdocs howto_libipt.md
(cd doc;cp -p %{develdocs} ..)
magic_rpm_clean.sh

%check
ctest -V %{?_smp_mflags}

%files
%doc README
%license LICENSE
%{_libdir}/%{name}.so.*

%files devel
%doc %{develdocs}
%{_includedir}/*
%{_libdir}/%{name}.so

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 1.4.3-3
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.4.3-2
- 更新到 1.4.3

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 1.4.2-2
- 为 Magic 3.0 重建

* Mon Aug 31 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 1.4.2-1
- Initial Fedora packaging.

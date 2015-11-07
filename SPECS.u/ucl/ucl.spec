Name:           ucl
Version:        1.03
Release:        11%{?dist}
Summary:        Portable lossless data compression library
Summary(zh_CN.UTF-8): 可移植的无损数据压缩库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
License:        GPLv2+
URL:            http://www.oberhumer.com/opensource/ucl/
Source0:        http://www.oberhumer.com/opensource/ucl/download/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
UCL is a portable lossless data compression library written in ANSI C.
UCL implements a number of compression algorithms that achieve an
excellent compression ratio while allowing *very* fast decompression.
Decompression requires no additional memory.

%description -l zh_CN.UTF-8
用 ANSI C 编写的可移植的无损数据压缩库。

%package        devel
Summary:        UCL development files
Summary(zh_CN.UTF-8):	%name 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:       %{name} = %{version}-%{release}

%description    devel
%{summary}.

%description devel -l zh_CN.UTF-8
%name 的开发包。

%prep
%setup -q


%build
%configure --disable-dependency-tracking --enable-shared --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libucl.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING NEWS README THANKS TODO
%{_libdir}/libucl.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/ucl/
%{_libdir}/libucl.so


%changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 1.03-11
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.03-10
- 为 Magic 3.0 重建



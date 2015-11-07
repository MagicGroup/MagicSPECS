Name:		dotconf
Version:	1.3
Release:	5%{?dist}
Summary:	Libraries to parse configuration files
Summary(zh_CN.UTF-8): 解析配置文件的库

Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	LGPLv2
URL:		http://www.opentts.org/projects/dotconf
Source:		http://files.opentts.org/dotconf/%{name}-%{version}.tar.gz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
 

%description
Dotconf is a library used to handle configuration files.

%description -l zh_CN.UTF-8
Dotconf 是用来处理配置文件的库。

%package        devel
Summary:	Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}
Requires: 	pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description    devel -l zh_CN.UTF-8
%{name}-devel 软件包包含了用 %{name} 开发应用程序所需的库和头文件。

%prep
%setup -q

# Override config.{guess,sub}
#cp -p /usr/lib/rpm/config.{guess,sub} .

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

find $RPM_BUILD_ROOT -type f -name "*.a" -o -name "*.la" | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README AUTHORS COPYING 
%{_libdir}/libdotconf*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/*

%{_libdir}/libdotconf*.so
%{_includedir}/dotconf.h
%{_libdir}/pkgconfig/dotconf.pc

%{_docdir}/dotconf/*

%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 1.3-5
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.3-3
- 为 Magic 3.0 重建



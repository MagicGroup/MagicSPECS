Name:           libspiro
Version:        20071029
Release:        4%{?dist}
Summary:        Library to simplify the drawing of beautiful curves
Summary(zh_CN.UTF-8): 简单描绘优美曲线的库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
License:        GPLv2+
URL:            http://libspiro.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}_src-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This library will take an array of spiro control points and 
convert them into a series of b茅zier splines which can then 
be used in the myriad of ways the world has come to use b茅ziers. 

%description -l zh_CN.UTF-8
简单描绘优美曲线的库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n libspiro-20071029

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README gpl.txt README-RaphLevien
%{_libdir}/*.so.*

%files devel
%doc README gpl.txt README-RaphLevien
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 20071029-4
- 为 Magic 3.0 重建

* Wed Jan 11 2012 Liu Di <liudidi@gmail.com> - 20071029-3
- 为 Magic 3.0 重建



Name:           libtiger
Version:        0.3.4
Release:        5%{?dist}
Summary:        Rendering library for Kate streams using Pango and Cairo
Summary(zh_CN.UTF-8): 使用 Pango 和 Cairo 的 Kate 流渲染库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://libtiger.googlecode.com
Source0:        http://libtiger.googlecode.com/files/libtiger-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libkate-devel >= 0.2.7
BuildRequires:  pango-devel
%ifnarch mips64el
BuildRequires:  valgrind
%endif
BuildRequires:  doxygen


%description
Libtiger is a rendering library for Kate streams using Pango and Cairo.
More information about Kate streams may be found at 
http://wiki.xiph.org/index.php/OggKate

%description -l zh_CN.UTF-8
Libtiger 是使用 Pango 和 Cairo 的 Kate 流渲染库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       pango-devel
Requires:       libkate-devel >= 0.2.7

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description    devel -l zh_CN.UTF-8
%{name}-devel 软件包包含了使用 %{name} 开发应用程序所需的库和头文件。


%package        doc
Summary:        Documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的文档
Group:          Documentation
Group(zh_CN.UTF-8): 文档
BuildArch:      noarch

%description    doc
The %{name}-doc package contains Documentation for %{name}.

%description doc -l zh_CN.UTF-8
%{name}-doc 软件包包含了 %{name} 的文档。



%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT __doc
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Fix timestramps change
touch -r include/tiger/tiger.h.in $RPM_BUILD_ROOT%{_includedir}/tiger/tiger.h

# Move docdir
mv $RPM_BUILD_ROOT%{_docdir}/%{name} __doc

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/tiger/
%{_libdir}/*.so
%{_libdir}/pkgconfig/tiger.pc

%files doc
%defattr(-,root,root,-)
%doc examples __doc/html


%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.3.4-5
- 为 Magic 3.0 重建

* Fri Aug 01 2014 Liu Di <liudidi@gmail.com> - 0.3.4-4
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.3.4-3
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Liu Di <liudidi@gmail.com> - 0.3.4-2
- 为 Magic 3.0 重建


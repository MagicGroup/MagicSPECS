%define with_java 0

Summary: A Grammar Checking library
Summary(zh_CN.UTF-8): 一个语法检查库
Name: link-grammar
Version: 4.7.4
Release: 3%{?dist}
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License: BSD
Source: http://www.abisource.com/downloads/link-grammar/%{version}/link-grammar-%{version}.tar.gz
URL: http://abisource.com/projects/link-grammar/
BuildRequires: aspell-devel, libedit-devel
%if %{with_java}
BuildRequires: java-devel, libgcj-devel, jpackage-utils, ant
%endif

%description
A library that can perform grammar checking.

%description -l zh_CN.UTF-8
可以进行语法检查的一个库。

%package devel
Summary: Support files necessary to compile applications with liblink-grammar
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group: Development/Libraries
Group(zh-CN.UTF-8): 开发/库
Requires: link-grammar = %{version}-%{release}

%description devel
Libraries, headers, and support files needed for using liblink-grammar.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件

%if %{with_java}
%package java
Summary: Java libraries for liblink-grammar
Summary(zh_CN.UTF-8): %{name} 的 Java 库
Group: Development/Libraries
Group(zh-CN.UTF-8): 开发/库
Requires: java >= 1:1.6.0
Requires: jpackage-utils
Requires: link-grammar = %{version}-%{release}

%description java
Java libraries for liblink-grammar

%description java -l zh_CN.UTF-8
%{name} 的 Java 库

%package java-devel
Summary: Support files necessary to compile Java applications with liblink-grammar
Summary(zh_CN.UTF-8): 使用 %{name} 编译 Java 程序需要的支持文件
Group: Development/Libraries
Group(zh-CN.UTF-8): 开发/库
Requires: link-grammar-java = %{version}-%{release}
Requires: link-grammar-devel = %{version}-%{release}

%description java-devel
Libraries for developing Java components using liblink-grammar.

%description java-devel -l zh_CN.UTF-8
使用 %{name} 编译 Java 程序需要的支持文件。
%endif

%prep
%setup -q

%build
%configure --disable-static --enable-pthreads \
%if ! %{with_java}
	   --disable-java-bindings
%endif
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
#make
# currently the build system can not handle smp_flags properly
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README ChangeLog
%{_bindir}/*
%{_libdir}/liblink-grammar.so.*
%{_datadir}/link-grammar
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/liblink-grammar.so
%{_libdir}/pkgconfig/link-grammar.pc
%{_includedir}/link-grammar

%if %{with_java}
%files java
%defattr(-,root,root,-)
%{_libdir}/liblink-grammar-java.so.*
%{_javadir}/linkgrammar*.jar

%files java-devel
%defattr(-,root,root,-)
%{_libdir}/liblink-grammar-java.so
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%if %{with_java}
%post java -p /sbin/ldconfig
%postun java -p /sbin/ldconfig
%endif

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.7.4-3
- 为 Magic 3.0 重建

* Sun Oct 28 2012 Liu Di <liudidi@gmail.com> - 4.7.4-2
- 为 Magic 3.0 重建

* Wed Oct 26 2011 Liu Di <liudidi@gmail.com> - 4.7.4-1
- 从 fedora 移植 spec

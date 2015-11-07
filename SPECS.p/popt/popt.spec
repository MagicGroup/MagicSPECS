Summary:	C library for parsing command line parameters
Summary(zh_CN.UTF-8):	用来解析命令行参数的 C 库。
Name:		popt
Version:	1.16
Release:	6%{?dist}
License:	MIT
Group:		System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
URL:		http://www.rpm5.org/
Source0:	http://www.rpm5.org/files/%{name}/%{name}-%{version}.tar.gz
Source1:	http://people.redhat.com/jantill/fedora/png-mtime.py
Patch0:		popt-1.13-multilib.patch
Patch1:		popt-1.13-popt_fprintf.patch
BuildRequires:	gettext, doxygen, graphviz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Popt is a C library for parsing command line parameters. Popt was
heavily influenced by the getopt() and getopt_long() functions, but
it improves on them by allowing more powerful argument expansion.
Popt can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments. Popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.

%description -l zh_CN.UTF-8
pt 是一个用来解析命令行参数的 C 库。Popt 受 getopt() 和 getopt_long()
函数的影响很深，但是它又对其有所改进，它允许更大的参数扩增。 Popt
能够解析任意 argv[] 样式的参数组，并且按照命令行参数来自动设立变量。
Popt 允许命令行参数通过配置文件来定别名，并包括使用 shell 一样的规则
把任意字串解析入 argv[] 参数组的工具函数。

%package devel
Summary:	Development files for the popt library
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group:		Development/Libraries
Group(zh_CN.UTF-8):   开发/库
Requires:	%{name} = %{version}-%{release}

%description devel
The popt-devel package includes header files and libraries necessary
for developing programs which use the popt C library. It contains the
API documentation of the popt library, too.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件

%package static
Summary:	Static library for parsing command line parameters
Summary(zh_CN.UTF-8): %{name} 的静态库
Group:		Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:	%{name}-devel = %{version}-%{release}

%description static
The popt-static package includes static libraries of the popt library.
Install it if you need to link statically with libpopt.

%description static -l zh_CN.UTF-8
%{name} 的静态库

%prep
%setup -q
#%patch0 -p1 -b .multilib
#%patch1 -p1 -b .popt_fprintf

%build
%configure 
make %{?_smp_mflags}
doxygen

# Solve multilib problems by changing the internal PNG timestamp to a reference timestamp;
# see http://fedoraproject.org/wiki/PackagingDrafts/MultilibTricks for further information.
#if [ $(ls doxygen/html/*{__,graph_legend}*.png 2> /dev/null | wc -l) -gt 0 ]; then
#  for png in doxygen/html/*{__,graph_legend}*.png; do python %{SOURCE1} $png CHANGES; done
#fi

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Move libpopt.{so,a} to %{_libdir}
rm -f $RPM_BUILD_ROOT%{_libdir}/libpopt.la

# Multiple popt configurations are possible
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/popt.d

magic_rpm_clean.sh
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc CHANGES COPYING
%{_sysconfdir}/popt.d
%{_libdir}/libpopt.so.*

%files devel
%defattr(-,root,root)
%doc README doxygen/html
%{_libdir}/libpopt.so
%{_libdir}/pkgconfig/popt.pc
%{_includedir}/popt.h
%{_mandir}/man3/popt.3*

%files static
%defattr(-,root,root)
%{_libdir}/libpopt.a

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.16-6
- 为 Magic 3.0 重建

* Tue Jul 28 2015 Liu Di <liudidi@gmail.com> - 1.16-5
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.16-4
- 为 Magic 3.0 重建

* Thu Jan 26 2012 Liu Di <liudidi@gmail.com> - 1.16-2
- 为 Magic 3.0 重建

* Fri Jul 25 2008 Liu Di <liudidi@gmail.com> - 1.13-1mgc
- 从 rpm 中分离

%{!?tcl_version: %define tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %define tcl_sitearch %{_libdir}/tcl%{tcl_version}}
%{!?tcl_sitelib: %define tcl_sitelib %{_datadir}/tcl%{tcl_version}}
%define tixmajor 8.4
%define tcltkver 8.4.13

Summary: A set of extension widgets for Tk
Summary(zh_CN.UTF-8): 一组 Tk 的扩展组件
Name: tix
Epoch: 1
Version: %{tixmajor}.3
Release: 13%{?dist}
License: BSD
Group: Development/Languages
Group(zh_CN.UTF-8): 开发/语言
URL: http://tix.sourceforge.net/
Source0: http://dl.sourceforge.net/sourceforge/tix/Tix%{version}-src.tar.gz
Patch0: tix-8.4.2-link.patch
Patch1: tix-8.4.3-tcl86.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: tcl(abi) = 8.6
Requires: tcl >= %{tcltkver}, tk >= %{tcltkver}
#Requires: /etc/ld.so.conf.d
Buildrequires: tcl-devel >= %{tcltkver}, tk-devel >= %{tcltkver}
BuildRequires: libX11-devel

%description
Tix, the Tk Interface eXtension, is a powerful set of user interface
components that expands the capabilities of your Tcl/Tk and Python
applications. Using Tix together with Tk will greatly enhance the
appearance and functionality of your application.

%description -l zh_CN.UTF-8
Tix (Tk 界面扩展) 是 Tk 构件集的增件，它是一个有 40 多个构件的可扩展集合。
通常来说，Tix 构件比在 Tk 中提供的构件更复杂更有能力。Tix 构件包括：组合
箱，Motif 样式的文件选择箱，MS Windows 样式的文件选择箱，分板的窗口，笔记
本，分层次的列表，目录树，以及文件管理器。

%package devel
Summary: Tk Interface eXtension development files
Summary(zh_CN.UTF-8): Tk 接口扩展开发文件
Group: Development/Languages
Group(zh_CN.UTF-8): 开发/语言
Requires: tix = %{epoch}:%{version}-%{release}

%description devel
Tix, the Tk Interface eXtension, is a powerful set of user interface
components that expands the capabilities of your Tcl/Tk and Python
applications. Using Tix together with Tk will greatly enhance the
appearance and functionality of your application.

This package contains the tix development files needed for building
tix applications.

%description devel -l zh_CN.UTF-8
Tix (Tk 界面扩展) 是 Tk 构件集的增件，它是一个有 40 多个构件的可扩展集合。
通常来说，Tix 构件比在 Tk 中提供的构件更复杂更有能力。Tix 构件包括：组合
箱，Motif 样式的文件选择箱，MS Windows 样式的文件选择箱，分板的窗口，笔记
本，分层次的列表，目录树，以及文件管理器。
 
这个包包含了建立tix应用程序需要的tix开发文件。

%package doc
Summary: Tk Interface eXtension documentation
Summary(zh_CN.UTF-8): %{name} 的文档
Group: Development/Languages
Group(zh_CN.UTF-8): 开发/语言
Requires: tix = %{epoch}:%{version}-%{release}

%description doc
Tix, the Tk Interface eXtension, is a powerful set of user interface
components that expands the capabilities of your Tcl/Tk and Python
applications. Using Tix together with Tk will greatly enhance the
appearance and functionality of your application.

This package contains the tix documentation

%description doc -l zh_CN.UTF-8
%{name} 的文档.

%prep
%setup -q -n Tix%{version}
%patch0 -p1 -b .link
%patch1 -p1 -b .tcl86

%build
%configure --with-tcl=%{_libdir} --with-tk=%{_libdir} --libdir=%{tcl_sitearch}
make all %{?_smp_mflags} PKG_LIB_FILE=libTix.so

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT PKG_LIB_FILE=libTix.so

# move shared lib to tcl sitearch
mv $RPM_BUILD_ROOT%{tcl_sitearch}/Tix%{version}/libTix.so \
	$RPM_BUILD_ROOT%{tcl_sitearch}
pwd
# make links
ln -sf ../libTix.so \
	$RPM_BUILD_ROOT%{tcl_sitearch}/Tix%{version}/libTix.so
ln -sf tcl%{tcl_version}/Tix%{version}/libTix.so $RPM_BUILD_ROOT%{_libdir}/libTix.so
ln -sf tcl%{tcl_version}/Tix%{version}/libTix.so $RPM_BUILD_ROOT%{_libdir}/libtix.so

# install demo scripts
mkdir -p $RPM_BUILD_ROOT%{tcl_sitelib}/Tix%{tixmajor}
cp -a demos $RPM_BUILD_ROOT%{tcl_sitelib}/Tix%{tixmajor}

# the header and man pages were in the previous package, keeping for now...
mkdir -p $RPM_BUILD_ROOT%{_includedir}
install -m 0644 generic/tix.h $RPM_BUILD_ROOT%{_includedir}/tix.h
mkdir -p $RPM_BUILD_ROOT%{_mandir}/mann
cp man/*.n $RPM_BUILD_ROOT%{_mandir}/mann

# Handle unique library path (so apps can actually find the library)
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
echo "%{tcl_sitearch}" > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/tix-%{_arch}.conf

# ship docs except pdf
rm -rf docs/pdf
find docs -name .cvsignore -exec rm '{}' ';'

# these files end up in the doc directory
rm -f $RPM_BUILD_ROOT%{_libdir}/Tix%{tixmajor}/README.txt
rm -f $RPM_BUILD_ROOT%{_libdir}/Tix%{tixmajor}/license.terms
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{tcl_sitearch}/libTix.so
%{tcl_sitearch}/Tix%{version}
%{_sysconfdir}/ld.so.conf.d/*
%doc *.txt *.html license.terms

%files devel
%defattr(-,root,root,-)
%{_includedir}/tix.h
%{_libdir}/libtix.so
%{_libdir}/libTix.so
%{_mandir}/mann/*.n*

%files doc
%defattr(-,root,root,-)
%doc docs/*
%doc %{tcl_sitelib}/Tix%{tixmajor}

%changelog
* Sat Oct 03 2015 Liu Di <liudidi@gmail.com> - 1:8.4.3-13
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 1:8.4.3-12
- 为 Magic 3.0 重建

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 1:8.4.3-11
- 为 Magic 3.0 重建

* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 1:8.4.3-10
- 为 Magic 3.0 重建

* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 1:8.4.3-9
- 为 Magic 3.0 重建

* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 1:8.4.3-8
- 为 Magic 3.0 重建

* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 1:8.4.3-7
- 为 Magic 3.0 重建

* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 1:8.4.3-6
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1:8.4.3-5
- 为 Magic 3.0 重建

* Wed Feb 15 2012 Liu Di <liudidi@gmail.com> - 1:8.4.3-4
- 为 Magic 3.0 重建



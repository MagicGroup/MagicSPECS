%define build_type release

Summary: automoc4
Summary(zh_CN.UTF-8): 自动 moc 文件生成工具
Name: automoc4
Version: 0.9.88
Release: 6%{?dist}
License: LGPL v2.1 or later
Group: Development/Tools
Group(zh_CN.UTF-8): 开发/工具
Source0: http://mirrors.ustc.edu.cn/kde/stable/%{name}/%{version}/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

BuildRequires: cmake >= 2.6.2
BuildRequires: qt4-devel >= 4.4.3
Requires: qt4 >= 4.4.3

Provides: automoc = %{version}

%description
automoc4 is a tool to add rules for generating Qt moc files
automatically to projects that use CMake as the buildsystem.

%description -l zh_CN.UTF-8
automoc4 是一个自动生成 Qt moc 文件的工具。使用 CMake 做为
建立系统。

%prep
%setup -q -n %{name}-%{version}

%build
mkdir build
cd build
export CFLAGS=$RPM_OPT_FLAGS
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_BUILD_TYPE=%{build_type} \
	-DCMAKE_CXX_FLAGS_DEBUG:STRING="$RPM_OPT_FLAGS" \
%if "%{?_lib}" == "lib64" 
        -DLIB_SUFFIX=64 \
%endif 
	-DLIB_INSTALL_DIR=%{_libdir} ..

make %{?_smp_mflags}

%install
cd build
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
%{_bindir}/automoc4
%{_libdir}/automoc4/*

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.9.88-6
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.9.88-4
- 为 Magic 3.0 重建

* Tue Dec 04 2012 Liu Di <liudidi@gmail.com> - 0.9.88-3
- 为 Magic 3.0 重建

* Fri Jan 23 2009 Ni Hui <shuizhuyuanluo@126.com> - 0.9.88-0.1mgc
- 更新至 0.9.88
- 戊子  十二月廿八

* Tue Jan 13 2009 Ni Hui <shuizhuyuanluo@126.com> - 0.9.87-0.2mgc
- 重建
- 戊子  十二月十八

* Sun Oct 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.9.87-0.1mgc
- 更新至 0.9.87
- 戊子  九月十四

* Fri Aug 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.9.84-0.2mgc
- 重建
- 戊子  七月廿九

* Thu Jul 24 2008 Liu Di <liudidi@gmail.com> - 0.9.84-0.1mgc
- 更新到 0.9.84

* Sat Jun 21 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.9.83-0.1mgc
- 更新至 0.9.83
- 包命名为 automoc4
- 戊子  五月十八  [夏至]

* Tue Jun 3 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.0.svn816294-0.1mgc
- 更新至 0.0.svn816294
- 戊子  四月三十

* Thu May 8 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.0.svn803436-0.1mgc
- 更新至 0.0.svn803436
- 首次生成 rpm 包
- 戊子  三月初四

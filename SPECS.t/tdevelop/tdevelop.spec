%define debug 0
%define final 0

%define kde_version 3.5.9
%define qt_version 3.3.8

%define git 1
%define gitdate 20111229

#真正的版本号，rpm的版本号是为和其它组件一致
%define real_ver 3.5.4

Name: tdevelop
Summary: Integrated Development Environment for C++/C
Summary(zh_CN.UTF-8): C++/C的集成开发环境
Version: 3.5.14
%if %{git}
Release: 0.git%{gitdate}%{?dist}
%else
Release: 0.1%{?dist}
%endif
URL: http://www.kdevelop.org/
Group: Development/Tools
Group(zh_CN.UTF-8): 开发/工具
BuildRoot: %{_tmppath}/%{name}-buildroot
License: GPL

%if %{git}
Source: %{name}-git%{gitdate}.tar.xz
%else
Source: ftp://ftp.kde.org/pub/kde/stable/apps/KDE3.x/ide/%{name}-%{version}.tar.bz2
%endif
Source1: make_tdevelop_git_package.sh
Source2: doctreeview.tar.gz

Patch3: kdevelop-gcc44.patch
Patch4: kchm-frame.patch
Patch5: kdevelop-kchmpart.patch

Prereq: /sbin/ldconfig

Requires: make
Requires: perl >= 5.004
Requires: autoconf >= 2.13
Requires: automake >= 1.4
Requires: flex >= 2.5.4
Requires: qt-designer >= %{qt_version}

BuildPrereq: autoconf
BuildPrereq: automake
BuildPrereq: libtool
BuildPrereq: kdelibs-devel >= %{kde_version}
Obsoletes: kdevelop-c_c++_ref

%description
The KDevelop Integrated Development Environment provides many features
that developers need as well as providing a unified interface to programs
like gdb, the C/C++ compiler, and make. KDevelop manages or provides:

All development tools needed for C++ programming like Compiler,
Linker, automake and autoconf; KAppWizard, which generates complete,
ready-to-go sample applications; Classgenerator, for creating new
classes and integrating them into the current project; File management
for sources, headers, documentation etc. to be included in the
project; The creation of User-Handbooks written with SGML and the
automatic generation of HTML-output with the KDE look and feel;
Automatic HTML-based API-documentation for your project's classes with
cross-references to the used libraries; Internationalization support
for your application, allowing translators to easily add their target
language to a project;

KDevelop also includes WYSIWYG (What you see is what you get)-creation
of user interfaces with a built-in dialog editor; Debugging your
application by integrating KDbg; Editing of project-specific pixmaps
with KIconEdit; The inclusion of any other program you need for
development by adding it to the "Tools"-menu according to your
individual needs.

%description -l zh_CN.UTF-8
KDevelop 集成开发环境提供了许多开发者需要的功能，它还提供了一个统一的到 
gdb(C/C++ 编译器)和 make 之类的程序的界面。KDevelop 管理或提供：所有 C++ 
编程所需的工具，如编译器、链接器、 automake、和 autoonf；生成完整的立刻
可用的范例程序的 KAppWizard；用来创建新类别并将它们集成到当前计划中去的 
Classgenerator；用于要包括在计划中的源码、头文件、文档等的文件管理；创建
用 SGML 编写的用户手册并自动生成带有 KDE 外观的 HTML 输出；自动化的带有
到使用库的跨参考的基于 HTML 的关于您的计划的类别的 API 文档；对国际化您
的程序的支持，允许翻译者在计划中添加他们的语言。 KDevelop 还包括使用内建
的对话框编辑器来创建用户界面的 WYSIWYG(所见即所得)；通过集成 KDbg 来调试
您的程序；用 KIconEdit 编辑计划特有的像素图；根据您的个人需要，通过在“工
具”菜单上添加来包括您开发所需的其它程序。

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Provides: kdevelop-devel = %{version}-%{release}
Requires: tdevelop = %{version}-%{release}
Requires: tdelibs-devel

%description devel
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。

%prep
%if %{git}
%setup -q -n %{name}-git%{gitdate}
%else
%setup -q
%endif
tar zxf %{SOURCE2} -C parts/
%patch4 -p1

#临时补丁
sed -i 's/tqApp/qApp/g' kdevdesigner/designer/listeditor.ui.h

%build
QTDIR="" && source /etc/profile.d/qt.sh

  export PATH=`pwd`:$PATH
mkdir build 
cd build
%cmake 	-DWITH_BUILDTOOL_ALL=ON \
	-DWITH_LANGUAGE_ALL=ON \
	-DWITH_VCS_ALL=ON \
	-DBUILD_ALL=ON \
	-DWITH_DEPRECATION=ON ..

make %{?_smp_mflags} 

%install
rm -rf %{buildroot}
cd build
make DESTDIR=%{buildroot} install

# remove useless files
rm -rf %{buildroot}%{_prefix}/kdevbdb

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/trinity/*
%{_libdir}/kconf_update_bin/*
%{_datadir}/applications/kde/*
%{_datadir}/apps/*
%{_datadir}/config/*
%{_datadir}/desktop-directories/*
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/icons/locolor/*/*/*
%{_datadir}/mimelnk/application/*
%{_datadir}/mimelnk/x-fortran.desktop
%{_datadir}/services/*
%{_datadir}/servicetypes/*
%{_libdir}/lib*.so.*
%{_libdir}/lib*.la

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_includedir}/*

%changelog
* Wed Oct 1 2008 Ni Hui <shuizhuyuanluo@126.com> - 3.5.3-1.1mgc
- 基于 subversion-1.5.x 重建
- 去除 kchm 补丁
- 拆出 devel 包
- 戊子  九月初三

* Mon Sep 01 2008 Liu Di <liudidi@gmail.com> - 3.5.3-1mgc
- 更新到 3.5.3

* Wed Feb 19 2008 Liu Di <liudidi@gmail.com> - 3.5.1-1mgc
- update to 3.5.1

* Fri Oct 19 2007 Liu Di <liudidi@gmail.com> - 3.5.0-1mgc
- update to 3.5.0

* Tue May 29 2007 Liu Di <liudidi@gmail.com> - 3.4.1-1mgc
- update to 3.4.1

* Sun Jan 27 2007 Liu Di <liudidi@gmail.com> - 3.4.0-1mgc
- update to 3.4.0

* Fri Jan 26 2007 Liu Di <liudidi@gmail.com> - 3.3.6-1mgc
- update to 3.3.6

* Sat Oct 21 2006 Liu Di <liudidi@gmail.com> - 3.3.5-1mgc
- update to 3.3.5

* Fri Aug 25 2006 Liu Di <liudidi@gmail.com> - 3.3.4-1mgc
- update to 3.3.4

* Thu Jul 01 2006 Liu Di <liudidi@gmail.com>
- update to 3.3.3

* Mon Apr 17 2006 KanKer <kanker@163.com>
- 3.3.2
* Tue Feb 9 2006 KanKer <kanker@163.com>
- 3.3.1
* Sat Nov 26 2005 KanKer <kanker@163.com>
- 3.3.0
* Thu Oct 18 2005 KanKer <kanker@163.com>
- 3.2.3
* Mon Aug 1 2005 KanKer <kanker@163.com>
- 3.2.2
* Tue Jun 2 2005 KanKer <kanker@163.com>
- 3.2.1
- patched kchmpart to display Chinese

* Sun Mar 21 2005 KanKer <kanker@163.com>
- 3.2.0

* Fri Dec 17 2004 KanKer <kanker@163.com>
- 3.1.2

* Fri Oct 15 2004 KanKer <kanker@163.com>
- update to 3.1.1

* Sat Aug 21 2004 KanKer <kanker@163.com>
- 3.1.0

* Mon Jul 12 2004 KanKer <kanker@163.com>
- add a patch for opening a chm file in frame.

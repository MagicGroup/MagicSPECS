# Disable -debuginfo package generation
#define debug_package   %{nil}
%define real_name kdepimlibs

%define apidocs 1

Name: kdepimlibs4
Summary: KDE PIM Libraries
License: LGPL v2 or later
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
URL: http://www.kde.org/
Version: 4.14.3
Release: 1%{?dist}
%define rversion %version
Source0: http://download.kde.org/stable/%{rversion}/src/%{real_name}-%{rversion}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# magic patches
# compability with Windows Live Writer, patch by nihui, Aug 8th 2010
Patch100: kdepimlibs-4.5.0-kxmlrpcclient-compability-datetime-query.patch

BuildRequires: boost-devel openldap-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: gpgme-devel
BuildRequires: libkdelibs4-devel >= %{version}
BuildRequires: qt4-devel >= 4.4.3
BuildRequires: libXpm-devel libXtst-devel
BuildRequires: akonadi-devel >= 1.13.0
BuildRequires: automoc4 >= 0.9.87
BuildRequires: libical-devel >= 0.33
BuildRequires: prison-devel >= 1.0
BuildRequires: qjson-devel 

%if %apidocs
BuildRequires: docbook-dtds
BuildRequires: doxygen
BuildRequires: graphviz
BuildRequires: qt4-doc
%endif

Requires: kdelibs4 >= %{version}
Requires: libkdepimlibs4 >= %{version}


%description
This package contains the basic packages for KDE PIM applications.

%description  -l zh_CN.UTF-8
KDE PIM 的基本程序.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package -n libkdepimlibs4
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: KDE PIM Libraries
Requires: libkdelibs4 >= %{version}

Provides: kdepimlibs4-libs = %{version}-%{release}
# 以下两个包自 KDE 4.2.95 起从 kdepim 移入 kdepimlibs
Obsoletes: kdepim4-libkholidays
Obsoletes: kdepim4-maildir

#Provides: kdepimlibs4-akonadi = %{version}-%{release}
#Obsoletes: kdepimlibs4-akonadi < %{version}-%{release}

%description -n libkdepimlibs4
This package contains the basic libraries for KDE PIM applications.

%description -n libkdepimlibs4 -l zh_CN.UTF-8
KDE PIM 程序的基本库.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package -n %{name}-akonadi
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: PIM Storage Service Libraries
Requires: libkdelibs4 >= %{version}

%description -n %{name}-akonadi
This package contains the libraries of Akonadi, the KDE PIM storage
service.

%description -n %{name}-akonadi -l zh_CN.UTF-8
KDE PIM 存储服务

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package -n libkdepimlibs4-devel
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: KDE PIM Libraries: Build Environment
Requires: kdepimlibs4 >= %{version} libkdelibs4-devel cyrus-sasl-devel openldap-devel boost-devel
Requires: libkdepimlibs4 >= %{version}

Provides: kdepimlibs4-devel = %{version}-%{release}

%description -n libkdepimlibs4-devel
This package contains all necessary include files and libraries needed
to develop KDE PIM applications.

%description -n libkdepimlibs4-devel -l zh_CN.UTF-8
libkdepimlibs4 的开发包.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package apidocs
Group: Development/Documentation
Group(zh_CN.UTF-8): 开发/文档
Summary: kdepimlibs API documentation
Summary(zh_CN.UTF-8): kdepimlibs API 文档

%description apidocs
This package includes the kdepimlibs API documentation in HTML
format for easy browsing.

%description apidocs -l zh_CN.UTF-8
本软件包包含 HTML 格式的 kdepimlibs API 文档。

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

%prep
%setup -q -n %{real_name}-%{rversion}

#%patch1 -p1
#%patch2 -p1

%patch100 -p0

%build

mkdir build
pushd build
%cmake_kde4 ..

make %{?_smp_mflags}
popd

# build apidocs
%if %apidocs
export QTDOCDIR="%{?_qt4_docdir}"
%{kde4_bindir}/kde4-doxygen.sh --doxdatadir=%{kde4_htmldir}/en/common .
%endif

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%if %apidocs
mkdir -p %{buildroot}%{kde4_htmldir}/en
cp -prf ../kdepimlibs-%{version}-apidocs %{buildroot}%{kde4_htmldir}/en/kdepimlibs4-apidocs
find   %{buildroot}%{kde4_htmldir}/en/ -name 'installdox' -exec rm -fv {} ';'
%endif

magic_rpm_clean.sh

%clean_kde4_desktop_files

# Strip ELF binaries
for f in `find "$RPM_BUILD_ROOT" -type f \( -perm -0100 -or -perm -0010 -or -perm -0001 \) -exec file {} \; | \
        grep -v "^${RPM_BUILD_ROOT}/\?usr/lib/debug"  | \
        grep -v ' shared object,' | \
        sed -n -e 's/^\(.*\):[  ]*ELF.*, not stripped/\1/p'`; do
        echo "$f"
        /usr/bin/strip -g -v "$f" || :
done
for f in `find "$RPM_BUILD_ROOT" -type f -a -exec file {} \; | \
        grep -v "^${RPM_BUILD_ROOT}/\?usr/lib/debug"  | \
        grep ' shared object,' | \
        sed -n -e 's/^\(.*\):[  ]*ELF.*, not stripped/\1/p'`; do
        echo "$f"
        /usr/bin/strip -v --strip-unneeded "$f"
done

# %check
# cd build
# make test || :

%post -n libkdepimlibs4 -p /sbin/ldconfig
%postun -n libkdepimlibs4 -p /sbin/ldconfig

%post -n %{name}-akonadi -p /sbin/ldconfig
%postun -n %{name}-akonadi -p /sbin/ldconfig

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files -n libkdepimlibs4
%defattr(-,root,root)
%{kde4_libdir}/libkabc.so.*
%{kde4_libdir}/libkabc_file_core.so.*
%{kde4_libdir}/libkcal.so.*
%{kde4_libdir}/libkholidays.so.*
%{kde4_libdir}/libkldap.so.*
%{kde4_libdir}/libkmime.so.*
%{kde4_libdir}/libkpimtextedit.so.*
%{kde4_libdir}/libkresources.so.*
%{kde4_libdir}/libktnef.so.*
%{kde4_libdir}/libkxmlrpcclient.so.*
%{kde4_libdir}/libsyndication.so.*
%{kde4_libdir}/libkimap.so.*
%{kde4_libdir}/libkblog.so.*
%{kde4_libdir}/libkpimutils.so.*
%{kde4_libdir}/libmicroblog.so.*
%{kde4_libdir}/libgpgme++.so.*
%{kde4_libdir}/libgpgme++-pthread.so.*
#%{kde4_libdir}/libgpgme++-pth.so.*
%{kde4_libdir}/libkpimidentities.so.*
%{kde4_libdir}/libqgpgme.so.*
%{kde4_libdir}/libkontactinterface.so.*
%{kde4_libdir}/libkcalcore.so.*
%{kde4_libdir}/libkcalutils.so.*
%{kde4_libdir}/libkmbox.so.*

%files -n %{name}-akonadi
%defattr(-,root,root)
%{kde4_libdir}/libakonadi-kabc.so*
%{kde4_libdir}/libakonadi-kde.so*
%{kde4_libdir}/libakonadi-kmime.so*
%{kde4_libdir}/libakonadi-contact.so*
%{kde4_libdir}/libakonadi-kcal.so*
%{kde4_libdir}/libakonadi-calendar.so.*
%{kde4_libdir}/libakonadi-socialutils.so*
%{kde4_libdir}/libmailtransport.so*
%{kde4_libdir}/libakonadi-notes.so*
%{kde4_libdir}/libkalarmcal.so*
%{kde4_appsdir}/akonadi
%{kde4_appsdir}/akonadi-kde
%{kde4_bindir}/akonadi2xml
%{kde4_bindir}/akonaditest
%{kde4_libdir}/libakonadi-xml.so.*
%{kde4_plugindir}/kcm_mailtransport.so
%{kde4_appsdir}/kconf_update/mailtransports.upd
%{kde4_appsdir}/kconf_update/migrate-transports.pl
%{kde4_servicesdir}/kcm_mailtransport.desktop
%{kde4_kcfgdir}/mailtransport.kcfg
%{kde4_datadir}/mime/packages/x-vnd.akonadi.socialfeeditem.xml
%{kde4_datadir}/akonadi/agents/knutresource.desktop

%files -n libkdepimlibs4-devel
%defattr(-,root,root)
%{kde4_includedir}/*
%{kde4_appsdir}/cmake
# internal cmake module
%{kde4_libdir}/cmake
%{kde4_libdir}/libkabc.so
%{kde4_libdir}/libkabc_file_core.so
%{kde4_libdir}/libkcal.so
%{kde4_libdir}/libkholidays.so
%{kde4_libdir}/libkldap.so
%{kde4_libdir}/libkmime.so
%{kde4_libdir}/libkpimtextedit.so
%{kde4_libdir}/libkresources.so
%{kde4_libdir}/libktnef.so
%{kde4_libdir}/libkxmlrpcclient.so
%{kde4_libdir}/libsyndication.so
%{kde4_libdir}/libkimap.so
%{kde4_libdir}/libkblog.so
%{kde4_libdir}/libkpimutils.so
%{kde4_libdir}/libmicroblog.so
%{kde4_libdir}/libgpgme++.so
%{kde4_libdir}/libgpgme++-pthread.so
#%{kde4_libdir}/libgpgme++-pth.so
%{kde4_libdir}/libkpimidentities.so
%{kde4_libdir}/libqgpgme.so
%{kde4_libdir}/libkontactinterface.so
%{kde4_libdir}/libmailtransport.so
%{kde4_libdir}/libakonadi-calendar.so
%{kde4_libdir}/libkcalcore.so
%{kde4_libdir}/libkcalutils.so
%{kde4_libdir}/libkmbox.so
%{kde4_libdir}/libakonadi-xml.so
%dir %{kde4_libdir}/gpgmepp
%{kde4_libdir}/gpgmepp/GpgmeppConfig.cmake
%{kde4_libdir}/gpgmepp/GpgmeppLibraryDepends.cmake

%files
%defattr(-,root,root)
%doc COPYING COPYING.BSD COPYING.LIB
%exclude %{kde4_appsdir}/cmake
%exclude %{kde4_appsdir}/akonadi
%exclude %{kde4_appsdir}/akonadi-kde
%{kde4_plugindir}/*
%{kde4_appsdir}/*
%{kde4_kcfgdir}/*
%{kde4_datadir}/mime/packages/kdepimlibs-mime.xml
%{kde4_dbus_interfacesdir}/*
%{kde4_servicesdir}/*
%{kde4_servicetypesdir}/*
#%{kde4_kcfgdir}/mailtransport.kcfg
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/kresources
%doc %lang(en) %{kde4_htmldir}/en/kioslave

%exclude %{kde4_plugindir}/kcm_mailtransport.so
%exclude %{kde4_appsdir}/kconf_update/mailtransports.upd
%exclude %{kde4_appsdir}/kconf_update/migrate-transports.pl
%exclude %{kde4_servicesdir}/kcm_mailtransport.desktop

%if %apidocs
%files apidocs
%defattr(-,root,root,-)
%{kde4_htmldir}/en/kdepimlibs4-apidocs
%endif

%changelog
* Tue Dec 30 2014 Liu Di <liudidi@gmail.com> - 4.14.3-1
- 更新到 4.14.3

* Wed Oct 22 2014 Liu Di <liudidi@gmail.com> - 4.14.2-1
- 更新到 4.14.2

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-1
- 更新到 4.13.3

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Thu May 22 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2.3
- 为 Magic 3.0 重建

* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2.2
- 为 Magic 3.0 重建

* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2.1
- 为 Magic 3.0 重建

* Sat Dec 5 2009 Ni Hui <shuizhuyuanluo@126.com> -4.3.4-1mgc
- 更新至 4.3.4
- 乙丑  十月十九

* Fri Jul 31 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-1mgc
- 更新至 4.3.0(KDE 4.3 try2)
- 己丑  六月初十

* Mon Jun 29 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.95-1mgc
- 更新至 4.2.95(KDE 4.3 RC1)
- 己丑  闰五月初七

* Thu Jun 11 2009 Liu Di <liudidi@gmail.com> - 4.2.90-1
- 更新到 4.2.90 ( 4.3 beta2 )
- 已丑　五月十九

* Fri May 29 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.88-1mgc
- 更新至 4.2.88
- 己丑  五月初六

* Sat May 16 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.85-1mgc
- 更新至 4.2.85(KDE 4.3 Beta1)
- 己丑  四月廿二

* Sat Apr 4 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.2-1mgc
- 更新至 4.2.2
- 己丑  三月初九  [清明]

* Sun Mar 8 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.1-0.2mgc
- 重建
- 己丑  二月十二

* Sun Mar 1 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.1-0.1mgc
- 更新至 4.2.1
- 使用 rpm 宏
- 己丑  二月初五

* Thu Jan 22 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.0-0.1mgc
- 更新至 4.2.0(KDE 4.2 try1)
- 戊子  十二月廿七

* Tue Jan 13 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.1.96-0.1mgc
- 更新至 4.1.96(KDE 4.2 RC1)
- relwithdeb 编译模式
- 戊子  十二月十八

* Fri Dec 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.85-0.1mgc
- 更新至 4.1.85(KDE 4.2 Beta2)
- 戊子  十一月十五

* Sun Nov 23 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.80-0.1mgc
- 更新至 4.1.80
- 戊子  十月廿六

* Sun Oct 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.69-0.1mgc
- 更新至 4.1.69
- debugfull 编译模式
- 戊子  九月十四

* Mon Sep 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.2-0.1mgc
- 更新至 4.1.2
- 戊子  九月初一

* Sun Sep 14 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.1-0.2mgc
- 上游补丁(patch 100)
- 戊子  八月十五

* Fri Aug 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.1-0.1mgc
- 更新至 4.1.1-try1(内部版本)
- 戊子  七月廿九

* Thu Jul 24 2008 Liu Di <liudidi@gmail.com> - 4.1.0-0.1mgc
- 更新到 4.1.0(KDE 4.1 正式版)

* Thu Jul 10 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.98-0.1mgc
- 更新至 4.0.98(KDE 4.1 RC1)
- release 模式编译(build_type release)
- 戊子  六月初八

* Sat Jul 5 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.85-0.1mgc
- 更新至 4.0.85
- 戊子  六月初三

* Fri Jun 27 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.84-0.1mgc
- 更新至 4.0.84
- 戊子  五月廿四

* Thu Jun 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.83-0.1mgc
- 更新至 4.0.83-try1(第一次 tag 4.1.0-beta2 内部版本)
- 戊子  五月十六

* Wed Jun 11 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.82-0.1mgc
- 更新至 4.0.82
- 戊子  五月初八

* Wed Jun 4 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.81-0.1mgc
- 更新至 4.0.81
- 戊子  五月初一

* Fri May 23 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.80-0.1mgc
- 更新至 4.0.80(try1 内部版本)
- 戊子  四月十九

* Fri May 16 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.74-0.1mgc
- 更新至 4.0.74
- 戊子  四月十二

* Sat May 10 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.73-0.1mgc
- 更新至 4.0.73
- 戊子  四月初六

* Sun May 4 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.72-0.1mgc
- 更新至 4.0.72
- 戊子  三月廿九

* Sat Apr 26 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.71-0.1mgc
- 更新至 4.0.71
- 戊子  三月廿一

* Sat Apr 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.70-0.1mgc
- 更新至 4.0.70
- 戊子  三月十四

* Sat Apr 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.69-0.1mgc
- 更新至 4.0.69
- 拆出 akonadi 包
- 戊子  三月初七

* Sun Mar 30 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.3-0.1mgc
- 更新至 4.0.3
- 定义 kde4 路径
- 戊子  二月廿三

* Fri Mar 7 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.2-0.2mgc
- 重建
- 关闭 verbose 编译模式(cmake_verbose_build = 0)
- 戊子  正月三十

* Sun Mar 2 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.2-0.1mgc
- 更新至 4.0.2
- 戊子  正月廿五

* Wed Feb 6 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.1-0.1mgc
- 更新至 4.0.1

* Fri Jan 11 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.0-0.1mgc
- 更新至 4.0.0

* Wed Dec 12 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.97.0-0.1mgc
- 更新至 3.97.0 (KDE4-RC2)
- 简化 spec 文件 %file 字段

* Sat Nov 24 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.96.0-0.1mgc
- 更新至 3.96.0 (KDE4-RC1)

* Sat Oct 20 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.94.0-0.1mgc
- 首次生成 rpm 包

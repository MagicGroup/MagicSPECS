#define svn_number rc1
%define real_name baloo

%define kde4_enable_final_bool ON

Name: kde4-%{real_name}
Summary: A framework for searching and managing metadata
Summary(zh_CN.UTF-8): 查找和管理元数据的框架
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Version: 4.13.1
Release: 1%{?dist}
License: LGPL
URL: http://extragear.kde.org/apps/kipi
%define rversion %version
Source0: http://mirror.bjtu.edu.cn/kde/stable/%{rversion}/src/%{real_name}-%{version}.tar.xz
Source1: 97-kde-baloo-filewatch-inotify.conf
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext
BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82
BuildRequires: kde4-kfilemetadata-devel

BuildRequires: pkgconfig(akonadi) >= 1.11.80
BuildRequires: pkgconfig(QJson)
# for %%{_polkit_qt_policydir} macro
BuildRequires: polkit-qt-devel
BuildRequires: xapian-core-devel

%description
A framework for searching and managing metadata.

%description -l zh_CN.UTF-8
查找和管理元数据的框架。

%package file
Summary: File indexing and search for %{name}
Summary(zh_CN.UTF-8): %{name} 的文件索引和搜索
Obsoletes: nepomuk-core < 4.13.0
Requires: %{name} = %{version}-%{release}
# for kcm.  since this is split out, we can afford to a%description -l zh_CN.UTF-8 this dep
# and not worry about circular dependencies
Requires: kdebase4-runtime
%description file
%{summary}.

%description file -l zh_CN.UTF-8
%{name} 的文件索引和搜索。

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
Contains the development files.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。包含 libbtcore 的开发文件。

%prep
%setup -q -n %{real_name}-%{rversion}

%build
mkdir build
cd build
%cmake_kde4 ..

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install/fast DESTDIR=%{buildroot} -C build

install -p -m644 -D %{SOURCE1} %{buildroot}%{_prefix}/lib/sysctl.d/97-kde-baloo-filewatch-inotify.conf
install -p -m644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/sysctl.d/97-kde-baloo-filewatch-inotify.conf

magic_rpm_clean.sh

%clean_kde4_desktop_files

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING COPYING.LIB
%{_kde4_bindir}/akonadi_baloo_indexer
%{_kde4_bindir}/balooctl
%{_kde4_bindir}/baloosearch
%{_kde4_bindir}/balooshow
%{_kde4_datadir}/akonadi/agents/akonadibalooindexingagent.desktop
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_datadir}/kde4/services/baloo_contactsearchstore.desktop
%{_kde4_datadir}/kde4/services/baloo_emailsearchstore.desktop
%{_kde4_datadir}/kde4/services/baloo_notesearchstore.desktop
%{_kde4_datadir}/kde4/services/baloosearch.protocol
%{_kde4_datadir}/kde4/services/plasma-runner-baloosearch.desktop
%{_kde4_datadir}/kde4/services/tags.protocol
%{_kde4_datadir}/kde4/services/timeline.protocol
%{_kde4_datadir}/kde4/servicetypes/baloosearchstore.desktop
%{_kde4_libdir}/kde4/akonadi/akonadi_baloo_searchplugin.so
%{_kde4_libdir}/kde4/akonadi/akonadibaloosearchplugin.desktop
%{_kde4_libdir}/kde4/baloo_contactsearchstore.so
%{_kde4_libdir}/kde4/baloo_emailsearchstore.so
%{_kde4_libdir}/kde4/baloo_notesearchstore.so
%{_kde4_libdir}/kde4/kio_baloosearch.so
%{_kde4_libdir}/kde4/kio_tags.so
%{_kde4_libdir}/kde4/kio_timeline.so
%{_kde4_libdir}/kde4/krunner_baloosearchrunner.so

%post file
if [ -f "%{_sysconfdir}/sysctl.d/97-kde-nepomuk-filewatch-inotify.conf" ]; then
  mv -f "%{_sysconfdir}/sysctl.d/97-kde-nepomuk-filewatch-inotify.conf" && \
        "%{_sysconfdir}/sysctl.d/97-kde-nepomuk-filewatch-inotify.conf.rpmsave"
fi

%files file
%ghost %config(missingok,noreplace) %{_sysconfdir}/sysctl.d/97-kde-baloo-filewatch-inotify.conf
%{_prefix}/lib/sysctl.d/97-kde-baloo-filewatch-inotify.conf
%{_kde4_datadir}/autostart/baloo_file.desktop
%{_kde4_bindir}/baloo_file
%{_kde4_bindir}/baloo_file_cleaner
%{_kde4_bindir}/baloo_file_extractor
%{_datadir}/dbus-1/interfaces/org.kde.baloo.file.indexer.xml
%{_kde4_libexecdir}/kde_baloo_filewatch_raiselimit
%{_sysconfdir}/dbus-1/system.d/org.kde.baloo.filewatch.conf
%{_datadir}/dbus-1/system-services/org.kde.baloo.filewatch.service
%{_polkit_qt_policydir}/org.kde.baloo.filewatch.policy
%{_kde4_libdir}/kde4/baloo_filesearchstore.so
%{_kde4_datadir}/kde4/services/baloo_filesearchstore.desktop
%{_kde4_datadir}/kde4/services/kcm_baloofile.desktop
%{_kde4_libdir}/kde4/kcm_baloofile.so
%{_kde4_libdir}/libbaloocore.so.4*
%{_kde4_libdir}/libbaloofiles.so.4*
%{_kde4_libdir}/libbaloopim.so.4*
%{_kde4_libdir}/libbalooxapian.so.4*

%files devel
%{_kde4_includedir}/baloo/
%{_kde4_libdir}/libbaloocore.so
%{_kde4_libdir}/libbaloofiles.so
%{_kde4_libdir}/libbaloopim.so
%{_kde4_libdir}/libbalooxapian.so
%{_kde4_libdir}/cmake/Baloo/

%changelog
* Thu May 22 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Thu Apr 24 2014 Liu Di <liudidi@gmail.com> - 4.13.0-4
- 为 Magic 3.0 重建

* Thu Apr 24 2014 Liu Di <liudidi@gmail.com> - 4.13.0-3
- 为 Magic 3.0 重建

* Thu Apr 24 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 4.13.0-1
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一

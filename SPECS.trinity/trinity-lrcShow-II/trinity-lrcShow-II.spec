# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif
%define tde_pkg kcometen3
%define tde_prefix /opt/trinity
%define tde_appdir %{tde_datadir}/applications
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity


Name: trinity-lrcShow-II
Summary: lrcShow-II amarok script
Summary(zh_CN.UTF-8): lrcShow-II amarok 动态歌词显示脚本
Version:	 0.9.2
Release: 6%{?dist}
License:	 GPL
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Url: http://www.sanfanling.cn/
Source0: http://www.kde-apps.org/CONTENT/content-files/71983-lrcShow-II.amarokscript.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: libtqt3-mt >= 3.2.0
Requires: trinity-amarok >= 1.4.1
# PyQt >= 3.17.3 编译参数为 qt-mt
Requires: trinity-python-trinity >= 3.16.3
Requires: python

# 修正路径为绝对路径
Patch0: lrcShow-II-0.4.2-fix-directpath.patch

%description
lrcShow-II amarok script.

%description -l zh_CN.UTF-8
lrcShow-II amarok 动态歌词显示脚本。

%prep
%setup -q -n lrcShow-II

#%patch0
# 修正路径为绝对路径，否则无法显示图标以及部分功能丧失
sed -i -e 's/\.\.\/scripts\/lrcShow-II\//\/opt\/trinity\/share\/apps\/amarok\/scripts\/lrcShow-II\//g' *.py

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{tde_datadir}/apps/amarok/scripts/lrcShow-II

cp -rf * %{buildroot}%{tde_datadir}/apps/amarok/scripts/lrcShow-II

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-, root, root)
%{tde_datadir}/apps/amarok/scripts/lrcShow-II

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 0.9.2-6
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 0.9.2-5
- 为 Magic 3.0 重建

* Wed Oct 14 2015 Liu Di <liudidi@gmail.com> - 0.9.2-4
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.9.2-3
- 为 Magic 3.0 重建

* Sun Sep 7 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.9.0-0.1mgc
- 更新至 0.9.0
- 戊子  八月初八  [白露]

* Mon Jun 30 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.8.0-0.1mgc
- 更新至 0.8.0
- 戊子  五月廿七

* Sun Jun 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.7.2-0.1mgc
- 更新至 0.7.2
- 戊子  五月廿六

* Thu Jan 24 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.6.0-0.1mgc
- 更新至 0.6.0

* Sun Jan 13 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.5.1-0.1mgc
- 更新至 0.5.1

* Sun Jan 06 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.5.0-0.1mgc
- 更新至 0.5.0
- 移除路径补丁，使用脚本替换

* Sun Dec 23 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.4.2-0.1mgc
- 更新至 0.4.2

* Tue Dec 18 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.4.0-0.1mgc
- 更新至 0.4.0

* Wed Dec 12 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.3.1-0.1mgc
- 升级至 0.3.2

* Mon Dec 10 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.3.1-0.1mgc
- 升级至 0.3.1

* Sun Dec 09 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.3.0-0.1mgc
- init rpm package

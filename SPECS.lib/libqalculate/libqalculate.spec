Summary:	Multi-purpose calculator library
Summary(zh_CN.UTF-8): 多用途的计算库
Name:		libqalculate
Version: 0.9.7
Release: 4%{?dist}
License:	GPLv2+
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:		http://qalculate.sourceforge.net/
Source0:	http://dl.sf.net/sourceforge/qalculate/%{name}-%{version}.tar.gz
Patch0:		libqalculate-gcc43.patch
Patch1:		libqalculate-cln12.patch
Patch2:		libqalculate-0.9.7-pkgconfig_private.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	glib2-devel, cln-devel
BuildRequires:	libxml2-devel
BuildRequires:	readline-devel, ncurses-devel
BuildRequires:	perl(XML::Parser), gettext
BuildRequires:	intltool, libtool, automake, autoconf

%description
This library underpins the Qalculate! multi-purpose desktop calculator for
GNU/Linux.

%description -l zh_CN.UTF-8
本库是 Qalculate! 的一部分，GNU/Linux 下的多用途桌面计算器。

%package	devel
Summary:	Development tools for the Qalculate calculator library
Summary(zh_CN.UTF-8): Qalculate 计算库的开发工具
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel, libxml2-devel, cln-devel

%description	devel
The libqalculate-devel package contains the header files needed for development
with libqalculate.

%description	devel -l zh_CN
libqalculate-devel 软件包包含了用 libqalculate 开发所需的头文件。

%package -n	qalculate
Summary:	Multi-purpose calculator, text mode interface
Summary(zh_CN.UTF-8): 多用途计算器，文本模式界面
Group:		Applications/Engineering
Group(zh_CN.UTF-8): 应用程序/工程
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description -n	qalculate
Qalculate! is a multi-purpose desktop calculator for GNU/Linux. It is
small and simple to use but with much power and versatility underneath.
Features include customizable functions, units, arbitrary precision, plotting.
This package provides the text-mode interface for Qalculate! The GTK and QT
frontends are provided by qalculate-gtk and qalculate-kde packages resp.

%description -n	qalculate -l zh_CN.UTF-8
Qalculate! 是一款 GNU/Linux 下的多用途桌面计算器。它小巧简单易用，但有强大的功能。
包含自定义函数、单位、任意参数、绘图等功能。本软件包提供了 Qalculate! 的文本模式界面。
GTK 和 QT 的前端由 qalculate-gtk 和 qalculate-kde 软件包提供。

%prep
%setup -q
%patch0 -p0 -b .gcc43
#%patch1 -p0 -b .cln
%patch2 -p1

%build
intltoolize --copy --force --automake
libtoolize --force --copy
aclocal
autoheader
automake
autoconf
%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
magic_rpm_clean.sh
%find_lang %{name}
rm -f %{buildroot}/%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

#%files
%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING TODO
%{_libdir}/libqalculate.so.*
%{_datadir}/qalculate/

%files devel
%defattr(-,root,root,-)
%{_libdir}/libqalculate.so
%{_libdir}/pkgconfig/libqalculate.pc
%{_includedir}/libqalculate/

%files -n qalculate
%defattr(-,root,root,-)
%{_bindir}/qalc

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.9.7-4
- 为 Magic 3.0 重建

* Sun Mar 25 2012 Liu Di <liudidi@gmail.com> - 0.9.7-3
- 为 Magic 3.0 重建

* Wed Jan 11 2012 Liu Di <liudidi@gmail.com> - 0.9.7-2
- 为 Magic 3.0 重建

* Sun Jan 25 2009 Ni Hui <shuizhuyuanluo@126.com> - 0.9.6-0.1mgc
- rebuild for Magic Linux 2.1
- 戊子  十二月三十

* Wed Feb 27 2008 Deji Akingunola <dakingun@gmail.com> - 0.9.6-4
- Rebuild (with patch) for cln-1.2

* Sun Feb 10 2008 Deji Akingunola <dakingun@gmail.com> - 0.9.6-3
- Rebuild for gcc43

* Sat Aug 25 2007 Deji Akingunola <dakingun@gmail.com> - 0.9.6-2
- Rebuild

* Fri Aug 03 2007 Deji Akingunola <dakingun@gmail.com> - 0.9.6-2
- License tag update

* Sun Jul 01 2007 Deji Akingunola <dakingun@gmail.com> - 0.9.6-1
- Update to new release

* Tue Jan 02 2007 Deji Akingunola <dakingun@gmail.com> - 0.9.5-1
- New release

* Mon Aug 28 2006 Deji Akingunola <dakingun@gmail.com> - 0.9.4-4
- Rebuild for FC6

* Thu Jun 28 2006 Deji Akingunola <dakingun@gmail.com> - 0.9.4-3
- Arbitrarily bump the release field to fix broken update path

* Wed Jun 27 2006 Deji Akingunola <dakingun@gmail.com> - 0.9.4-1
- New version 0.9.4

* Tue Apr 30 2006 Deji Akingunola <dakingun@gmail.com> - 0.9.3-2
- More BRs from Paul Howarth (#193481)

* Thu Mar 30 2006 Deji Akingunola <dakingun@gmail.com> - 0.9.3-1
- Update to newer version

* Mon Feb 13 2006 Deji Akingunola <dakingun@gmail.com> - 0.9.2-2
- Rebuild for Fedora Extras 5

* Tue Dec 27 2005 Deji Akingunola <dakingun@gmail.com> - 0.9.2-1
- Upgrade to new version

* Sat Nov 05 2005 Deji Akingunola <dakingun@gmail.com> - 0.9.0-1
- Upgrade to new version

* Mon Oct 17 2005 Deji Akingunola <deji.aking@gmail.com> - 0.8.2-3
- Add patch to allow build with cln-1.1.10

* Mon Oct 17 2005 Deji Akingunola <deji.aking@gmail.com> - 0.8.2-2
- Bump the release tag to make even with FC-4 and FC-3 branches

* Tue Oct 11 2005 Paul Howarth <paul@city-fan.org> - 0.8.2-1
- Split off separate qalculate subpackage
- Update to 0.8.2

* Mon Oct 10 2005 Paul Howarth <paul@city-fan.org> - 0.8.1.2-2
- Don't include static libraries
- Include license text
- Don't include README, which only contains a URL
- Include AUTHORS & TODO
- Remove redundant manual dependencies
- Split off separate devel subpackage
- Be more explicit in %%files list
- Add %%post and %%postun scripts to run ldconfig
- Use DESTDIR with make instead of %%makeinstall
- Add buildreqs readline-devel and ncurses-devel

* Wed Oct 05 2005 Deji Akingunola <deji.aking@gmail.com> - 0.8.1.2-1
- Initial package

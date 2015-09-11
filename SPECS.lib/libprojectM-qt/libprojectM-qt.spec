Name:		libprojectM-qt
Version:	2.0.1
Release:	5%{?dist}
Summary:	The Qt frontend to the projectM visualization plugin
Summary(zh_CN.UTF-8): projectM 音乐可视化插件的 Qt 前端
Group:		Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
License:	GPLv2+
URL:		http://projectm.sourceforge.net/
Source0:	http://downloads.sourceforge.net/projectm/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	cmake, qt4-devel, libprojectM-devel = %{version}

%description
projectM-qt is a GUI designed to enhance the projectM user and preset writer
experience.  It provides a way to browse, search, rate presets and setup
preset playlists for projectM-jack and projectM-pulseaudio.

%description -l zh_CN.UTF-8
projectM-qt 是 projectM 的 GUI 前端。提供浏览、搜索等功能。

%package	devel
Summary:	Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}, pkgconfig, libprojectM-devel, qt4-devel

%description	devel
projectM-qt is a GUI designed to enhance the projectM user and preset writer
experience.  It provides a way to browse, search, rate presets and setup
preset playlists for projectM-jack and projectM-pulseaudio.
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description    devel -l zh_CN.UTF-8
projectM-qt 是 projectM 的 GUI 前端。提供浏览、搜索等功能。

%prep
%setup -q

%build
%cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} -DLIB_INSTALL_DIR=%{_libdir} .
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{_datadir}/pixmaps/prjm16-transparent.svg

%files devel
%defattr(-,root,root,-)
%doc ReadMe
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Sep 11 2015 Liu Di <liudidi@gmail.com> - 2.0.1-5
- 为 Magic 3.0 重建

* Mon Jul 28 2014 Liu Di <liudidi@gmail.com> - 2.0.1-4
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.0.1-3
- 为 Magic 3.0 重建

* Wed Jan 11 2012 Liu Di <liudidi@gmail.com> - 2.0.1-2
- 为 Magic 3.0 重建


%define build_type release

%define real_name phonon-backend-vlc

Name: %{real_name}
Summary: VLC backend to Phonon
Summary(zh_CN.UTF-8): Phonon 的 VLC 后端
Version: 0.6.1
Release: 1%{?dist}
URL: http://www.videolan.org/
Source: ftp://ftp.kde.org/pub/kde/stable/%{real_name}/%{version}/src/%{real_name}-%{version}.tar.xz
License: LGPL v2+
Group: System/Libraries
Group(zh_CN.UTF-8): 系统/库
BuildRequires: cmake >= 2.6.2
BuildRequires: qt4-devel >= 4.4.3
BuildRequires: automoc4 >= 0.9.86
BuildRequires: phonon-devel
BuildRequires: vlc-devel
Requires: vlc-core
Provides: phonon-backend

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)


%description
VLC backend to Phonon.

%description -l zh_CN.UTF-8
Phonon 的 VLC 后端。

#--------------------------------------------------------------------

%prep
%setup -q -n %{real_name}-%{version}

%build
mkdir build
cd build
%{cmake_kde4} -DPHONON_LIBRARY="-lphonon" ..
make %{?_smp_mflags}

%install
cd build
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
%{kde4_libdir}/kde4/plugins/phonon_backend/phonon_vlc.so
%{kde4_servicesdir}/phononbackends/vlc.desktop
#%ICON_INSTALL_DIR/hicolor/*/apps/phonon-vlc.*

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.4.1-2
- 为 Magic 3.0 重建

* Thu Aug 19 2010 Ni Hui <shuizhuyuanluo@126.com> - 0.2.0-1mgc
- 首次生成 rpm 包
- 庚寅  七月初十

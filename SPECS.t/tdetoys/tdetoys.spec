%define debug 0
%define final 0
%define libtool 0

%define qt_version 3.3.8
%define arts_version 1.5.10
%define arts 1

%define git 1
%define gitdate 20111228

Summary: KDE Toys Program
Summary(zh_CN.UTF-8): KDE 玩具程序
Name:          tdetoys
Version:       3.5.14
%if %{git}
Release:	0.git%{?gitdate}%{?dist}
%else
Release:       1%{?dist}
%endif
License:     GPL
URL: http://www.kde.org
Group:        User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
BuildRoot:   %{_tmppath}/%{name}-buildroot
%if %{git}
Source0:	%{name}-git%{gitdate}.tar.xz
%else
Source:  ftp://ftp.kde.org/pub/kde/stable/%{version}/src/%{name}-%{version}.tar.bz2
%endif
Source1: make_tdetoys_git_package.sh
Patch:	tdetoys-libtool.patch
Requires: qt, arts, tdelibs, tdebase, alsa-lib, SDL

%description
Toys programs for KDE

%description -l zh_CN.UTF-8
KDE 下的玩具程序。

%prep
%if %{git}
%setup -q  -n %{name}-git%{?gitdate}
%else
%setup -q 
%endif
%patch -p1

%Build
unset QTDIR || : ; . /etc/profile.d/qt.sh

export KDEDIR=%{prefix}
export CXXFLAGS="$RPM_OPT_FLAGS -DNDEBUG -DNO_DEBUG"
export CFLAGS="$RPM_OPT_FLAGS -DNDEBUG -DNO_DEBUG"
make -f admin/Makefile.common
#CFLAGS="$CFLAGS -lXext -lkparts -lz -lsoundserver_idl -lkmedia2_idl -lartsflow_idl -lmcop -ldl -lkdecore -lkdeui -lkdesu -lX11 -lDCOP -lkio -lkdefx" \
#CXXFLAGS="$CXXFLAGS -lXext -lkparts -lz -lsoundserver_idl -lkmedia2_idl -lartsflow_idl -lmcop -ldl -lkdecore -lkdeui -lkdesu -lX11 -lDCOP -lkio -lkdefx" \
%configure \
   --enable-closure \
   --disable-rpath \
%if %{final}
   --enable-final \
%endif
   --with-qt-libraries=$QTDIR/lib

make
%install
mkdir -p $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean   
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr
%exclude /usr/*/debug*

%changelog
* Tue Oct 21 2008 Liu Di <liudidi@gmail.com> - 3.5.10-1mgc
- 为 magic 2.1 打包

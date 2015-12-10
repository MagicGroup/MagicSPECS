%define breq qt4-devel
%define qmake /usr/bin/qmake-qt4
%define lrelease /usr/bin/lrelease-qt4

%define date 20090322

Name:           anticodeluxe
BuildRequires:  gcc-c++ %{breq}
Version:        0.1.96
Release:        6%{?dist}
License:        GPL v2 or later
#Source:         %{name}-git%{date}.tar.bz2
Source0:		http://anticodeluxe.googlecode.com/files/%{name}-%{version}.tar.bz2
Source1:	%{name}-kdm.desktop
Patch1:		%{name}-libx11.patch
Patch2:		anticodeluxe-gcc47.patch
Group:          User Interface/Desktops
Group(zh_CN.UTF-8):	用户界面/桌面
Summary:        Antico Deluxe is a Qt4/X11 Window/Desktop manager for GNU/Linux.
Summary(zh_CN.UTF-8): 用 QT4 写的一个窗口管理器
Prefix:         /usr
Url:		http://code.google.com/p/anticodeluxe/
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

BuildRequires: libao-devel

%description
Antico Deluxe is a fork of famous Antico WM/DE
(http://antico.wordpress.com/), with some new features added and many
new planned.

The goal is to create a Window/Desktop manager simple and fast, with
very aesthetic
and familiar look and feel. 
A very few parameters must be configured from few files, avoiding
unnecessary complications, following the K.I.S.S. philosophy. Any
other configurations like themes, icons etc. should be avoided.
Keeping in very small size while having relatively rich feature set
makes AnticoDeluxe very suitable for netbooks and low-end computers.

%description -l zh_CN.UTF-8
用 QT4 写的一个轻量级窗口管理器。

%prep
%setup -q -n %{name}
%patch1 -p1
%patch2 -p1

%if %{_lib}=="lib64" 
sed -i 's/\/usr\/lib/\/usr\/lib64/g' amelib/amelib.pro
%endif

%build
%{qmake}
make 


%install
%{__rm} -rf %{buildroot}
%{makeinstall} INSTALL_ROOT=%{buildroot}
# FIXME!
rm -rf %{buildroot}/usr/include/ame
mkdir -p %{buildroot}%_datadir/xsessions
install -m 755 %{SOURCE1} %{buildroot}%_datadir/xsessions/%{name}.desktop
mkdir -p %{buildroot}%_datadir/apps/kdm/sessions
install -m 755 %{SOURCE1} %{buildroot}%_datadir/apps/kdm/sessions/%{name}.desktop

%clean
rm -rf %{buildroot}
rm -rf %{buiddir}/%{buildsubdir}

%files
%defattr(-,root,root,-)
%doc AUTHORS BUGS CHANGELOG COPYING README
%{_bindir}/*
%{_libdir}/libame*
%{_datadir}/themes/antico/*
%{_datadir}/xsessions/%{name}.desktop
%_datadir/apps/kdm/sessions/%{name}.desktop

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 0.1.96-6
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.1.96-5
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.1.96-3
- 为 Magic 3.0 重建

* Sat Oct 29 2011 Liu Di <liudidi@gmail.com> - 0.1.96-2
- 为 Magic 3.0 重建

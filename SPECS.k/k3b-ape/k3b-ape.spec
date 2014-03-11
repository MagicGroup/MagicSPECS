%define         tartopdir      k3bmonkeyaudioplugin


Name:           k3b-ape
Version:        3.1
Release:        8%{?dist}
Summary:        Monkey's audio decoder/encoder plugin for K3b
Summary(zh_CN.UTF-8): K3b的APE编码/解码插件
Group:          Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
License:        GPL
URL:            http://www.k3b.org
Source:         http://dl.sf.net/k3b/k3bmonkeyaudioplugin-%{version}.tar.bz2
Patch0:		k3b-ape-gcc44.patch
Patch1:		k3b-ape-tde.patch
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

Requires:       k3b >= 0.11

BuildRequires:  k3b >= 0.11
BuildRequires:  kdelibs-devel >= 3.1, arts-devel
BuildRequires:  zlib-devel, libjpeg-devel
BuildRequires:  libX11-devel


%description
This package adds support for decoding/encoding Monkey's Audio files
to K3b.

%description -l zh_CN.UTF-8
这个包为K3b添加了解码/编码Monkey's Audio文件(APE)的支持。

%prep
%setup -q -n %{tartopdir}-%{version}
%patch0 -p1
%patch1 -p1

%build
[ -z "$QTDIR" ] && . %{_sysconfdir}/profile.d/qt.sh
%configure --prefix=$(kde-config --prefix) --libdir=%{_libdir} --with-extra-includes=%{_includedir}/tqt
%{__make}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,755)
%{_libdir}/kde3/libk3bmonkey*
%{_datadir}/apps/k3b/plugins/k3bmonkey*.plugin


%changelog
* Thu Dec 15 2011 Liu Di <liudidi@gmail.com> - 3.1-8
- 为 Magic 3.0 重建

* Thu Dec 15 2011 Liu Di <liudidi@gmail.com> - 3.1-7
- 为 Magic 3.0 重建

* Mon Oct 09 2006 Liu Di <liudidi@gmail.com> - 3.1-1mgc
- 3.1

* Sat Aug 26 2006 Liu Di <liudidi@gmail.com> - 3.0-1mgc
- 3.0

* Thu Jun 14 2005 KanKer <kanker@163.com>
- 2.0
* Sat Jun 12 2004 KanKer <kanker@163.com>
- rebuild 
* Wed Apr 14 2004 Mihai Maties <mihai@xcyb.org> - 0:1.0-0.fdr.4
- Removed the Packager tag as Ville Skytt盲 suggested
- Indeed "Thu" != "Tuesday" :) - corrected - (thanx Michael Schwendt) 

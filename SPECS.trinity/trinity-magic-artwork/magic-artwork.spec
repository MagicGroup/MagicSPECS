Summary: Artwork for Magic Linux 2.1
Summary(zh_CN.UTF-8): MagicLinux 2.1 的美工
Name:          magic-artwork
Version:       2.1.20071002
Release:       1%{?dist}
License:		GPL
Group:		User Interface/Desktop
Group(zh_CN.UTF-8):	用户界面/桌面
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
Source:		%{name}-%{version}.tar.bz2
Patch1:		magic-artwork-2.1.20071002-tde.patch
Requires:	kdelibs, kdebase

%description
Artwork for Magic Linux 2.1, include kde, gtk, gtk2 themes, wallpapers, and so on.

%description -l zh_CN.UTF-8
Magic Linux 2.1 的美工，包括 kde, gtk, gtk2 主题，墙纸和其它。

%prep
%setup -q
%patch1 -p1

%Build
#pushd plastik 
#./configure --prefix=/usr --enable-final
#make
#popd

pushd screensaver
chmod 777 admin/*
make -f admin/Makefile.common
%configure 
#临时措施
sed -i 's/\/include\/tqt/\/include\/tqt \-lqt\-mt \-ltdecore \-ltdeui \-lDCOP \-lkio \-lX11/g' kscreensaver/*/Makefile
make %{?_smp_mflags}
popd

pushd lipstik-2.2
chmod 777 admin/*
make -f admin/Makefile.common
%configure
sed -i 's/\/include\/tqt/\/include\/tqt \-lqt\-mt \-ltdecore \-ltdeui \-lDCOP \-lkio \-lX11/g' style/*/Makefile
sed -i 's/\/include\/tqt/\/include\/tqt \-lqt\-mt \-ltdecore \-ltdeui \-lDCOP \-lkio \-lX11/g' style/Makefile
sed -i 's/kdefx/tdefx/g' style/Makefile
make %{?_smp_mflags}
popd

# ksplash themes' moodin engin
pushd moodin
chmod 777 admin/*
make -f admin/Makefile.common
%configure 
sed -i 's/\/include\/tqt/\/include\/tqt \-lqt\-mt \-ltdecore \-ltdeui \-ltdefx \-lDCOP \-lkio \-lX11/g' src/Makefile
make %{?_smp_mflags}
popd

%install
#pushd plastik 
#make install DESTDIR=%{buildroot}
#popd

pushd screensaver
make install DESTDIR=%{buildroot}
popd

pushd lipstik-2.2
make install DESTDIR=%{buildroot}
popd

pushd moodin
make install DESTDIR=%{buildroot}
popd

#install wallpapers
mkdir -p %{buildroot}/usr/share
cp -rf wallpapers  %{buildroot}/usr/share/

#install kicker pictures
mkdir -p %{buildroot}/usr/share/apps/kicker/pics
cp -rf kicker-pics/* %{buildroot}/usr/share/apps/kicker/pics

#install kdm themes
mkdir -p %{buildroot}/usr/share/apps/kdm/themes
cp -rf kdm-theme/* %{buildroot}/usr/share/apps/kdm/themes/

#install ksplash themes
mkdir -p %{buildroot}/usr/share/apps/ksplash/Themes
cp -rf ksplash-theme/* %{buildroot}/usr/share/apps/ksplash/Themes/

mkdir -p %{buildroot}/boot/grub
cp grub/grub-splash.xpm.gz %{buildroot}/boot/grub/splash.xpm.gz

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}


%files
%defattr(-,root,root)
/usr
/boot
%exclude /usr/*/debug*
# Do not use this old theme

%changelog
* Tue Oct 2 2007 kde <athena_star {at} 163 {dot} com> - 2.1.20071002-1mgc
- add some wallpapers
- move kicker pics and ksplash themes to here from magic-kde-config package
- delete the old kde splash theme MoodinKDE

* Mon Sep 17 2007 kde <athena_star {at} 163 {dot} com> - 2.1-2mgc
- add 3 oxygen color-schemes

* Thu Jan 11 2007 Liu Di <liudidi@gmail.com> - 2.1-1mgc
- update lipstik to 2.2

* Wed Nov 30 2005 KanKer <kanker@163.com>
- update lipstik to 1.3
- move wallpapers here from magic-kde-config

* Fri Jul 29 2005 KanKer <kanker@163.com>
- add kde-theme:lipstik

* Wed Jul 27 2005 KanKer <kanker@163.com>
- fix group error.

* Tue May 26 2005 KanKer <kanker@163.com>
- remove plastik theme

* Sat Oct 23 2003 cjacker
- update for Magic Linux 1.2
- with kde 3.2cvs

* Mon Jul 14 2003 cjacker
- first build for Magic Linux 1.2

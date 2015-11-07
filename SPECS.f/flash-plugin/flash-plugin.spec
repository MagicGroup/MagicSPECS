# Prevent stripping
%define __spec_install_post /usr/lib/rpm/brp-compress
# Turn off debuginfo package
%define debug_package %{nil}

Summary: Macromedia Flash Player 9.0
Summary(zh_CN.UTF-8): Macromedia Flash 播放器 9.0
Name: flash-plugin
Version: 11.2.202.346
Release: %{?dist}.1
License: Commercial
BuildArch: i686 x86_64
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
#Source0: flash-plugin-%{version}.tar.gz
Source0: http://fpdownload.macromedia.com/get/flashplayer/pdc/%{version}/install_flash_player_11_linux.x86_64.tar.gz
Source5: http://fpdownload.macromedia.com/get/flashplayer/pdc/%{version}/install_flash_player_11_linux.i386.tar.gz
# http://fpdownload.macromedia.com/get/shockwave/flash/english/linux/7.0r25/install_flash_player_7_linux.tar.gz
Source1: homecleanup
Source2: appease-lawyers.c
Source4: setup
URL: http://macromedia.mplug.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gtk2-devel

%description
Macromedia Flash Plugin 7.0.25
Fully Supported: Mozilla 1.0+, Netscape 7.x, Firefox 0.8+
Partially Supported: Opera, Konqueror 3.x

http://videl.ics.hawaii.edu/mailman/listinfo/linuxflash
If you see any error messages or any problems in the installer, please
send a report to the linuxflash mailing list above.  Please include 
text of the error messages that you see, your distribution and versions of 
web browsers.  You MUST subscribe in order to post.

%description -l zh_CN.UTF-8
Macromedia Flash 插件 9.0.115.0
完全支持：Mozilla 1.0+，Netscape 7.x，Firefox 0.8+
部分支持：Opera，Konqueror 3.x

%prep
rm -rf %{name}-%{version}
mkdir -p %{name}-%{version}
cd %{name}-%{version}
%ifarch %{ix86}
tar xvf %{SOURCE5}
%endif
%ifarch x86_64
tar xvf %{SOURCE0}
%endif
/bin/chmod -Rf a+rX,u+w,g-w,o-w .

%build
cd %{name}-%{version}
gcc -Wall `pkg-config --cflags --libs gtk+-2.0` -o show-license %SOURCE2

%install
cd %{name}-%{version}
rm -rf $RPM_BUILD_ROOT
strip show-license

mkdir -p $RPM_BUILD_ROOT%{_libdir}/flash-plugin
mkdir -p $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins
mkdir -p $RPM_BUILD_ROOT%{_libdir}/firefox/plugins
chmod 755 $RPM_BUILD_ROOT%{_libdir}/flash-plugin

find $RPM_BUILD_ROOT -type d | xargs chmod 755

install -pm 755 libflashplayer.so $RPM_BUILD_ROOT%{_libdir}/flash-plugin
pushd $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins
ln -s %{_libdir}/flash-plugin/libflashplayer.so
popd
pushd $RPM_BUILD_ROOT%{_libdir}/firefox/plugins
ln -s %{_libdir}/flash-plugin/libflashplayer.so
popd

cp -r usr %{buildroot}/

%clean
rm -rf $RPM_BUILD_ROOT

%post

%preun


%files
%defattr(-,root,root,-)
%{_libdir}/flash-plugin/libflashplayer.so
%{_libdir}/mozilla/plugins/libflashplayer.so
%{_libdir}/firefox/plugins/libflashplayer.so
%{kde4_plugindir}/*
%ifarch x86_64
%{_prefix}/lib/kde4/*.so
%endif
%{kde4_servicesdir}/*
%{_bindir}/*
%{_datadir}/

%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 11.2.202.346-.1
- 为 Magic 3.0 重建

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 11-2
- 为 Magic 3.0 重建

* Mon Jul 14 2008 Liu Di <liudidi@gmail.com> - 9.0.124.0-1mgc
- 更新到 9.0.124.0

* Mon Feb 18 2008 Liu Di <liudidi@gmail.com> - 9.0.115.0-1mgc
- update to 9.0.115.0

* Fri Jan 19 2007 Liu Di <liudidi@gmail.com> - 9.0.31.0-1mgc
- update to 9.0.31.0

* Sat Oct 07 2006 Liu Di <liudidi@gmail.com> - 7.0.68-1mgc
- update to 7.0.68

* Thu May 27 2004 Warren Togami <warrren@togami.com> 7.0.25-1
- update to 7.0.25
- scan for versioned firefox dirs

%define cvsdate 20051130
%define ver 0.2

Summary: Magic xDSL Dialer
Summary(zh_CN): Magic xDSL 拨号器
Name: mxd
Version: %{ver}
Release: 8mgc
License: GPL
URL: http://www.magiclinux.org/people/yunfan/mxd
Group: Applications/Internet
Group(zh_CN): 应用程序/互联网
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
#Source0:%{name}-%{ver}.tar.bz2
Source0: %{name}.tar.bz2
Source1: mxd-restart
Patch0: rppppoek.sh-removesudo.patch
Patch1: mxd-autostart.patch
Prefix: %{_prefix}
Requires: qt, kdelibs, rp-pppoe, ppp, magic-system-config
Packager: KanKer<kanker@163.com>, Magic Group

%description
Magic xDSL Dialer.

%description -l zh_CN
Magic xDSL 拨号器

%prep
#%setup -q -n %{name}-%{version}
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
chmod 777 admin/*

%Build
make -f admin/Makefile.common
%configure
#临时措施
sed -i 's/\/include\/tqt/\/include\/tqt \-lqt\-mt \-ltdecore \-ltdeui \-lDCOP \-lkio/g' src/Makefile
make 

%install
rm -rf %{buildroot}
make DESTDIR=$RPM_BUILD_ROOT install
chmod 755 $RPM_BUILD_ROOT%{_bindir}/*
mv $RPM_BUILD_ROOT/usr/share/applnk/Utilities $RPM_BUILD_ROOT/usr/share/applnk/Internet
install -m 755 -D %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/mxd-restart

%post
#set user's sudo right.
[ -x /usr/bin/magic_sudo_add.sh ] && /usr/bin/magic_sudo_add.sh

%postun
#set user's sudo right.
if [ $1 -eq 0 ]; then
[ -x /usr/bin/magic_sudo_del.sh ] && /usr/bin/magic_sudo_del.sh
fi

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}


%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*
%exclude /usr/*/debug*

%changelog
* Tue Sep 09 2008 Liu Di <liudidi@gmail.com> - 0.2-7mgc
- 重新加入 sudo

* Mon Apr 23 2007 kde <athena_star {at} 163 {dot} com> 0.2-6mgc
- fix the mxd-restart script

* Sun Apr 22 2007 kde <athena_star {at} 163 {dot} com> 0.2-5mgc
- fix the autostart configuration
- add mxd-restart script
 
* Fri Oct 20 2006 kde <jack@linux.net.cn> -0.2-3mgc
- recreate rppppoek.sh-removesudo.patch
- fix postun script

* Mon May 29 2006 KanKer <kanker@163.com> -0.2-2mgc
- fix spec post scripts

* Wed Nov 30 2005 KanKer <kanker@163.com> -0.2-1mgc
- update 20051130cvs

* Thu Nov 29 2005 KanKer <kanker@163.com>
- update 20051129cvs
* Mon Nov 28 2005 KanKer <kanker@163.com>
- fix a spec bug
* Sun Nov 27 2005 KanKer <kanker@163.com>
- first spec


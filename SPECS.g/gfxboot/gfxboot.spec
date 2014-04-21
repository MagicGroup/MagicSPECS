Name:           gfxboot
BuildRequires:  freetype-devel nasm xmlto
License:        GNU General Public License (GPL)
Group:          Applications/System
Group(zh_CN.UTF-8):	应用程序/系统
Obsoletes:      gfxboot-devel
Requires:       perl-HTML-Parser
Autoreqprov:    on
Summary:        Graphical Boot Logo for LILO and SYSLINUX
Summary(zh_CN.UTF-8):	LILO 和 SYSLINUX 以及 grub 的图形启动 Logo
Version:        4.5.2
Release:        1%{?dist}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source:         gfxboot-%{version}.tar.bz2
Source1:        NLD.tar.bz2
Source2:        SuSE.tar.bz2
Source3:        Zen.tar.bz2
Source4:        openSUSE.tar.bz2
Source5:        SLED.tar.bz2
Source6:        SLES.tar.bz2
Source7:        upstream.tar.bz2
Source8:        examples.tar.bz2

%description
Here, find the graphical boot logo. It is suitable for both LILO and
SYSLINUX.

%description -l zh_CN.UTF-8 
这是一个图形启动logo，它适合于 LILO 和 SYSLINUX 以及 grub。

%prep
%setup
%setup -T -D -a 1
%setup -T -D -a 2
%setup -T -D -a 3
%setup -T -D -a 4
%setup -T -D -a 5
%setup -T -D -a 6
%setup -T -D -a 7
%setup -T -D -a 8

%build
make X11LIBS=/usr/%_lib
make doc
make themes

%install
make DESTDIR=%{buildroot} install
gzip -9c doc/gfxboot.8 >gfxboot.8.gz
install -d -m 755 %{buildroot}%{_mandir}/man8
install -m 644 gfxboot.8.gz %{buildroot}%{_mandir}/man8

%clean 
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_sbindir}/gfxboot
%{_sbindir}/gfxboot-compile
%{_sbindir}/gfxboot-font
%{_sbindir}/gfxtest
%doc doc/gfxboot.html
%doc doc/gfxboot.txt
%{_sysconfdir}/bootsplash/themes/*
%{_mandir}/man8/gfxboot.8.gz

%changelog -n gfxboot
* Fri Apr 04 2014 Liu Di <liudidi@gmail.com> - 4.5.2-1
- 升级到 4.5.2

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 4.3.8-5
- 为 Magic 3.0 重建

* Wed Nov 30 2011 Liu Di <liudidi@gmail.com> - 4.3.8-4
- 为 Magic 3.0 重建

* Thu Jan 11 2007 Liu Di <liudidi@gmail.com> - 3.3.18-1mgc
- created package for Magic

%define rver 82044
Name:           pcsxr
BuildRequires:  gtk2-devel nasm libglade2-devel libXv-devel libX11-devel libXext-devel libXxf86vm-devel libXtst-devel gettext mesa-libGL-devel SDL-devel
URL:            http://pcsxr.codeplex.com
#pcsxr 本身是 GPL 的，但 BIOS 文件版权属于 Sony
License:        GPL + Copyright
Group:          Applications/Emulators
Group(zh_CN.UTF-8):	应用程序/模拟器
Obsoletes:      pcsx
Provides:	pcsx
Autoreqprov:    on
Version:        1.9.92
Release:        svn%{rver}%{dist}
Summary:        Free Sony PlayStation emulator
Summary(zh_CN.UTF-8):	自由的 Sony PlayStation 模拟器
Source0:        pcsxr-%{rver}.zip
Source1:        scph1000.bin
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
This application emulates all components of a Sony PlayStation on
regular PC hardware. It features a sophisticated plugin system allowing
for easy extension and is highly configurable.

To be able to play commercial games on this emulator you need an image
of a Sony PlayStation BIOS ROM. The BIOS is copyrighted by Sony
Computer Entertainment and can therefore not be included in this
package. Information on how to create such an image can be found at the
following web page:

http://www.psxemu.com/faq/faq-bios.shtml

BIOS images can be placed in ~/.pcsx/bios

Authors:
--------
    Linuzappz <linuzappz@pcsx.net>
    Shadow  <shadow@pcsx.net>
    Pete Bernert <blackdove@addcom.de>
    Lewpy <lewpy@psxemu.com>
    lu_zero
    Darko Matesic <thedarkma@ptt.yu>
    syo <syo68k@geocities.co.jp>
    Lamer0 <Lamer0@mediaone.net>
    Ryan Schultz <schultz.ryan@gmail.com>
    Andrew Burton <adb@iinet.net.au>
    Stephen Chao <schao@myrealbox.com>
    Marcus Comstedt <marcus@mc.pp.se>
    Stefan Sikora <hoshy@schrauberstube.de>
    Wei Mingzhi <whistler_wmz@users.sf.net>
    edgbla <edgbla@yandex.ru>

%description -l zh_CN.UTF-8
自由的 Sony PlayStation 模拟器。

%prep
%setup -n pcsxr

%build
sh autogen.sh
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -pthread -w" %configure --enable-opengl
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_datadir}/pixmaps
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_datadir}/pcsx
install -m644 %{SOURCE1} $RPM_BUILD_ROOT/usr/share/pcsx
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr (-,root,root)
%doc AUTHORS ChangeLog INSTALL NEWS README doc/*.txt
%{_bindir}/pcsxr
%{_datadir}/applications/*.desktop
%_libdir/games/*
%doc %_mandir/man1/pcsxr.1*
%{_datadir}/pcsx/*
%{_datadir}/pcsxr/*
%{_datadir}/psemu/*
%{_datadir}/locale/zh_CN/LC_MESSAGES/*
%{_datadir}/locale/zh_TW/LC_MESSAGES/*
%{_datadir}/pixmaps/*

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.9.92-svn73976.1
- 为 Magic 3.0 重建



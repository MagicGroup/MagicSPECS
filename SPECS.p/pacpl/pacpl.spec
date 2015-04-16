Name: pacpl
Summary: A tool for converting multiple audio types from one format to another
Summary(zh_CN): 一个用于转换多种音频格式的工具
Version:	5.0.1
Release:	1%{?dist}
Group: Applications/Multimedia
Group(zh_CN): 应用程序/多媒体
License: GPL
Source0: http://downloads.sourceforge.net/project/pacpl/pacpl/%{version}/%{name}-%{version}.tar.gz
Source1: zh_CN.po
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
URL: http://viiron.googlepages.com/
Prefix: %{_prefix}
Packager: Ni Hui <shuizhuyuanluo@126.com>
# perl 模块依赖
BuildRequires: perl(Getopt::Long)
BuildRequires: perl(Switch)
BuildRequires: perl(strict)
BuildRequires: perl(warnings)
BuildRequires: perl(Pod::Usage)
BuildRequires: perl(File::Basename)
BuildRequires: perl(File::Find)
BuildRequires: perl(File::Spec::Functions)
BuildRequires: perl(CDDB_get)
#BuildRequires: perl(Ogg::Vorbis::Header)
BuildRequires: perl(Audio::Musepack)
#BuildRequires: perl(Audio::APETags)
BuildRequires: perl(Audio::WMA)
BuildRequires: perl(MP3::Tag)
BuildRequires: perl(MP4::Info)
BuildRequires: perl(Audio::FLAC::Header)
BuildRequires: perl
# 编码解码器依赖
BuildRequires: lame >= 3.96.1
BuildRequires: libogg >= 1.0.1
BuildRequires: speex >= 1.1
BuildRequires: flac-devel >= 1.1.3
BuildRequires: mac >= 3.99
BuildRequires: shorten >= 3.5.1
BuildRequires: sox >= 12.17.8
BuildRequires: faac >= 1.25
BuildRequires: faad2 >= 2.0
BuildRequires: ffmpeg >= 0.4.9
BuildRequires: mppenc >= 1.15
BuildRequires: wavpack >= 4.3.2

%description
Perl Audio Converter is a tool for converting multiple audio types from
one format to another. It supports AAC, AC3, AIFF, APE, AU, AVR, BONK,
CDR, FLA, FLAC, LA, LPAC, M4A, MP2, MP3, MP4, MPC, MPP, OFR, OFS, OGG, PAC,
RA, RAM, RAW, SHN, SMP, SND, SPX, TTA, VOC, WAV, WMA, and WV. It can also
convert audio from the following video extensions: RM, RV, ASF, DivX, MPG, 
MKV, MPEG, AVI, MOV, OGM, QT, VCD, SVCD, M4V, NSV, NUV, PSP, SMK, VOB, FLV, 
and WMV. A CD ripping function with CDDB support, batch conversion, tag 
preservation for most supported formats, independent tag reading/writing, 
and extensions for Amarok, Dolphin, and Konqueror are also provided.

%package -n pacpl-konqueror
Group: Applications/Multimedia
Group(zh_CN): 应用程序/多媒体
Summary: pacpl konqueror servicemenu
Summary(zh_CN): pacpl konqueror 菜单

Requires: pacpl = %{version}
Requires: kdebase >= 3.5.3

%description -n pacpl-konqueror
pacpl konqueror servicemenu.

%description -n pacpl-konqueror -l zh_CN
pacpl konqueror 菜单。

%package -n pacpl-amarok
Group: Applications/Multimedia
Group(zh_CN): 应用程序/多媒体
Summary: pacpl amarok plugin
Summary(zh_CN): pacpl amarok 插件

Requires: pacpl = %{version}
Requires: amarok >= 1.4

%description -n pacpl-amarok
pacpl amarok plugin.

%description -n pacpl-amarok -l zh_CN
pacpl amarok 插件。

%package -n pacpl-dolphin
Group: Applications/Multimedia
Group(zh_CN): 应用程序/多媒体
Summary: pacpl dolphin servicemenu
Summary(zh_CN): pacpl dolphin 菜单

Requires: pacpl = %{version}
Requires: dolphin >= 0.8.1

%description -n pacpl-dolphin
pacpl dolphin servicemenu.

%description -n pacpl-dolphin -l zh_CN
pacpl dolphin 菜单。

%prep
%setup -q -n %{name}-%{version}

%build
%configure  --enable-kde || :
#--enable-nautilus

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pacpl/po/zh_CN.UTF-8.po

# 修正 doc 目录错位
#pushd %{buildroot}%{_prefix}
#mv doc share/
#popd

# 修正语言文件名称
#pushd %{buildroot}%{_sysconfdir}/pacpl/po/
#mv zh_CN.po zh_CN.UTF-8.po
#popd

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
%{_sysconfdir}/pacpl*
%{_bindir}/*
%{_docdir}/pacpl*
#%{_datadir}/mimelnk/audio/*.desktop
%{_mandir}/man1/*.1.gz
%{_datadir}/pacpl/*
%{_datadir}/kde4/*

%if 0
%files -n pacpl-konqueror
%defattr(-,root,root)
%{_datadir}/apps/konqueror*

%files -n pacpl-amarok
%defattr(-,root,root)
%{_datadir}/apps/amarok*

%files -n pacpl-dolphin
%defattr(-,root,root)
%{_datadir}/apps/dolphin*
%endif

%changelog
* Tue Apr 14 2015 Liu Di <liudidi@gmail.com> - 5.0.1-1
- 更新到 5.0.1

* Sat Nov 10 2007 Ni Hui <shuizhuyuanluo@126.com> - 4.0.0-0.3mgc
- 修正语言文件名称，使之与 $LANG 变量对应

* Sat Nov 10 2007 Ni Hui <shuizhuyuanluo@126.com> - 4.0.0-0.2mgc
- update to 4.0.0
- 修正 doc 目录错位

* Sun Oct 14 2007 Ni Hui <shuizhuyuanluo@126.com> - 4.0.0-0.1mgc
- first spec file for MagicLinux-2.1
- 4.0.0beta3

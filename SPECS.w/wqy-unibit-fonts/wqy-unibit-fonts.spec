%define fontname wqy-unibit

Name:           %{fontname}-fonts
Version:        1.1.0
Release:        11%{?dist}
Summary:        WenQuanYi Unibit Bitmap Font
Summary(zh_CN.UTF-8): 文泉驿标准双等宽点阵字体

Group:          User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
License:        GPLv2 with exceptions
URL:            http://wenq.org/enindex.cgi
Source0:        http://downloads.sourceforge.net/wqy/wqy-unibit-bdf-%{version}-1.tar.gz
Patch0:         wqy-unibit-fixes-build.patch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:      noarch
BuildRequires:  fontpackages-devel, bdftopcf
Requires:       fontpackages-filesystem

%description
The Wen Quan Yi Unibit is designed as a dual-width (16x16,16x8) 
bitmap font to provide the most complete international symbol 
coverage, serving as the system-wide fall-back font. This font 
has covered over 46000 Unicode code points in BMP.
It is intended to supersede the outdated GNU Unifont.
This font was created by merging the latest update of GNU 
Unifont [GPL] (by Roman Czyborra and David Starner et al., the 
font was last updated in 2004), WenQuanYi Bitmap Song [GPL] 
0.8.1 (by Qianqian Fang and WenQuanYi contributors) and 
Fixed-16x8 [public domain] bitmap fonts from X11 core fonts. 
The entire CJK Unified Ideographics (U4E00-U9FA5) and CJK Unified 
Ideographics Extension A(U3400-U4DB5) blocks were replaced by 
high-quality glyphs from China National Standard GB19966-2005 
(public domain). Near a thousand of non-CJK characters were improved by 
WenQuanYi contributors via their collaborative font editing website at
http://wenq.org/eindex.cgi?Unicode_Chart_EN

%description -l zh_CN.UTF-8
文泉驿标准双等宽点阵字体。

%prep
%setup -q -n %{fontname}
%patch0 -p1

%build
make

%install
rm -fr %{buildroot}

install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p *.pcf %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}


%clean
rm -fr %{buildroot}


%_font_pkg *.pcf

%doc AUTHORS ChangeLog COPYING README
%dir %{_fontdir}


%changelog
* Tue Oct 20 2015 Liu Di <liudidi@gmail.com> - 1.1.0-11
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.1.0-10
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

*Tue Feb 10 2009 Qianqian Fang <fangqq@gmail.com> 1.1.0-5
- use fontpackages macro

*Sun Sep 30 2007 Qianqian Fang <fangqq@gmail.com> 1.1.0-4
- more spec file clean up

*Thu Sep 27 2007 Qianqian Fang <fangqq@gmail.com> 1.1.0-3
- change install directory to /usr/share/fonts/wenquanyi-unibit/

*Tue Sep 25 2007 Qianqian Fang <fangqq@gmail.com> 1.1.0-2
- change install directory to /usr/share/fonts/wqy-unibit/

*Fri Sep 14 2007 Qianqian Fang <fangqq@gmail.com> 1.1.0-1
- add more than 80 new glyphs between 0xFF00-0xFFFD, totaling 46443 glyphs

*Tue Sep 11 2007 Qianqian Fang <fangqq@gmail.com> 1.0.0-3
- remove non-ascii character from README, update upstream tarball

*Tue Sep 11 2007 Qianqian Fang <fangqq@gmail.com> 1.0.0-2
- change package name from wqy-unibit to wqy-unibit-fonts
- follow the new guideline for F8, use font catalogue symlink (#252279)

*Sun Sep 9 2007 Qianqian Fang <fangqq@gmail.com> 1.0.0-1
- initial release of the font
- initial packaging for Fedora (#285561)

%define fontname  wqy-bitmap
%define fontconf  61-wqy-bitmapsong.conf
%define wqyroot   wqy-bitmapsong

Name:           %{fontname}-fonts
Version:        1.0.0
Release:        0.5.rc1%{?dist}
Summary:        WenQuanYi Bitmap Chinese Fonts
Summary(zh_CN.UTF-8): 文泉驿位图中文字体

Group:          User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
License:        GPLv2 with exceptions
URL:            http://wenq.org/enindex.cgi
Source0:        http://downloads.sourceforge.net/wqy/wqy-bitmapsong-bdf-1.0.0-RC1.tar.gz
Source1:        61-wqy-bitmapsong.conf
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:      noarch
BuildRequires:  fontpackages-devel, bdftopcf
Requires:       fontpackages-filesystem

%description
WenQuanYi bitmap fonts include all 20,932 Unicode 5.2
CJK Unified Ideographs (U4E00 - U9FA5) and 6,582
CJK Extension A characters (U3400 - U4DB5) at
5 different pixel sizes (9pt-12X12, 10pt-13X13,
10.5pt-14x14, 11pt-15X15 and 12pt-16x16 pixel).
Use of this bitmap font for on-screen display of Chinese
(traditional and simplified) in web pages and elsewhere
eliminates the annoying "blurring" problems caused by
insufficient "hinting" of anti-aliased vector CJK fonts.
In addition, Latin characters, Japanese Kanas and
Korean Hangul glyphs (U+AC00~U+D7A3) are also included.

%description -l zh_CN.UTF-8
文泉驿位图中文字体。

%prep
%setup -q -n %{wqyroot}
sed -i 's/shift(ARGV)/shift(@ARGV)/g' bdfmerge.pl

%build
make wqyv1


%install
rm -fr %{buildroot}

install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p *.pcf %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}

ln -s %{_fontconfig_templatedir}/%{fontconf} \
      %{buildroot}%{_fontconfig_confdir}/%{fontconf}


%clean
rm -fr %{buildroot}


%_font_pkg -f %{fontconf} *.pcf

%doc AUTHORS ChangeLog COPYING README LOGO.png
%dir %{_fontdir}


%changelog
* Tue Oct 20 2015 Liu Di <liudidi@gmail.com> - 1.0.0-0.5.rc1
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.0.0-0.4.rc1
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.3.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

*Sun Mar 14 2010 Qianqian Fang <fangqq@gmail.com> 1.0.0-0.1.rc1
- Reset release id based on Fedora's naming guideline (#573100)

*Fri Mar 12 2010 Qianqian Fang <fangqq@gmail.com> 1.0.rc1-0
- New upstream realse (1.0.0 RC1) (#573100)

*Thu Feb 25 2010 Qianqian Fang <fangqq@gmail.com> 0.9.9-12
- Remove all font preference settings from 61-wqy-bitmapsong.conf (#492510)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

*Thu Apr 23 2009 Qianqian Fang <fangqq@gmail.com> 0.9.9-10
- correct outdated uming font names for F11 (#492510)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

*Tue Feb 10 2009 Qianqian Fang <fangqq@gmail.com> 0.9.9-8
- add bdftopcf to BuildRequires

*Tue Feb 10 2009 Qianqian Fang <fangqq@gmail.com> 0.9.9-7
- use fontpackages macros

*Tue May 11 2008 Qianqian Fang <fangqq@gmail.com> 0.9.9-6
- remove bold font files, as Xft can do fake-emboldening byitself

*Tue May 11 2008 Qianqian Fang <fangqq@gmail.com> 0.9.9-5
- remove 61-wqy-bitmapsong.conf from source, add to cvs instead
- replace DejaVu LGC to DejaVu as LCG variants are not default anymore

*Tue Dec 11 2007 Qianqian Fang <fangqq@gmail.com> 0.9.9-4
- used tag 0.9.9-3 due to previous mistake, have to bump release to tag

*Tue Dec 11 2007 Qianqian Fang <fangqq@gmail.com> 0.9.9-3
- replace SOURCE1 by actual config file name

*Tue Dec 11 2007 Qianqian Fang <fangqq@gmail.com> 0.9.9-2
- fontconfig file was rewriten to minimize impact to non-CJK users (#381311)

*Sat Nov 17 2007 Qianqian Fang <fangqq@gmail.com> 0.9.9-1
- avoid using Latin glyphs from this font in monospace environment such as in consoles

*Sat Nov 10 2007 Qianqian Fang <fangqq@gmail.com> 0.9.9-0
- include the complete CJK Extension A glyphs (6,582 x 4 point sizes), provide full coverage to Standard GB18030
- first round standard-compliance validation for all CJK basic characters between U4E00-U9FA5
- numerous bitmap glyph fine-tuning and corrections

* Tue Aug 28 2007 Jens Petersen <petersen@redhat.com> - 0.8.1-8
- fix font catalogue symlink (#252279)
- drop fontconfig and xorg-x11-font-utils requires for scripts
- drop freetype and xorg-x11-font-utils requires
- run mkfontdir at buildtime
- use the standard font scriptlets

*Thu Aug 16 2007 Qianqian Fang <fangqq@gmail.com> 0.8.1-7
- drop chkfontpath from the spec file, use fontpath.d instead (#252279)

*Fri May 18 2007 Qianqian Fang <fangqq@gmail.com> 0.8.1-6
- final polishing of spec file and initial upload to cvs

*Thu May 10 2007 Qianqian Fang <fangqq@gmail.com> 0.8.1-5
- further polishing the spec file (by Jens Petersen)

*Sun May 06 2007 Qianqian Fang <fangqq@gmail.com> 0.8.1-4
- use nightly-build cvs20070506-bdf as sources

*Fri May 04 2007 Qianqian Fang <fangqq@gmail.com> 0.8.1-3
- remove superfluous conflicts and provides

*Thu Apr 12 2007 Qianqian Fang <fangqq@gmail.com> 0.8.1-2
- update to upstream new release 0.8.1-7

*Sun Feb 18 2007 Qianqian Fang <fangqq@gmail.com> 0.8.0-1
- initial packaging for Fedora (#230560)

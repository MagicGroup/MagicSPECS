%global priority  59
%global fontname liberation
%global fontconf %{priority}-%{fontname}
%global archivename %{name}-%{version}
%global common_desc \
The Liberation Fonts are intended to be replacements for the three most \
commonly used fonts on Microsoft systems: Times New Roman, Arial, and Courier \
New.

%define catalogue %{_sysconfdir}/X11/fontpath.d

Name:             %{fontname}-fonts
Summary:          Fonts to replace commonly used Microsoft Windows fonts
Summary(zh_CN.UTF-8): 替换微软视察字体的字体
Version:          1.07.4
Release:          3%{?dist}
Epoch:          1
# The license of the Liberation Fonts is a EULA that contains GPLv2 and two
# exceptions:
# The first exception is the standard FSF font exception.
# The second exception is an anti-lockdown clause somewhat like the one in
# GPLv3. This license is Free, but GPLv2 and GPLv3 incompatible.
License:          Liberation
Group:            User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
URL:              http://fedorahosted.org/liberation-fonts/
Source0:          https://fedorahosted.org/releases/l/i/liberation-fonts/%{archivename}.tar.gz
Source2:          %{name}-mono.conf
Source3:          %{name}-sans.conf
Source4:          %{name}-serif.conf
Source5:          %{name}-narrow.conf
BuildArch:        noarch
BuildRequires:    fontpackages-devel >= 1.13, xorg-x11-font-utils
BuildRequires:    fontforge

%description
%common_desc

Meta-package of Liberation fonts which installs Sans, Serif, and Monospace,
Narrow families.

%package -n %{fontname}-fonts-common
Epoch:  1
Summary:          Shared common files of Liberation font families
Group:            User Interface/X
Requires:         fontpackages-filesystem >= 1.13

%description -n %{fontname}-fonts-common
%common_desc

Shared common files of Liberation font families.

%files -n %{fontname}-fonts-common
%doc AUTHORS ChangeLog COPYING License.txt README TODO
%dir %{_fontdir}
%verify(not md5 size mtime) %{_fontdir}/fonts.dir
%verify(not md5 size mtime) %{_fontdir}/fonts.scale
%{catalogue}/%{name}

%package -n %{fontname}-sans-fonts
Summary:      Sans-serif fonts to replace commonly used Microsoft Arial
Group:        User Interface/X
Requires:     %{fontname}-fonts-common = %{epoch}:%{version}-%{release}

%description -n %{fontname}-sans-fonts
%common_desc

This is Sans-serif TrueType fonts that replaced commonly used Microsoft Arial.

%_font_pkg -n sans -f *-%{fontname}-sans.conf  LiberationSans-*.ttf

%package -n %{fontname}-serif-fonts
Summary:      Serif fonts to replace commonly used Microsoft Times New Roman
Group:        User Interface/X
Requires:     %{fontname}-fonts-common = %{epoch}:%{version}-%{release}

%description -n %{fontname}-serif-fonts
%common_desc

This is Serif TrueType fonts that replaced commonly used Microsoft Times New \
Roman.

%_font_pkg -n serif -f *-%{fontname}-serif.conf  LiberationSerif*.ttf

%package -n %{fontname}-mono-fonts
Summary:      Monospace fonts to replace commonly used Microsoft Courier New
Group:        User Interface/X
Requires:     %{fontname}-fonts-common = %{epoch}:%{version}-%{release}

%description -n %{fontname}-mono-fonts
%common_desc

This is Monospace TrueType fonts that replaced commonly used Microsoft Courier \
New.

%_font_pkg -n mono -f *-%{fontname}-mono.conf  LiberationMono*.ttf

%package -n %{fontname}-narrow-fonts
Summary:      Sans-serif Narrow fonts to replace commonly used Microsoft Arial Narrow
Group:        User Interface/X
Requires:     %{fontname}-fonts-common = %{epoch}:%{version}-%{release}

%description -n %{fontname}-narrow-fonts
%common_desc

This is Sans-Serif Narrow TrueType fonts that replaced commonly used Microsoft \
Arial Narrow.

%_font_pkg -n narrow -f *-%{fontname}-narrow.conf LiberationSansNarrow*.ttf

%prep
%setup -q -n %{archivename}

%build
make %{?_smp_mflags} 
mv liberation-fonts-ttf-%{version}/* .


%install
# fonts .ttf
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p *.ttf %{buildroot}%{_fontdir}
# catalogue
install -m 0755 -d %{buildroot}%{catalogue}
ln -s %{_fontdir} %{buildroot}%{catalogue}/%{name}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

# Repeat for every font family
install -m 0644 -p %{SOURCE2} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-mono.conf
install -m 0644 -p %{SOURCE3} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-sans.conf
install -m 0644 -p %{SOURCE4} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-serif.conf
install -m 0644 -p %{SOURCE5} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-narrow.conf

for fconf in %{fontconf}-mono.conf \
             %{fontconf}-sans.conf \
             %{fontconf}-serif.conf \
             %{fontconf}-narrow.conf; do
  ln -s %{_fontconfig_templatedir}/$fconf \
        %{buildroot}%{_fontconfig_confdir}/$fconf
done

# fonts.{dir,scale}
mkfontscale %{buildroot}%{_fontdir}
mkfontdir %{buildroot}%{_fontdir}

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1:1.07.4-3
- 为 Magic 3.0 重建

* Tue Jul 15 2014 Liu Di <liudidi@gmail.com> - 1:1.07.4-2
- 为 Magic 3.0 重建

* Wed Aug 28 2013 Pravin Satpute <psatpute@redhat.com> - 1:1.07.3-2
- Resolved #715309: Improved Bold 'u' hinting

* Fri Aug 23 2013 Pravin Satpute <psatpute@redhat.com> - 1:1.07.3-1
- Upstream release 1.07.3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.07.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.07.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 15 2013 Pravin Satpute <psatpute@redhat.com> - 1:1.07.2-12
- Corrected font conf priority from 30-0 to 59
- building from f18 to rawhide

* Fri Dec 07 2012 Pravin Satpute <psatpute@redhat.com> - 1:1.07.2-11
- Decided to defer Liberation 2.0 feature in Fedora 18.
- Reverting to Liberation 1.07.2. 
- Using 11 release to match with Liberation Sans Narrow

* Wed Nov 21 2012 Pravin Satpute <psatpute@redhat.com> - 2.00.1-4
- Improved spec file

* Tue Nov 20 2012 Pravin Satpute <psatpute@redhat.com> - 2.00.1-3
- Resolved bug 878305

* Tue Nov 20 2012 Pravin Satpute <psatpute@redhat.com> - 2.00.1-2
- Resolved issues of md5sum

* Thu Oct 04 2012 Pravin Satpute <psatpute@redhat.com> - 2.00.1-1
- Upstream release of 2.00.1 version

* Wed Sep 12 2012 Pravin Satpute <psatpute@redhat.com> - 2.00.0-2
- Removed fontconf files of 59 priority, now only has 30-0 alias file

* Thu Jul 26 2012 Pravin Satpute <psatpute@redhat.com> - 2.00.0-1
- First upstream release with OFL license
- Added conf files with 59 priority

* Tue Jun 26 2012 Pravin Satpute <psatpute@redhat.com> - 1.07.2-6
- Resolves bug 835182

* Tue Jun 26 2012 Pravin Satpute <psatpute@redhat.com> - 1.07.2-5
- Resolves bug 835182

* Thu May 10 2012 Pravin Satpute <psatpute@redhat.com> - 1.07.2-4
- Resolves bug 799384

* Sat Feb 18 2012 Pravin Satpute <psatpute@redhat.com> - 1.07.2-3
- Resolved bug 714191

* Mon Feb 13 2012 Pravin Satpute <psatpute@redhat.com> - 1.07.2-2
- Resolved #715309

* Thu Feb 09 2012 Pravin Satpute <psatpute@redhat.com> - 1.07.2-1
- Upstream release 1.07.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Pravin Satpute <psatpute@redhat.com> - 1.07.1-3
- Resolved bug 753572, removed hint of cent sign

* Fri Oct 14 2011 Pravin Satpute <psatpute@redhat.com> - 1.07.1-2
- Resolved bug 657849, added support in Sans and Serif

* Wed Sep 21 2011 Pravin Satpute <psatpute@redhat.com> - 1.07.1-1
- Upstream Release 1.07.1
- Resolved bug 738264, 729989

* Mon May 30 2011 Pravin Satpute <psatpute@redhat.com> - 1.07.0-1
- Upstream Release 1.07.0
- Resolved bug 659214, 708330, 707973 

* Thu Feb 24 2011 Pravin Satpute <psatpute@redhat.com> - 1.06.0.20100721-5
- bug 659214: added bulgarian characters

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06.0.20100721-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 13 2010 Pravin Satpute <psatpute@redhat.com> - 1.06.0.20100721-3
- bug 642493: use consistent ttf names

* Tue Oct 12 2010 Pravin Satpute <psatpute@redhat.com> - 1.06.0.20100721-2
- Building from sources
- Applying Monospace font patch bug 620273

* Thu Jul 22 2010 Pravin Satpute <psatpute@redhat.com> - 1.06.0.20100721-1
- Upstream New Release
- Added New Family Narrow

* Wed Jun 16 2010 Caius 'kaio' Chance <cchance@redhat.com> - 1.05.3.20100510-2
- Updated Source URL to FedoraHosted and repackaged.

* Mon May 10 2010 Caius 'kaio' Chance <me at kaio.net> - 1.05.3.20100510-1
- Updated from upstream.
- Fixed correct Romanian glyphs in Liberation Fonts. (rhbz#440992)

* Fri May 07 2010 Caius 'kaio' Chance <me at kaio.net> - 1.05.3.20100506-2
- Updated package URL and source URL.

* Thu May 06 2010 Caius 'kaio' Chance <me at kaio.net> - 1.05.3.20100506-1
- Updated from upstream.
- Cleaned up points and auto-instructed hinting of 'u', 'v', 'w', 'y'.
(rhbz#463036)

* Wed May 05 2010 Caius 'kaio' Chance <k at kaio.net> - 1.05.3.20100505-2
- Made 0x00A2 cent sign be coressed in Sans Narrow.

* Wed May 05 2010 Caius 'kaio' Chance <k at kaio.net> - 1.05.3.20100505-1
- Updated from upstream.
- Resolves: rhbz#474522 - Incorrect cent sign glyph (U+00A2) in Sans and Mono style in Liberation fonts.

* Wed Apr 28 2010 Caius 'kaio' Chance <k at kaio.net> - 1.05.3.20100428-1
- rhbz#510174: Corrected version number of all SFD files.
- Corrected license exceptions to GPLv2.
- Updated README file.

* Tue Apr 27 2010 Caius 'kaio' Chance <k at kaio.net> - 1.05.3.20100427-1
- Updated source from upstream.
- Introduced Sans Narrow by upstream.

* Wed Jan 13 2010 Caius 'kaio' Chance <k at kaio.me> - 1.05.2.20091019-5.fc13
- Removed 'Provides liberation-fonts and liberation-fonts-compat by
  liberation-fonts-common.'

* Tue Jan 12 2010 Caius 'kaio' Chance <k at kaio.me> - 1.05.2.20091019-4.fc13
- Rebuilt w/ macro fixes.

* Tue Jan 12 2010 Caius 'kaio' Chance <k at kaio.me> - 1.05.2.20091019-3.fc13
- Removed full stop in Summary.
- Set default file permission in files.
- Provides liberation-fonts and liberation-fonts-compat by 
  liberation-fonts-common.
- Macro as much as possible in .spec.

* Mon Oct 19 2009 Caius 'kaio' Chance <k at kaio.me> - 1.05.2.20091019-2.fc13
- Rebuilt.

* Mon Oct 19 2009 Caius 'kaio' Chance <k at kaio.me> - 1.05.2.20091019-1.fc13
- Resolves: rhbz#525498 - wrongly encoded glyphs after U+10000.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05.1.20090721-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Caius 'kaio' Chance <k at kaio.me> - 1.05.1.20090721-1.fc12
- Fixed fontforge scripting of sfd -> ttf generation.
- Checked existance of traditionat kern table in Sans and Serif.

* Tue Jul 14 2009 Caius 'kaio' Chance <k at kaio.me> - 1.05.1.20090713-2.fc12
- Required fontforge ver 20090408 which supports generation with traditional
  kern table. (rhbz#503430)

* Mon Jul 13 2009 Caius 'kaio' Chance <k at kaio.me> - 1.05.1.20090713-1.fc12
- Updated to upstream 1.05.1.20090713.
- Generate TTFs with traditional kern table via fontforge scripts. (rh#503430)

* Mon Jul 06 2009 Caius 'kaio' Chance <k at kaio.me> - 1.05.1.20090706-1.fc12
- Updated to upstream 1.05.1.20090706.
- Reconverted from original TTF with traditional kern table. (rh#503430)

* Tue Jun 30 2009 Caius 'kaio' Chance <k at kaio.me> - 1.05.1.20090630-1.fc12
- Updated to upstream 1.05.1.20090630.
- Reconverted from original TTF with better procedures of data conservation.

* Tue May 19 2009 Jens Petersen <petersen@redhat.com> - 1.04.93-11
- remove redundant obsoletes, provides and conflicts from new subpackages

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04.93-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 05 2009 Caius Chance <cchance@redhat.com> - 1.04.93-9.fc11
- Fixed inter-subpackage dependencies with reference of dejavu.

* Wed Feb 04 2009 Caius Chance <cchance@redhat.com> - 1.04.93-8.fc11
- Fixed inter-subpackage dependencies.

* Wed Feb 04 2009 Caius Chance <cchance@redhat.com> - 1.04.93-7.fc11
- Create -compat subpackage as meta-package for installing all font families.

* Tue Jan 20 2009 Matthias Clasen <mclasen@redhat.com> - 1.04.93-6.fc11
- Fix busted inter-subpackage dependencies

* Tue Jan 20 2009 Caius Chance <cchance@redhat.com> - 1.04.93-5.fc11
- Resolved: rhbz#477410
- Refined .spec file based on Mailhot's review on rhbz.

* Mon Jan 19 2009 Caius Chance <cchance@redhat.com> - 1.04.93-4.fc11
- Resolves: thbz#477410
- Package renaming for post-1.13 fontpackages macros.

* Fri Jan 09 2009 Caius Chance <cchance@redhat.com> - 1.04.93-3.fc11
- Resolves: rhbz#477410 (Convert to new font packaging guidelines.)

* Tue Dec 09 2008 Caius Chance <cchance@redhat.com> - 1.04.93-2.fc11
- Resolves: rhbz#474522 (Cent sign is not coressed in Sans & Mono.)

* Wed Dec 03 2008 Caius Chance <cchance@redhat.com> - 1.04.93-1.fc11
- Resolves: rhbz#473481
  (Blurriness of Greek letter m (U+03BC) in Liberation Sans Regular.)

* Thu Jul 17 2008 Caius Chance <cchance@redhat.com> - 1.04.90-1.fc10
- Resolves: rhbz#258592
  (Incorrect glyph points and missing hinting instructions for U+0079, U+03BC,
   U+0431, U+2010..2012.)

* Thu Jul 17 2008 Caius Chance <cchance@redhat.com> - 1.04-1.fc10
- Resolves: rhbz#455717 (Update sources to version 1.04.)
- Improved .spec file.

* Thu Jun 12 2008 Caius Chance <cchance@redhat.com> - 1.04-0.1.beta2.fc10
- Updated source version to 1.04.beta2.
- Removed License.txt and COPYING as already included in sources.

* Thu Apr 10 2008 Caius Chance <cchance@redhat.com> - 1.03-1.fc9
- Resolves: rhbz#251890 (Exchanged and incomplete glyphs.)
- Repack source tarball and re-align source version number.

* Mon Mar 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.02-2
- correct license tag, license explanation added

* Tue Mar 25 2008 Caius Chance <cchance@redhat.com> - 1.02-1.fc9
- Resolves: rhbz#240525 (Alignment mismatch of dot accents.)

* Wed Jan 16 2008 Caius Chance <cchance@redhat.com> - 1.01-1.fc9
- Moved source tarball from cvs to separated storage.

* Mon Jan 14 2008 Caius Chance <cchance@redhat.com> - 1.0-1.fc9
- Resolves: rhbz#428596 (Liberation fonts need to be updated to latest font.)

* Wed Nov 28 2007 Caius Chance <cchance@redhat.com> - 0.2-4.fc9
- Resolves: rhbz#367791 (remove 59-liberation-fonts.conf)

* Wed Sep 12 2007 Jens Petersen <petersen@redhat.com> - 0.2-3.fc8
- add fontdir macro
- create fonts.dir and fonts.scale (reported by Mark Alford, #245961)
- add catalogue symlink

* Wed Sep 12 2007 Jens Petersen <petersen@redhat.com> - 0.2-2.fc8
- update license field to GPLv2

* Thu Jun 14 2007 Caius Chance <cchance@redhat.com> 0.2-1.fc8
- Updated new source tarball from upstream: '-3' (version 0.2).

* Tue May 15 2007 Matthias Clasen <mclasen@redhat.com> 0.1-9
- Bump revision

* Tue May 15 2007 Matthias Clasen <mclasen@redhat.com> 0.1-8
- Change the license tag to "GPL + font exception"

* Mon May 14 2007 Matthias Clasen <mclasen@redhat.com> 0.1-7
- Correct the source url

* Mon May 14 2007 Matthias Clasen <mclasen@redhat.com> 0.1-6
- Incorporate package review feedback

* Fri May 11 2007 Matthias Clasen <mclasen@redhat.com> 0.1-5
- Bring the package in sync with Fedora packaging standards

* Wed Apr 25 2007 Meethune Bhowmick <bhowmick@redhat.com> 0.1-4
- Require fontconfig package for post and postun

* Tue Apr 24 2007 Meethune Bhowmick <bhowmick@redhat.com> 0.1-3
- Bump version to fix issue in RHEL4 RHN

* Thu Mar 29 2007 Richard Monk <rmonk@redhat.com> 0.1-2rhis
- New license file

* Thu Mar 29 2007 Richard Monk <rmonk@redhat.com> 0.1-1rhis
- Inital packaging

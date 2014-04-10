%global fontname gnu-free
%global fontconf 67-%{fontname}

Name:      %{fontname}-fonts
Version:   20100919
Release:   6%{?dist}
Summary:   Free UCS Outline Fonts
Summary(zh_CN.UTF-8): 自由的 UCS Outline 字体
Group:     User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
# Standard font exception
License:   GPLv3+ with special font exception
URL:       http://www.gnu.org/software/freefont/ 
Source0:   http://savannah.nongnu.org/download/freefont/freefont-sfd-%{version}.tar.gz
Source1:   gnu-free-fonts-buildscript 
Source2:   %{fontconf}-mono.conf
Source3:   %{fontconf}-sans.conf
Source4:   %{fontconf}-serif.conf
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: fontpackages-devel fontforge

%global common_desc \
Gnu FreeFont is a free family of scalable outline fonts, suitable for general \
use on computers and for desktop publishing. It is Unicode-encoded for \
compatibility with all modern operating systems. \
 \
Besides a full set of characters for writing systems based on the Latin \
alphabet, FreeFont contains large selection of characters from other writing \
systems some of which are hard to find elsewhere. \
 \
FreeFont also contains a large set of symbol characters, both technical and \
decorative. We are especially pleased with the Mathematical Operators range, \
with which most of the glyphs used in LaTeX can be displayed.

%description
%common_desc


%package common
Summary:  Common files for freefont (documentation…)
Requires: fontpackages-filesystem

%description common
%common_desc

This package consists of files used by other %{name} packages.


%package -n %{fontname}-mono-fonts
Summary:  GNU FreeFont Monospaced Font
Requires: %{name}-common = %{version}-%{release}

%description -n %{fontname}-mono-fonts
%common_desc

This package contains the GNU FreeFont monospaced font.


%package -n %{fontname}-sans-fonts
Summary:  GNU FreeFont Sans-Serif Font
Requires: %{name}-common = %{version}-%{release}

%description -n %{fontname}-sans-fonts
%common_desc

This package contains the GNU FreeFont sans-serif font.


%package -n %{fontname}-serif-fonts
Summary:  GNU FreeFont Serif Font
Requires: %{name}-common = %{version}-%{release}

%description -n %{fontname}-serif-fonts
%common_desc

This package contains the GNU FreeFont serif font.


%package compat
Summary: GNU freefont compatibility package
Obsoletes: freefont < 20090104-4
Requires:  gnu-free-mono-fonts = %{version}-%{release}
Requires:  gnu-free-sans-fonts = %{version}-%{release}
Requires:  gnu-free-serif-fonts = %{version}-%{release}

%description compat
This package only exists to help transition pre 20090104-4 freefont users to \
the new package split. It will be removed after one distribution release \
cycle, please do not reference it or depend on it in any way.\
\
It can be safely uninstalled.


%prep
%setup -qn freefont-%{version}


%build
fontforge -lang=ff -script %{SOURCE1} *.sfd

%install
rm -rf %{buildroot}

install -m 0755 -d %{buildroot}%{_fontdir}
install -p -m 644 *.ttf  %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE2} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-mono.conf

install -m 0644 -p %{SOURCE3} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-sans.conf

install -m 0644 -p %{SOURCE4} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-serif.conf


for fconf in %{fontconf}-mono.conf \
                %{fontconf}-sans.conf \
                %{fontconf}-serif.conf ; do
  ln -s %{_fontconfig_templatedir}/$fconf \
        %{buildroot}%{_fontconfig_confdir}/$fconf
done

rm %{buildroot}%{_datadir}/fonts/gnu-free/Untitled1.ttf

%clean
rm -rf %{buildroot}

%_font_pkg -n mono -f %{fontconf}-mono.conf FreeMono*.ttf
%_font_pkg -n sans -f %{fontconf}-sans.conf FreeSans*.ttf
%_font_pkg -n serif -f %{fontconf}-serif.conf FreeSerif*.ttf

%files common
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog CREDITS COPYING README Untitled1.ttf

%files compat

%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 20100919-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20100919-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20100919-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 30 2010 Jon Ciesla <limb@jcomserv.net> 20100919-3
- Fixed URL.

* Sun Dec 12 2010 Jon Ciesla <limb@jcomserv.net> 20100919-2
- Fixed license tag, URL, BZ 644992.

* Tue Oct 05 2010 Jon Ciesla <limb@jcomserv.net> 20100919-1
- New upstream.

* Tue Aug 10 2010 Jon Ciesla <limb@jcomserv.net> 20090104-12
- Moved priority from 60 to 67, BZ 621498.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090104-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 23 2009 Jon Ciesla <limb@jcomserv.net> 20090104-10
- Moved closer to template in effort to correct symlinks.

* Fri Mar 20 2009 Jon Ciesla <limb@jcomserv.net> 20090104-9
- Fixed compat requires.
- Fixed symlinks.

* Wed Mar 18 2009 Jon Ciesla <limb@jcomserv.net> 20090104-8
- Changed fontname, fixed symlinks, typos.

* Mon Mar 09 2009 Jon Ciesla <limb@jcomserv.net> 20090104-7
- Tidied Requires and Obsoletes.

* Thu Mar 05 2009 Jon Ciesla <limb@jcomserv.net> 20090104-6
- Converted last define to global.
- Dropped -common group declaration.
- Dropped free from package names.
- Dropped unneccessary requires and obsoletes.
- Dropped fontdir from -common.
- Fixed conf install and names.

* Thu Mar 05 2009 Jon Ciesla <limb@jcomserv.net> 20090104-5
- Added -lang=ff to build script.

* Thu Mar 05 2009 Jon Ciesla <limb@jcomserv.net> 20090104-4
- Changed define to global.
- Dropped main package, created compat package.
- Dropped freefont-ttf Obsoletes.
- Fixed subpackage requires.
- Dropped subpackage Groups.
- Fixed font_pkg syntax.
- Buildrequire fontforge.
- Added fontconfig rules.
- Minor spec order corrections.

* Tue Feb 17 2009 Jon Ciesla <limb@jcomserv.net> 20090104-3
- For BZ 477336:
- Renamed from freefont to gnu-free-fonts.
- Build from sfd now.
- Removed Requires for fontconfig.
- Drop old Provides.

* Mon Feb 09 2009 Jon Ciesla <limb@jcomserv.net> 20090104-2
- Implemented font_pkg.
- Corrected subpackage names.

* Mon Jan 12 2009 Orion Poplawski <orion@cora.nwra.com> 20090104-1
- update to 20090104
- conform to font package guidelines

* Fri Jul 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 20080323-1
- fix license tag
- update to 20080323

* Fri Jan  5 2007 Orion Poplawski <orion@cora.nwra.com> 20060126-4
- Require fontconfig, not /usr/share/fonts

* Tue Oct 31 2006 Orion Poplawski <orion@cora.nwra.com> 20060126-3
- BOO!
- Make Provides/Osoletes versioned
- Make setup quiet

* Wed Oct 25 2006 Orion Poplawski <orion@cora.nwra.com> 20060126-2
- Remove fonts.cache refs
- fc-cache /usr/share/fonts/freefont

* Thu Oct 12 2006 Orion Poplawski <orion@cora.nwra.com> 20060126-1
- freefont-ttf-20060126

* Tue Dec 06 2005 Rex Dieter 20051206-1
- freefont-ttf-20051206

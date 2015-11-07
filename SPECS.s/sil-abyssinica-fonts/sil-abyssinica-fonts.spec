%global fontname     sil-abyssinica
%global archive_name AbyssinicaSIL
%global fontconf     66-%{fontname}.conf


Name:           %{fontname}-fonts
Version:        1.200
Release:        8%{?dist}
Summary:        SIL Abyssinica fonts
Summary(zh_CN.UTF-8): SIL Abyssinica 字体

License:        OFL
URL:            http://scripts.sil.org/AbyssinicaSIL
# download from http://scripts.sil.org/cms/scripts/render_download.php?site_id=nrsi&format=file&media_id=AbyssinicaSIL1.200.zip&filename=AbyssinicaSIL1.200.zip
Source0:        %{archive_name}%{version}.zip
Source1:        %{fontconf}

BuildArch:      noarch

Requires:       fontpackages-filesystem
BuildRequires:  fontpackages-devel
BuildRequires:  dos2unix


%description
SIL Abyssinica is a Unicode typeface family containing glyphs for the
Ethiopic script.

The Ethiopic script is used for writing many of the languages of Ethiopia and
Eritrea. Abyssinica SIL supports all Ethiopic characters which are in Unicode
including the Unicode 4.1 extensions. Some languages of Ethiopia are not yet
able to be fully represented in Unicode and, where necessary, we have included
non-Unicode characters in the Private Use Area (see Private-use (PUA)
characters supported by Abyssinica SIL).

Abyssinica SIL is based on Ethiopic calligraphic traditions. This release is
a regular typeface, with no bold or italic version available or planned.

%description -l zh_CN.UTF-8
SIL Abyssinica 字体。

%prep
%setup -q -n %{archive_name}-%{version}


%build
dos2unix FONTLOG.txt OFL.txt OFL-FAQ.txt README.txt documentation/DOCUMENTATION.txt


%install
#fonts
install -d -m 0755 %{buildroot}%{_fontdir}
install -m 0644 *.ttf %{buildroot}%{_fontdir}

#fontconfig
install -d -m 0755 %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}
install -m 0644 -p %{SOURCE1} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}
ln -s %{_fontconfig_templatedir}/%{fontconf} \
      %{buildroot}%{_fontconfig_confdir}/%{fontconf}
magic_rpm_clean.sh

%_font_pkg -f %{fontconf} *.ttf

%doc FONTLOG.txt OFL.txt OFL-FAQ.txt README.txt
%doc documentation/*


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.200-8
- 为 Magic 3.0 重建

* Sun Sep 27 2015 Liu Di <liudidi@gmail.com> - 1.200-7
- 为 Magic 3.0 重建

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.200-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.200-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 13 2012 Parag Nemade <pnemade AT redhat DOT com> - 1.200-4
- Resolves:rh#847576:-better enabling autohinting by default 

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.200-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 1.200-2
- Spec file cleanup, remove stuff that is not needed any more.
- Fix build with latest release.

* Fri Feb 03 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 1.200-1
- New upstream release.
- Remove Obsoletes/Provides from package rename.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jun 12 2010 Mathieu Bridon <bochecha@fedoraproject.org> - 1.0-9
- Add fontconfig configuration file (BZ#586248)

* Tue Feb 16 2010 Mathieu Bridon <bochecha@fedoraproject.org> - 1.0-8
- Fix Obsolete: that was wrong when renaming the package.
- The font base folder was listed twice (one was hidden in the font macro)

* Thu Feb 11 2010 Mathieu Bridon <bochecha@fedoraproject.org> - 1.0-7
- Use new archive from upstream at same location (which is lowercase now)
- Remove dubious Provides: (RHBZ#563395)

* Wed Feb 10 2010 Mathieu Bridon <bochecha@fedoraproject.org> - 1.0-6
- Renamed from abyssinica-fonts to sil-abyssinica-fonts

* Mon Feb  1 2010 Jens Petersen <petersen@redhat.com>
- use general SIL url and simplify download url

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 21 2008 Bernie Innocenti <bernie@codewiz.org> 1.0-3
- Updated to current Fedora font packaging guidelines

* Thu Oct 04 2007 Todd Zullinger <tmz@pobox.com> 1.0-2
- use upstream zip file as Source0
- fix license tag

* Fri Sep 14 2007 Bernardo Innocenti <bernie@codewiz.org> 1.0-1
- Initial packaging, borrowing many things from gentium-fonts

%global fontname lato
%global fontconf 61-%{fontname}.conf

Name:           %{fontname}-fonts
Version:        2.015
Release:        1%{?dist}
Summary:        A sanserif typeface family

Group:          User Interface/X
License:        OFL
URL:            http://www.latofonts.com/
# Fonts retrieved 2015-08-07 from http://www.latofonts.com/download/Lato2OFL.zip
Source0:        %{name}-%{version}.zip
Source1:        %{name}-fontconfig.conf
Source2:        %{fontname}.metainfo.xml

BuildArch:      noarch
BuildRequires:  fontpackages-devel
Requires:       fontpackages-filesystem
Provides:       google-lato-fonts = %{version}-%{release}
Obsoletes:      google-lato-fonts < 1.014-1

%description
Lato is a sanserif typeface family designed in the Summer 2010 by Warsaw-based
designer Łukasz Dziedzic ("Lato" means "Summer" in Polish). In December 2010 the
Lato family was published under the open-source Open Font License by his foundry
tyPoland, with support from Google.

When working on Lato, Łukasz tried to carefully balance some potentially
conflicting priorities. He wanted to create a typeface that would seem quite
"transparent" when used in body text but would display some original treats when
used in larger sizes. He used classical proportions (particularly visible in the
uppercase) to give the letterforms familiar harmony and elegance. At the same
time, he created a sleek sanserif look, which makes evident the fact that Lato
was designed in 2010 - even though it does not follow any current trend.

The semi-rounded details of the letters give Lato a feeling of warmth, while the
strong structure provides stability and seriousness. "Male and female, serious
but friendly. With the feeling of the Summer," says Łukasz.

Lato consists of nine weights (plus corresponding italics), including a
beautiful hairline style. It covers 2300+ glyphs per style and supports 100+
Latin-based languages, 50+ Cyrillic-based languages as well as Greek and IPA
phonetics.


%prep
%setup -q -c

# Fix wrong end-of-lines encoding
sed "s/\r//" Lato2OFL/OFL.txt > Lato2OFL/OFL.txt.new
touch -r Lato2OFL/OFL.txt Lato2OFL/OFL.txt.new
mv Lato2OFL/OFL.txt.new Lato2OFL/OFL.txt

# Fix permissions
chmod 0644 Lato2OFL/{OFL.txt,README.txt}


%build


%install
install -m 0755 -d $RPM_BUILD_ROOT%{_fontdir}
install -m 0644 -p Lato2OFL/*.ttf $RPM_BUILD_ROOT%{_fontdir}

install -m 0755 -d $RPM_BUILD_ROOT%{_fontconfig_templatedir} $RPM_BUILD_ROOT%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} $RPM_BUILD_ROOT%{_fontconfig_templatedir}/%{fontconf}
ln -s %{_fontconfig_templatedir}/%{fontconf} $RPM_BUILD_ROOT%{_fontconfig_confdir}/%{fontconf}

# Add AppStream metadata
install -Dm 0644 -p %{SOURCE2} \
        %{buildroot}%{_datadir}/appdata/%{fontname}.metainfo.xml

%_font_pkg -f %{fontconf} *.ttf
%doc Lato2OFL/README.txt
%license Lato2OFL/OFL.txt
%{_datadir}/appdata/%{fontname}.metainfo.xml


%changelog
* Fri Aug 07 2015 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.015-1
- Update to 2.015

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.010-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Oct 15 2014 Richard Hughes <richard@hughsie.com> - 2.010-2
- Add a MetaInfo file for the software center; this is a font we want to show.

* Thu Sep 04 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.010-1
- Update to 2.010

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 02 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.007-1
- Update to 2.007

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.105-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 06 2013 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.105-1
- Update to 1.105

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.014-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Sep 29 2012 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.014-2
- Drop useless Buildroot cleaning

* Sun Sep 23 2012 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.014-1
- Initial release, to replace google-lato-fonts package

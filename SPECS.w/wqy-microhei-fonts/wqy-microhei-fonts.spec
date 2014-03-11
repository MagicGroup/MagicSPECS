%global fontname wqy-microhei
%global fontconf 65-%{fontname}.conf

%global archivename %{fontname}-%{version}-beta

Name:           %{fontname}-fonts
Version:        0.2.0
Release:        0.10.beta%{?dist}
Summary:        Compact Chinese fonts derived from Droid

Group:          User Interface/X
License:        ASL 2.0 or GPLv3 with exceptions
URL:            http://wenq.org/enindex.cgi?MicroHei(en)
Source0:        http://downloads.sourceforge.net/wqy/%{archivename}.tar.gz
Source1:        %{name}-fontconfig.conf
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:      noarch
BuildRequires:  fontpackages-devel
Requires:       fontpackages-filesystem

%description
A new Sans Serif CJK font derived from Google's "Droid Sans Fallback"
and covers the entire GBK code points (20932 Han glyphs).

%prep
%setup -q -n %{fontname}

mv README.txt{,.orig}
iconv -f iso8859-1 -t utf8 README.txt.orig > README.txt


%build


%install
rm -fr %{buildroot}

install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p *.ttc %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}
ln -s %{_fontconfig_templatedir}/%{fontconf} \
      %{buildroot}%{_fontconfig_confdir}/%{fontconf}


%clean
rm -fr %{buildroot}


%_font_pkg -f %{fontconf} *.ttc
%doc LICENSE_Apache2.txt LICENSE_GPLv3.txt README.txt


%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.2.0-0.10.beta
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-0.9.beta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 26 2011  Peng Wu <pwu@redhat.com> - 0.2.0-0.8.beta
- Update wqy-microhei-fonts-fontconfig.conf

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-0.7.beta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon May 31 2010  Peng Wu <pwu@redhat.com> - 0.2.0-0.6.beta
- Add fontconfig file back to wqy-microhei-fonts.

* Wed May 26 2010  Peng Wu <pwu@redhat.com> - 0.2.0-0.5.beta
- Clean up rpm spec file and remove unused patches.

* Wed May 26 2010  Peng Wu <pwu@redhat.com> - 0.2.0-0.4.beta
- Improves Simplified Chinese and Traditional Chinese fonts.
  In order to keep the WenQuanYi Zen Hei as default Simplified Chinese font,
  the fontconfig file of this WenQuanYi Micro Hei font is removed.

* Mon Apr 19 2010  Peng Wu <pwu@redhat.com> - 0.2.0-0.3.beta
- get rid of binding="same", fixes [rhbz#578050] (New: lang-specific overrides rule doesn't work as expected).

* Mon Dec  7 2009 Jens Petersen <petersen@redhat.com> - 0.2.0-0.1.beta
- initial packaging for fedora

%define fontname sj
%define fontconf 63-%{fontname}

%define common_desc Two fonts by Steve Jordi released under the GPL 

Name:          %{fontname}-fonts
Version:       2.0.2
Release:       10%{?dist}
Summary:       Two fonts by Steve Jordi released under the GPL

Group:         User Interface/X
License:       GPLv2 with exceptions
URL:           http://sjfonts.sourceforge.net
Source0:       sjfonts-source-2.0.2.tar.bz2
Source1:       %{name}-delphine-fontconfig.conf
Source2:       %{name}-stevehand-fontconfig.conf
BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:     noarch
BuildRequires: fontpackages-devel
BuildRequires: fontforge

%description
%common_desc

%package common
Summary:       Common files for %{name}
Group:         User Interface/X
Requires:      fontpackages-filesystem

%description common
%common_desc

This package consists of files used by other %{name} packages.

%package -n %{fontname}-delphine-fonts
Summary:       Handwriting font
Group:         User Interface/X
Requires:      %{name}-common = %{version}-%{release}

%description -n %{fontname}-delphine-fonts
%common_desc

Handwriting font by Steve Jordi covering latin glyphs.

%_font_pkg -n delphine -f %{fontconf}-delphine.conf Delphine.ttf

%package -n %{fontname}-stevehand-fonts
Summary:       Handwriting font
Group:         User Interface/X
Requires:      %{name}-common = %{version}-%{release}

%description -n %{fontname}-stevehand-fonts
%common_desc

Handwriting font by Steve Jordi covering latin glyphs.

%_font_pkg -n stevehand -f %{fontconf}-stevehand.conf SteveHand.ttf

%prep
%setup -q -c %{name}-%{version}

%build
fontforge -lang=ff -script "-" Delphine.sfd SteveHand.sfd <<EOF
i = 1
while ( i < \$argc )
  Open (\$argv[i], 1)
  Generate (\$fontname + ".ttf")
  PrintSetup (5)
  PrintFont (0, 0, "", \$fontname + "-sample.pdf")
  Close()
  i++
endloop
EOF

%install
rm -rf $RPM_BUILD_ROOT

install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p *.ttf %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-delphine.conf
install -m 0644 -p %{SOURCE2} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-stevehand.conf

for fontconf in %{fontconf}-delphine.conf %{fontconf}-stevehand.conf ; do
  ln -s %{_fontconfig_templatedir}/$fontconf %{buildroot}%{_fontconfig_confdir}/$fontconf
done

%clean
rm -rf $RPM_BUILD_ROOT

%files common
%defattr(0644,root,root,0755)
%doc COPYING
%doc README

%dir %{_fontdir}

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.0.2-10
- 为 Magic 3.0 重建

* Sun Sep 27 2015 Liu Di <liudidi@gmail.com> - 2.0.2-9
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.0.2-8
- 为 Magic 3.0 重建

* Mon Feb 06 2012 Liu Di <liudidi@gmail.com> - 2.0.2-7
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 15 2009 Nicolas Mailhot <nicolas.mailhot at laposte.net> - 2.0.2-4
— Make sure F11 font packages have been built with F11 fontforge

* Sat Feb 28 2009 Sven Lankes <sven@lank.es> - 2.0.2-3
- Adjust fontforge call to fix ftbfs 

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 25 2008 Sven Lankes <sven@lank.es> - 2.0.2-1
- Initial packaging


%global fontname cjkuni-uming
%global fontconf 65-0-ttf-arphic-uming.conf
%global fontconf3 90-ttf-arphic-uming-embolden.conf

%global catalogue        %{_sysconfdir}/X11/fontpath.d

%global common_desc \
CJK Unifonts are Unicode TrueType fonts derived from original fonts made \
available by Arphic Technology under "Arphic Public License" and extended by \
the CJK Unifonts project.

%global umingbuilddir %{name}-%{version}

Name:           %{fontname}-fonts
Version:        0.2.20080216.1
Release:        53%{?dist}
Summary:        Chinese Unicode TrueType font in Ming face
Summary(zh_CN.UTF-8): 明体字体

Group:          User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
License:        Arphic
URL:            http://www.freedesktop.org/wiki/Software/CJKUnifonts
Source0:        http://ftp.debian.org/debian/pool/main/t/ttf-arphic-uming/ttf-arphic-uming_%{version}.orig.tar.gz
Source1:        %{name}-fontconfig.conf
Source3:        %{fontconf3}

BuildArch:      noarch
BuildRequires:  fontpackages-devel
Requires:       fontpackages-filesystem
Obsoletes:      cjkuni-fonts-common < 0.2.20080216.1-42
Provides:       cjkuni-fonts-common = 0.2.20080216.1-42

%description
%common_desc

CJK Unifonts in Ming face.

%description -l zh_CN.UTF-8
明体字体。

%prep
%setup -q -c -n %{name}-%{version}


%build
%{nil}

%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p *.ttc %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}
ln -s %{_fontconfig_templatedir}/%{fontconf} \
      %{buildroot}%{_fontconfig_confdir}/%{fontconf}


install -m 0644 -p %{SOURCE3} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf3}
ln -s %{_fontconfig_templatedir}/%{fontconf3} \
      %{buildroot}%{_fontconfig_confdir}/%{fontconf3}

# catalogue
install -m 0755 -d %{buildroot}%{catalogue}
ln -s %{_fontdir}/ %{buildroot}%{catalogue}/%{name}


%_font_pkg -f *.conf *.ttc

%defattr(-,root,root,-)
%doc ../%{umingbuilddir}/license
%doc ../%{umingbuilddir}/CONTRIBUTERS
%doc ../%{umingbuilddir}/FONTLOG
%doc ../%{umingbuilddir}/KNOWN_ISSUES
%doc ../%{umingbuilddir}/NEWS
%doc ../%{umingbuilddir}/README
%{catalogue}/%{name}

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.2.20080216.1-53
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.2.20080216.1-52
- 为 Magic 3.0 重建

* Tue Nov 13 2012  Peng Wu <pwu@redhat.com> - 0.2.20080216.1-51
- Improves spec file

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.20080216.1-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012  Peng Wu <pwu@redhat.com> - 0.2.20080216.1-49
- Fixes fontconf

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.20080216.1-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Mar 16 2011  Peng Wu <pwu@redhat.com> - 0.2.20080216.1-47
- Clean up spec.
  Remove fonts.dir, fonts.scale and 25-ttf-arphic-uming-render.conf.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.20080216.1-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 20 2010  Peng Wu <pwu@redhat.com> - 0.2.20080216.1-45
- Fixes font_pkg macro usage.

* Mon Jul 19 2010  Peng Wu <pwu@redhat.com> - 0.2.20080216.1-44
- Clean up the spec.

* Mon Jul 12 2010  Peng Wu <pwu@redhat.com> - 0.2.20080216.1-43
- The Initial Version.
  Split from cjkuni-fonts.

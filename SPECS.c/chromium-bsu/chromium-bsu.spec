Name:           chromium-bsu
Version:	0.9.15.1
Release:        2%{?dist}
Summary:        Fast paced, arcade-style, top-scrolling space shooter
Summary(zh_CN.UTF-8): 一个纵版飞行射击街机游戏
Group:          Amusements/Games
Group(zh_CN.UTF-8): 娱乐/游戏
License:        Artistic clarified
URL:            http://chromium-bsu.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  desktop-file-utils SDL-devel alsa-lib-devel libvorbis-devel
BuildRequires:  SDL_image-devel SDL_mixer-devel libpng-devel libglpng-devel quesoglc-devel
BuildRequires:  openal-soft-devel freealut-devel >= 1.1.0-10
Requires:       hicolor-icon-theme

%description
You are captain of the cargo ship Chromium B.S.U., responsible for delivering
supplies to our troops on the front line. Your ship has a small fleet of
robotic fighters which you control from the relative safety of the Chromium
vessel. This is an OpenGL-based shoot 'em up game with fine graphics.

%description -l zh_CN.UTF-8
一个纵版飞行射击街机游戏。

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
cp -a AUTHORS README COPYING NEWS \
  $RPM_BUILD_ROOT%{_docdir}/%{name}
magic_rpm_clean.sh
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_mandir}/man6/%{name}.6.gz


%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.9.15.1-2
- 为 Magic 3.0 重建

* Mon Mar 10 2014 Liu Di <liudidi@gmail.com> - 0.9.15.1-1
- 更新到 0.9.15.1

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 14 2011 Hans de Goede <hdegoede@redhat.com> - 0.9.15-1
- New upstream release 0.9.15

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jun 21 2010 Hans de Goede <hdegoede@redhat.com> 0.9.14.1-1
- New upstream release 0.9.14.1
- Drop Fedora specific README.license (upstream has fixed the included license)
- This fixes the FTBFS of the previous version (#599832)

* Fri Oct  9 2009 Hans de Goede <hdegoede@redhat.com> 0.9.14-6
- Switch to quesoglc instead of ftgl (glc is the upstream default)
- This fixes chromium-bsu not finding its font, as quesoglc properly uses
  fontconfig instead of using a hardcoded path to the font (#526995)

* Sun Aug 16 2009 Hans de Goede <hdegoede@redhat.com> 0.9.14-5
- Switch to openal-soft

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 27 2009 Hans de Goede <hdegoede@redhat.com> 0.9.14-3
- Fix build errors (#502191)

* Fri May 22 2009 Hans de Goede <hdegoede@redhat.com> 0.9.14-2
- Minor packaging cleanups from review (#502191)

* Sun May 17 2009 Hans de Goede <hdegoede@redhat.com> 0.9.14-1
- Initial Fedora package

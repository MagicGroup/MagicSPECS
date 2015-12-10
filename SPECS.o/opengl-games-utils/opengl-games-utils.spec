Name:           opengl-games-utils
Version:        0.2
Release:        6%{?dist}
Summary:        Utilities to check proper 3d support before launching 3d games
Group:          Amusements/Games
License:        Public Domain
URL:            http://fedoraproject.org/wiki/SIGs/Games
Source0:        opengl-game-wrapper.sh
Source1:        opengl-game-functions.sh
Source2:        README
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       zenity glx-utils

%description
This package contains various shell scripts which are intented for use by
3D games packages. These shell scripts can be used to check if direct rendering
is available before launching an OpenGL game. This package is intended for use
by other packages and is not intended for direct end user use!


%prep
%setup -c -T
cp %{SOURCE2} .


%build
# nothing to build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
install -p -m 755 %{SOURCE0} $RPM_BUILD_ROOT%{_bindir}
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/%{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README
%{_bindir}/opengl-game-wrapper.sh
%{_datadir}/%{name}


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.2-6
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0.2-5
- 为 Magic 3.0 重建

* Fri Mar 27 2015 Liu Di <liudidi@gmail.com> - 0.2-4
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.2-3
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 15 2011 Hans de Goede <hdegoede@redhat.com> 0.2-1
- Recognize software rendering as such now that it is done with gallium
  llvmpipe, rather then the classic software renderer
- Add a new hasDri function to opengl-game-functions.sh

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 10 2009 Hans de Goede <hdegoede@redhat.com> 0.1-8
- Recognize software rendering as such with new Mesa which always says
  DRI = Yes (rh 494174)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 13 2008 Hans de Goede <hdegoede@redhat.com> 0.1-6
- Handle glxinfo output not containing any dri info at all (rh 471374)

* Fri Jan 11 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1-5
- Fix DRI detection to work with dual head configurations

* Tue Oct 16 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1-4
- Fix a minor spelling error in the dialog shown when DRI is not available

* Mon Sep 24 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1-3
- Put DRI checking functionality in a checkDriOK bash function in
  opengl-game-functions.sh, for usage from existing wrapper scripts

* Sun Sep 16 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1-2
- Various spelling fixes thanks to Rahul Sundaram

* Sun Sep 16 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1-1
- Initial Fedora package

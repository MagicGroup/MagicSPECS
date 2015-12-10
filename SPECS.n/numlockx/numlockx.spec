Name:           numlockx
Version:        1.2
Release:        6%{?dist}
Summary:        Turns on NumLock after starting X
Summary(zh_CN.UTF-8): 启动 X 后打开 Numlock

Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
License:        MIT
URL:            http://ktown.kde.org/~seli/numlockx/
Source0:        http://ktown.kde.org/~seli/numlockx/numlockx-%{version}.tar.gz
Source1:        numlockx.sh

BuildRequires:  libX11-devel libXtst-devel libXext-devel libXt-devel imake
Requires:       xorg-x11-xinit

%description
%{summary}

%description -l zh_CN.UTF-8
启动 X 后打开 Numlock。

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -p -D %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/numlockx.sh
magic_rpm_clean.sh


%files
%defattr(-,root,root,-)
%{_bindir}/numlockx
%{_sysconfdir}/X11/xinit/xinitrc.d/numlockx.sh
%doc AUTHORS README LICENSE

%changelog
* Wed Nov 11 2015 Liu Di <liudidi@gmail.com> - 1.2-6
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.2-5
- 为 Magic 3.0 重建

* Sat Feb 28 2015 Liu Di <liudidi@gmail.com> - 1.2-4
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.2-3
- 为 Magic 3.0 重建

* Thu Jan 19 2012 Liu Di <liudidi@gmail.com> - 1.2-2
- 为 Magic 3.0 重建

* Sat Mar 26 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 1.2-1
- New upstream release
- Update spec to match current guidelines
 
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0-14
- Autorebuild for GCC 4.3

* Fri Aug 24 2007 John Mahowald <jpmahowald@gmail.com> - 1.0-13
- Rebuild for buildid

* Thu Sep 07 2006 John Mahowald <jpmahowald@gmail.com> - 1.0-11
- Rebuild for Fedora Extras 6

* Wed Feb 15 2006 John Mahowald <jpmahowald@gmail.com> 1.0-9
- Rebuild for Fedora Extras 5

* Tue Nov 29 2005 John Mahowald <jpmahowald@gmail.com> 1.0-7
- More Buildreqires fixes to satisfy configure

* Tue Nov 29 2005 John Mahowald <jpmahowald@gmail.com> 1.0-6
- Buildrequires fixes

* Mon Nov 28 2005 John Mahowald <jpmahowald@gmail.com> 1.0-5
- Change requires xinitrc to xorg-x11-xinit

* Mon Aug 29 2005 John Mahowald <jpmahowald@gmail.com> 1.0-4
- %%{?dist} in Release

* Sun Aug 28 2005 John Mahowald <jpmahowald@gmail.com> 1.0-3
- Macro changes

* Sat Aug 27 2005 John Mahowald <jpmahowald@gmail.com> 1.0-2
- Script for xinitrc.d
- Use more macros

* Fri Aug 26 2005 John Mahowald <jpmahowald@gmail.com> 1.0-1
- Initial rpm

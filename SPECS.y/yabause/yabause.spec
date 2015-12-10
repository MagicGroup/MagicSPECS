%undefine _hardened_build

Name:           yabause
Version:	0.9.14
Release:	4%{?dist}
Summary:        A Sega Saturn emulator
Summary(zh_CN): Sega 土星模拟器
Group:          Applications/Emulators
Group(zh_CN):	应用程序/模拟器
License:        GPLv2+
URL:            http://yabause.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:        %{name}.desktop
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  desktop-file-utils
BuildRequires:  freeglut-devel
BuildRequires:  gtk+-devel
BuildRequires:  gtkglext-devel
BuildRequires:  libGLU-devel
BuildRequires:  libICE-devel
BuildRequires:  libXt-devel
BuildRequires:  pkgconfig
BuildRequires:  SDL-devel
Requires:       hicolor-icon-theme

%description
Yabause is a Sega Saturn emulator. A popular console of the early 1990s. It
includes an 'emulated' Saturn BIOS which is compatible with at least some games
but optionally a real Saturn BIOS can be used, however it is not included.

%description -l zh_CN
这是一个世嘉土星模拟器，在 1990 年代早期流行的家用机。它包括了一个模拟的土星 BIOS，
但是也可以使用真正的土星 BIOS（未包含在此包中）。

%prep
%setup -q

%build
%cmake -DBUILD_SHARED_LIBS:BOOL=OFF -DYAB_PORTS=qt -DYAB_OPTIMIZATION=-O2 .
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%doc AUTHORS ChangeLog COPYING GOALS README README.QT TODO


%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 0.9.14-4
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 0.9.14-3
- 为 Magic 3.0 重建

* Tue Oct 27 2015 Liu Di <liudidi@gmail.com> - 0.9.14-2
- 更新到 0.9.14

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.9.11.1-2
- 为 Magic 3.0 重建



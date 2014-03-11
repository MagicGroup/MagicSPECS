Name:           yabause
Version:        0.9.11.1
Release:        2%{?dist}
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
mkdir build
cd build
%cmake ..
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps

# Some cleanups
rm -rf %{buildroot}%{_datadir}/%{name} %{buildroot}%{_datadir}/pixmaps
rm -f %{buildroot}%{_datadir}/applications/*.desktop %{buildroot}%{_bindir}/gen68k
mkdir %{buildroot}%{_libdir}
install -pm0755 src/libyabause.so %{buildroot}%{_libdir}/

install -pm0644 ../src/logo.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png

desktop-file-install --vendor magic \
                     --dir %{buildroot}%{_datadir}/applications \
                     %{SOURCE1}


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_libdir}/*.so
%{_mandir}/man1/%{name}.1.gz
%{_datadir}/applications/magic-%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%doc AUTHORS ChangeLog COPYING GOALS README README.LIN TODO


%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.9.11.1-2
- 为 Magic 3.0 重建



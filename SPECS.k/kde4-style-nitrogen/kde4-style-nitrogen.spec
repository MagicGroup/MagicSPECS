Name:           kde4-style-nitrogen
BuildRequires:  kdebase4-workspace-devel
Requires:       kdebase4-workspace
License:        GPL v2 or later
Url:            http://kde-look.org/content/show.php/Nitrogen?content=99551
Group:          System/GUI/KDE
Group(zh_CN):	”√ªßΩÁ√Ê/◊¿√Ê
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Summary:        A fork of the Oxygen/Ozone decoration
Summary(zh_CN): Oxygen/Ozone ¥∞ø⁄◊∞ Œµƒ“∆÷≤
Version:        3.3.2
Release:        3%{?dist}
Source:         99551-kde4-windeco-nitrogen-%{version}-Source.tar.gz

%description
The Nitrogen window decoration is a fork of the Oxygen/Ozone decoration that allows notably to 
 
 - resize window borders, 
 - change buttons size,
 - hide the horizontal separator.
 - select different title bar blending and frame border size depending on the window title or name, in order to have better integration of GTK based windows in the decoration style.
 - add a size-grip handle in the bottom-right corner of windows. This is particularly useful when the no-border option is selected.

%description -l zh_CN
Oxygen/Ozone ¥∞ø⁄◊∞ Œµƒ“∆÷≤°£

%prep
%setup -n kde4-windeco-nitrogen-%{version}-Source -q

%build
mkdir build
pushd build
%cmake_kde4 ..
%{__make} %{?_smp_mflags}
popd 

%install
rm -rf %{buildroot}
pushd build
make install DESTDIR=%{buildroot}
magic_rpm_clean.sh
%find_lang kwin_nitrogen || :
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%kde4_plugindir/kwin3_nitrogen.so
%kde4_plugindir/kwin_nitrogen_config.so
%kde4_appsdir/kwin/nitrogenclient.desktop
%doc COPYING README

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 3.3.2-3
- ‰∏∫ Magic 3.0 ÈáçÂª∫

* Wed Dec 21 2011 Liu Di <liudidi@gmail.com> - 3.3.2-2
- ‰∏∫ Magic 3.0 ÈáçÂª∫



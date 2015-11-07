Name:           kde4-style-nitrogen
BuildRequires:  kdebase4-workspace-devel
Requires:       kdebase4-workspace
License:        GPL v2 or later
Url:            http://kde-look.org/content/show.php/Nitrogen?content=99551
Group:          User Interface/Desktops
Group(zh_CN.UTF-8):	用户界面/桌面
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Summary:        A fork of the Oxygen/Ozone decoration
Summary(zh_CN.UTF-8): Oxygen/Ozone 窗口装饰的移植
Version:        3.3.2
Release:        5%{?dist}
Source:         99551-kde4-windeco-nitrogen-%{version}-Source.tar.gz

%description
The Nitrogen window decoration is a fork of the Oxygen/Ozone decoration that allows notably to 
 
 - resize window borders, 
 - change buttons size,
 - hide the horizontal separator.
 - select different title bar blending and frame border size depending on the window title or name, in order to have better integration of GTK based windows in the decoration style.
 - add a size-grip handle in the bottom-right corner of windows. This is particularly useful when the no-border option is selected.

%description -l zh_CN.UTF-8
Oxygen/Ozone 窗口装饰的移植。

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
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 3.3.2-5
- 为 Magic 3.0 重建

* Thu Jun 05 2014 Liu Di <liudidi@gmail.com> - 3.3.2-4
- 为 Magic 3.0 重建


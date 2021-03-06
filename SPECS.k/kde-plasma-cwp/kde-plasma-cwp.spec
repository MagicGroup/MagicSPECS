Name:           kde-plasma-cwp
Version:	1.12.0
Release:        3%{?dist}
Summary:        Customizable Weather Plasmoid
Summary(zh_CN.UTF-8):	可定制的天气 Plasmoid
Group:          User Interface/Desktops
Group(zh_CN.UTF-8):	用户界面/桌面
License:        GPLv2+
URL:            http://www.kde-look.org/content/show.php?content=98925
Source0:        http://kde-look.org/CONTENT/content-files/98925-cwp-%{version}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  kdelibs4-devel


%description
This is another weather plasmoid.
It aims to be highly customizable, but a little harder to setup than other
weather plasmoids.
Nearly any weather forecast provider can be used, as long as the data is
provided as html files (no flash).
The information how to extract the information from these html files is
stored inside xml files.
Commands like grep, head, tail, sed, awk, ... will do this job.

%description -l zh_CN.UTF-8
可定制的天气 Plasmoid

%prep
%setup -q -n cwp-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make VERBOSE=1 %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang plasma_applet_cwp

%clean
rm -rf %{buildroot}


%files -f plasma_applet_cwp.lang
%defattr(-,root,root,-)
%doc ChangeLog COPYING README
%{_kde4_libdir}/kde4/plasma_applet_cwp.so
%{_kde4_datadir}/kde4/services/plasma-applet-cwp.desktop
%{_kde4_appsdir}/plasma-cwp/*.xml
%{_kde4_appsdir}/plasma-cwp/background_*.png
%{_kde4_appsdir}/desktoptheme/default/widgets/*.svgz
%{_kde4_datadir}/icons/oxygen/*/status/weather-windy.*


%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 1.12.0-3
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.12.0-2
- 更新到 1.12.0

* Fri Jun 06 2014 Liu Di <liudidi@gmail.com> - 1.11.0-1
- 更新到 1.11.0

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.5.7-2
- 为 Magic 3.0 重建


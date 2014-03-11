Name:		kde-plasma-smooth-tasks
Version:	0.0.1
Release:	0.1.wip20101106%{?dist}
Summary:	KDE taskbar replacement with window peeking ability
Summary(zh_CN): kDE 任务栏的增强

Group:		User Interface/Desktops
Group(zh_CN):	用户界面/桌面
License:	GPLv2+
URL:		http://www.kde-look.org/content/show.php/Smooth+Tasks?content=101586
Source0:	http://www.kde-look.org/CONTENT/content-files/101586-smooth-tasks-src-wip-2010-11-06.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gettext, kdebase4-workspace-devel
Requires:	kdebase4-workspace

#global kde4_version %((kde4-config --version 2>/dev/null || echo "KDE 4.3.0") | grep ^KDE | cut -d' ' -f2)

#{?_kde4_macros_api:Requires: kde4-macros(api) = %{_kde4_macros_api} }

%description
This taskbar replacement has window peeking similar to Windows 7 
when you use the kwin 'highlite window' effect. 
Even if this effect is not used you can click the tooltip in order 
to activate the corresponding window.

%description -l zh_CN
KDE 任务栏的增强

%prep
%setup -q -n smooth-tasks-src-wip-2010-11-06
## Due to the name change this sed is needed for find-lang.
sed -i 's,set(catalogname plasma_applet_smooth-tasks),set(catalogname kde-plasma-smooth-tasks),g' po/CMakeLists.txt

%build
mkdir build
cd build
%cmake_kde4 ..

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}

magic_rpm_clean.sh

# some more cleaning
rm -rfv %{buildroot}%{kde4_localedir}/uk_UA

%clean_kde4_desktop_files

#find_lang %{name} --with-kde

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README COPYING
%{kde4_plugindir}/plasma_applet_smooth-tasks.so
%{kde4_servicesdir}/plasma-applet-smooth-tasks.desktop
%{kde4_localedir}/*

%changelog


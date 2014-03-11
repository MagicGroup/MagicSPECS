Name:           bleachbit
Version:	1.0
Release:        2%{?dist}
Summary:        Remove unnecessary files, free space, and maintain privacy
Summary(zh_CN): 清除不需要的文件，释放空间的软件
License:        GPLv3+
BuildRequires:  python-devel desktop-file-utils gettext  
Requires:       gnome-python2 pygtk2
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Group:          Applications/Productivity
Group(zh_CN):	应用程序/生产力
BuildArch:      noarch
URL:            http://bleachbit.sourceforge.net/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
BleachBit deletes unnecessary files to free valuable disk space, maintain 
privacy, and remove junk. Rid your system of old clutter including cache, 
cookies, Internet history, localizations, logs, temporary files, and broken 
shortcuts. Designed for Linux and Windows systems, it wipes clean Adobe Reader, 
APT, Bash, Beagle, Chromium, Epiphany, Firefox, Flash, GIMP, Google Chrome, 
Google Earth, Internet Explorer, Java, KDE, OpenOffice.org, Opera, RealPlayer, 
Safari, Skype, VIM, XChat, Yum, and more.

%description -l zh_CN
清除不需要的文件，释放空间的软件。

%prep
%setup -q

%build
make -C po local 
%{__python} setup.py build

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} INSTALL="install -p" install \
 prefix=%{_prefix}

desktop-file-validate %{buildroot}/%{_datadir}/applications/bleachbit.desktop
magic_rpm_clean.sh
%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/
%{_datadir}/pixmaps/%{name}.png
%doc COPYING README


%changelog
* Tue Mar 04 2014 Liu Di <liudidi@gmail.com> - 1.0-2
- 更新到 1.0

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.9.0-2
- 为 Magic 3.0 重建

* Wed Nov 02 2011 Liu Di <liudidi@gmail.com> - 0.9.0-1
- 更新到 0.9.0

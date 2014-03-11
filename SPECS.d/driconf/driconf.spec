%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           driconf
Version:        0.9.1
Release:        11%{?dist}
Summary:        A configuration applet for the Direct Rendering Infrastructure
Summary(zh_CN.UTF-8): 直接渲染基础的配置工具

Group:          User Interface/X
Group(zh_CN.UTF-8):	用户界面/X
License:        GPLv2+
URL:            http://dri.freedesktop.org/wiki/DriConf
Source0:        http://people.freedesktop.org/~fxkuehl/driconf/driconf-%{version}.tar.gz
Patch1:         driconf-0.9.1-setup.patch
Patch2:		driconf-0.9.1-glxinfo-unicode.patch
Patch3:		driconf-0.9.1-update-toolbar-methods.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
BuildRequires:  desktop-file-utils
BuildArch:      noarch
Requires:	pygtk2
Requires:	glx-utils

%description
DRIconf is a configuration applet for the Direct Rendering Infrastructure. 
It allows customizing performance and visual quality settings of OpenGL 
drivers on a per-driver, per-screen and/or per-application level.

The settings are stored in system wide and per-user XML configuration files,
which are parsed by the OpenGL drivers on startup. 

DRIConf is written in Python with the python-gtk toolkit bindings. 

%description -l zh_CN.UTF-8
DRI是在X.org中的直接渲染基础，它可以提供3D硬件加速。
DRI驱动包含一个可以调整性能和可视质量的数字选项。DRIconf是调整这些
参数的工具。

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT --prefix=%{_prefix}
magic_rpm_clean.sh
#%find_lang driconf

cat << EOF > %{name}.desktop
[Desktop Entry]
Name=Driconf
Comment=configuration applet for the Direct Rendering Infrastructure
Exec=/usr/bin/driconf
Icon=/usr/share/driconf/driconf-icon.png
Terminal=false
Type=Application
Encoding=UTF-8
Categories=Settings;
EOF

desktop-file-install --vendor fedora \
        --dir $RPM_BUILD_ROOT/%{_datadir}/applications/ %{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

#%files -f driconf.lang
%files
%defattr(-,root,root,-)
%doc COPYING CHANGELOG README TODO
%{_bindir}/driconf
%{python_sitelib}/dri.py
%{python_sitelib}/dri.pyc
%{python_sitelib}/dri.pyo
%{python_sitelib}/driconf.py
%{python_sitelib}/driconf.pyc
%{python_sitelib}/driconf.pyo
%{python_sitelib}/driconf_commonui.py
%{python_sitelib}/driconf_commonui.pyc
%{python_sitelib}/driconf_commonui.pyo
%{python_sitelib}/driconf_complexui.py
%{python_sitelib}/driconf_complexui.pyc
%{python_sitelib}/driconf_complexui.pyo
%{python_sitelib}/driconf_simpleui.py
%{python_sitelib}/driconf_simpleui.pyc
%{python_sitelib}/driconf_simpleui.pyo
%{python_sitelib}/driconf-0.9.1-py*egg-info
%dir %{_datadir}/driconf
%{_datadir}/driconf/card.png
%{_datadir}/driconf/drilogo.jpg
%{_datadir}/driconf/screen.png
%{_datadir}/driconf/screencard.png
%{_datadir}/driconf/driconf-icon.png
%{_datadir}/applications/*.desktop

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.9.1-11
- 为 Magic 3.0 重建

* Sun Jun  8 2008 Kevin Fenzi <kevin@tummy.com> - 0.9.1-8
- Improve unicode support (fixes bug #450083)

* Tue Jan 15 2008 Kevin Fenzi <kevin@tummy.com> - 0.9.1-7
- Add egginfo file. 

* Tue Aug 21 2007 Kevin Fenzi <kevin@tummy.com> - 0.9.1-6
- Update license tag. 

* Wed Dec 20 2006 Kevin Fenzi <kevin@tummy.com> - 0.9.1-5
- Remove unneeded post/postun.

* Tue Dec 19 2006 Kevin Fenzi <kevin@tummy.com> - 0.9.1-4
- Changed desktop catigory to Settings. 

* Mon Dec 18 2006 Kevin Fenzi <kevin@tummy.com> - 0.9.1-3
- Changed pygtk2-devel BuildRequires to python-devel
- Added desktop file. 

* Sat Dec 16 2006 Kevin Fenzi <kevin@tummy.com> - 0.9.1-2
- Added Requires for pygtk2 and glx-utils

* Sat Dec 16 2006 Kevin Fenzi <kevin@tummy.com> - 0.9.1-1
- Inital fedora extras packaging

* Fri Mar 31 2005 D. Hageman <dhageman@dracken.com> 0.9.0-1
- Updated RPM spec file to handle new version

* Mon Mar 14 2005 D. Hageman <dhageman@dracken.com> 0.2.3-1
- Created the initial rpm spec file.

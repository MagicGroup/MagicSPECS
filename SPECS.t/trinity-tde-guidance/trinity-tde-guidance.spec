%{!?python_sitearch:%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif
%define tdeversion 3.5.13.2

# TDE 3.5.13 specific building variables
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_appdir %{tde_datadir}/applications

%define tde_tdeappdir %{tde_appdir}/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}

%define __arch_install_post %{nil}

Name:		trinity-tde-guidance
Summary:	A collection of system administration tools for Trinity
Version:	0.8.0svn20080103
Release:	4%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.simonzone.com/software/guidance

Prefix:    %{tde_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	kde-guidance-trinity-%{tdeversion}.tar.xz

BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-tdebase-devel >= 3.5.13.1
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires:	trinity-pykdeextensions
BuildRequires:	trinity-libpythonize0-devel
BuildRequires:	python-trinity
BuildRequires:	chrpath
BuildRequires:	gcc-c++

# SIP support
%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	python-sip
%endif
%if 0%{?suse_version}
BuildRequires:	python-sip-devel
%endif
%if 0%{?rhel} == 5
BuildRequires:	trinity-sip-devel
%endif
%if 0%{?rhel} >= 6 || 0%{?fedora}
BuildRequires:	sip-devel
%endif

# PYTHON-QT support
%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	python-qt
Requires:	python-qt
%endif
%if 0%{?rhel} == 5 || 0%{?suse_version}
BuildRequires:	trinity-PyQt-devel
Requires:	trinity-PyQt
%endif
%if 0%{?rhel} >= 6 || 0%{?fedora}
BuildRequires:	PyQt-devel
Requires:	PyQt
%endif


Requires:		python-trinity
Requires:		%{name}-backends
Requires:		python
%if 0%{?rhel} || 0%{?fedora} || 0%{?mgaversion} || 0%{?mdkversion}
Requires:		hwdata
%endif


%if "%{tde_prefix}" == "/usr"
Conflicts:	guidance-power-manager
Conflicts:	kde-guidance-powermanager
%endif

%description
Guidance currently consists of four programs designed to help you
look after your system:
 o  userconfig - User and Group administration
 o  serviceconfig - Service/daemon administration
 o  mountconfig - Disk and filesystem administration
 o  wineconfig - Wine configuration

These tools are available in Trinity Control Center, System Settings 
or can be run as standalone applications.



%package backends
Group:		Applications/Utilities
Summary:	collection of system administration tools for GNU/Linux [Trinity]
%if 0%{?rhel} || 0%{?fedora} || 0%{?mgaversion} || 0%{?mdkversion}
Requires:	hwdata
%endif
Requires:	python

%description backends
This package contains the platform neutral backends used in the
Guidance configuration tools.


%package powermanager
Group:		Applications/Utilities
Summary:	HAL based power manager applet [Trinity]
Requires:	%{name} = %{version}-%{release}

%description powermanager
A power management applet to indicate battery levels and perform hibernate or
suspend using HAL.


%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n kde-guidance-trinity-%{tdeversion}


%build
unset QTDIR; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export PYTHONPATH=%{python_sitearch}/trinity-sip:%{python_sitearch}/trinity-PyQt
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir} -I%{tde_includedir}/tde"
export CFLAGS="-L%{tde_libdir} -I%{tde_includedir} -I%{tde_includedir}/tde"
export CXXFLAGS="-L%{tde_libdir} -I%{tde_includedir} -I%{tde_includedir}/tde"
export EXTRA_MODULE_DIR="%{python_sitearch}/%{name}"
export KDEDIR=%{tde_prefix}

# Avoids 'error: byte-compiling is disabled.' on Mandriva/Mageia
export PYTHONDONTWRITEBYTECODE=

./setup.py build


%install
unset QTDIR; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export PYTHONPATH=%{python_sitearch}/trinity-sip:%{python_sitearch}/trinity-PyQt
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir} -I%{tde_includedir}/tde"
export EXTRA_MODULE_DIR="%{python_sitearch}/%{name}"

# Avoids 'error: byte-compiling is disabled.' on Mandriva/Mageia
export PYTHONDONTWRITEBYTECODE=

%__rm -rf %{buildroot}
./setup.py install \
	--prefix=%{tde_prefix} \
	--root=%{buildroot}

# Fix building directories stored inside .py files
for f in %{buildroot}%{tde_datadir}/apps/guidance/*.py; do
	%__sed -i "${f}" -e "s|%{buildroot}||g"
done

##### MAIN PACKAGE INSTALLATION 
# install icons to right place
%__mkdir_p %{buildroot}%{tde_datadir}/icons/crystalsvg/32x32/apps
%__mv -f %{buildroot}%{tde_datadir}/apps/guidance/pics/hi32-app-daemons.png \
	%{buildroot}%{tde_datadir}/icons/crystalsvg/32x32/apps/daemons.png
%__mv -f %{buildroot}%{tde_datadir}/apps/guidance/pics/kcmpartitions.png \
	%{buildroot}%{tde_datadir}/icons/crystalsvg/32x32/apps/disksfilesystems.png
%__mv -f %{buildroot}%{tde_datadir}/apps/guidance/pics/hi32-user.png \
	%{buildroot}%{tde_datadir}/icons/crystalsvg/32x32/apps/userconfig.png
%__mv -f %{buildroot}%{tde_datadir}/apps/guidance/pics/hi32-display.png \
	%{buildroot}%{tde_datadir}/icons/crystalsvg/32x32/apps/displayconfig.png
%__mv -f %{buildroot}%{tde_datadir}/apps/guidance/pics/32-wine.png \
	%{buildroot}%{tde_datadir}/icons/crystalsvg/32x32/apps/wineconfig.png
%__install -D -p -m0644 kde/wineconfig/pics/16x16/wineconfig.png \
	%{buildroot}%{tde_datadir}/icons/crystalsvg/16x16/apps/wineconfig.png

# fix binary-or-shlib-defines-rpath
chrpath -d %{buildroot}%{tde_tdelibdir}/kcm_*.so

# fix executable-not-elf-or-script
%__chmod 0644 %{buildroot}%{tde_datadir}/apps/guidance/pics/kdewinewizard.png

# move python modules in %{python_sitearch}
%__mkdir_p %{buildroot}%{python_sitearch}/%{name} 
%__mv -f %{buildroot}%{tde_datadir}/apps/guidance/*.py %{buildroot}%{python_sitearch}/%{name}

# fix the link properly
%__rm -f %{buildroot}%{tde_bindir}/*
#%__ln_s -f %{python_sitearch}/%{name}/displayconfig.py %{buildroot}%{tde_bindir}/displayconfig
%__ln_s -f %{python_sitearch}/%{name}/mountconfig.py %{buildroot}%{tde_bindir}/mountconfig
%__ln_s -f %{python_sitearch}/%{name}/serviceconfig.py %{buildroot}%{tde_bindir}/serviceconfig
%__ln_s -f %{python_sitearch}/%{name}/userconfig.py %{buildroot}%{tde_bindir}/userconfig
%__ln_s -f %{python_sitearch}/%{name}/wineconfig.py %{buildroot}%{tde_bindir}/wineconfig
%__ln_s -f %{python_sitearch}/%{name}/grubconfig.py %{buildroot}%{tde_bindir}/grubconfig

# (obsolete)  put this here since gnome people probably don't want it by default
#%__ln_s -f %{_python_sitearch}/%{name}/displayconfig-restore.py %{buildroot}%{tde_bindir}/displayconfig-restore

# fix script-not-executable
%__chmod 0755 %{buildroot}%{python_sitearch}/%{name}/fuser.py
%__chmod 0755 %{buildroot}%{python_sitearch}/%{name}/grubconfig.py

%__mv -f %{buildroot}%{tde_datadir}/applications/kde/displayconfig.desktop %{buildroot}%{tde_datadir}/applications/kde/guidance-displayconfig.desktop

##### BACKENDS INSTALLATION
# install displayconfig-hwprobe.py script
%__install -D -p -m0755 displayconfig/displayconfig-hwprobe.py \
	%{buildroot}%{python_sitearch}/%{name}/displayconfig-hwprobe.py

# The xf86misc stuff should not go under /opt/trinity bur under /usr !!!
%__mv -f %{buildroot}%{tde_libdir}/python*/site-packages/ixf86misc.so %{buildroot}%{python_sitearch}
%__mv -f %{buildroot}%{tde_libdir}/python*/site-packages/xf86misc.py* %{buildroot}%{python_sitearch}/%{name}

%if 0%{?rhel} || 0%{?fedora} || 0%{?mgaversion} || 0%{?mdkversion}
%__rm -f %{buildroot}%{tde_datadir}/apps/guidance/MonitorsDB
%__ln_s -f /usr/share/hwdata/MonitorsDB %{buildroot}%{tde_datadir}/apps/guidance/MonitorsDB
%endif


##### POWERMANAGER INSTALLATION
# install icon to right place
%__install -D -p -m0644 kde/powermanager/pics/battery-charging-100.png \
		%{buildroot}%{tde_datadir}/icons/hicolor/22x22/apps/power-manager.png
%__install -D -p -m0644 kde/powermanager/pics/*.png \
		%{buildroot}%{tde_datadir}/apps/guidance/pics/

# install desktop file
%__install -D -p -m0644 powermanager/guidance-power-manager.desktop \
		%{buildroot}%{tde_datadir}/autostart/guidance-power-manager.desktop

# copy python modules in PYSUPPORT_PATH
%__cp powermanager/guidance_power_manager_ui.py %{buildroot}%{python_sitearch}/%{name}
%__cp powermanager/notify.py %{buildroot}%{python_sitearch}/%{name}
%__cp powermanager/tooltip.py %{buildroot}%{python_sitearch}/%{name}

# generate guidance-power-manager script
cat <<EOF >%{buildroot}%{tde_bindir}/guidance-power-manager
#!/bin/sh
export PYTHONPATH=%{python_sitearch}/%{name}
%{python_sitearch}/%{name}/guidance-power-manager.py &
EOF
chmod +x %{buildroot}%{tde_bindir}/guidance-power-manager

# fix script-not-executable
chmod 0755 %{buildroot}%{python_sitearch}/%{name}/powermanage.py
chmod 0755 %{buildroot}%{python_sitearch}/%{name}/gpmhelper.py


# Replace all '#!' calls to python with /usr/bin/python
# and make them executable
for i in `find %{buildroot} -type f`; do
	sed '1s,#!.*python[^ ]*\(.*\),#! /usr/bin/python\1,' \
		$i > $i.temp;
	if cmp --quiet $i $i.temp; then
		rm -f $i.temp;
	else
		mv -f $i.temp $i;
		chmod 755 $i;
		echo "fixed interpreter: $i";
	fi;
done

# Removes useless files
find %{buildroot} -name "*.egg-info" -exec rm -f {} \;
find %{buildroot}%{tde_libdir} -name "*.a" -exec rm -f {} \;

# Removes obsolete display config manager
%__rm -f %{?buildroot}/etc/X11/Xsession.d/40guidance-displayconfig_restore
%__rm -f %{?buildroot}%{tde_tdelibdir}/kcm_displayconfig.*
%__rm -f %{?buildroot}%{python_sitearch}/%{name}/displayconfig.py
%__rm -f %{?buildroot}%{python_sitearch}/%{name}/displayconfigwidgets.py 


%clean
%__rm -rf %{buildroot}


%post
touch --no-create %{tde_datadir}/icons/crystalsvg || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/crystalsvg || :
/sbin/ldconfig || :

%postun
touch --no-create %{tde_datadir}/icons/crystalsvg || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/crystalsvg || :
/sbin/ldconfig || :

%post powermanager
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :

%postun powermanager
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :


%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING README TODO
#%{tde_bindir}/displayconfig
#%{tde_bindir}/displayconfig-restore
%{tde_bindir}/grubconfig
%{tde_bindir}/mountconfig
%{tde_bindir}/serviceconfig
%{tde_bindir}/userconfig
%{tde_bindir}/wineconfig
%attr(0644,root,root) %{tde_tdelibdir}/*.so
%attr(0644,root,root) %{tde_tdelibdir}/*.la
%{tde_datadir}/apps/guidance/
%{tde_datadir}/applications/kde/*.desktop
%{tde_datadir}/icons/crystalsvg/*/*/*.png
%{tde_datadir}/icons/crystalsvg/*/*/*.svg
%{python_sitearch}/%{name}/SMBShareSelectDialog.py*
%{python_sitearch}/%{name}/SimpleCommandRunner.py*
%{python_sitearch}/%{name}/fuser.py*
%{python_sitearch}/%{name}/fuser_ui.py*
%{python_sitearch}/%{name}/grubconfig.py*
%{python_sitearch}/%{name}/ktimerdialog.py*
%{python_sitearch}/%{name}/mountconfig.py*
%{python_sitearch}/%{name}/servertestdialog.py*
%{python_sitearch}/%{name}/serviceconfig.py*
%{python_sitearch}/%{name}/sizeview.py*
%{python_sitearch}/%{name}/unixauthdb.py*
%{python_sitearch}/%{name}/userconfig.py*
%{python_sitearch}/%{name}/wineconfig.py*
%{tde_tdedocdir}/HTML/en/guidance/

# Files from backends
%exclude %{tde_datadir}/apps/guidance/vesamodes
%exclude %{tde_datadir}/apps/guidance/extramodes
%exclude %{tde_datadir}/apps/guidance/widescreenmodes
%exclude %{tde_datadir}/apps/guidance/Cards+
%exclude %{tde_datadir}/apps/guidance/pcitable
%exclude %{tde_datadir}/apps/guidance/MonitorsDB

# Files from powermanager
%exclude %{tde_datadir}/icons/hicolor/22x22/apps/power-manager.png
%exclude %{tde_datadir}/apps/guidance/pics/ac-adapter.png
%exclude %{tde_datadir}/apps/guidance/pics/battery*.png
%exclude %{tde_datadir}/apps/guidance/pics/processor.png

%files backends
%defattr(-,root,root,-)
%{python_sitearch}/%{name}/MicroHAL.py*
%{python_sitearch}/%{name}/ScanPCI.py*
%{python_sitearch}/%{name}/infimport.py*
%{python_sitearch}/%{name}/displayconfigabstraction.py*
%{python_sitearch}/%{name}/displayconfig-hwprobe.py*
%{python_sitearch}/%{name}/displayconfig-restore.py*
%{python_sitearch}/%{name}/drivedetect.py*
%{python_sitearch}/%{name}/execwithcapture.py*
%{python_sitearch}/%{name}/wineread.py*
%{python_sitearch}/%{name}/winewrite.py*
%{python_sitearch}/%{name}/xf86misc.py*
%{python_sitearch}/%{name}/xorgconfig.py*
%{python_sitearch}/ixf86misc.so
%{tde_datadir}/apps/guidance/vesamodes
%{tde_datadir}/apps/guidance/extramodes
%{tde_datadir}/apps/guidance/widescreenmodes
%{tde_datadir}/apps/guidance/Cards+
%{tde_datadir}/apps/guidance/pcitable
%{tde_datadir}/apps/guidance/MonitorsDB



%files powermanager
%defattr(-,root,root,-)
%{tde_bindir}/guidance-power-manager
%{python_sitearch}/%{name}/MicroHAL.py*
%{python_sitearch}/%{name}/guidance-power-manager.py*
%{python_sitearch}/%{name}/powermanage.py*
%{python_sitearch}/%{name}/gpmhelper.py*
%{python_sitearch}/%{name}/powermanager_ui.py*
%{python_sitearch}/%{name}/guidance_power_manager_ui.py*
%{python_sitearch}/%{name}/notify.py*
%{python_sitearch}/%{name}/tooltip.py*
%{tde_datadir}/icons/hicolor/22x22/apps/power-manager.png
%{tde_datadir}/apps/guidance/pics/ac-adapter.png
%{tde_datadir}/apps/guidance/pics/battery*.png
%{tde_datadir}/apps/guidance/pics/processor.png
%{tde_datadir}/autostart/guidance-power-manager.desktop



%changelog
* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 0.8.0svn20080103-4
- Initial build for TDE 3.5.13.1

* Fri May 11 2012 Francois Andriot <francois.andriot@free.fr> - 0.8.0svn20080103-3
- Fix Python search dir

* Tue May 01 2012 Francois Andriot <francois.andriot@free.fr> - 0.8.0svn20080103-2
- Rebuilt for Fedora 17
- Fix post and postun
- Fix library locations

* Thu Dec 01 2011 Francois Andriot <francois.andriot@free.fr> - 0.8.0svn20080103-1
- Initial build for RHEL 5, RHEL 6, Fedora 15, Fedora 16

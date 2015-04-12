%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:		obmenu
Version:	1.0
Release:	10%{?dist}
Summary:	A graphical menu editor for Openbox
Summary(zh_CN.UTF-8): Openbox 的图形化菜单编辑器
Group:		User Interface/Desktops
Group(zh_CN.UTF-8):	用户界面/桌面
License:	GPLv2+
URL:		http://obmenu.sourceforge.net/

Source0:	http://download.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source2:	%{name}.desktop
Patch0:		%{name}-copy-default-xdg-menu.patch 

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

Requires:	pygtk2-libglade

BuildRequires:	desktop-file-utils
BuildRequires:	python-devel

%description
obmenu is a graphical menu editor for the Openbox window manager. Openbox uses
XML to store its menu preferences, and editing these by hand can quickly become
tedious; and even moreso when generating an entire menu for oneself! However,
this utility provides a convenient method of editing the menu in a graphical
interface, while not losing the powerful features of Openbox such as its
pipe menus. 

This also provides a Python module named obxml that can be used to further
script Openbox's menu system. 

%description -l zh_CN.UTF-8
Openbox 的图形化菜单编辑器。

%prep
%setup -q
%patch0 -p0


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
chmod +x %{buildroot}%{python_sitelib}/obxml.py
desktop-file-install --vendor fedora	\
	--dir %{buildroot}%{_datadir}/applications	\
	%{SOURCE2}
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING README
%{_bindir}/%{name}
%{_bindir}/obm-*
%{_datadir}/%{name}/
%{_datadir}/applications/fedora-%{name}.desktop
%{python_sitelib}/obxml.py
%{python_sitelib}/obxml.pyc
%{python_sitelib}/obxml.pyo
%{python_sitelib}/*.egg-info


%changelog
* Tue Mar 03 2015 Liu Di <liudidi@gmail.com> - 1.0-10
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.0-9
- 为 Magic 3.0 重建



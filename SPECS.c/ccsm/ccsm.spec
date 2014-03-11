%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif
%define         basever 0.9.5.92

Name:           ccsm
Version:        0.9.5.92
Release:        1%{?dist}
Summary:        Plugin and configuration tool - Compiz Fusion Project
Summary(zh_CN.UTF-8): 插件和配置工具 - Compiz Fusion 项目

Group:          User Interface/Desktops
Group(zh_CN.UTF-8):   用户界面/桌面
License:        GPLv2+
URL:            http://www.compiz.org

Source0:        http://releases.compiz.org/%{version}/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch102:       widgets_filter.patch
# libdrm is not available on these arches
ExcludeArch:    s390 s390x ppc64
BuildArch:      noarch
BuildRequires:  python-devel, gettext, desktop-file-utils, intltool
Requires:       compizconfig-python >= %{basever} , libcompizconfig >= %{basever}, compiz
Requires:       pygtk2 >= 2.10, python-sexy

%description
The Compiz Project brings 3D desktop visual effects that improve
usability of the X Window System and provide increased productivity
though plugins and themes contributed by the community giving a
rich desktop experience.

This package contains a gui configuration tool to configure Compiz
plugins and the composite window manager.

%description -l zh_CN.UTF-8
Compiz 项目为 X 窗口系统提供了一个 3D 桌面。

这个包包含了配置 Compiz 插件和复合窗口管理器的一个图形界面配置工具。

%prep
%setup -q
%patch102 -p1 -b .widgets_filter

%build
CFLAGS="$RPM_OPT_FLAGS" python setup.py build --prefix=%{_usr}

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --prefix=%{_prefix} --skip-build --root=$RPM_BUILD_ROOT
desktop-file-install --vendor="fedora" \
      --dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
      --remove-category="Compiz" \
      --delete-original \
      $RPM_BUILD_ROOT%{_datadir}/applications/ccsm.desktop
magic_rpm_clean.sh
%find_lang %{name}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING VERSION
%{_bindir}/ccsm
%{_datadir}/applications/fedora-ccsm.desktop
%dir %{_datadir}/ccsm
%{_datadir}/ccsm/*
%{_datadir}/icons/hicolor/*/apps/ccsm.*
%dir %{python_sitelib}/ccm
%{python_sitelib}/ccm/*
%{python_sitelib}/ccsm-%{version}-py?.?.egg-info


%changelog
* Fri Nov 04 2011 Liu Di <liudidi@gmail.com> - 0.9.95.2-1
- 更新到 0.9.95.2

* Mon Jun 02 2008 Liu Di <liudidi@gmail.com> - 0.7.6-1mgc
- 更新到 0.7.6

* Fri May 30 2008 Liu Di <liudidi@gmail.com> - 0.7.4-1mgc
- 更新到 0.7.4

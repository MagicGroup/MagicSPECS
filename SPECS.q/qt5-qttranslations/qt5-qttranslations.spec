
%global qt_module qttranslations

Summary: Qt5 - QtTranslations module
Summary(zh_CN.UTF-8): Qt5 - 翻译模块
Name:    qt5-%{qt_module}
Version: 5.4.1
Release: 1%{?dist}

License: LGPLv2 with exceptions or GPLv3 with exceptions and GFDL
Url:     http://qt-project.org/
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
%if 0%{?pre:1}
Source0: http://download.qt-project.org/development_releases/qt/%{majorver}/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0: http://download.qt-project.org/official_releases/qt/%{majorver}/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif

BuildArch: noarch

BuildRequires: qt5-qttools-devel >= %{version}

%description
%{summary}.

%description -l zh_CN.UTF-8
Qt5 - 翻译模块。

%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}


%build
qmake-qt5
make %{?_smp_mflags}


%install
make install INSTALL_ROOT=$RPM_BUILD_ROOT
magic_rpm_clean.sh
%find_lang %{name} --all-name --with-qt --without-mo


%files -f %{name}.lang
%doc LGPL_EXCEPTION.txt
## skip this if using %%find_lang macro
#{_qt5_translationdir}/*


%changelog
* Fri Mar 20 2015 Liu Di <liudidi@gmail.com> - 5.4.1-1
- 更新到 5.4.1

* Wed Aug 06 2014 Liu Di <liudidi@gmail.com> - 5.3.1-2
- 为 Magic 3.0 重建

* Tue Jun 17 2014 Jan Grulich <jgrulich@redhat.com> - 5.3.1-1
- 5.3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jan Grulich <jgrulich@redhat.com> 5.3.0-1
- 5.3.0

* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Thu Dec 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- 5.2.0

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.10.rc1
- 5.2.0-rc1

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.2.beta1
- 5.2.0-beta1

* Wed Oct 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.1.alpha
- 5.2.0-alpha

* Sun Sep 22 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-1
- Initial packaging

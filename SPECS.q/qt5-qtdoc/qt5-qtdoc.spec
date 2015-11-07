
%global qt_module qtdoc

Summary: Main Qt5 Reference Documentation
Summary(zh_CN.UTF-8): 主要的 Qt5 参考文档
Name:    qt5-%{qt_module}
Version: 5.5.1
Release: 2%{?dist}

License: GFDL
Url:     http://qt-project.org/
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
%if 0%{?pre:1}
Source0: http://download.qt-project.org/development_releases/qt/%{majorver}/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0: http://download.qt-project.org/official_releases/qt/%{majorver}/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif

BuildArch: noarch

BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qttools-devel

%description
QtDoc contains the main Qt Reference Documentation, which includes
overviews, Qt topics, and examples not specific to any Qt module.

%description -l zh_CN.UTF-8
主要的 Qt5 参考文档。

%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}


%build
qmake-qt5
make docs %{?_smp_mflags}


%install
make install_docs INSTALL_ROOT=%{buildroot}
magic_rpm_clean.sh

%files
%doc LGPL_EXCEPTION.txt
%{_qt5_docdir}/qtdoc.qch
%{_qt5_docdir}/qtdoc/


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 5.5.1-2
- 更新到 5.5.1

* Fri Sep 11 2015 Liu Di <liudidi@gmail.com> - 5.5.0-1
- 更新到 5.5.0

* Tue Mar 17 2015 Liu Di <liudidi@gmail.com> - 5.4.1-1
- 更新到 5.4.1

* Tue Aug 05 2014 Liu Di <liudidi@gmail.com> - 5.3.1-2
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

* Fri Dec 06 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.11.rc1
- BR: qt5-qtbase-devel

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.10.rc1
- 5.2.0-rc1

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.2.beta1
- 5.2.0-beta1

* Thu Oct 10 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.1.alpha
- 5.2.0-alpha

* Mon Sep 30 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-2
- License: GFDL

* Sun Sep 22 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-1
- Initial packaging

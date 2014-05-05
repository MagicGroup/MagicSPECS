
%global qt_module qtdoc

Summary: Main Qt5 Reference Documentation
Name:    qt5-%{qt_module}
Version: 5.2.1
Release: 1%{?dist}

License: GFDL
Url:     http://qt-project.org/
%if 0%{?pre:1}
Source0: http://download.qt-project.org/development_releases/qt/5.2/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0: http://download.qt-project.org/official_releases/qt/5.2/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif

BuildArch: noarch

BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qttools-devel

%description
QtDoc contains the main Qt Reference Documentation, which includes
overviews, Qt topics, and examples not specific to any Qt module.


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}


%build
qmake-qt5
make docs %{?_smp_mflags}


%install
make install_docs INSTALL_ROOT=%{buildroot}


%files
%doc LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt
%{_qt5_docdir}/qtdoc.qch
%{_qt5_docdir}/qtdoc/


%changelog
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

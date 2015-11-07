
%global qt_module qtwebchannel

# define to build docs, need to undef this for bootstrapping
# where qt5-qttools builds are not yet available
# only primary archs (for now), allow secondary to bootstrap
#global bootstrap 1

%if ! 0%{?bootstrap}
%ifarch %{arm} %{ix86} x86_64
%define docs 1
%endif
%endif

Summary: Qt5 - WebChannel component
Summary(zh_CN.UTF-8): Qt5 - WebChannel 组件
Name:    qt5-%{qt_module}
Version: 5.5.1
Release: 2%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
# See also http://doc.qt.io/qt-5/licensing.html
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt.io
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
%if 0%{?pre:1}
Source0: http://download.qt.io/development_releases/qt/%{majorver}/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0: http://download.qt.io/official_releases/qt/%{majorver}/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif

BuildRequires:  qt5-qtbase-devel >= %{version}
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Quick)

# Qt5WebSockets package is optional and only needed for examples
BuildRequires:  pkgconfig(Qt5WebSockets)

%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}

%description
The Qt WebChannel module provides a library for seamless integration of C++
and QML applications with HTML/JavaScript clients. Any QObject can be
published to remote clients, where its public API becomes available.

%description -l zh_CN.UTF-8
Qt5 - WebChannel 组件。

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的 API 文档
License: GFDL
Requires: %{name} = %{version}-%{release}
BuildRequires: qt5-qhelpgenerator
BuildArch: noarch
%description doc
%{summary}.
%description doc -l zh_CN.UTF-8
%{name} 的 API 文档。
%endif

%package examples
Summary: Programming examples for %{name}
Summary(zh_CN.UTF-8): %{name} 的程序样例
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.
%description examples -l zh_CN.UTF-8
%{name} 的程序样例。


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{qmake_qt5} ..

make %{?_smp_mflags}

%if 0%{?docs}
# HACK to avoid multilib conflicts in noarch content
# see also https://bugreports.qt.io/browse/QTBUG-42071
QT_HASH_SEED=0; export QT_HASH_SEED
make %{?_smp_mflags} docs
%endif
popd


%install
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}

%if 0%{?docs}
make install_docs INSTALL_ROOT=%{buildroot} -C %{_target_platform}
%endif

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LICENSE.GPL* LICENSE.LGPL*
%{_qt5_libdir}/libQt5WebChannel.so.5*
%{_qt5_archdatadir}/qml/QtWebChannel/

%files devel
%{_qt5_headerdir}/QtWebChannel/
%{_qt5_libdir}/libQt5WebChannel.so
%{_qt5_libdir}/libQt5WebChannel.prl
%dir %{_qt5_libdir}/cmake/Qt5WebChannel/
%{_qt5_libdir}/cmake/Qt5WebChannel/Qt5WebChannelConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5WebChannel.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_webchannel*.pri

%if 0%{?docs}
%files doc
%{_qt5_docdir}/%{qt_module}.qch
%{_qt5_docdir}/%{qt_module}/
%endif

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 5.5.1-2
- 更新到 5.5.1

* Thu Sep 10 2015 Liu Di <liudidi@gmail.com> - 5.5.0-4
- 为 Magic 3.0 重建

* Wed Jul 29 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-3
- -docs: BuildRequires: qt5-qhelpgenerator, standardize bootstrapping

* Thu Jul 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-2
- tighten qtbase dep (#1233829)

* Thu Jul 09 2015 Jan Grulich <jgrulich@redhat.com> - 5.5.0-1
- 5.5.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 07 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-1
- 5.4.2

* Tue Dec 23 2014 Taylor Braun-Jones <taylor.braun-jones@ge.com> - 5.4.0-1
- Initial release.

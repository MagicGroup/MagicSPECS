%define pykde4_akonadi 1
%define pyqt4_version_min 4.8.4
%define sip_version_min 4.12
%global python_ver %(%{__python} -c "import sys ; print sys.version[:3]")

Name: PyKDE4 
Version: 4.13.0
Release: 1%{?dist}
Summary: Python bindings for KDE4 
Summary(zh_CN.UTF-8): KDE4 的 Python 绑定

# http://techbase.kde.org/Policies/Licensing_Policy
License: LGPLv2+
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
URL: http://developer.kde.org/language-bindings/
Source0: http://download.kde.org/stable/%{version}/src/pykde4-%{version}.tar.xz

Patch100: pykde4-pyqt495.patch

# debian patches
Patch200: make_pykde4_respect_sip_flags.diff
Patch201: fix_kpythonpluginfactory_build.diff

# rhel patches
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  akonadi-devel
BuildRequires:  kdebase4-workspace-devel >= %{version}
## okular bindings
BuildRequires:  kde4-okular-devel >= %{version}
BuildRequires:  kdelibs4-devel >= %{version}
BuildRequires:  kdepimlibs4-devel >= %{version}
## kate bindings
BuildRequires:  kde4-kate-devel >= %{version}
BuildRequires:  python-devel
BuildRequires:  PyQt4-devel >= %{pyqt4_version_min}, sip-devel >= %{sip_version_min}
%if 0%{?python3}
BuildRequires:  python3-devel
BuildRequires:  python3-PyQt4-devel >= %{pyqt4_version_min}, python3-sip-devel >= %{sip_version_min}
%global python3_inc %(%{__python3} -c "from distutils.sysconfig import get_python_inc; print(get_python_inc(1))")
%global python3_ver %(%{__python3} -c "import sys ; print (\\"%s%s\\" % (sys.version[:3],getattr(sys,'abiflags','')))")
%global python3_pyqt4_version %(%{__python3} -c 'import PyQt4.pyqtconfig; print(PyQt4.pyqtconfig._pkg_config["pyqt_version_str"])' 2> /dev/null || echo %{pyqt4_version_min})
%endif
BuildRequires:  qscintilla-devel >= 2.4
BuildRequires:  qimageblitz-devel
BuildRequires:  soprano-devel

## FIXME/TODO
#-- The following OPTIONAL packages could NOT be located on your system.
#-- Consider installing them to enable more features from this software.
#-----------------------------------------------------------------------------
#   * Qwt5 for Qt4  <http://qwt.sourceforge.net>
#     Qwt5 libraries for Qt4
#     Needed to compile Qwt5 bindings

Requires: kdelibs4 >= %{version}
%global pyqt4_version %(%{__python} -c 'import PyQt4.pyqtconfig; print(PyQt4.pyqtconfig._pkg_config["pyqt_version_str"])' 2> /dev/null || echo %{pyqt4_version_min})
Requires: PyQt4 >= %{pyqt4_version}
%{?_sip_api:Requires: sip-api(%{_sip_api_major}) >= %{_sip_api}}
%if ! 0%{?pykde4_akonadi}
Provides: PyKDE4-akonadi%{?_isa} = %{version}-%{release}
Requires: kdepimlibs4-akonadi%{?_isa} >= %{version}
%endif

%description
%{summary}.

%package akonadi
Summary: Akonadi runtime support for PyKDE4 
Group: Development/Languages 
Requires: %{name} = %{version}-%{release}
Requires: kdepimlibs4-akonadi%{?_isa} >= %{version} 
%description akonadi 
%{summary}.

%package devel
Group:    Development/Languages
Summary:  Files needed to build PyKDE4-based applications
Requires: PyQt4-devel
Requires: %{name} = %{version}-%{release}
%if 0%{?pykde4_akonadi}
Requires: %{name}-akonadi%{?_isa} = %{version}-%{release}
%endif
%description devel
%{summary}.

%package -n python3-PyKDE4
Summary: Python 3 bindings for KDE 
Group:   Development/Languages
Requires: python3-PyQt4 >= %{python3_pyqt4_version}
%{?_sip_api:Requires: python3-sip-api(%{_sip_api_major}) >= %{_sip_api}}
%if ! 0%{?pykde4_akonadi}
Provides: python3-PyKDE4-akonadi%{?_isa} = %{version}-%{release}
Requires: kdepimlibs4-akonadi%{?_isa} >= %{version}
%endif
%description -n python3-PyKDE4
%{summary}.

%package -n python3-PyKDE4-akonadi
Summary: Akonadi runtime support for PyKDE4
Group: Development/Languages
Requires: python3-PyKDE4 = %{version}-%{release}
Requires: kdepimlibs4-akonadi%{?_isa} >= %{version}
%description -n python3-PyKDE4-akonadi
%{summary}.

%package -n python3-PyKDE4-devel
Group:    Development/Languages
Summary:  Files needed to build PyKDE4-based applications
Requires: python3-PyQt4-devel
Requires: python3-PyKDE4 = %{version}-%{release}
%if 0%{?pykde4_akonadi}
Requires: python3-PyKDE4-akonadi%{?_isa} = %{version}-%{release}
%endif
%description -n python3-PyKDE4-devel
%{summary}.


%prep
%setup -q -n pykde4-%{version}

#%patch100 -p1 -b .pyqt495
#%patch200 -p1 -b .respect_sip_flags
#%patch201 -p1 -b .kpythonpluginfactory_slots

%build
%if 0%{?python3}
mkdir -p %{_target_platform}-python3
pushd    %{_target_platform}-python3
%{cmake_kde4} \
  -DPYTHON_EXECUTABLE:PATH=%{__python3} \
  -DPython_ADDITIONAL_VERSIONS=%{python3_ver} \
  -DPYTHON_LIBRARY=%{_libdir}/libpython%{python3_ver}.so.1.0 \
  -DPYTHON_LIBRARIES=%{_libdir}/libpython%{python3_ver}.so.1.0 \
  -DPYTHON_INCLUDE_PATH=%{_includedir}/python%{python3_ver} \
  ..

make %{?_smp_mflags} -C python/
popd
%endif

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} \
  -DPYTHON_LIBRARY=%{_libdir}/libpython%{python_ver}.so.1.0 \
  -DPYTHON_LIBRARIES=%{_libdir}/libpython%{python_ver}.so.1.0 \
  -DPYTHON_INCLUDE_PATH=%{_includedir}/python%{python_ver} \
  ..
  
  make %{?_smp_mflags}
popd
 


%install
rm -rf %{buildroot}

%if 0%{?python3}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}-python3/python/

# not python3 compat yet
rm -fv %{buildroot}%{_kde4_libdir}/kde4/kpythonpluginfactory.so 

# HACK: fix multilib conflict, similar to PyQt4's http://bugzilla.redhat.com/509415
rm -fv %{buildroot}%{kde4_bindir}/pykdeuic4
mv %{buildroot}%{python3_sitearch}/PyQt4/uic/pykdeuic4.py \
   %{buildroot}%{_bindir}/python3-pykdeuic4
ln -s %{_bindir}/python3-pykdeuic4 \
      %{buildroot}%{python3_sitearch}/PyQt4/uic/pykdeuic4.py

# install pykde4 examples under correct dir
mkdir -p %{buildroot}%{_docdir}
rm -fv %{buildroot}%{_kde4_appsdir}/pykde4/examples/*.py?
mv %{buildroot}%{_kde4_appsdir}/pykde4 %{buildroot}%{_docdir}/python3-pykde4
%endif

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

magic_rpm_clean.sh

%clean
rm -rf %{buildroot}


%files 
%defattr(-,root,root,-)
%{python_sitearch}/PyKDE4/
%{python_sitearch}/PyQt4/uic/widget-plugins/kde4.py*
%{_kde4_libdir}/kde4/kpythonpluginfactory.so
%{kde4_bindir}/pykdeuic4-2.7

%if 0%{?pykde4_akonadi}
%exclude %{python_sitearch}/PyKDE4/akonadi.so
%files akonadi
%defattr(-,root,root,-)
%{python_sitearch}/PyKDE4/akonadi.so
%endif

%files devel
%defattr(-,root,root,-)
%{_kde4_bindir}/pykdeuic4
%{python_sitearch}/PyQt4/uic/pykdeuic4.py*
%{_datadir}/sip/PyKDE4/
%{kde4_appsdir}/pykde4/examples/

%if 0%{?python3}
%files -n python3-PyKDE4
%defattr(-,root,root,-)
%doc COPYING
%{python3_sitearch}/PyKDE4/
%{python3_sitearch}/PyQt4/uic/widget-plugins/kde4.py*
%dir %{_docdir}/python3-pykde4

%if 0%{?pykde4_akonadi}
%exclude %{python3_sitearch}/PyKDE4/akonadi.so
%files -n python3-PyKDE4-akonadi
%defattr(-,root,root,-)
%{python3_sitearch}/PyKDE4/akonadi.so
%endif

%files -n python3-PyKDE4-devel
%defattr(-,root,root,-)
%{_kde4_bindir}/python3-pykdeuic4
%{python3_sitearch}/PyQt4/uic/pykdeuic4.py*
%{_docdir}/python3-pykde4/examples/
%{_kde4_datadir}/python3-sip/PyKDE4/
%endif


%changelog
* Fri May 02 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 4.9.3-3
- 为 Magic 3.0 重建

* Thu Oct 18 2012 Liu Di <liudidi@gmail.com> - 4.9.2-2
- 为 Magic 3.0 重建

* Tue Jul 26 2011 Jaroslav Reznik <jreznik@redhat.com> 4.7.0-1
- 4.7.0

* Fri Jul 08 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.95-1
- 4.6.95

* Thu Jul 07 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.90-1
- first try


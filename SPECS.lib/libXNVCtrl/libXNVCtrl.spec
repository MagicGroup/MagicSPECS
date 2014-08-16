Name:           libXNVCtrl
Version:        169.12
Release:        9%{?dist}
Summary:        Library providing the NV-CONTROL API
Summary(zh_CN.UTF-8): 提供 NV 显卡控制 API 的库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        GPLv2+
URL:            ftp://download.nvidia.com/XFree86/nvidia-settings/
Source0:        ftp://download.nvidia.com/XFree86/nvidia-settings/nvidia-settings-%{version}.tar.gz
Patch0:         libXNVCtrl-imake.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  imake libX11-devel libXext-devel

%description
This packages contains the libXNVCtrl library from the nvidia-settings
application. This library provides the NV-CONTROL API for communicating with
the proprietary NVidia xorg driver. This package does not contain the
nvidia-settings tool itself as that is included with the proprietary drivers
themselves. 

%description -l zh_CN.UTF-8
提供 NV 显卡控制 API 的库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}, libX11-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n nvidia-settings-1.0
%patch0 -p1 -z .imake
pushd src/%{name}
xmkmf
#libdir doesnt get set right on sparc64 and mips64el
%ifarch sparc64 mips64el
sed -i -e 's|/usr/lib|/usr/lib64|g' Makefile
%endif
popd


%build
pushd src/%{name}
make %{?_smp_mflags} CDEBUGFLAGS="$RPM_OPT_FLAGS"
popd


%install
rm -rf $RPM_BUILD_ROOT
pushd src/%{name}
make install DESTDIR=$RPM_BUILD_ROOT INSTINCFLAGS="-p -m 644"
popd
# imake installs these under X11/extensions, but apps expect them under NVCtrl
mv $RPM_BUILD_ROOT%{_includedir}/X11/extensions \
  $RPM_BUILD_ROOT%{_includedir}/NVCtrl
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING src/%{name}/README.LIBXNVCTRL
%{_libdir}/%{name}.so.0*

%files devel
%defattr(-,root,root,-)
%doc doc/NV-CONTROL-API.txt doc/FRAMELOCK.txt
%{_includedir}/NVCtrl
%{_libdir}/%{name}.so


%changelog
* Fri Aug 08 2014 Liu Di <liudidi@gmail.com> - 169.12-9
- 为 Magic 3.0 重建

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 169.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 169.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 169.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 169.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 169.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 169.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 08 2008 Dennis Gilmore <dennis@ausil.us> 169.12-2
- make sure libdir is set right on sparc64

* Wed Mar  5 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 169.12-1
- Update to new upstream 169.12 release (talking about version inflation)

* Tue Feb 19 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0-7
- Rebase to latest upstream, which is still called 1.0 (GRRRR)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0-6
- Autorebuild for GCC 4.3

* Mon Aug 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0-5
- Update License tag for new Licensing Guidelines compliance

* Fri Jul 27 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0-4
- Add missing libXext-devel BuildRequires

* Fri Jul 27 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0-3
- Link the lib against libX11 and libXext to avoid undefined non weak symbols
  (through updated libXNVCtrl-imake.patch)

* Sun Jul 22 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0-2
- Honor optflags
- Preserve timestamps of headers when installing them

* Sun Jul 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0-1
- Initial Fedora Extras version

Name:           dumb
Version:        0.9.3
Release:        20%{?dist}
Summary:        IT, XM, S3M and MOD player library
Summary(zh_CN.UTF-8): IT, XM, S3M 和 MOD 播放器库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        zlib
URL:            http://dumb.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}-autotools.tar.gz
Source2:        license-clarification.eml
Patch0:         dumb-0.9.3-CVE-2006-3668.patch
Patch1:         dumb-0.9.3-license-clarification.patch
Patch2:         dumb-0.9.3-weak-symbols.patch
BuildRequires:  allegro-devel

%description
IT, XM, S3M and MOD player library. Mainly targeted for use with the allegro
game programming library, but it can be used without allegro. Faithful to the
original trackers, especially IT.

%description -l zh_CN.UTF-8
IT, XM, S3M 和 MOD 播放器库。主要目的是和 allegro 游戏程序库一块使用，不过可以
不用 allegro。

%package devel
Summary: Development libraries and headers for dumb
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}
Requires: allegro-devel

%description devel
The developmental files that must be installed in order to compile
applications which use dumb.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -b 01
%patch0 -p1 -z .cve-2006-3668
%patch1 -p1
%patch2 -p1
cp %{SOURCE2} .


%build
%configure
make %{?_smp_mflags} LIBS=-lm


%install
%make_install
#clean out .la and static libs
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc licence.txt release.txt readme.txt license-clarification.eml
%{_bindir}/dumb*
%{_libdir}/lib*-%{version}.so

%files devel
%doc docs/deprec.txt docs/dumb.txt docs/faq.txt docs/fnptr.txt docs/howto.txt docs/ptr.txt
%{_includedir}/*.h
%{_libdir}/libdumb.so
%{_libdir}/libaldmb.so


%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 0.9.3-20
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 0.9.3-19
- 为 Magic 3.0 重建

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 10 2013 Hans de Goede <hdegoede@redhat.com> - 0.9.3-17
- Remove no longer needed autoreconf call, %%configure from redhat-rpm-config
  >= 9.1.0-42 updates config.guess and config.sub for new architecture support

* Wed May  1 2013 Hans de Goede <hdegoede@redhat.com> - 0.9.3-16
- run autoreconf for aarch64 support (rhbz#925281)
- fix unresolved weak symbols in libaldmb

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 13 2011 Hans de Goede <hdegoede@redhat.com> - 0.9.3-12
- Rebuilt for new allegro-4.4

* Tue Mar 08 2011 Hans de Goede <hdegoede@redhat.com> - 0.9.3-11
- Fix unresolved symbols from libm in the libraries

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.3-7
- Autorebuild for GCC 4.3

* Tue Aug  7 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.9.3-6
- Clarify license after talking about it with upstream
- Include permission notice from upstream for license clarification
- Update License tag for new Licensing Guidelines compliance

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.9.3-5
- FE6 Rebuild

* Thu Jul 27 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.9.3-4
- Fix CVE-2006-3668, thanks to Debian for the patch

* Wed Mar 29 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.9.3-3
- Add Requires: allegro-devel to -devel package

* Thu Mar 16 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.9.3-2
- Drop modplug.txt from %%doc and move release.txt and readme.txt from the
 -devel package to the main package (bz 185576).

* Fri Jan 27 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.9.3-1
- Initial Fedora Extras package

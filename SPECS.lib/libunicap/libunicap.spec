%define _use_internal_dependency_generator 0
%{expand:%%define prev__find_provides %{__find_provides}}
%define __find_provides sh %{SOURCE1} %{prev__find_provides}
%{expand:%%define prev__find_requires %{__find_requires}}
%define __find_requires sh %{SOURCE1} %{prev__find_requires}

Summary:	Library to access different kinds of (video) capture devices
Summary(zh_CN.UTF-8): 访问不同类型的视频捕捉设备的库
Name:		libunicap
Version:	0.9.12
Release:	9%{?dist}
License:	GPLv2+
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:		http://www.unicap-imaging.org/
Source0:	http://www.unicap-imaging.org/downloads/%{name}-%{version}.tar.gz
Source1:	%{name}-filter.sh
Patch0:		libunicap-0.9.12-includes.patch
Patch1:		libunicap-0.9.12-memerrs.patch
Patch2:		libunicap-0.9.12-arraycmp.patch
Patch3:		libunicap-0.9.12-warnings.patch
Patch4:		libunicap-bz641623.patch
Patch5:		libunicap-bz642118.patch
Patch6:		libunicap-v4l.patch
BuildRequires:	intltool, /usr/bin/perl, perl(XML::Parser), gettext, gtk-doc >= 1.4
%ifnarch s390 s390x
BuildRequires:	libraw1394-devel >= 1.1.0
%endif
%if 0%{?rhel}%{?fedora} >= 6
BuildRequires:	libv4l-devel, libtool, automake, autoconf
%endif
Obsoletes:	unicap <= 0.9.7-1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Unicap provides a uniform interface to video capture devices. It allows
applications to use any supported video capture device via a single API.
The unicap library offers a high level of hardware abstraction while
maintaining maximum performance. Zero copy capture of video buffers is
possible for devices supporting it allowing fast video capture with low
CPU usage even on low-speed architectures.

%description -l zh_CN.UTF-8
访问不同类型的视频捕捉设备的库。

%package devel
Summary:	Development files for the unicap library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}, pkgconfig
Obsoletes:	unicap-devel <= 0.9.7-1

%description devel
The libunicap-devel package includes header files and libraries necessary
for for developing programs which use the unicap library. It contains the
API documentation of the library, too.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1 -b .includes
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

# Needed to get rid of rpath
%if 0%{?rhel}%{?fedora} >= 6
libtoolize --force
autoreconf --force --install
%endif

%build
%if 0%{?rhel}%{?fedora} >= 6
%configure --disable-rpath --enable-gtk-doc --disable-libv4l
%else
%configure --disable-rpath --enable-gtk-doc
%endif
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Don't install any static .a and libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/{,unicap2/cpi/}*.{a,la}

# Use ATTRS rather SYSFS for udev where appropriate
%if 0%{?rhel}%{?fedora} >= 6
sed -e 's/\(SYSFS\|ATTRS\)/ATTRS/g' -i $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/50-euvccam.rules
%else
sed -e 's/\(SYSFS\|ATTRS\)/SYSFS/g' -i $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/50-euvccam.rules
%endif
touch -c -r {data,$RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d}/50-euvccam.rules
magic_rpm_clean.sh
%find_lang unicap

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f unicap.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%config %{_sysconfdir}/udev/rules.d/50-euvccam.rules
%{_libdir}/%{name}.so.*
%{_libdir}/unicap2

%files devel
%defattr(-,root,root,-)
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/unicap
%{_datadir}/gtk-doc/html/%{name}

%changelog
* Fri Aug 01 2014 Liu Di <liudidi@gmail.com> - 0.9.12-9
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.9.12-8
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Liu Di <liudidi@gmail.com> - 0.9.12-7
- 为 Magic 3.0 重建

* Tue Nov 02 2010 Kamil Dudka <kdudka@redhat.com> 0.9.12-6
- fix a crasher bug introduced by libunicap-0.9.12-memerrs.patch (#647880)

* Fri Oct 29 2010 Robert Scheck <robert@fedoraproject.org> 0.9.12-5
- Use ATTRS rather SYSFS for udev where appropriate (#643729)

* Tue Oct 12 2010 Kamil Dudka <kdudka@redhat.com> 0.9.12-4
- do not use "private" as identifier in a public header (#642118)

* Sat Oct 09 2010 Kamil Dudka <kdudka@redhat.com> 0.9.12-3
- avoid SIGSEGV in v4l2_capture_start() (#641623)

* Thu Oct 07 2010 Kamil Dudka <kdudka@redhat.com> 0.9.12-2
- build the package in %%build
- fix tons of compile-time warnings
- fix some memory errors in the code

* Mon Oct 04 2010 Robert Scheck <robert@fedoraproject.org> 0.9.12-1
- Upgrade to 0.9.12 (#635377)

* Sun Feb 21 2010 Robert Scheck <robert@fedoraproject.org> 0.9.8-1
- Upgrade to 0.9.8 (#530702, #567109, #567110, #567111)
- Splitting of unicap into libunicap, libucil and libunicapgtk

* Sat Oct 24 2009 Robert Scheck <robert@fedoraproject.org> 0.9.7-1
- Upgrade to 0.9.7 (#530702)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Dan Horak <dan[at]danny.cz> 0.9.5-2
- don't require libraw1394 on s390/s390x

* Sun May 03 2009 Robert Scheck <robert@fedoraproject.org> 0.9.5-1
- Upgrade to 0.9.5

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 0.9.3-2
- Rebuild against gcc 4.4 and rpm 4.6

* Mon Oct 13 2008 Robert Scheck <robert@fedoraproject.org> 0.9.3-1
- Upgrade to 0.9.3 (#466825, thanks to Hans de Goede)
- Enabled libv4l support for the new gspca kernel driver

* Sat Aug 09 2008 Robert Scheck <robert@fedoraproject.org> 0.2.23-4
- Rebuild to get missing dependencies back (#443015, #458527)

* Tue Aug 05 2008 Robert Scheck <robert@fedoraproject.org> 0.2.23-3
- Filter the unicap plugins which overlap with libv4l libraries

* Wed Jul 22 2008 Robert Scheck <robert@fedoraproject.org> 0.2.23-2
- Rebuild for libraw1394 2.0.0

* Mon May 19 2008 Robert Scheck <robert@fedoraproject.org> 0.2.23-1
- Upgrade to 0.2.23
- Corrected packaging of cpi/*.so files (thanks to Arne Caspari)

* Sat May 17 2008 Robert Scheck <robert@fedoraproject.org> 0.2.22-1
- Upgrade to 0.2.22 (#446021)

* Sat Feb 16 2008 Robert Scheck <robert@fedoraproject.org> 0.2.19-3
- Added patch to correct libdir paths (thanks to Ralf Corsepius)

* Mon Feb 04 2008 Robert Scheck <robert@fedoraproject.org> 0.2.19-2
- Changes to match with Fedora Packaging Guidelines (#431381)

* Mon Feb 04 2008 Robert Scheck <robert@fedoraproject.org> 0.2.19-1
- Upgrade to 0.2.19
- Initial spec file for Fedora and Red Hat Enterprise Linux

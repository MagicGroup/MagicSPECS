%global debug_package %{nil}

Name:           lv2core
Version:        6.0
Release:        4%{?dist}
Summary:        Audio Plugin Standard
Summary(zh_CN.UTF-8): 音频插件标准
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        ISC
URL:            http://lv2plug.in
Source:         http://lv2plug.in/spec/lv2core-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python2

%description
LV2 is a standard for plugins and matching host applications, mainly
targeted at audio processing and generation.  

There are a large number of open source and free software synthesis
packages in use or development at this time. This API ('LV2') attempts
to give programmers the ability to write simple 'plugin' audio
processors in C/C++ and link them dynamically ('plug') into a range of
these packages ('hosts').  It should be possible for any host and any
plugin to communicate completely through this interface.

LV2 is a successor to LADSPA, created to address the limitations of
LADSPA which many hosts have outgrown.

%description -l zh_CN.UTF-8
音频插件标准。

%package        devel
Summary:        API for the LV2 Audio Plugin Standard
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}

%description    devel
lv2-devel contains the lv2.h header file.

Definitive technical documentation on LV2 plug-ins for both the host
and plug-in is contained within copious comments within the lv2.h
header file.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
./waf configure -vv --prefix=%{_prefix} --libdir=%{_libdir}
./waf -vv %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
DESTDIR=$RPM_BUILD_ROOT ./waf -vv install
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc AUTHORS COPYING NEWS README
%{_libdir}/lv2/

%files devel
%{_includedir}/lv2.h
%{_includedir}/lv2/
%{_libdir}/pkgconfig/lv2core.pc

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 6.0-4
- 为 Magic 3.0 重建

* Fri Jul 04 2014 Liu Di <liudidi@gmail.com> - 6.0-3
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 6.0-2
- 为 Magic 3.0 重建

* Sun Dec 25 2011 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 6.0-1
- Update to 6.0

* Sun Mar 27 2011 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 4.0-3
- New tarball. Upstream released another 4.0 version. *sigh*

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 02 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 4.0-1
- Update to 4.0

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 08 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 3.0-3
- Add Requires: pkgconfig to the -devel subpackage.

* Mon Mar 30 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 3.0-2
- Add BR: python

* Mon Mar 30 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 3.0-1
- Update to 3.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Anthony Green <green@redhat.com> - 2.0-4
- Fix tagging bug.

* Fri Dec 19 2008 Anthony Green <green@redhat.com> - 2.0-3
- Tweak %%files section, License, Summary and %%description.

* Mon Nov 10 2008 Anthony Green <green@redhat.com> - 2.0-2
- Don't generate a debug package.

* Tue Nov 04 2008 Anthony Green <green@redhat.com> - 2.0-1
- Upgrade

* Tue Jan 22 2008 Anthony Green <green@redhat.com> - 1.0-2
- Fix License tag.

* Mon Jan 21 2008 Anthony Green <green@redhat.com> - 1.0-1
- Upgraded source.

* Thu Mar 15 2007 Anthony Green <green@redhat.com> - 1.0-0.1.beta1
- Created.


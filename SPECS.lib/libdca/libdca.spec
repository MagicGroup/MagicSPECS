# $Id: libdca.spec,v 1.2 2009/03/29 13:23:51 thl Exp $

Summary: DTS Coherent Acoustics decoder library
Summary(zh_CN.UTF-8): DTS 相干声学解码库
Name: libdca
Version: 0.0.5
Release: 9%{?dist}
URL: http://www.videolan.org/developers/libdca.html
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source: http://download.videolan.org/pub/videolan/libdca/0.0.5/%{name}-%{version}.tar.bz2
Patch0: libdca-0.0.5-relsymlinks.patch
Patch1: libdca-0.0.5-strict-aliasing.patch
License: GPLv2+
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
libdca is a free library for decoding DTS Coherent Acoustics streams. It is
released under the terms of the GPL license. The DTS Coherent Acoustics
standard is used in a variety of applications, including DVD, DTS audio CD and
radio broadcasting.

%description -l zh_CN.UTF-8
DTS 相干声学解码库。

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Obsoletes: libdts-devel < 0.0.2-2
Provides: libdts-devel = 0.0.2-2
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Development files for %{name}.

Install %{name}-devel if you wish to develop or compile
applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package tools
Summary: Various tools for use with %{name}
Summary(zh_CN.UTF-8): 使用 %{name} 的多种工具
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体

%description tools
Various tools that use %{name}.

%description tools -l zh_CN.UTF-8
使用 %{name} 的多种工具。

%prep
%setup -q
%patch0 -p1 -b .relsymlinks
%patch1 -p1 -b .aliasing
iconv -f ISO8859-1 -t UTF-8 AUTHORS > tmp; mv tmp AUTHORS

%build
%configure --disable-static
# Get rid of the /usr/lib64 RPATH on 64bit (as of 0.0.5)
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# Force PIC as applications fail to recompile against the lib on x86_64 without
%{__make} %{?_smp_mflags} OPT_CFLAGS="$RPM_OPT_FLAGS -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/%{name}.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/%{name}.so.*

%files tools
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%doc TODO doc/%{name}.txt
%{_libdir}/pkgconfig/libd??.pc
%{_includedir}/d??.h
%{_libdir}/%{name}.so

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 0.0.5-9
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.0.5-8
- 为 Magic 3.0 重建

* Mon Jul 14 2014 Liu Di <liudidi@gmail.com> - 0.0.5-7
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.0.5-6
- 为 Magic 3.0 重建

* Thu Jan 05 2012 Liu Di <liudidi@gmail.com> - 0.0.5-5
- 为 Magic 3.0 重建

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.5-4
- rebuild for new F11 features

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.0.5-3
- rebuild

* Fri Nov  2 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.0.5-2
- Merge freshrpms spec into livna spec for rpmfusion:
- Update to latest upstream releae 0.0.5 as used by freshrpms
- Set release to 2 to be higher as both livna and freshrpms latest release
- Drop x86_64 patch (not needed since we override OPT_CFLAGS anyways)
- Drop visibility patch, this should be done upstream
- Drop upstream integrated libtool patch
- No longer regenerate the autoxxx scripts as this is no longer needed
- Port strict aliasing patch to 0.0.5 release
- Add relative symlink creation patch from freshrpms
- Update license tag in accordance with new license tag guidelines

* Sat Nov 25 2006 Dominik Mierzejewski <rpm@greysector.net> 0.0.2-3
- added patches from gentoo (shared build, strict aliasing and visibility)

* Sat Oct 28 2006 Dominik Mierzejewski <rpm@greysector.net> 0.0.2-2
- renamed to libdca
- added Obsoletes/Provides
- simplified autotools call

* Mon Aug 07 2006 Dominik Mierzejewski <rpm@greysector.net> 0.0.2-1
- stop pretending we have a newer version

* Sat Apr 16 2005 Dominik Mierzejewski <rpm@greysector.net> 0.0.3-0.20040725.1
- adapted ArkLinux specfile
- x86_64 portability patch

* Sun Jul 25 2004 Bernhard Rosenkraenzer <bero@arklinux.org> 0.0.3-0.20040725.1ark
- Force -fPIC
- Update

* Wed Jul 07 2004 Bernhard Rosenkraenzer <bero@arklinux.org> 0.0.3-0.20040707.1ark
- initial RPM

Name:          libmms
Version: 0.6.4
Release:       3%{?dist}
Summary:       Library for Microsoft Media Server (MMS) streaming protocol
Summary(zh_CN.UTF-8): 微软流媒体服务协议 (MMS) 的库
License:       LGPLv2+
Group:         System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:           http://libmms.sourceforge.net/
Source0:       http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: glib2-devel

%description
MMS is a proprietary streaming protocol used in Microsoft server products,
commonly used to stream WMV data.  You can encounter mms:// style URLs all over
the net, especially on news sites and other content-serving sites. Libmms
allows you to download content from such sites, making it easy to add MMS
support to your media applications.

%description -l zh_CN.UTF-8
微软媒体服务流协议 (MMS) 的库。

%package devel
Summary:       Development package for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:         Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:      %{name} = %{version}-%{release}, pkgconfig

%description devel
This package contains development files for %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q


%build
%configure --disable-dependency-tracking --disable-static
make %{?_smp_mflags} 


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/%{name}.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig 


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING.LIB ChangeLog README*
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 0.6.4-3
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.6.4-2
- 为 Magic 3.0 重建

* Tue Jul 22 2014 Liu Di <liudidi@gmail.com> - 0.6.4-1
- 更新到 0.6.4

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.6.2-6
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Liu Di <liudidi@gmail.com> - 0.6.2-5
- 为 Magic 3.0 重建

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.4-4
- rebuild for new F11 features

* Thu Jul 24 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4-3
- Rebuild for buildsys cflags issue

* Wed Jul 23 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4-2
- Release bump for rpmfusion build

* Fri Dec 21 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4-1
- New upstream release 0.4
- Drop all patches (all upstreamed)

* Tue Dec 11 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.3-6
- Add a patch with various fixes from CVS
- Add a patch fixing a small bug I introduced in mmsh

* Sat Dec  8 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.3-5
- Add a patch from debian adding mms seeking support
- Add various fixes to Debians seeking patch
- Add self written mmsh seeking patch
- Add patch exporting some asf header info

* Sat Sep 12 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.3-4
- Add a patch from Debian fixing another crash
- Merge freshrpms spec into livna spec for rpmfusion:
- Set release to 4 to be higher as both livna and freshrpms latest release
- Update License tag for new Licensing Guidelines compliance
- Add pkgconfig Requires to -devel package
- Include some more doc files

* Wed Mar 28 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.3-3
- Add a patch fixing a crash (livna-bz 1463)

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.3-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.3-1
- New upstream release 0.3
- This new release fixes CVS-2006-2200

* Sun Sep 24 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2-2
- Rebuild for FC-6

* Sat Jul 29 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2-1
- Minor specfile cleanups for livna submission.

* Mon Jun 12 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.2-0.gst.2
- new release

* Wed Jan 05 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.1-0.gst.1
- initial package

%global pre 21

Summary: A DSP library for telephony
Summary(zh_CN.UTF-8): 通信用的 DSP 库
Name: spandsp
Version: 0.0.6
Release: 0.7%{?pre:.pre%{pre}}%{?dist}
License: LGPLv2 and GPLv2
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.soft-switch.org/
Source: http://www.soft-switch.org/downloads/spandsp/spandsp-%{version}%{?pre:pre%{pre}}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

## upstreamable patches
# touch configure only
Patch50: spandsp-0.0.6-brackets.patch
# more upstreamable touching-configure.ac version
Patch51: spandsp-0.0.6-brackets_am.patch

BuildRequires: libtiff-devel%{?_isa}
BuildRequires: libxml2-devel%{?_isa}
BuildRequires: audiofile-devel%{?_isa}
BuildRequires: doxygen
BuildRequires: libxslt
BuildRequires: docbook-style-xsl

%description
SpanDSP is a library of DSP functions for telephony, in the 8000
sample per second world of E1s, T1s, and higher order PCM channels. It
contains low level functions, such as basic filters. It also contains
higher level functions, such as cadenced supervisory tone detection,
and a complete software FAX machine. The software has been designed to
avoid intellectual property issues, using mature techniques where all
relevant patents have expired. See the file DueDiligence for important
information about these intellectual property issues.

%description -l zh_CN.UTF-8
通信用的 DSP 库。

%package devel
Summary: SpanDSP development files
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: spandsp%{?_isa} = %{version}-%{release}
Requires: libtiff-devel

%description devel
SpanDSP development files.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package apidoc
Summary: SpanDSP API documentation
Summary(zh_CN.UTF-8): %{name} 的开发文档
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description apidoc
SpanDSP API documentation.

%description apidoc -l zh_CN.UTF-8
%{name} 的开发文档。

%prep
%setup -q

%patch50 -p1 -b .brackets

%{__sed} -i 's/\r//' ChangeLog
%{__sed} -i 's/\r//' AUTHORS
%{__sed} -i 's/\r//' DueDiligence

%build
%configure --enable-doc --disable-static --disable-rpath
make
find doc/api -type f | xargs touch -r configure

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm %{buildroot}%{_libdir}/libspandsp.la
mkdir -p %{buildroot}%{_datadir}/spandsp
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc DueDiligence ChangeLog AUTHORS COPYING NEWS README

%{_libdir}/libspandsp.so.*

%{_datadir}/spandsp

%files devel
%defattr(-,root,root,-)
%{_includedir}/spandsp.h
%{_includedir}/spandsp
%{_libdir}/libspandsp.so
%{_libdir}/pkgconfig/spandsp.pc

%files apidoc
%defattr(-,root,root,-)
%doc doc/api/html/*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Mon Sep 28 2015 Liu Di <liudidi@gmail.com> - 0.0.6-0.7.pre21
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.0.6-0.6.pre18
- 为 Magic 3.0 重建

* Tue Dec 27 2011 Rex Dieter <rdieter@fedoraproject.org> 0.0.6-0.5.pre18
- use of brackets confuses autotools (#691039)

* Wed Feb  9 2011 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.6-0.4.pre18
- 0.0.6pre18

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.6-0.3.pre17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Aug  1 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.6-0.2.pre17
- Update to 0.0.6pre17

* Tue Jul 28 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.6-0.1.pre12
- Update to 0.0.6pre12

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.5-0.3.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.5-0.2.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 30 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.5-0.1.pre4
- Update to 0.0.5pre4

* Thu Mar 20 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.10.pre18
- Update to 0.0.4pre18

* Mon Feb 11 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.9.pre16
- Rebuild for GCC 4.3

* Fri Nov 30 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.8.pre16
- Fix release version

* Fri Nov 30 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.8.pre16
- Update to 0.0.4pre16

* Fri Nov  1 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.7.pre15
- Update to 0.0.4pre15

* Fri Nov  1 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.6.pre11
- Try and fix multilib problems with generated API docs.

* Fri Oct 26 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.5.pre11
- Update to 0.0.4pre11

* Fri Sep  7 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.4.pre8
- Update to 0.0.4pre8

* Sat Aug 25 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.2.pre7
- Update to 0.0.4pre7

* Wed Aug 22 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.1.pre6
- Bump release because I forgot to upload new sources...

* Wed Aug 22 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.1.pre6
- Update to 0.0.4pre6
- Update license tag.

* Wed Aug  8 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.1.pre4
- Update to 0.0.4pre4

* Mon Jun 11 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.1.pre3
- Update to 0.0.4pre3

* Fri Apr 13 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.3-3
- Fix usage of dist macro, pointed out by dgilmore

* Mon Apr  9 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.3-2
- Update to final 0.0.3.

* Tue Mar  6 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.3-1.pre28
- Update to 0.0.3pre28

* Mon Dec 11 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.3-1.pre27
- Update to 0.0.3pre27

* Tue Nov 21 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.3-1.pre25
- Update to 0.0.3pre25

* Sat Oct  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.3-1.pre24
- Update to 0.0.3pre24
- Add dist tag.

* Thu Oct  5 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.3-1.pre23
- Update to 0.0.3pre23

* Thu Oct  5 2006 David Woodhouse <dwmw2@infradead.org> - 0.0.2-1.pre26
- Update to 0.0.2pre26

* Mon Mar  6 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.2-1.pre25
- "Downgrade" to 0.0.2pre25 - 0.0.3 does not work with Asterisk.
- Don't use dos2unix, use sed.

* Mon Nov 14 2005 Jeffrey C. Ollie <jcollie@lt16585.campus.dmacc.edu> - 0.0.3-0.3.pre6
- Update to 0.0.3pre6

* Mon Oct 24 2005 Jeffrey C. Ollie <jcollie@lt16585.campus.dmacc.edu> - 0.0.3-0.2.pre4
- Changed Source0 to Source
- Changed setup0 to setup
- Added COPYING to doc in main package.
- Removed html API docs from main package.

* Tue Oct 18 2005 Jeffrey C. Ollie <jcollie@lt16585.campus.dmacc.edu> - 0.0.3-0.1.pre4
- Initial build.


Name:		pps-tools
Version:	0
Release:	0.8.20120407git0deb9c%{?dist}
Summary:	LinuxPPS user-space tools
Summary(zh_CN.UTF-8): LinuxPPS 用户空间工具

Group:		System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
License:	GPLv2+
URL:		https://github.com/ago/pps-tools

# git clone git://github.com/ago/pps-tools; cd pps-tools
# git archive --prefix=pps-tools/ ac0aa6 | gzip > pps-tools-20120215gitac0aa6.tar.gz
Source0:	pps-tools-20120407git0deb9c.tar.xz

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
This package includes the LinuxPPS user-space tools.

%description -l zh_CN.UTF-8
LinuxPPS 用户空间工具。

%package devel
Summary: LinuxPPS PPSAPI header file
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/System
Group(zh_CN.UTF-8): 开发/库

%description devel
This package includes the header needed to compile PPSAPI (RFC-2783)
applications.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}

%build
CFLAGS="$RPM_OPT_FLAGS" make %{?_smp_mflags} 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_includedir}/sys}
install -m755 -t $RPM_BUILD_ROOT%{_bindir} ppsctl ppsfind ppstest ppswatch
install -p -m644 -t $RPM_BUILD_ROOT%{_includedir} timepps.h
ln -s ../timepps.h $RPM_BUILD_ROOT%{_includedir}/sys
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING debian/README debian/copyright
%{_bindir}/pps*

%files devel
%defattr(-,root,root,-)
%{_includedir}/timepps.h
%{_includedir}/sys/timepps.h

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0-0.8.20120407git0deb9c
- 为 Magic 3.0 重建

* Tue Aug 04 2015 Liu Di <liudidi@gmail.com> - 0-0.7.20120407git0deb9c
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0-0.6.20120215gitac0aa6
- 为 Magic 3.0 重建

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.5.20120215gitac0aa6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 01 2012 Miroslav Lichvar <mlichvar@redhat.com> 0-0.4.20120215gitac0aa6
- update to 20120215gitac0aa6

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.3.20100413git74c32c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 09 2011 Miroslav Lichvar <mlichvar@redhat.com> 0-0.2.20100413git74c32c
- include README and copyright (#692069) 
- provide also <sys/timepps.h>

* Wed Mar 30 2011 Miroslav Lichvar <mlichvar@redhat.com> 0-0.1.20100413git74c32c
- initial release

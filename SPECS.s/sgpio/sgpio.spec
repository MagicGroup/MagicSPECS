Summary: SGPIO captive backplane tool
Summary(zh_CN.UTF-8): SGPIO 专属背板工具
Name: sgpio
Version: 1.2.0.10
Release: 10%{?dist}
License: GPLv2+
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
URL: http://sources.redhat.com/lvm2/wiki/DMRAID_Eventing
Source: sgpio-1.2-0.10-src.tar.gz
# there is no official download link for the latest package
#Source: http://sources.redhat.com/lvm2/wiki/DMRAID_Eventing?action=AttachFile&do=get&target=sgpio-1.2.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Patch0: sgpio-1.2-makefile.patch
Patch1: sgpio-1.2-coverity.patch
BuildRequires: dos2unix

%description
Intel SGPIO enclosure management utility

%description -l zh_CN.UTF-8
SGPIO 专属背板工具。

%prep
%setup -q -n sgpio
%patch0 -p1 -b .makefile
%patch1 -p1
dos2unix --keepdate README
chmod a-x *

%build
#@@@ workaround for #474755 - remove with next update
make clean
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT SBIN_DIR=$RPM_BUILD_ROOT/sbin MANDIR=$RPM_BUILD_ROOT%{_mandir}
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)
%doc README
/sbin/sgpio
%{_mandir}/man1/sgpio.*

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.2.0.10-10
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.2.0.10-9
- 为 Magic 3.0 重建

* Sun Sep 27 2015 Liu Di <liudidi@gmail.com> - 1.2.0.10-8
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.2.0.10-7
- 为 Magic 3.0 重建

* Mon Feb 06 2012 Liu Di <liudidi@gmail.com> - 1.2.0.10-6
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun  1 2009  Jiri Moskovcak <jmoskovc@redhat.com> 1.2.0.10-3
- rebuild for F12

* Tue Apr 14 2009  Jiri Moskovcak <jmoskovc@redhat.com> 1.2.0.10-2
- move the EOL conversion and the removal of 
  executable bits from %%install to %%prep section

* Wed Dec 10 2008 Jiri Moskovcak <jmoskovc@redhat.com> 1.2.0_10-1
- initial Fedora release

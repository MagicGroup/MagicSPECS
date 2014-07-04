#
# Copyright (C) 2011-2012 Red Hat, Inc
#
Summary: Device-mapper thin provisioning tools
Summary(zh_CN.UTF-8):  设备映射器自动精简配置工具
Name: device-mapper-persistent-data
Version: 0.3.2
Release: 3%{?dist}
License: GPLv3+
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
URL: https://github.com/jthornber/thin-provisioning-tools
Source0: https://github.com/jthornber/thin-provisioning-tools/archive/v%{version}.tar.gz
BuildRequires: expat-devel, libstdc++-devel, boost-devel
Requires: expat

%description
thin-provisioning-tools contains dump,restore and repair tools to
manage device-mapper thin provisioning target metadata devices.

%description -l zh_CN.UTF-8
设备映射器自动精简配置工具。

%prep
%setup -q -n thin-provisioning-tools-%{version}

%build
autoreconf
%configure --enable-debug --enable-testing
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} MANDIR=%{_mandir} install
magic_rpm_clean.sh

%clean

%files
%doc COPYING 
%{_mandir}/man8/thin_dump.8.gz
%{_mandir}/man8/thin_check.8.gz
%{_mandir}/man8/thin_restore.8.gz
%{_mandir}/man8/cache_check.8.gz
%{_mandir}/man8/cache_dump.8.gz
%{_mandir}/man8/cache_repair.8.gz
%{_mandir}/man8/cache_restore.8.gz
%{_sbindir}/cache_check
%{_sbindir}/cache_dump
%{_sbindir}/cache_repair
%{_sbindir}/cache_restore
%{_sbindir}/era_check
%{_sbindir}/era_dump
%{_sbindir}/era_invalidate
%{_sbindir}/thin_dump
%{_sbindir}/thin_check
%{_sbindir}/thin_restore
%{_sbindir}/thin_metadata_size
%{_sbindir}/thin_repair
%{_sbindir}/thin_rmap
%{_datadir}/man/man8/thin_metadata_size.8.gz
%{_datadir}/man/man8/thin_repair.8.gz
%{_datadir}/man/man8/thin_rmap.8.gz

%changelog
* Fri Jul 04 2014 Liu Di <liudidi@gmail.com> - 0.3.2-3
- 更新到 0.3.2

* Wed Mar 19 2014 Liu Di <liudidi@gmail.com> - 0.2.8-3
- 更新到 0.2.8

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 19 2012 Milan Broz <mbroz@redhat.com> - 0.1.4-1
- Fix thin_check man page (add -q option).
- Install utilities in /usr/sbin.

* Tue Mar 13 2012 Milan Broz <mbroz@redhat.com> - 0.1.2-1
- New upstream version.

* Mon Mar 05 2012 Milan Broz <mbroz@redhat.com> - 0.1.1-1
- Fix quiet option.

* Fri Mar 02 2012 Milan Broz <mbroz@redhat.com> - 0.1.0-1
- New upstream version.

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-3
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Milan Broz <mbroz@redhat.com> - 0.0.1-1
- Initial version

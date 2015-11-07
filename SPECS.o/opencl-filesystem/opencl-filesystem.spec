Name:		opencl-filesystem
Version:	1.0
Release:	5%{?dist}
Summary:	OpenCL filesystem layout
Summary(zh_CN.UTF-8): OpenCL 文件系统结构

Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	Public Domain
URL:		http://www.khronos.org/registry/cl/

BuildArch:	noarch


%description
This package provides some directories required by packages which use OpenCL.

%description -l zh_CN.UTF-8
OpenCL 文件系统结构。

%prep


%install
# ICD Loader Vendor Enumeration
# http://www.khronos.org/registry/cl/extensions/khr/cl_khr_icd.txt
mkdir -p %{buildroot}/%{_sysconfdir}/OpenCL/vendors/


%files
%{_sysconfdir}/OpenCL/


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.0-5
- 为 Magic 3.0 重建

* Mon Sep 07 2015 Liu Di <liudidi@gmail.com> - 1.0-4
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 28 2013 Fabian Deutsch <fabiand@fedoraproject.org> - 1.0-1
- Initial package

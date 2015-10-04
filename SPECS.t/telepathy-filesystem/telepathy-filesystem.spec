Name:           telepathy-filesystem
Version:        0.0.2
Release:        6%{?dist}
Summary:        Telepathy filesystem layout
Summary(zh_CN.UTF-8): Telepathy 的文件系统结构

Group:          System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
License:        Public Domain
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
Requires:       filesystem


%description
This package provides some directories which are required by other
packages which comprise the Telepathy release.  

%description -l zh_CN.UTF-8
Telepathy 的文件系统结构。

%prep


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/telepathy/managers
mkdir -p $RPM_BUILD_ROOT%{_datadir}/telepathy/clients
mkdir -p $RPM_BUILD_ROOT%{_includedir}/telepathy-1.0


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%dir %{_datadir}/telepathy
%dir %{_datadir}/telepathy/managers
%dir %{_datadir}/telepathy/clients
%dir %{_includedir}/telepathy-1.0


%changelog
* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 0.0.2-6
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.0.2-5
- 为 Magic 3.0 重建

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 26 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.2-1
- Add clients dir.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jun  5 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.0.1-2
- Add telepathy-1.0 dir.

* Thu Sep 21 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.0.1-1
- Initial FE spec.


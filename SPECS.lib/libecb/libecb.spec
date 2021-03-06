%global snapshot 20130509
Name:       libecb
Version:    0.%{snapshot}
Release:    7%{?dist}
Summary:    Compiler built-ins
Summary(zh_CN.UTF-8): 编译器插件
Group:      Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:    BSD
URL:        http://software.schmorp.de/pkg/libecb
# Snapshot from CVS :pserver:anonymous@cvs.schmorp.de/schmorpforge libecb 
Source0:    %{name}-%{snapshot}.tar.xz
BuildArch:  noarch
Requires:   glibc-headers

%description
This project delivers you many GCC built-ins, attributes and a number of
generally useful low-level functions, such as popcount, expect, prefetch,
noinline, assume, unreachable and so on.

%description -l zh_CN.UTF-8
这个包提供了很多 GCC 插件和一些低级功能。

%prep
%setup -q -n %{name}-%{snapshot}

%build
# Keep empty %%build section for possible RPM hooks

%install
install -d %{buildroot}%{_includedir}
install -m 0644 -t %{buildroot}%{_includedir} *.h 
magic_rpm_clean.sh

%files
%doc Changes ecb.pod LICENSE README
%{_includedir}/*

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 0.20130509-7
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.20130509-6
- 为 Magic 3.0 重建

* Tue Jul 15 2014 Liu Di <liudidi@gmail.com> - 0.20130509-5
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.20130509-4
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20130509-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20130509-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 09 2013 Petr Pisar <ppisar@redhat.com> - 0.20130509-1
- CVS snapshot taken on 2013-05-09

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20121022-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 22 2012 Petr Pisar <ppisar@redhat.com> - 0.20121022-1
- CVS snapshot taken on 2012-10-22

* Mon Oct 08 2012 Petr Pisar <ppisar@redhat.com> - 0.20121008-1
- CVS snapshot taken on 2012-10-08
- Fix for building on big-endian systems (bug #863991)


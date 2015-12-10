Name: libfli
Version: 1.7
Release: 12%{?dist}
Summary: Library for FLI CCD Camera & Filter Wheels
Summary(zh_CN.UTF-8): FLI CCE 相机和滤光轮库

%define majorver 1

Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
# Code and LICENSE.LIB have different versions of the BSD license
# https://sourceforge.net/tracker2/?func=detail&aid=2568511&group_id=90275&atid=593019
License: BSD
URL: http://indi.sourceforge.net/index.php

Source0: http://downloads.sourceforge.net/indi/%{name}%{majorver}_%{version}.tar.gz
Patch0: libfli-suffix.patch
Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: cmake 

%description
Finger Lakes Instrument library is used by applications to control FLI 
line of CCDs and Filter wheels

%description -l zh_CN.UTF-8
FLI CCE 相机和滤光轮库。

%package devel
Summary: Libraries, includes, etc. used to develop an application with %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
%description devel
These are the header files needed to develop a %{name} application

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}%{majorver}-%{version}
%patch0 -p1

%build
%cmake
make VERBOSE=1 %{?_smp_mflags}

%install
rm -fr %{buildroot}
make install DESTDIR=%{buildroot}
magic_rpm_clean.sh

%clean
rm -fr %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE.BSD
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 1.7-12
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.7-11
- 为 Magic 3.0 重建

* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 1.7-10
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.7-9
- 为 Magic 3.0 重建

* Tue Apr 03 2012 Liu Di <liudidi@gmail.com> - 1.7-8
- 为 Magic 3.0 重建

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 06 2009 Sergio Pascual <sergiopr at fedoraproject.org> -  1.7-4
- Adding disttag

* Thu Feb 05 2009 Sergio Pascual <sergiopr at fedoraproject.org> -  1.7-3
- Description lines wrapped around
- Consistent macros 
- Redownloaded source from upstream

* Mon Jan 28 2009 Sergio Pascual <sergiopr at fedoraproject.org> -  1.7-2
- Added patch to use LIB_SUFFIX

* Mon Jan 28 2009 Sergio Pascual <sergiopr at fedoraproject.org> -  1.7-1
- First specfile version


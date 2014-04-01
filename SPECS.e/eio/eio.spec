Name:           eio
Version:	1.7.10
Release:        1%{?dist}
Summary:        Extension of ecore for parallel io operations
Summary(zh_CN.UTF-8): 并行操作的 ecore 扩展
License:        LGPLv2+ and GPLv2+
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Url:            http://enlightenment.org/
Source:         http://download.enlightenment.org/releases/%{name}-%{version}.tar.bz2
BuildRequires:  doxygen 
BuildRequires:  ecore-devel 
BuildRequires:  libeina-devel
BuildRequires:  iputils 
BuildRequires:  zlib

#RHBZ 1003692
Obsoletes: libeio < 4.18-3

%description
Enlightenment Input Output Library

%description -l zh_CN.UTF-8
Enlightement 输入输出库。

%package devel
Summary:  Development files for eio
Summary(zh_CN.UTF-8): %{name} 的开发包
License:  LGPLv2+
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files, examples, man and HTML documentation for eio package.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure                            \
            --disable-doc             \
            --disable-win32-threads   \
            --disable-notify-win32    \
            --disable-libtool-lock    \
            --disable-static          

make %{?_smp_mflags} V=1

%install
%make_install
magic_rpm_clean.sh
find %{buildroot} -name '*.la' -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README COPYING NEWS AUTHORS
%{_libdir}/libeio*so.1*


%files devel
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_libdir}/libeio.so

%changelog
* Sat Mar 29 2014 Liu Di <liudidi@gmail.com> - 1.7.10-1
- 更新到 1.7.10

* Thu Nov 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.9-1
- Update to 1.7.9

* Tue Sep 24 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-2
- Fix #1003692

* Sun Aug 18 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-1
- Bump to 1.7.8

* Fri Aug 16 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.7-3
- Disable doc building as it was causing builds to fail

* Fri Aug 16 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.7-2
- Clean up the spec file some more as devel subpackage was not installing.

* Fri Aug 16 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.7-1
- Update to 1.7.7

* Fri Jun 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.6-1
- Update to 1.7.6 and clean up spec

* Fri Dec 28 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 1.7.4-1 
- initial spec

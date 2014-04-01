Name:           embryo
Version:	1.7.10
Release:        1%{?dist}
Summary:        Shared libraries for Enlightenment
Summary(zh_CN.UTF-8): Enlightement 的共享库
License:        BSD and GPLv2+
URL:            http://www.enlightenment.org
Source0:        http://download.enlightenment.org/releases/%{name}-%{version}.tar.bz2

BuildRequires: ecore-devel
BuildRequires: eet-devel
BuildRequires: evas-devel
BuildRequires: libeina-devel

%description
Small Pawn based virtual machine and compiler.

%description -l zh_CN.UTF-8
Enlightement 的共享库。

%package devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description devel
Headers, test programs and documentation for %{name}

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --disable-static --disable-doc
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -rf {} ';'
find %{buildroot} -name '*.a' -exec rm -rf {} ';'
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING README NEWS
%{_bindir}/embryo_cc
%{_libdir}/libembryo.so.*
   
%files devel
%{_includedir}/embryo-1/Embryo.h
%{_libdir}/libembryo.so
%{_libdir}/pkgconfig/embryo.pc
%{_datadir}/embryo/include/default.inc

%changelog
* Sat Mar 29 2014 Liu Di <liudidi@gmail.com> - 1.7.10-1
- 更新到 1.7.10

* Thu Nov 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.9-1
- Update to 1.7.9 release

* Sun Aug 18 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.8-3
- Create devel subpackage and put devel files where they belong.

* Sun Aug 18 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.8-2
- Bump release version

* Sat Aug 17 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.8-1
- Update to 1.7.8 release
- Disable docs

* Sun Jul 28 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.7-1
- Update to 1.7.7 release

* Wed Jun 05 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.6-1
- Update to 1.7.6 
- Remove dbus-glib-devel from BR

* Sun Dec 30 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 1.7.4-2
- add libeina-devel as BR.  Fixed find command to be concise 

* Fri Dec 28 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 1.7.4-1
- initial spec. some changes from Terje Rosten <terje.rosten@ntnu.no> 

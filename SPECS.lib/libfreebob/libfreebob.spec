Summary:       FreeBoB firewire audio driver library
Summary(zh_CN.UTF-8): FreeBoB 火线音频驱动
Name:          libfreebob
Version:       1.0.11
Release:       13%{?dist}
License:       GPLv2+
Group:         System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source0:       http://surfnet.dl.sourceforge.net/sourceforge/freebob/libfreebob-%{version}.tar.gz
Patch1:	       libfreebob-1.0.11-includes.patch
Patch2:        libfreebob-gcc46.patch
Patch3:		libfreebob-1.0.11-gcc4.patch
URL:           http://freebob.sourceforge.net
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libavc1394-devel >= 0.5.3, libiec61883-devel, libraw1394-devel
BuildRequires: alsa-lib-devel libxml2-devel autoconf
ExcludeArch:   s390 s390x

%description
libfreebob implements a userland driver for BeBoB-based fireware audio
devices.

%description -l zh_CN.UTF-8
FreeBoB 火线音频驱动库。

%package devel
Summary: Libraries, includes etc to develop with libfreebob
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Libraries, includes etc to develop with libfreebob.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch1 -p1
%patch2 -p1 
%patch3 -p1

# Tweak libiec61883 build requirements.
perl -pi -e 's/1.1.0/1.0.0/' configure

%build
%configure --disable-static
make %{?_smp_mflags} 

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/libfreebob.pc
%{_includedir}/*

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 1.0.11-13
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.0.11-12
- 为 Magic 3.0 重建

* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 1.0.11-11
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.11-10
- 为 Magic 3.0 重建

* Sat Jan 07 2012 Liu Di <liudidi@gmail.com> - 1.0.11-9
- 为 Magic 3.0 重建


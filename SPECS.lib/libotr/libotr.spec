Summary: Off-The-Record Messaging library and toolkit
Summary(zh_CN.UTF-8): Off-The-Record (OTR) 消息库和工具
Name: libotr
Version: 4.1.0
Release: 2%{?dist}
License: GPLv2 and LGPLv2
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source0: http://otr.cypherpunks.ca/%{name}-%{version}.tar.gz
Url: http://otr.cypherpunks.ca/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides: libotr-toolkit = %{version}
Obsoletes: libotr-toolkit < %{version}
Requires: libgcrypt >= 1.2.0
Requires: pkgconfig
BuildRequires: libgcrypt-devel >= 1.2.0, libgpg-error-devel 

%description
Off-the-Record Messaging Library and Toolkit
This is a library and toolkit which implements Off-the-Record (OTR) Messaging.
OTR allows you to have private conversations over IM by providing Encryption,
Authentication, Deniability and Perfect forward secrecy.

%description -l zh_CN.UTF-8
Off-The-Record (OTR) 消息库和工具。

%package devel
Summary: Development library and include files for libotr
Summary(zh_CN.UTF-8): %name 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}, libgcrypt-devel >= 1.2.0

%description devel

The devel package contains the libotr library and the include files

%description devel -l zh_CN.UTF-8
%name 的开发包。

%prep
%setup -q

%build

%configure --with-pic --disable-rpath
make %{?_smp_mflags} all

%install
rm -rf $RPM_BUILD_ROOT
make \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBINSTDIR=%{_libdir} \
	install
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files 
%defattr(-,root,root)
%doc AUTHORS README COPYING COPYING.LIB NEWS Protocol*
%{_libdir}/libotr.so.*
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%doc ChangeLog
%{_libdir}/libotr.so
%{_libdir}/libotr.a
%{_libdir}/pkgconfig/libotr.pc
%dir %{_includedir}/libotr
%{_includedir}/libotr/*
%{_datadir}/aclocal/*


%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 4.1.0-2
- 更新到 4.1.0

* Wed Jul 23 2014 Liu Di <liudidi@gmail.com> - 4.0.0-1
- 更新到 4.0.0

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 3.2.0-6
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Liu Di <liudidi@gmail.com> - 3.2.0-5
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Liu Di <liudidi@gmail.com> - 3.2.0-4
- 为 Magic 3.0 重建



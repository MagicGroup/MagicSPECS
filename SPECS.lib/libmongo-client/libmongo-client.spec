Name:		libmongo-client
Version: 0.1.8
Release:	2%{?dist}
Summary:	Alternative C driver for MongoDB
Summary(zh_CN.UTF-8): MongoDB 可选的 C 驱动

License:	ASL 2.0
URL:		https://github.com/algernon/libmongo-client
Source0:	https://github.com/algernon/libmongo-client/archive/libmongo-client-%{version}.tar.gz
# source obtained from https://github.com/algernon/libmongo-client/tags
# tar xfz libmongo-client-0.1.6.1.tar.gz
# mv libmongo-client-libmongo-client-0.1.6.1 libmongo-client-0.1.6.1
# tar czf libmongo-client-0.1.6.1.tar.gz libmongo-client-0.1.6.1

BuildRequires: libtool
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: glib2-devel

%package devel
Summary: Development files for libmongo-client
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name}%{?_isa} = %{version}-%{release}

%package doc
Summary: Documentation for libmongo-client
Summary(zh_CN.UTF-8): %{name} 的文档
Group: Documentation
Group(zh_CN.UTF-8): 文档
%{?fedora:BuildArch: noarch}
BuildRequires: graphviz
BuildRequires: doxygen

%description
Alternative C driver for MongoDB. Libmongo-client is meant
to be a stable (API, ABI and quality alike), clean, well documented
and well tested shared library, that strives to make the most
common use cases as convenient as possible.

%description -l zh_CN.UTF-8
MongoDB 可选的 C 驱动。

%description devel
Development files (libraries and include files) for libmongo-client

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%description doc
Subpackage contains documentation for libmongo-client

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q -n %{name}-%{name}-%{version}

%build
autoreconf -i
%configure --disable-static
make %{?_smp_mflags}
make doxygen


%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
rm -f %{buildroot}/%{_libdir}/*.{a,la}
magic_rpm_clean.sh

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc LICENSE NEWS
%{_libdir}/libmongo-client.so.*


%files devel
%{_libdir}/pkgconfig/libmongo-client.pc
%{_libdir}/libmongo-client.so
%{_includedir}/mongo-client

%files doc
%doc docs/html


%changelog
* Tue Jul 22 2014 Liu Di <liudidi@gmail.com> - 0.1.8-2
- 为 Magic 3.0 重建

* Tue Jul 22 2014 Liu Di <liudidi@gmail.com> - 0.1.8-1
- 更新到 0.1.8

* Mon Nov  5 2012 Milan Bartos <mbartos@redhat.com> - 0.1.6.1-1
- update to 0.1.6.1

* Mon Oct  8 2012 Milan Bartos <mbartos@redhat.com> - 0.1.5-6
- includedir mongo-client owned by -devel subpackage

* Wed Oct  3 2012 Milan Bartos <mbartos@redhat.com> - 0.1.5-5
- added dependencies for autogen.sh

* Wed Oct  3 2012 Milan Bartos <mbartos@redhat.com> - 0.1.5-4
- changed documentation location as standalone subpackage

* Wed Oct  3 2012 Milan Bartos <mbartos@redhat.com> - 0.1.5-3
- added documentation to devel subpackage

* Tue Oct  2 2012 Milan Bartos <mbartos@redhat.com> - 0.1.5-2
- added %{?_isa} to Requires for devel subpackage

* Wed Sep 26 2012 Milan Bartos <mbartos@redhat.com> - 0.1.5-1
- initial port


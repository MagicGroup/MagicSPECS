Name:           libfabric
Version:        1.1.1
Release:        2%{?dist}
Summary:        Open Fabric Interfaces
Summary(zh_CN.UTF-8): 开放的 Fabric 接口

License:        BSD or GPLv2
URL:            http://ofiwg.github.io/libfabric/
Source0:        http://downloads.openfabrics.org/downloads/ofi/libfabric-%{version}.tar.bz2

BuildRequires:  libibverbs-devel
BuildRequires:  libnl3-devel
BuildRequires:  librdmacm-devel

%description
OpenFabrics Interfaces (OFI) is a framework focused on exporting fabric
communication services to applications.  OFI is best described as a collection
of libraries and applications used to export fabric services.  The key
components of OFI are: application interfaces, provider libraries, kernel
services, daemons, and test applications.

Libfabric is a core component of OFI.  It is the library that defines and
exports the user-space API of OFI, and is typically the only software that
applications deal with directly.  It works in conjunction with provider
libraries, which are often integrated directly into libfabric.

%description -l zh_CN.UTF-8
开放的 Fabric 接口。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q


%build
%configure --disable-static --disable-silent-rules
make %{?_smp_mflags}


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_bindir}/fi_info
%{_libdir}/*.so.1*

%files devel
%license COPYING
%doc AUTHORS README
# We knowingly share this with kernel-headers and librdmacm-devel
# https://github.com/ofiwg/libfabric/issues/1277
%{_includedir}/rdma/
%{_libdir}/*.so
%{_mandir}/man3/*.3*
%{_mandir}/man7/*.7*


%changelog
* Tue Nov 17 2015 Liu Di <liudidi@gmail.com> - 1.1.1-2
- 为 Magic 3.0 重建

* Wed Aug 26 2015 Orion Poplawski <orion@cora.nwra.com> - 1.1.0-1
- Update to 1.1.0

* Mon Jul 20 2015 Orion Poplawski <orion@cora.nwra.com> - 1.0.0-1
- Initial package

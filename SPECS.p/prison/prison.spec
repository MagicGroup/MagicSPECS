Name:           prison
Version:        1.0
Release:        5%{?dist}
Summary:        A Qt-based barcode abstraction library

Group:          System Environment/Libraries
License:        MIT
URL:            https://projects.kde.org/projects/kdesupport/prison
Source0:        ftp://ftp.kde.org/pub/kde/stable/prison/1.0/src/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cmake
BuildRequires:  libdmtx-devel
BuildRequires:  qrencode-devel
BuildRequires:  qt4-devel

%description
Prison is a Qt-based barcode abstraction layer/library that provides
an uniform access to generation of barcodes with data.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}


%prep
%setup -q


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd
make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}
make install/fast -C %{_target_platform} DESTDIR=%{buildroot}


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/libprison.so.0*

%files devel
%defattr(-,root,root,-)
%{_includedir}/prison/
%{_libdir}/libprison.so
%{_libdir}/cmake/Prison/


%changelog
* Tue Jan 08 2013 Liu Di <liudidi@gmail.com> - 1.0-5
- 为 Magic 3.0 重建

* Wed Jan 25 2012 Liu Di <liudidi@gmail.com> - 1.0-4
- 为 Magic 3.0 重建

* Wed Jun 29 2011 Rex Dieter <rdieter@fedoraproject.org> - 1.0-3
- %%files: track soname
- minor cosmetics

* Fri May 20 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.0-2
- prison is qt only library

* Fri May 20 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.0-1
- initial package

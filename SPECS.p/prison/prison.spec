Name:           prison
Version:        1.1.1
Release:        5%{?dist}
Summary:        A Qt-based barcode abstraction library
Summary(zh_CN.UTF-8): 基于 Qt 的条码抽象库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        MIT
URL:            https://projects.kde.org/projects/kdesupport/prison
Source0:        http://download.kde.org/stable/prison/%{version}/src/%{name}-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cmake
BuildRequires:  libdmtx-devel
BuildRequires:  qrencode-devel
BuildRequires:  qt4-devel

%description
Prison is a Qt-based barcode abstraction layer/library that provides
an uniform access to generation of barcodes with data.

%description -l zh_CN.UTF-8
基于 Qt 的条码抽象库。

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

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
magic_rpm_clean.sh

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
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.1.1-5
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.1.1-4
- 为 Magic 3.0 重建

* Tue Aug 04 2015 Liu Di <liudidi@gmail.com> - 1.1.1-3
- 为 Magic 3.0 重建

* Tue Aug 04 2015 Liu Di <liudidi@gmail.com> - 1.1.1-2
- 为 Magic 3.0 重建

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

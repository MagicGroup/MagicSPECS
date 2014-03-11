# No FUSE on RHEL5
%if %{?el5:1}0
%define _without_fuse 1
%endif

Name:           afpfs-ng
Version:        0.8.1
Release:        13%{?dist}
Summary:        Apple Filing Protocol client
Summary(zh_CN.UTF-8): 苹果文件协议的客户端
Group:          System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
License:        GPL+
URL:            http://alexthepuffin.googlepages.com/home
Source0:        http://downloads.sourceforge.net/afpfs-ng/%{name}-%{version}.tar.bz2
Patch0:         afpfs-ng-0.8.1-overflows.patch
Patch1:         afpfs-ng-0.8.1-pointer.patch
Patch2:		afpfs-ng-0.8.1-headers.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%{?!_without_fuse:BuildRequires: fuse-devel}
BuildRequires: libgcrypt-devel gmp-devel readline-devel


%description
A command line client to access files exported from Mac OS system via
Apple Filing Protocol.
%{?!_without_fuse:The FUSE filesystem module for AFP is in fuse-afp package}

%description -l zh_CN.UTF-8
一个通过苹果文件协议(AFP)来从 Mac OS 系统上导入访问文件的命令行客户端。
%{?!_without_fuse:AFP 的 FUSE 文件系统模块在 fuse-afp 包}

%if %{?!_without_fuse:1}0
%package -n fuse-afp
Summary:        FUSE driver for AFP filesystem
Summary(zh_CN.UTF-8): AFP 文件系统的 FUSE 驱动
Group:          System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本

%description -n fuse-afp
A FUSE file system server to access files exported from Mac OS system
via AppleTalk or TCP using Apple Filing Protocol.
The command line client for AFP is in fuse-afp package

%description -n fuse-afp -l zh_CN.UTF-8
使用苹果文件协议通过 AppleTalk 或 TCP 来从 Mac OS 系统上导入访问文件
的 FUSE 文件系统服务。
%endif


%package devel
Summary:        Development files for afpfs-ng
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}

%description devel
Library for dynamic linking and header files of afpfs-ng.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。

%prep
%setup -q
%patch0 -p1 -b .overflows
%patch1 -p1 -b .pointer
%patch2 -p1

%build
# make would rebuild the autoconf infrastructure due to the following:
# Prerequisite `configure.ac' is newer than target `Makefile.in'.
# Prerequisite `aclocal.m4' is newer than target `Makefile.in'.
# Prerequisite `configure.ac' is newer than target `aclocal.m4'.
touch --reference aclocal.m4 configure.ac Makefile.in

%configure %{?_without_fuse:--disable-fuse} --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}/afpfs-ng
cp -p include/* $RPM_BUILD_ROOT%{_includedir}/afpfs-ng
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/afpcmd
%{_bindir}/afpgetstatus
%{_mandir}/man1/afpcmd.1*
%{_mandir}/man1/afpgetstatus.1*
%{_libdir}/*.so.*
%exclude %{_libdir}/*.la
%doc COPYING AUTHORS ChangeLog docs/README docs/performance docs/FEATURES.txt docs/REPORTING-BUGS.txt


%if %{?!_without_fuse:1}0
%files -n fuse-afp
%defattr(-,root,root,-)
%{_bindir}/afp_client
%{_bindir}/afpfs
%{_bindir}/afpfsd
%{_bindir}/mount_afp
%{_mandir}/man1/afp_client.1*
%{_mandir}/man1/afpfsd.1*
%{_mandir}/man1/mount_afp.1*
%doc COPYING AUTHORS ChangeLog
%endif


%files devel
%defattr(-,root,root,-)
%{_includedir}/afpfs-ng
%{_libdir}/*.so


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.8.1-12.3
- 为 Magic 3.0 重建

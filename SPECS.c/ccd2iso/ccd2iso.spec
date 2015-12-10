%define name ccd2iso
%define version 0.3
%define release 5%{?dist}

Summary: CloneCD image to ISO image file converter
Summary(zh_CN.UTF-8): CloneCD 镜像到 ISO 镜像的转换器
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://downloads.sourceforge.net/project/ccd2iso/ccd2iso/ccd2iso-0.3/%{name}-%{version}.tar.gz
License: GPLv2+
Group: Applications/Archiving
Group(zh_CN.UTF-8): 应用程序/归档
# Not yet real page
Url: http://sourceforge.net/projects/ccd2iso/
BuildRoot: %{_tmppath}/%{name}-buildroot

%description
CloneCD image to ISO image file converter

Easy... normally you would have 3 file from CloneCD image, they are .ccd, .img, 
and .sub, just type:

ccd2iso <.img filename> <.iso filename>

%description -l zh_CN.UTF-8
CloneCD 镜像到 ISO 镜像的转换器

%prep
%setup -q -n %name-%version
chmod a-x src/*.[ch]

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README INSTALL AUTHORS
%_bindir/ccd2iso

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 0.3-5
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.3-4
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.3-3
- 为 Magic 3.0 重建



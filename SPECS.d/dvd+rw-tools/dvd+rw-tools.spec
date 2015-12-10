Summary:	Toolchain to master DVD+RW/+R media
Summary(zh_CN.UTF-8): 管理 DVD+RW/+R 媒体的工具链
Name:		dvd+rw-tools
Version:	7.1
Release:	6%{?dist}
License:	GPLv2
Group:		Applications/Multimedia
Group(zh_CN.UTF-8): 	应用程序/多媒体
Source:		http://fy.chalmers.se/~appro/linux/DVD+RW/tools/dvd+rw-tools-%{version}.tar.gz
Source1:	index.html
Patch1:		dvd+rw-tools-7.0.manpatch
Patch2:		dvd+rw-tools-7.0-wexit.patch
Patch3:		dvd+rw-tools-7.0-glibc2.6.90.patch
Patch4: 	dvd+rw-tools-7.0-reload.patch
Patch5: 	dvd+rw-tools-7.0-wctomb.patch
URL:		http://fy.chalmers.se/~appro/linux/DVD+RW/
Requires:	mkisofs >= 2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	kernel-headers m4

%description
Collection of tools to master DVD+RW/+R media. For further
information see http://fy.chalmers.se/~appro/linux/DVD+RW/.

%description -l zh_CN.UTF-8
管理 DVD+RW/+R 媒体的工具集合。更多的信息可以访问：
http://fy.chalmers.se/~appro/linux/DVD+RW/。

%prep
%setup -q
%patch1 -p1 -b .manpatch
%patch2 -p1 -b .wexit
%patch3 -p1 -b .glibc2.6.90
%patch4 -p1 -b .reload
%patch5 -p0 -b .wctomb
install -m 644 %{SOURCE1} index.html

%build
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
make WARN="-DDEFAULT_BUF_SIZE_MB=16 -DRLIMIT_MEMLOCK" %{?_smp_mflags}

%install
rm -rf %{buildroot}
# make install DESTDIR= does not work here
%makeinstall

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc index.html LICENSE
%{_bindir}/*
%{_mandir}/man1/growisofs.1*

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 7.1-6
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 7.1-5
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 7.1-4
- 为 Magic 3.0 重建



%define htmldir %{_docdir}/liblognorm/html

Name:		liblognorm
Version:	1.1.2
Release:	3%{?dist}
Summary:	Fast samples-based log normalization library
Summary(zh_CN.UTF-8): 基于快速样本的日志归一库

License:	LGPLv2+
URL:		http://www.liblognorm.com
Source0:	http://www.liblognorm.com/download/files/download/%{name}-%{version}.tar.gz

BuildRequires:	libestr-devel, libee-devel, chrpath

%description
Briefly described, liblognorm is a tool to normalize log data. 

People who need to take a look at logs often have a common problem. Logs from
different machines (from different vendors) usually have different formats for 
their logs. Even if it is the same type of log (e.g. from firewalls), the log 
entries are so different, that it is pretty hard to read these. This is where
liblognorm comes into the game. With this tool you can normalize all your logs.
All you need is liblognorm and its dependencies and a sample database that fits
the logs you want to normalize.

%description -l zh_CN.UTF-8
基于快速样本的日志归一库。

%package devel
Summary:	Development tools for programs using liblognorm library
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	libee-devel%{?_isa} libestr-devel%{?_isa}

%description devel
The liblognorm-devel package includes header files, libraries necessary for
developing programs which use liblognorm library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary: HTML documentation for liblognorm
Summary(zh_CN.UTF-8): %{name} 的文档
Group: Documentation
Group(zh_CN.UTF-8): 文档
BuildRequires: python-sphinx

%description doc
This sub-package contains documentation for liblognorm in a HTML form.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%package utils
Summary:	Lognormalizer utility for normalizing log files
Summary(zh_CN.UTF-8): %{name} 的工具
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description utils
The lognormalizer is the core of liblognorm, it is a utility for normalizing
log files.

%description utils -l zh_CN.UTF-8
%{name} 的工具。

%prep
%setup -q

%build
%configure \
	--docdir=%{htmldir} \
	--enable-docs \
	--enable-regexp \
V=1 make

%install
make install INSTALL="install -p" DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.{a,la}
chrpath -d %{buildroot}%{_bindir}/lognormalizer
chrpath -d %{buildroot}%{_libdir}/liblognorm.so
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/lib*.so.*

%files devel
%{_libdir}/lib*.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc

%files doc
%doc %{htmldir}

%files utils
%{_bindir}/lognormalizer


%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 1.1.2-3
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.1.2-2
- 为 Magic 3.0 重建

* Fri Sep 18 2015 Liu Di <liudidi@gmail.com> - 1.1.2-1
- 更新到 1.1.2

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 1.0.1-2
- 为 Magic 3.0 重建

* Fri Oct 05 2012 mdarade <mdarade@redhat.com> - 0.3.4-4
- Modified description of main & util package 

* Thu Sep 20 2012 Mahaveer Darade <mdarade@redhat.com> - 0.3.4-3
- Renamed normalizer binary to lognormalizer
- Updated pc file to exclude lee and lestr

* Mon Aug 27 2012 mdarade <mdarade@redhat.com> - 0.3.4-2
- Updated BuildRequires to contain libestr-devel

* Wed Aug  1 2012 Milan Bartos <mbartos@redhat.com> - 0.3.4-1
- initial port

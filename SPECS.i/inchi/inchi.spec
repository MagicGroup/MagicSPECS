%define inchi_so_ver 1.03.00
%define url_ver 1.04

Summary: The IUPAC International Chemical Identifier library
Summary(zh_CN.UTF-8): IUPAC 国际化学标识库
Name: inchi
Version: 1.0.4
Release: 4%{?dist}
URL: http://www.inchi-trust.org
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Source0: http://www.inchi-trust.org/sites/default/files/%{name}-%{url_ver}/INCHI-1-API.zip
Source1: http://www.inchi-trust.org/sites/default/files/%{name}-%{url_ver}/INCHI-1-DOC.zip 
Patch0: %{name}-rpm.patch
License: LGPLv2+
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The IUPAC International Chemical Identifier (InChITM) is a non-proprietary
identifier for chemical substances that can be used in printed and
electronic data sources thus enabling easier linking of diverse data
compilations. It was developed under IUPAC Project 2000-025-1-800 during
the period 2000-2004. Details of the project and the history of its
progress are available from the project web site.

%description -l zh_CN.UTF-8
IUPAC 国际化学标识库。

%package devel
Summary: Development headers for the InChI library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
The inchi-devel package includes the header files and libraries
necessary for developing programs using the InChI library.

If you are going to develop programs which will use this library
you should install inchi-devel.  You'll also need to have the
inchi package installed.

%description -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary: Documentation for the InChI library
Summary(zh_CN.UTF-8): %{name} 的文档
Group: Documentation
Group(zh_CN.UTF-8): 文档
Requires: %{name} = %{version}-%{release}

%description doc
The inchi-doc package contains user documentation for the InChI software
and InChI library API reference for developers.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q -n INCHI-1-API -a 1
%patch0 -p1 -b .r
rm INCHI_API/gcc_so_makefile/result/{libinchi,inchi}*

%build
pushd INCHI_API/gcc_so_makefile
%{__make} ISLINUX=1 OPTFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/inchi}
install -p INCHI_API/gcc_so_makefile/result/libinchi.so.%{inchi_so_ver} $RPM_BUILD_ROOT%{_libdir}
ln -s libinchi.so.%{inchi_so_ver} $RPM_BUILD_ROOT%{_libdir}/libinchi.so.1
ln -s libinchi.so.1 $RPM_BUILD_ROOT%{_libdir}/libinchi.so
sed -i 's/\r//' INCHI_API/inchi_dll/inchi_api.h
install -pm644 INCHI_API/inchi_dll/inchi_api.h $RPM_BUILD_ROOT%{_includedir}/inchi
sed -i 's/\r//' LICENSE readme.txt
magic_rpm_clean.sh

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir} 

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE readme.txt
%{_libdir}/libinchi.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/inchi
%{_libdir}/libinchi.so

%files doc
%defattr(-,root,root,-)
%doc INCHI-1-DOC/*

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.0.4-4
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.4-3
- 为 Magic 3.0 重建

* Wed Oct 31 2012 Liu Di <liudidi@gmail.com> - 1.0.4-2
- 为 Magic 3.0 重建

* Wed Nov 02 2011 Liu Di <liudidi@gmail.com> - 1.0.4-1
- 更新到 1.0.4

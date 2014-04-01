Summary:	A C++ port of Lucene
Summary(zh_CN.UTF-8): Lucene 的 C++ 移植
Name:		clucene
Version:	2.3.3.4
Release:	5%{?dist}
License:	LGPLv2+ or ASL 2.0
Group:		Development/System
Group(zh_CN.UTF-8): 开发/系统
URL:		http://www.sourceforge.net/projects/clucene
Source0:	http://downloads.sourceforge.net/clucene/clucene-core-2.3.3.4.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	automake gawk cmake zlib-devel boost-devel

%description
CLucene is a C++ port of the popular Apache Lucene search engine
(http://lucene.apache.org/java). 
CLucene aims to be a high-speed alternative to Java Lucene, its API is very
similar to that of the Java version. CLucene has recently been brought up to
date with Lucene 2.3.2. It contains most of the same functionality as the Java version.

%description -l zh_CN.UTF-8
这是一个流行的 Apache Lucene 搜索引擎 (http://lucene.apache.org/java) 的
C++ 移植版本。

%package core
Summary:	Core clucene module
Summary(zh_CN.UTF-8): %{name} 的核心模块
Group:		Development/System
Group(zh_CN.UTF-8): 开发/系统
Provides:	clucene
#Requires: %{name} = %{version}-%{release}

%description core
The core clucene module

%description core -l zh_CN.UTF-8
%{name} 的核心模块。

%package core-devel
Summary:	Headers for developing programs that will use %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name}-core = %{version}-%{release}

%description core-devel
This package contains the static libraries and header files needed for
developing with clucene

%description core-devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -n %{name}-core-%{version}

%build
mkdir fedora
cd fedora
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export FFLAGS="%{optflags}"
%ifarch x86_64 ppc64 mips64el
%define lib_suffix 64
%else
%define lib_suffix %{nil}
%endif
cmake	-DCMAKE_INSTALL_PREFIX=%{_prefix}				\
	-DLIB_DESTINATION=%{_libdir}  -DLIB_SUFFIX=%{lib_suffix}	\
	-DLUCENE_SYS_INCLUDES=%{_libdir}				\
	..
make VERBOSE=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}
cd fedora
make DESTDIR=%{buildroot} install

rm -rf %{buildroot}%{_libdir}/CLuceneConfig.cmake
magic_rpm_clean.sh

%check
cd fedora
make cl_test
make test

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files core
%defattr(-, root, root, -)
%doc APACHE.license AUTHORS ChangeLog COPYING LGPL.license README
%{_libdir}/libclucene*.so.*

%files core-devel
%defattr(-, root, root, -)
%dir %{_includedir}/CLucene
%dir %{_libdir}/CLucene
%{_includedir}/CLucene/*
%{_includedir}/CLucene.h
%{_libdir}/libclucene*.so
%{_libdir}/CLucene/clucene-config.h
%{_libdir}/CLucene/CLuceneConfig.cmake
%{_libdir}/pkgconfig/libclucene-core.pc

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 2.3.3.4-4
- 为 Magic 3.0 重建

* Wed Oct 10 2012 Liu Di <liudidi@gmail.com> - 2.3.3.4-3
- 为 Magic 3.0 重建

* Thu Jun 02 2011 Deji Akingunola <dakingun@gmail.com> - 2.3.3.4-1
- Update to version 2.3.3.4

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.21b-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 08 2010 Deji Akingunola <dakingun@gmail.com> 0.9.21b-2
- Include the license text in the -core subpackage.

* Sun Jun 06 2010 Robert Scheck <robert@fedoraproject.org> 0.9.21b-1
- Update to 0.9.21b

* Wed Nov 04 2009 Dennis Gilmore <dennis@ausil.us> - 0.9.21-5
- disable 'make check on sparc64 along with ppc64 and s390x

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 14 2009 Karsten Hopp <karsten@redhat.com> 0.9.21-3
- bypass 'make check' on s390x, similar to ppc64

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 27 2008 Deji Akingunola <dakingun@gmail.com> - 0.9.21-1
- Update to version 0.9.21

* Sun Feb 10 2008 Deji Akingunola <dakingun@gmail.com> - 0.9.20-4
- Rebuild for gcc43

* Wed Oct 25 2007 Deji Akingunola <dakingun@gmail.com> - 0.9.20-3
- Fix a typo in the License field

* Wed Oct 25 2007 Deji Akingunola <dakingun@gmail.com> - 0.9.20-2
- Fix multiarch conflicts (BZ #340891)
- Bypass 'make check' for ppc64, its failing two tests there

* Tue Aug 21 2007 Deji Akingunola <dakingun@gmail.com> - 0.9.20-1
- Update to version 0.9.20

* Sat Aug 11 2007 Deji Akingunola <dakingun@gmail.com> - 0.9.19-1
- Latest release update

* Fri Aug 03 2007 Deji Akingunola <dakingun@gmail.com> - 0.9.16a-2
- License tag update

* Thu Feb 22 2007 Deji Akingunola <dakingun@gmail.com> - 0.9.16a-2
- Add -contrib subpackage 

* Thu Dec 07 2006 Deji Akingunola <dakingun@gmail.com> - 0.9.16a-1
- Update to latest stable release 
- Run make check during build

* Mon Nov 20 2006 Deji Akingunola <dakingun@gmail.com> - 0.9.15-3
- Don't package APACHE.license since we've LGPL instead 
- Package documentation in devel subpackage

* Mon Nov 13 2006 Deji Akingunola <dakingun@gmail.com> - 0.9.15-2
- Fix a bunch of issues with the spec (#215258)
- Moved the header file away from lib dir

* Sat Nov 04 2006 Deji Akingunola <dakingun@gmail.com> - 0.9.15-1
- Initial packaging for Fedora Extras

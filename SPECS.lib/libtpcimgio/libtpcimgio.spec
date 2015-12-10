Name:           libtpcimgio
Version: 2.1.8
Release: 4%{?dist}
Summary:        Turku PET Centre for image file input and output procedures
Summary(zh_CN.UTF-8): 图像文件的输入和输出库 (TPC)

License:        LGPLv2+
URL:            http://www.turkupetcentre.net/software/libdoc/%{name}/index.html
%define ver %(echo %{version} | sed -e 's/\\./_/g')
Source0:        http://www.turkupetcentre.net/software/libsrc/%{name}_%{ver}_src.zip
Patch0:         %{name}-add-header.patch
Patch1:         %{name}-shared.patch
Patch2:		libtpcimgio-fixheader.patch
BuildRequires:  libtpcmisc-devel
BuildRequires:  doxygen dos2unix
BuildRequires:  graphviz


%description
The libtpcimgio library is a collection of commonly used C files 
in Turku PET Centre for image file input and output procedures. 
Libtpcimgio library supports Analyze 7.5, Ecat 6.x, Ecat 7.x and 
partly interfile formats.

%description -l zh_CN.UTF-8
图像文件的输入和输出库 (TPC)。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        static
Summary:        Static libraries for %{name}
Summary(zh_CN.UTF-8): %{name} 的静态库

%description    static
This package contains static libraries for %{name}.

%description static -l zh_CN.UTF-8
%{name} 的静态库。

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1 -b .shared
%patch2 -p1
sed -i "/^CFLAGS/d" Makefile

# Fix encodings and line endings.
dos2unix -k History Readme TODO
iconv -f ISO_8859-1 -t utf8 -o History.new History && mv -f History.new History


%build
# c99 standard since they use declarations in the for loops
# includedirs since it doesn't find them on their own
# the _XOPEN_SOURCE for timezone declaration
# undefine STRICT_ANSI since c99 sets it, and it conflicts with the strings.h declaration
# PIC for shared objects

export CFLAGS="%{optflags} -std=c99 -Iinclude/ -I%{_includedir}/libtpcmisc/ -D_XOPEN_SOURCE -U__STRICT_ANSI__ -fPIC -DPIC"
export CXXFLAGS="%{optflags} -fPIC -DPIC"
make %{?_smp_mflags} 

# Build doxygen documentation
mkdir doc
( cat Doxyfile ; echo "OUTPUT_DIRECTORY=./doc" ) | doxygen -


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_includedir}/%{name}
install -d $RPM_BUILD_ROOT%{_bindir}

install -p -m 0755 %{name} -t $RPM_BUILD_ROOT%{_bindir}/
install -p -m 0644 %{name}.a -t $RPM_BUILD_ROOT%{_libdir}/
install -p -m 0755 %{name}.so.0.0.0 -t $RPM_BUILD_ROOT%{_libdir}/
install -p -m 0644 include/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/

pushd $RPM_BUILD_ROOT%{_libdir}/
ln -s %{name}.so.0.0.0 %{name}.so.0
ln -s %{name}.so.0.0.0 %{name}.so
popd
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc History Readme TODO
%{_bindir}/%{name}
%{_libdir}/%{name}.so.*

%files devel
%doc doc/%{name}/*
%{_libdir}/%{name}.so
%{_includedir}/*

%files static
%{_libdir}/%{name}.a

%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 2.1.8-4
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 2.1.8-3
- 为 Magic 3.0 重建

* Fri Aug 01 2014 Liu Di <liudidi@gmail.com> - 2.1.8-2
- 为 Magic 3.0 重建

* Fri Aug 01 2014 Liu Di <liudidi@gmail.com> - 2.1.8-1
- 更新到 2.1.8

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 06 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.5.10-5
- spec bump for gcc 4.7 rebuild

* Mon Aug 08 2011 Tom Callaway <spot@fedoraproject.org> - 1.5.10-4
- compile with -fPIC so that xmedcon can use it in shared libs later
- build shared libs, put static libs in separate subpackage

* Mon Aug 01 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.5.10-3
- Add graphviz to BR

* Sun Jul 31 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.5.10-2
- Changes that Richard made:
- Add more documentation
- Fix line endings and encoding
- Add architecture specific requires
- https://bugzilla.redhat.com/show_bug.cgi?id=714327#c1

* Fri Jun 17 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.5.10-1
- initial rpm build

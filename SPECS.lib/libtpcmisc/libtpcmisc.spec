Name:           libtpcmisc
Version: 2.2.5
Release: 2%{?dist}
Summary:        Miscellaneous PET functions
Summary(zh_CN.UTF-8): PET 的杂项函数

License:        LGPLv2+
URL:            http://www.turkupetcentre.net/software/libdoc/%{name}/index.html
%define ver %(echo %{version} | sed -e 's/\\./_/g')
Source0:        http://www.turkupetcentre.net/software/libsrc/%{name}_%{ver}_src.zip
Patch0:         %{name}-shared.patch

BuildRequires:  doxygen dos2unix graphviz


%description
Former libpet, the common PET C library, has been divided up in 
smaller sub-libraries that each handle a specific task. 
This library includes miscellaneous functions utilized in PET 
data processing.

%description -l zh_CN.UTF-8
PET 的杂项函数。

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

%description	static
This package contains static libraries for %{name}.

%description static -l zh_CN.UTF-8
%{name} 的静态库。

%prep
%setup -q -n %{name}
%patch0 -p1 -b .shared
sed -i "/^CFLAGS/d" Makefile

# Fix encodings and line endings.
dos2unix -k History Readme
iconv -f ISO_8859-1 -t utf8 -o History.new History && mv -f History.new History


%build
# c99 standard since they use declarations in the for loops
export CFLAGS="%{optflags} -std=c99 -fPIC -DPIC -D_POSIX_C_SOURCE=200112L"
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

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc History Readme
%{_bindir}/%{name}
%{_libdir}/%{name}.so.*

%files devel
%doc doc/%{name}/*
%{_libdir}/%{name}.so
%{_includedir}/*

%files static
%{_libdir}/%{name}.a

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 2.2.5-2
- 为 Magic 3.0 重建

* Fri Aug 01 2014 Liu Di <liudidi@gmail.com> - 2.2.5-1
- 更新到 2.2.5

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 06 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.4.8-5
- spec bump for gcc 4.7 rebuild

* Mon Aug 08 2011 Tom Callaway <spot@fedoraproject.org> - 1.4.8-4
- build shared libraries with PIC
- put static lib in subpackage

* Mon Aug 01 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.4.8-3
- Add graphviz to BR

* Sun Jul 31 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.4.8-2
- Changes that Richard made:
- Add more documentation
- Fix line endings and encoding
- Add architecture specific requires
- https://bugzilla.redhat.com/show_bug.cgi?id=714326#c2

* Fri Jun 17 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.4.8-1
- initial rpm build

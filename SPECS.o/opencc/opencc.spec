Name:       opencc
Version:    0.2.0
Release:    4%{?dist}
Summary:    Libraries for Simplified-Traditional Chinese Conversion
License:    ASL 2.0
Group:      System Environment/Libraries
URL:        http://code.google.com/p/open-chinese-convert/
Source0:    http://open-chinese-convert.googlecode.com/files/%{name}-%{version}.tar.gz

BuildRequires:  gettext
BuildRequires:  cmake

%description
OpenCC is a library for converting characters and phrases between
Traditional Chinese and Simplified Chinese.


%package tools
Summary:    Command line tools for OpenCC
Group:      Applications/Text
Requires:   %{name} = %{version}-%{release}

%description tools
Command line tools for OpenCC, including tools for conversion via CLI and
for building dictionaries.


%package devel
Summary:    Development files for OpenCC
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q

%build
%cmake . -DENABLE_GETTEXT:BOOL=ON -DCMAKE_INSTALL_LIBDIR=%{_libdir}
make VERBOSE=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%check
ctest

#%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

#%files -f %{name}.lang
%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/lib*.so.*
%{_datadir}/opencc/
%{_datadir}/locale/*

%files tools
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/man/man1/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.2.0-4
- 为 Magic 3.0 重建

* Thu Jan 19 2012 Liu Di <liudidi@gmail.com> - 0.2.0-3
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 25 2010 BYVoid <byvoid.kcp@gmail.com> - 0.2.0-1
- Upstream release.
- Use CMake instead of autotools.

* Wed Sep 29 2010 jkeating - 0.1.2-2
- Rebuilt for gcc bug 634757

* Fri Sep 17 2010 BYVoid <byvoid.kcp@gmail.com> - 0.1.2-1
- Upstream release.

* Thu Aug 12 2010 BYVoid <byvoid.kcp@gmail.com> - 0.1.1-1
- Upstream release.

* Thu Jul 29 2010 BYVoid <byvoid.kcp@gmail.com> - 0.1.0-1
- Upstream release.

* Fri Jul 16 2010 BYVoid <byvoid.kcp@gmail.com> - 0.0.4-1
- Initial release of RPM.


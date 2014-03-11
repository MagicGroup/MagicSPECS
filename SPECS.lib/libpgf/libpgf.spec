Name:           libpgf
Version:        6.11.42
Release:        2%{?dist}
Summary:        PGF (Progressive Graphics File) library

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.libpgf.org
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}-src.zip

BuildRequires:  doxygen
BuildRequires:  libtool

%description
libPGF contains an implementation of the Progressive Graphics File (PGF)
which is a new image file format, that is based on a discrete, fast
wavelet transform with progressive coding features. PGF can be used
for lossless and lossy compression.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}

sed -i 's|$(DESTDIR)$(datadir)/doc/$(DOC_MODULE)|$(RPM_BUILD_DIR)/libpgf|g' doc/Makefile.am


%build
sh autogen.sh

%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING README
%{_libdir}/libpgf.so.4*

%files devel
%doc html
%{_includedir}/%{name}
%{_libdir}/libpgf.so
%{_libdir}/pkgconfig/libpgf.pc
%{_mandir}/man3/*


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 6.11.42-2
- 为 Magic 3.0 重建

* Fri Oct 28 2010 Alexey Kurov <nucleo@fedoraproject.org> - 6.11.42-1
- libpgf-6.11.42

* Fri Sep 23 2010 Alexey Kurov <nucleo@fedoraproject.org> - 6.11.24-1
- Initial RPM release
- added svn r46-48 fixes (6.11.32)
- install docs in -devel

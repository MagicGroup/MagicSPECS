Name:           soxr
Version:	0.1.2
Release:	2%{?dist}
Summary:        The SoX Resampler library
Summary(zh_CN.UTF-8): SoX 重采样库

License:        LGPLv2+
URL:            https://sourceforge.net/p/soxr/wiki/Home/ 
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}-Source.tar.xz

BuildRequires:  cmake

%description
The SoX Resampler library `libsoxr' performs one-dimensional sample-rate
conversion -- it may be used, for example, to resample PCM-encoded audio.
%description -l zh_CN.UTF-8
SoX 重采样库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-%{version}-Source


%build
rm -rf build && mkdir build && pushd build
export LDFLAGS="-Wl,--as-needed"
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       ../
make %{?_smp_mflags}


%install
pushd build
%make_install

# Remove docs and use the rpmbuild macro instead
rm -rf %{buildroot}%{_docdir}/*
magic_rpm_clean.sh

%check
pushd build
make test


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc LICENCE NEWS README
%{_libdir}/*.so.*

%files devel
%doc examples
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/soxr-lsr.pc
%{_libdir}/pkgconfig/soxr.pc


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.1.2-2
- 为 Magic 3.0 重建

* Mon Sep 28 2015 Liu Di <liudidi@gmail.com> - 0.1.2-1
- 更新到 0.1.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Richard Shaw <hobbes1069@gmail.com> - 0.1.1-1
- Initial packaging.

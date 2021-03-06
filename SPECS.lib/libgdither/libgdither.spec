Name:           libgdither
Version:        0.6
Release:        9%{?dist}
Summary:        Library for applying dithering to PCM audio sources
Summary(zh_CN.UTF-8): 为 PCM 音源添加抖动的库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        GPLv2+
URL:            http://plugin.org.uk/libgdither/README
Source0:        http://plugin.org.uk/libgdither/libgdither-%{version}.tar.gz
Patch0:         libgdither-0.6-default.patch
Patch1:         libgdither-0.6-gavl.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  fftw-devel >= 3.0.0
    

%description
Libgdither is a GPL'd library library for performing audio dithering on 
PCM samples. The dithering process should be carried out before reducing 
the bit width of PCM audio data (eg. float to 16 bit int conversions) to 
preserve audio quality.

%description -l zh_CN.UTF-8
为 PCM 音源添加抖动的库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1 -b .default
%patch1 -p1 -b .gavl_fix


%build
export INIT_CFLAGS="${RPM_OPT_FLAGS}"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT LIBDIR=%{_libdir}
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

sed -i -e 's|/usr/local|%{_prefix}|g' \
   $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libgdither.pc
sed -i -e 's|%{_prefix}/lib|%{_libdir}|' \
  $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libgdither.pc
magic_rpm_clean.sh

%check
make test CFLAGS="${RPM_OPT_FLAGS} -Werror --std=c99 -I%{_builddir}/%{?buildsubdir}"

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/libgdither/
%{_libdir}/*.so
%{_libdir}/pkgconfig/libgdither.pc

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 0.6-9
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.6-8
- 为 Magic 3.0 重建

* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 0.6-7
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.6-6
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 27 2008 kwizart < kwizart at gmail.com > - 0.6-1
- Backport patch from gavl

* Mon Jun 16 2008 kwizart < kwizart at gmail.com > - 0.6-0
- Initial package

Name:           freealut
Version:        1.1.0
Release:        16%{?dist}
Summary:        Implementation of OpenAL's ALUT standard
Summary(zh_CN.UTF-8): OpenAL 的 ALUT 标准的实现 

Group:          System Environment/Libraries
Group(zh_CN.UTF): 系统环境/库
License:        LGPLv2
URL:            http://openal.org/
Source0:        http://openal.org/openal_webstf/downloads/freealut-1.1.0.tar.gz
Patch0:         freealut-openal.patch
Patch1:         freealut-multiarch.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  openal-soft-devel
BuildRequires:  libtool

%description
freealut is a free implementation of OpenAL's ALUT standard. See the file
AUTHORS for the people involved.

%description -l zh_CN.UTF-8
OpenAL 的 ALUT 标准的自由版本实现。

%package devel
Summary:        Development files for freealut
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release} 
Requires:       pkgconfig
Requires:       openal-soft-devel

%description devel
Development headers and libraries needed for freealut development

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0
%patch1
libtoolize
autoreconf

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT/%{_libdir}/libalut.la

# don't have dsp devices in buildroot
#%check
#pushd test_suite
#./test_errorstuff || exit $?  
#./test_fileloader || exit $?  
#./test_memoryloader || exit $?
#./test_retrostuff || exit $?
#./test_version || exit $?  
#./test_waveforms || exit $?
#popd

touch -r ChangeLog $RPM_BUILD_ROOT/%{_bindir}/freealut-config
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_libdir}/libalut.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/* examples/*.c
%{_bindir}/freealut-config
%{_includedir}/AL
%{_libdir}/libalut.so
%{_libdir}/pkgconfig/freealut.pc

%changelog
* Tue Dec 18 2012 Liu Di <liudidi@gmail.com> - 1.1.0-16
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 29 2012 Jon Ciesla <limburgher@gmail.com> - 1.1.0-14
- Rebuild for GCC4.7 ABI bugfix.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Nov 07 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.0-11
- require openal-soft in devel (#533599)

* Tue Aug 11 2009 Jochen Schmitt <Jochen herr-schmitt de> 1.1.0-10
- Build agains openal-soft

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 18 2009 Robert Scheck <robert@fedoraproject.org> - 1.1.0-8
- Rebuilt against libtool 2.2 to avoid libtool errors 

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.0-6
- Autorebuild for GCC 4.3

* Wed Jan 02 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.0-5
- fix #341161 multiarch conflicts

* Wed Aug 22 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.0-4
- fix license tag
- rebuild for buildid

* Mon Mar 12 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.1.0-3
- fix #231132

* Fri Sep 15 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.1.0-2
- FE6 rebuild

* Tue Jun 13 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.1.0-1
- version upgrade

* Fri Feb 17 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0.0-3
- Rebuild for Fedora Extras 5

* Sun Feb 05 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0.0-2
- Add examples to devel doc
- Fix openal linking

* Sat Feb 04 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0.0-1
- Initial release

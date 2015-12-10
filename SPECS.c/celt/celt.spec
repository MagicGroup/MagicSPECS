Name:          celt
Version:       0.11.3
Release:       4%{?dist}
Summary:       An audio codec for use in low-delay speech and audio communication
Summary(zh_CN.UTF-8): 一种用于低延迟对话和音频通讯的声音编码

Group:         System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:       BSD
URL:           http://www.celt-codec.org/
Source0:       http://downloads.us.xiph.org/releases/%{name}/%{name}-%{version}.tar.gz

BuildRequires: libogg-devel

%description
CELT (Constrained Energy Lapped Transform) is an ultra-low delay audio 
codec designed for realtime transmission of high quality speech and audio. 
This is meant to close the gap between traditional speech codecs 
(such as Speex) and traditional audio codecs (such as Vorbis). 

%description -l zh_CN.UTF-8
一种用于低延迟对话和音频通讯的声音编码。

%package devel
Summary: Development package for celt
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: libogg-devel
Requires: celt = %{version}-%{release}
Requires: pkgconfig

%description devel
Files for development with celt.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --enable-custom-modes
# Remove rpath as per https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

rm %{buildroot}%{_libdir}/*.a
rm %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING README TODO
%{_bindir}/celtenc
%{_bindir}/celtdec
%{_libdir}/libcelt0.so.2
%{_libdir}/libcelt0.so.2.0.0

%files devel
%doc COPYING README
%{_includedir}/celt
%{_libdir}/pkgconfig/celt.pc
%{_libdir}/libcelt0.so

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 0.11.3-4
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.11.3-3
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.11.3-2
- 为 Magic 3.0 重建

* Thu Feb  6 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.3-1
- 0.11.3 release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Feb 20 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.1-2
- add --enable-custom-modes

* Wed Feb 16 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.1-1
- New 0.11.1 release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.10.0-1
- New 0.10.0 release

* Wed Sep 29 2010 jkeating - 0.8.1-2
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.1-1
- New 0.8.1 release

* Fri Jul  2 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.0-2
- Cleanup the spec file and update lib names

* Fri Jul  2 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.0-1
- New 0.8.0 upstream release

* Fri Oct 30 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.0-1
- New 0.7.0 upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul  6 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.0-1
- New 0.6.0 upstream release

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.5.2-1
- New upstream release, remove note about license as fix upstream

* Mon Feb 2 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.5.1-2
- Updates for package review

* Mon Jan 5 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.5.1-1
- Initial package

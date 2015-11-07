Name:          opusfile
Version:       0.6
Release:       5%{?dist}
Summary:       A high-level API for decoding and seeking within .opus files
Summary(zh_CN.UTF-8): 解码和定位 .opus 文件的高级 API

Group:         System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:       BSD
URL:           http://www.opus-codec.org/
Source0:       http://downloads.xiph.org/releases/opus/%{name}-%{version}.tar.gz

BuildRequires: libogg-devel
BuildRequires: openssl-devel
BuildRequires: opus-devel

%description
libopusfile provides a high-level API for decoding and seeking 
within .opus files. It includes:
* Support for all files with at least one Opus stream (including
multichannel files or Ogg files where Opus is muxed with something else).
* Full support, including seeking, for chained files.
* A simple stereo downmixing API (allowing chained files to be
decoded with a single output format, even if the channel count changes).
* Support for reading from a file, memory buffer, or over HTTP(S)
(including seeking).
* Support for both random access and streaming data sources.

%description -l zh_CN.UTF-8
解码和定位 .opus 文件的高级 API。

%package devel
Summary: Development package for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
Files for development with %{name}.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --disable-static

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

#Remove libtool archives.
find %{buildroot} -type f -name "*.la" -delete
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING AUTHORS
%{_libdir}/libopusfile.so.*
%{_libdir}/libopusurl.so.*

%files devel
%doc %{_docdir}/%{name}
%{_includedir}/opus/opus*
%{_libdir}/pkgconfig/opusfile.pc
%{_libdir}/pkgconfig/opusurl.pc
%{_libdir}/libopusfile.so
%{_libdir}/libopusurl.so

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0.6-5
- 为 Magic 3.0 重建

* Mon Sep 28 2015 Liu Di <liudidi@gmail.com> - 0.6-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 13 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.6-1
- Update to 0.6

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jan 12 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.5-1
- Update to 0.5

* Tue Aug 20 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.4-1
- Update to 0.4

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 14 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.2-1
- Update to 0.2

* Sun Nov  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.1-1
- Initial package

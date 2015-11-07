Name:          sbc
Version:	1.3
Release:	2%{?dist}
Summary:       Sub Band Codec used by bluetooth A2DP
Summary(zh_CN.UTF-8): 蓝牙 A2DP 使用的子频带编解码器

License:       GPLv2 and LGPLv2+
URL:           http://www.bluez.org
Source0:       http://www.kernel.org/pub/linux/bluetooth/%{name}-%{version}.tar.xz

BuildRequires: libsndfile-devel

%description
SBC (Sub Band Codec) is a low-complexity audio codec used in the Advanced Audio 
Distribution Profile (A2DP) bluetooth standard but can be used standalone. It 
uses 4 or 8 subbands, an adaptive bit allocation algorithm in combination with 
an adaptive block PCM quantizers.

%description -l zh_CN.UTF-8
蓝牙 A2DP 使用的子频带编解码器。

%package devel
Summary: Development package for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release}

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
find %{buildroot} -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING AUTHORS ChangeLog
%{_bindir}/sbc*
%{_libdir}/libsbc.so.1*

%files devel
%{_includedir}/sbc/
%{_libdir}/pkgconfig/sbc.pc
%{_libdir}/libsbc.so

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.3-2
- 为 Magic 3.0 重建

* Fri Sep 25 2015 Liu Di <liudidi@gmail.com> - 1.3-1
- 更新到 1.3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 18 2012 Rex Dieter <rdieter@fedoraproject.org> 1.0-2
- track lib soname, minor .spec cleanup

* Sat Dec  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.0-1
- Initial package

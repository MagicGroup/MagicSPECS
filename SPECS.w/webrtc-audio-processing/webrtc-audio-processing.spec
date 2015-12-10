
Name:           webrtc-audio-processing
Version:        0.1
Release:        6%{?dist}
Summary:        Library for echo cancellation
Summary(zh_CN.UTF-8): 回声消除库

License:        BSD
URL:            http://www.freedesktop.org/software/pulseaudio/webrtc-audio-processing/
Source0:        http://freedesktop.org/software/pulseaudio/webrtc-audio-processing/%{name}-%{version}.tar.xz

ExclusiveArch: %{ix86} x86_64 %{arm}

%description
%{name} is a library derived from Google WebRTC project that 
provides echo cancellation functionality. This library is used by for example
PulseAudio to provide echo cancellation.

%description -l zh_CN.UTF-8
回声消除库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header
files for developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure                                                              \
  --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc COPYING NEWS AUTHORS PATENTS
%{_libdir}/*.so.*

%files devel
%{_libdir}/libwebrtc_audio_processing.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/webrtc_audio_processing/


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 0.1-6
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 0.1-5
- 为 Magic 3.0 重建

* Tue Oct 20 2015 Liu Di <liudidi@gmail.com> - 0.1-4
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.1-3
- 为 Magic 3.0 重建

* Tue Oct 9 2012 Dan Horák <dan[at]danny.cz> 0.1-2
- set ExclusiveArch x86 and ARM for now

* Fri Oct 5 2012 Christian Schaller <christian.schaller@gmail.com> 0.1-1
- Initial Fedora spec.

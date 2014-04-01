Name:           emotion
Version:	1.7.10
Release:        1%{?dist}
License:        GPLv2+ and BSD
Summary:        Media Library for EFL
Summary(zh_CN.UTF-8): EFL 的媒体库
Url:            http://www.enlightenment.org
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source:         http://download.enlightenment.org/releases/%{name}-%{version}.tar.bz2

BuildRequires:  doxygen
BuildRequires:  edje-devel
BuildRequires:  ecore-devel
BuildRequires:  eet-devel
BuildRequires:  eeze-devel
BuildRequires:  evas-devel
BuildRequires:  eio-devel
BuildRequires:  evas-generic-loaders
BuildRequires:  gstreamer-devel
BuildRequires:  gstreamer-devel
BuildRequires:  gstreamer-plugins-base-devel
BuildRequires:  libX11-devel

%description
Emotion is a video (and audio) codec playback library that acts as a
front-end to libxine or gstreamer (or something else more generic)
that provides and evas object as a control object and video output
point. 

%description -l zh_CN.UTF-8
这是一个音视频解码播放库，它提供了 libxine 或 gstreamer 的前端。

%package        devel
Summary:        Emotion headers, documentation and test programs
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}
 
%description devel
Headers, test programs and documentation for Emotion Media Library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --disable-static --disable-silent-rules --enable-xine=no
make %{?_smp_mflags} V=1

%install
%make_install
find %{buildroot} -name '*.la' -delete
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc ChangeLog README COPYING*
%{_bindir}/emotion_*
%{_datadir}/emotion
%{_libdir}/edje
%{_libdir}/emotion
%{_libdir}/libemotion.so.*

%files devel
%{_libdir}/pkgconfig/emotion.pc
%{_includedir}/emotion-1
%{_libdir}/libemotion.so

%changelog
* Mon Mar 31 2014 Liu Di <liudidi@gmail.com> - 1.7.10-1
- 更新到 1.7.10

* Fri Nov 08 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.9-1
- Update to 1.7.9

* Thu Aug 29 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-8
- Tighten and alphabetize BR
- Add eeze-devel to BR

* Thu Aug 29 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-7
- Add ecore-devel to BR

* Tue Aug 27 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-6
- Remove xine support

* Mon Aug 26 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-5
- Update again for review

* Mon Aug 26 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-4
- Clean up spec file as per review

* Sat Aug 24 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-3
- Clean up RPMlint errors
- Ensure build against edje

* Fri Aug 23 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-2
- Update BRs

* Tue Aug 20 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-1
- Update to 1.7.8 

* Wed Jan 02 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 1.7.4-1 
- initial spec


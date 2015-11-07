Name: deadbeef
Version: 0.6.2
Release: 3%{?dist}

Summary: mp3/ogg/flac/sid/mod/nsf music player based on GTK2
Summary(zh_CN.UTF-8): 基于 GTK2 的音乐播放器
License: GPLv2+
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Url: http://deadbeef.sourceforge.net/

Source0: http://downloads.sourceforge.net/project/deadbeef/%name-%version.tar.bz2

BuildRequires: gcc-c++ alsa-lib-devel libcurl-devel flac-devel gtk2-devel libmad-devel libsamplerate-devel libsndfile-devel libvorbis-devel wavpack-devel

%description
mp3/ogg/flac/sid/mod/nsf music player based on GTK2.

%description -l zh_CN.UTF-8
基于 GTK2 的音乐播放器.

%prep
%setup -q
#临时性的

%build
%configure \
  --disable-static
%{__make} %{?_smp_mflags}

%install
%makeinstall
magic_rpm_clean.sh
rm %{buildroot}%{_libdir}/deadbeef/*.la

%files
%_bindir/*
%dir %_libdir/deadbeef
%_libdir/deadbeef/*.so*
%_libdir/deadbeef/convpresets/*
%dir %_datadir/deadbeef
%_datadir/deadbeef/
%_datadir/applications/deadbeef.desktop
%_datadir/icons/hicolor/*/apps/deadbeef.*
%_includedir/deadbeef/*.h
%_docdir/*
%_datadir/locale/*

%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 0.6.2-3
- 为 Magic 3.0 重建

* Tue Sep 22 2015 Liu Di <liudidi@gmail.com> - 0.6.2-2
- 为 Magic 3.0 重建

* Mon Mar 30 2015 Liu Di <liudidi@gmail.com> - 0.6.2-1
- 更新到 0.6.2

* Wed Mar 19 2014 Liu Di <liudidi@gmail.com> - 0.6.1-1
- 更新到 0.6.1

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.5.6-2
- 为 Magic 3.0 重建



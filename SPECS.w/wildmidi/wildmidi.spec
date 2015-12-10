Name:           wildmidi
Version:	0.3.8
Release:	3%{?dist}
Summary:        Softsynth midi player
Summary(zh_CN.UTF-8): 软波表 MIDI 播放器
Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
License:        GPLv3+
URL:            https://github.com/Mindwerks/wildmidi
Source0:        https://github.com/Mindwerks/wildmidi/archive/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  alsa-lib-devel libtool
Requires:       %{name}-libs = %{version}-%{release}

%description
WildMidi is a software midi player which has a core softsynth library that can
be used with other applications.
%description -l zh_CN.UTF-8
软波表 MIDI 播放器，自带软波表库，可以被其它程序使用。

%package libs
Summary:        WildMidi Midi Wavetable Synth Lib
Summary(zh_CN.UTF-8): %{name} 的运行库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv3+
Requires:       timidity++-patches

%description libs
This package contains the WildMidi core softsynth library. The library is
designed to process a midi file and stream out the stereo audio data
through a buffer which an external program can then process further.
%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        LGPLv3+
Requires:       %{name}-libs = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-%{name}-%{version}

%build
%cmake
make %{?_smp_mflags}


%install
%make_install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
ln -s ../timidity.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.cfg


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%doc docs/license/GPLv3.txt
%{_sysconfdir}/%{name}
%{_bindir}/%{name}
%{_mandir}/man1/*

%files libs
%doc docs/license/LGPLv3.txt
%{_libdir}/libWildMidi.so.1*
%{_mandir}/man5/*

%files devel
%{_includedir}/*
%{_libdir}/libWildMidi.so
%{_mandir}/man3/*

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 0.3.8-3
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 0.3.8-2
- 为 Magic 3.0 重建

* Tue Oct 20 2015 Liu Di <liudidi@gmail.com> - 0.3.8-1
- 更新到 0.3.8

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.2.3.5-2
- 为 Magic 3.0 重建

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.2.3.4-2
- Rebuilt for gcc bug 634757

* Sun Sep 12 2010 Hans de Goede <hdegoede@redhat.com> 0.2.3.4-1
- New upstream release 0.2.3.4-1

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-6
- Fixup Summary

* Mon Jul  7 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-5
- Fix wildmidi cmdline player sound output on bigendian archs (bz 454198),
  patch by Ian Chapman

* Sat Feb  9 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-4
- Change alsa output code to use regular write mode instead of mmap to make
  it work with pulseaudio (bz 431846)

* Sun Oct 14 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-3
- Require timidity++-patches instead of timidity++ itself so that we don't
  drag in arts and through arts, qt and boost.

* Wed Aug 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-2
- Put the lib in a seperate -libs subpackage
- Update License tags for new Licensing Guidelines compliance

* Sat Jul 14 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-1
- Initial Fedora Extras version

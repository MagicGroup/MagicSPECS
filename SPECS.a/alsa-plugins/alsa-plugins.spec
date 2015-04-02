%if 0%{?rhel}
%define with_jack 0
%else
%define with_jack 1
%endif

Name:           alsa-plugins
Version:	1.0.29
Release:        4%{?dist}
Summary:        The Advanced Linux Sound Architecture (ALSA) Plugins
Summary(zh_CN.UTF-8): 高级 Linux 声音架构 (ALSA) 插件
# All packages are LGPLv2+ with the exception of samplerate which is GPLv2+
# pph plugin is BSD-like licensed
License:        GPLv2+ and LGPLv2+ and BSD
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:            http://www.alsa-project.org/
Source0:        ftp://ftp.alsa-project.org/pub/plugins/%{name}-%{version}.tar.bz2
%if 0%{?with_jack}
Source1:        50-jack.conf
%endif
Source2:        50-pcm-oss.conf
Source3:        10-speex.conf
Source4:        10-samplerate.conf
Source5:        50-upmix.conf
Source6:        97-vdownmix.conf
Source8:        50-arcamav.conf
Source9:        98-maemo.conf
Patch1:		alsa-plugins-1.0.27-ffmpeg55.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  alsa-lib-devel

%description
The Advanced Linux Sound Architecture (ALSA) provides audio and MIDI
functionality to the Linux operating system.

This package includes plugins for ALSA.

%description -l zh_CN.UTF-8
这个包包含了 ALSA 的插件。

%if 0%{?with_jack}
%package jack
Requires:       alsa-utils
Requires:       jack-audio-connection-kit
BuildRequires:  jack-audio-connection-kit-devel
Summary:        Jack PCM output plugin for ALSA
Summary(zh_CN.UTF-8): ALSA 的 JACK PCM 输出插件
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
%description jack
This plugin converts the ALSA API over JACK (Jack Audio Connection
Kit, http://jackit.sf.net) API.  ALSA native applications can work
transparently together with jackd for both playback and capture.
This plugin provides the PCM type "jack"

%description jack -l zh_CN.UTF-8
这个插件转换 ALSA API 到 JACK API，ALSA 本地程序可以和 jackd 一块
工作，进行回放和捕捉。
这个插件提供了 PCM 类型 "jack"。
%endif

%package oss
Requires:       alsa-utils
BuildRequires:  alsa-lib-devel
Summary:        Oss PCM output plugin for ALSA
Summary(zh_CN.UTF-8): ALSA 的 Oss PCM 输出插件
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+ 
%description oss
This plugin converts the ALSA API over OSS API.  With this plugin,
ALSA native apps can run on OSS drivers.

This plugin provides the PCM type "oss".

%description oss -l zh_CN.UTF-8
这个插件转换 ALSA API 到 Oss API，ALSA 本地程序可以运行在 OSS 驱动上。
这个插件提供了 PCM 类型 "oss"。

%package pulseaudio
Requires:       alsa-utils
Requires:       pulseaudio
BuildRequires:  pulseaudio-libs-devel
Summary:        Alsa to PulseAudio backend
Summary(zh_CN.UTF-8): Alsa 转 PulseAudio 后端
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
%description pulseaudio
This plugin allows any program that uses the ALSA API to access a PulseAudio
sound daemon. In other words, native ALSA applications can play and record
sound across a network. There are two plugins in the suite, one for PCM and
one for mixer control.

%description pulseaudio -l zh_CN.UTF-8
这个插件允许任何使用 ALSA API 的程序访问 PulseAudio 声音服务。换句话说，本地
ALSA 程序可以通过网络播放和录制声音。这个包里有两个插件，一个是 PCM 的，一个
是音量控制。

%package samplerate
Requires:       alsa-utils
BuildRequires:  libsamplerate-devel
Summary:        External rate converter plugin for ALSA
Summary(zh_CN.UTF-8): ALSA 的外部采样转换插件
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        GPLv2+
%description samplerate
This plugin is an external rate converter using libsamplerate by Erik de
Castro Lopo.

%description samplerate -l zh_CN.UTF-8
这个插件是一个使用了 libsamplerate 库的外部采样转换器。

%package upmix
Requires:       alsa-utils
BuildRequires:  libsamplerate-devel
Summary:        Upmixer channel expander plugin for ALSA
Summary(zh_CN.UTF-8): ALSA 的上混扩展插件
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
%description upmix
The upmix plugin is an easy-to-use plugin for upmixing to 4 or
6-channel stream.  The number of channels to be expanded is determined
by the slave PCM or explicitly via channel option.

%description upmix -l zh_CN.UTF-8
上混插件是一个很易用的从 2 声道转到 4 或 6 声道的插件。

%package vdownmix
Requires:       alsa-utils
BuildRequires:  libsamplerate-devel
Summary:        Downmixer to stereo plugin for ALSA
Summary(zh_CN.UTF-8): ALSA 的下混插件
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
%description vdownmix
The vdownmix plugin is a downmixer from 4-6 channels to 2-channel
stereo headphone output.  This plugin processes the input signals with
a simple spacialization, so the output sounds like a kind of "virtual
surround".

%description vdownmix -l zh_CN.UTF-8
Alsa 的下混插件，即把 4-6 声道的声音降到 2 声道立体声输出。

%package usbstream
Summary:        USB stream plugin for ALSA
Summary(zh_CN.UTF-8): ALSA 的 USB 流插件
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库 
License:        LGPLv2+
%description usbstream
The usbstream plugin is for snd-usb-us122l driver. It converts PCM
stream to USB specific stream.

%description usbstream -l zh_CN.UTF-8
这个插件是 snd-usb-us1221 驱动，它转换 PCM 流到 USB 流。

%package arcamav
Summary:        Arcam AV amplifier plugin for ALSA
Summary(zh_CN.UTF-8): ALSA 的雅骏 AV 功放插件
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
%description arcamav
This plugin exposes the controls for an Arcam AV amplifier
(see: http://www.arcam.co.uk/) as an ALSA mixer device.

%description arcamav -l zh_CN.UTF-8
这个插件把雅骏 AV 功放做为 ALSA 的一个混音设备来控制。

%package speex
Requires:       speex
BuildRequires:  speex-devel
Summary:        Rate Converter Plugin Using Speex Resampler
Summary(zh_CN.UTF-8): 使用 Speex 重采样的采样率转换插件
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
%description speex
The rate plugin is an external rate converter using the Speex resampler
(aka Public Parrot Hack) by Jean-Marc Valin. The pcm plugin provides
pre-processing of a mono stream like denoise using libspeex DSP API.

%description speex -l zh_CN.UTF-8
使用 Speex 重采样器的采样率转换插件。

%package maemo
#BuildRequires:  alsa-lib-devel = %{version}
BuildRequires:  dbus-devel
Summary:        Maemo plugin for ALSA
Summary(zh_CN.UTF-8): ALSA 的 Maemo 插件
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
%description maemo
This plugin converts the ALSA API over PCM task nodes protocol. In this way,
ALSA native applications can run over DSP Gateway and use DSP PCM task nodes.

%description maemo -l zh_CN.UTF-8
这个插件转换 ALSA API 到 PCM 任务节点协议。在这种方式下，ALSA 本地程序可以运行
在 DSP 网关上，并且可以使用 DSP PCM 任务节点。

%prep
%setup -q -n %{name}-%{version}%{?prever}
#%patch1 -p1

%build
%configure --disable-static \
           --with-speex=lib \
           --enable-maemo-plugin \
           --enable-maemo-resource-manager
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -d ${RPM_BUILD_ROOT}%{_datadir}/alsa/alsa.conf.d
%if 0%{?with_jack}
install -m 644 %SOURCE1 ${RPM_BUILD_ROOT}%{_datadir}/alsa/alsa.conf.d
%endif
install -m 644 %SOURCE2 \
               %SOURCE3 \
               %SOURCE4 \
               %SOURCE5 \
               %SOURCE6 \
               %SOURCE8 \
               %SOURCE9 \
               ${RPM_BUILD_ROOT}%{_datadir}/alsa/alsa.conf.d
mv ${RPM_BUILD_ROOT}%{_datadir}/alsa/alsa.conf.d/99-pulseaudio-default.conf.example \
	${RPM_BUILD_ROOT}%{_datadir}/alsa/alsa.conf.d/99-pulseaudio-default.conf

find $RPM_BUILD_ROOT -name "*.la" -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%if 0%{?with_jack}
%files jack
%defattr(-,root,root,-)
%doc COPYING COPYING.GPL doc/README-jack
%dir %{_datadir}/alsa/alsa.conf.d
%config(noreplace) %{_datadir}/alsa/alsa.conf.d/50-jack.conf
%{_libdir}/alsa-lib/libasound_module_pcm_jack.so
%endif

%files oss
%defattr(-,root,root,-)
%doc COPYING COPYING.GPL doc/README-pcm-oss
%dir %{_datadir}/alsa/alsa.conf.d
%config(noreplace) %{_datadir}/alsa/alsa.conf.d/50-pcm-oss.conf
%{_libdir}/alsa-lib/libasound_module_ctl_oss.so
%{_libdir}/alsa-lib/libasound_module_pcm_oss.so

%files pulseaudio
%defattr(-,root,root,-)
%doc COPYING COPYING.GPL doc/README-pulse
%{_libdir}/alsa-lib/libasound_module_pcm_pulse.so
%{_libdir}/alsa-lib/libasound_module_ctl_pulse.so
%{_libdir}/alsa-lib/libasound_module_conf_pulse.so
%dir %{_datadir}/alsa/alsa.conf.d
%config(noreplace) %{_datadir}/alsa/alsa.conf.d/50-pulseaudio.conf
%config(noreplace) %{_datadir}/alsa/alsa.conf.d/99-pulseaudio-default.conf

%files samplerate
%defattr(-,root,root,-)
%doc COPYING COPYING.GPL doc/samplerate.txt
%dir %{_datadir}/alsa/alsa.conf.d
%config(noreplace) %{_datadir}/alsa/alsa.conf.d/10-samplerate.conf
%{_libdir}/alsa-lib/libasound_module_rate_samplerate.so
%{_libdir}/alsa-lib/libasound_module_rate_samplerate_best.so
%{_libdir}/alsa-lib/libasound_module_rate_samplerate_linear.so
%{_libdir}/alsa-lib/libasound_module_rate_samplerate_medium.so
%{_libdir}/alsa-lib/libasound_module_rate_samplerate_order.so

%{_libdir}/alsa-lib/libasound_module_pcm_a52.so
%{_libdir}/alsa-lib/libasound_module_rate_lavcrate.so
%{_libdir}/alsa-lib/libasound_module_rate_lavcrate_fast.so
%{_libdir}/alsa-lib/libasound_module_rate_lavcrate_faster.so
%{_libdir}/alsa-lib/libasound_module_rate_lavcrate_high.so
%{_libdir}/alsa-lib/libasound_module_rate_lavcrate_higher.so

%files upmix
%defattr(-,root,root,-)
%doc COPYING COPYING.GPL doc/upmix.txt
%dir %{_datadir}/alsa/alsa.conf.d
%config(noreplace) %{_datadir}/alsa/alsa.conf.d/50-upmix.conf
%{_libdir}/alsa-lib/libasound_module_pcm_upmix.so

%files vdownmix
%defattr(-,root,root,-)
%doc COPYING COPYING.GPL doc/vdownmix.txt
%dir %{_datadir}/alsa/alsa.conf.d
%config(noreplace) %{_datadir}/alsa/alsa.conf.d/97-vdownmix.conf
%{_libdir}/alsa-lib/libasound_module_pcm_vdownmix.so

%files usbstream
%defattr(-,root,root,-)
%doc COPYING COPYING.GPL
%{_libdir}/alsa-lib/libasound_module_pcm_usb_stream.so

%files arcamav
%defattr(-,root,root,-)
%doc COPYING COPYING.GPL doc/README-arcam-av
%dir %{_datadir}/alsa/alsa.conf.d
%config(noreplace) %{_datadir}/alsa/alsa.conf.d/50-arcamav.conf
%{_libdir}/alsa-lib/libasound_module_ctl_arcam_av.so

%files speex
%defattr(-,root,root,-)
%doc COPYING COPYING.GPL doc/speexdsp.txt doc/speexrate.txt
%dir %{_datadir}/alsa/alsa.conf.d
%config(noreplace) %{_datadir}/alsa/alsa.conf.d/10-speex.conf
%{_libdir}/alsa-lib/libasound_module_pcm_speex.so
%{_libdir}/alsa-lib/libasound_module_rate_speexrate.so
%{_libdir}/alsa-lib/libasound_module_rate_speexrate_best.so
%{_libdir}/alsa-lib/libasound_module_rate_speexrate_medium.so

%files maemo
%defattr(-,root,root,-)
%doc COPYING COPYING.GPL doc/README-maemo
%dir %{_datadir}/alsa/alsa.conf.d
%config(noreplace) %{_datadir}/alsa/alsa.conf.d/98-maemo.conf
%{_libdir}/alsa-lib/libasound_module_ctl_dsp_ctl.so
%{_libdir}/alsa-lib/libasound_module_pcm_alsa_dsp.so


%changelog
* Fri Mar 27 2015 Liu Di <liudidi@gmail.com> - 1.0.29-4
- 为 Magic 3.0 重建

* Fri Mar 27 2015 Liu Di <liudidi@gmail.com> - 1.0.29-3
- 更新到 1.0.29

* Sat Jul 06 2013 Liu Di <liudidi@gmail.com> - 1.0.27-2
- 为 Magic 3.0 重建

* Fri Apr 12 2013 Jaroslav Kysela <jkysela@redhat.com> - 1.0.27-1
- Updated to 1.0.27

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep  6 2012 Jaroslav Kysela <jkysela@redhat.com> - 1.0.26-2
- Changed dependency on pulseaudio-lib-devel to pulseaudio-libs-devel

* Thu Sep  6 2012 Jaroslav Kysela <jkysela@redhat.com> - 1.0.26-1
- Updated to 1.0.26

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 23 2012 Paul Howarth <paul@city-fan.org> - 1.0.25-3
- Bump and rebuild to maintain upgrade path (#806218)

* Wed Feb  1 2012 Jaroslav Kysela <jkysela@redhat.com> - 1.0.25-1
- Updated to 1.0.25
- Moved plugin specific configuration from /etc/alsa/pcm to /usr/share/alsa/alsa.conf.d

* Thu Jan 19 2012 Nikola Pajkovsky <npajkovs@redhat.com> - 1.0.24-4
- 761244 - please disable JACK for RHEL

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 28 2011 Jaroslav Kysela <jkysela@redhat.com> - 1.0.24-1
- Updated to 1.0.24

* Thu Jan 14 2010 Jaroslav Kysela <jkysela@redhat.com> - 1.0.22-1
- Updated to 1.0.22

* Mon Sep 7 2009 Eric Moret <eric.moret@gmail.com> - 1.0.21-2
- Added missing dbus-devel dependency to maemo subpackage

* Mon Sep 7 2009 Eric Moret <eric.moret@gmail.com> - 1.0.21-1
- Updated to 1.0.21
- Patch clean up
- Added maemo subpackage

* Tue Aug 4 2009 Lennart Poettering <lpoetter@redhat.com> - 1.0.20-5
- Add a couple of more clean up patches for the pulse plugin

* Fri Jul 31 2009 Lennart Poettering <lpoetter@redhat.com> - 1.0.20-4
- Add a couple of clean up patches for the pulse plugin

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 24 2009 Eric Moret <eric.moret@gmail.com> - 1.0.20-2
- Added speex subpackage
- Removed ascii-art from jack's plugin description

* Fri May 8 2009 Eric Moret <eric.moret@gmail.com> - 1.0.20-1
- Updated to 1.0.20
- Added arcam-av subpackage

* Fri Apr 24 2009 Eric Moret <eric.moret@gmail.com> - 1.0.19-1
- Updated to 1.0.19
- Added Requires: alsa-utils to address #483322
- Added dir {_sysconfdir}/alsa/pcm to address #483322

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 28 2008 Eric Moret <eric.moret@gmail.com> - 1.0.18-2
- Updated to 1.0.18 final

* Thu Sep 11 2008 Jaroslav Kysela <jkysela@redhat.com> - 1.0.18-1.rc3
- Updated to 1.0.18rc3
- Added usbstream subpackage

* Mon Jul 21 2008 Jaroslav Kysela <jkysela@redhat.com> - 1.0.17-1
- Updated to 1.0.17

* Tue Mar 25 2008 Lubomir Kundrak <lkundrak@redhat.com> - 1.0.16-4
- Kind of fix the plugins not to complain about the hints

* Wed Mar 19 2008 Eric Moret <eric.moret@gmail.com> - 1.0.16-3
- Fixing jack.conf (#435343)

* Sun Mar 09 2008 Lubomir Kundrak <lkundrak@redhat.com> - 1.0.16-2
- Add descriptions to various PCM plugins, so they're visible in aplay -L

* Sat Mar 08 2008 Lubomir Kundrak <lkundrak@redhat.com> - 1.0.16-1
- New upstream, dropping upstreamed patches
- Do not assert fail when pulseaudio is unavailable (#435148)

* Tue Mar 04 2008 Lubomir Kundrak <lkundrak@redhat.com> - 1.0.15-4
- Be more heplful when there's PulseAudio trouble.
- This may save us some bogus bug reports

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.15-3
- Autorebuild for GCC 4.3

* Fri Jan 18 2008 Eric Moret <eric.moret@epita.fr> - 1.0.15-2
- Update to upstream 1.0.15 (#429249)
- Add "Requires: pulseaudio" to alsa-plugins-pulseaudio (#368891)
- Fix pulse_hw_params() when state is SND_PCM_STATE_PREPARED (#428030)
- run /sbin/ldconfig on post and postun macros

* Thu Oct 18 2007 Lennart Poettering <lpoetter@redhat.com> - 1.0.14-6
- Merge the whole /etc/alsa/pcm/pulseaudio.conf stuff into
  /etc/alsa/pulse-default.conf, because the former is practically
  always ignored, since it is not referenced for inclusion by any other
  configuration file fragment (#251943)
  The other fragments installed in /etc/alsa/pcm/ are useless, too. But
  since we are in a freeze and they are not that important, I am not fixing
  this now.

* Wed Oct 17 2007 Lennart Poettering <lpoetter@redhat.com> - 1.0.14-5
- Split pulse.conf into two, so that we can load one part from
  form /etc/alsa/alsa.conf. (#251943)

* Mon Oct 1 2007 Lennart Poettering <lpoetter@redhat.com> - 1.0.14-4
- In the pulse plugin: reflect the XRUN state back to the application.
  Makes XMMS work on top of the alsa plugin. (#307341)

* Mon Sep 24 2007 Lennart Poettering <lpoetter@redhat.com> - 1.0.14-3
- Change PulseAudio buffering defaults to more sane values

* Tue Aug 14 2007 Eric Moret <eric.moret@epita.fr> - 1.0.14-2
- Adding pulse as ALSA "default" pcm and ctl when the alsa-plugins-pulseaudio
package is installed, fixing #251943.

* Mon Jul 23 2007 Eric Moret <eric.moret@epita.fr> - 1.0.14-1
- update to upstream 1.0.14
- use configure --without-speex instead of patches to remove a52

* Tue Mar 13 2007 Matej Cepl <mcepl@redhat.com> - 1.0.14-0.3.rc2
- Really remove a52 plugin package (including changes in
  configure and configure.in)

* Thu Feb 15 2007 Eric Moret <eric.moret@epita.fr> 1.0.14-0.2.rc2
- Adding configuration files
- Removing a52 plugin package

* Wed Jan 10 2007 Eric Moret <eric.moret@epita.fr> 1.0.14-0.1.rc2
- Initial package for Fedora

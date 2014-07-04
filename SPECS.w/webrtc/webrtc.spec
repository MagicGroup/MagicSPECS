%global svndate 20130531
# Chromium 23 needs this revision.
%global svnrev 3704

Name:		webrtc
Version:	0.1
Release:	0.11.%{svndate}svn%{svnrev}%{?dist}
Summary:	Libraries to provide Real Time Communications via the web
License:	BSD
URL:		http://www.webrtc.org/
# No source tarballs. This is a google failure^Wproject.
# svn -r 3704 export http://webrtc.googlecode.com/svn/trunk/ webrtc
# mv webrtc/ webrtc-20130531svn3704
# tar --exclude-vcs -cjf webrtc-20130531svn3704.tar.bz2 webrtc-20130531svn3704
Source0:	webrtc-%{svndate}svn%{svnrev}.tar.bz2
BuildRequires:	libjpeg-turbo-devel, libyuv-devel, libvpx-devel
BuildRequires:	pulseaudio-libs-devel, opus-devel
BuildRequires:	autoconf, automake, libtool
BuildRequires:	libXext-devel, libX11-devel, alsa-lib-devel
# Google provides no real way to build this code, except as part of Chromium
# That's just stupid.
Patch0:		webrtc-20130531svn3704-build-sanity.patch
# // in include paths breaks debuginfo generation
Patch1:		webrtc-20130326svn3237-no-double-slashes-in-include-paths.patch
Patch2:		webrtc-20130531svn3704-disable-sse2.patch

%description
WebRTC is a free, open project that enables web browsers with Real-Time 
Communications (RTC) capabilities via simple Javascript APIs. The 
WebRTC components have been optimized to best serve this purpose. 

%package devel
Summary:	Development files for WebRTC
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	libjpeg-turbo-devel, libyuv-devel, libvpx-devel

%description devel
Development files for WebRTC.

%prep
%setup -q -n webrtc-%{svndate}svn%{svnrev}
touch NEWS README ChangeLog
ln -s LICENSE COPYING
%patch0 -p1 -b .SANITY
%patch1 -p1 -b .doubleslash
%ifarch mips64el
%patch2 -p1 -b .sse
%endif
autoreconf -if

%build
%ifarch armv7l armv7hl
%configure --disable-static --enable-armv7
%else
%configure --disable-static
%endif
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LICENSE PATENTS AUTHORS
%{_bindir}/frame_analyzer
%{_bindir}/frame_editor
%{_bindir}/psnr_ssim_analyzer
%{_bindir}/rgba_to_i420_converter
%{_libdir}/libCNG.so.*
%{_libdir}/libG711.so.*
%{_libdir}/libG722.so.*
%{_libdir}/libNetEq.so.*
%{_libdir}/libPCM16B.so.*
%{_libdir}/libaec.so.*
%{_libdir}/libaecm.so.*
%{_libdir}/libagc.so.*
%{_libdir}/libapm_util.so.*
%{_libdir}/libaudio_coding_module.so.*
%{_libdir}/libaudio_conference_mixer.so.*
%{_libdir}/libaudio_device.so.*
%{_libdir}/libaudio_processing.so.*
%{_libdir}/libbitrate_controller.so.*
%{_libdir}/libcommon_video.so.*
%{_libdir}/libframe_editing_lib.so.*
%{_libdir}/libiLBC.so.*
%{_libdir}/libiSAC.so.*
%{_libdir}/libiSACFix.so.*
%{_libdir}/libmedia_file.so.*
%{_libdir}/libns.so.*
%{_libdir}/libpaced_sender.so.*
%{_libdir}/libremote_bitrate_estimator.so.*
%{_libdir}/libresampler.so.*
%{_libdir}/librtp_rtcp.so.*
%{_libdir}/libsignal_processing.so.*
%{_libdir}/libcommand_line_parser.so.*
%{_libdir}/libsystem_wrappers.so.*
%{_libdir}/libudp_transport.so.*
%{_libdir}/libvad.so.*
%{_libdir}/libvideo_capture_module.so.*
%{_libdir}/libvideo_coding_utility.so.*
%{_libdir}/libvideo_engine_core.so.*
%{_libdir}/libvideo_processing.so.*
%{_libdir}/libvideo_quality_analysis.so.*
%{_libdir}/libvideo_render_module.so.*
%{_libdir}/libvoice_engine_core.so.*
%{_libdir}/libwebrtc_i420.so.*
# %%{_libdir}/libwebrtc_jpeg.so.*
# %%{_libdir}/libwebrtc_libyuv.so.*
%{_libdir}/libwebrtc_opus.so.*
%{_libdir}/libwebrtc_utility.so.*
%{_libdir}/libwebrtc_video_coding.so.*
%{_libdir}/libwebrtc_vp8.so.*

%files devel
%{_includedir}/webrtc/
%{_libdir}/libCNG.so
%{_libdir}/libG711.so
%{_libdir}/libG722.so
%{_libdir}/libNetEq.so
%{_libdir}/libPCM16B.so
%{_libdir}/libaec.so
%{_libdir}/libaecm.so
%{_libdir}/libagc.so
%{_libdir}/libapm_util.so
%{_libdir}/libaudio_coding_module.so
%{_libdir}/libaudio_conference_mixer.so
%{_libdir}/libaudio_device.so
%{_libdir}/libaudio_processing.so
%{_libdir}/libbitrate_controller.so
%{_libdir}/libcommon_video.so
%{_libdir}/libframe_editing_lib.so
%{_libdir}/libiLBC.so
%{_libdir}/libiSAC.so
%{_libdir}/libiSACFix.so
%{_libdir}/libmedia_file.so
%{_libdir}/libns.so
%{_libdir}/libpaced_sender.so
%{_libdir}/libremote_bitrate_estimator.so
%{_libdir}/libresampler.so
%{_libdir}/librtp_rtcp.so
%{_libdir}/libsignal_processing.so
%{_libdir}/libcommand_line_parser.so
%{_libdir}/libsystem_wrappers.so
%{_libdir}/libudp_transport.so
%{_libdir}/libvad.so
%{_libdir}/libvideo_capture_module.so
%{_libdir}/libvideo_coding_utility.so
%{_libdir}/libvideo_engine_core.so
%{_libdir}/libvideo_processing.so
%{_libdir}/libvideo_quality_analysis.so
%{_libdir}/libvideo_render_module.so
%{_libdir}/libvoice_engine_core.so
%{_libdir}/libwebrtc_i420.so
# %%{_libdir}/libwebrtc_jpeg.so
# %%{_libdir}/libwebrtc_libyuv.so
%{_libdir}/libwebrtc_opus.so
%{_libdir}/libwebrtc_utility.so
%{_libdir}/libwebrtc_video_coding.so
%{_libdir}/libwebrtc_vp8.so

%changelog
* Fri May 31 2013 Tom Callaway <spot@fedoraproject.org> - 0.1-0.11.20130531svn3704
- chromium 27

* Tue Mar 26 2013 Tom Callaway <spot@fedoraproject.org> - 0.1-0.10.20130326svn3237
- rebase to the exact rev that chromium 25 wants

* Tue Dec 18 2012 Tom Callaway <spot@fedoraproject.org> - 0.1-0.9.20121218svn2718
- rebase to the exact rev that chromium 23 wants

* Fri Dec 14 2012 Tom Callaway <spot@fedoraproject.org> - 0.1-0.8.20121214svn3295
- rebase to current SVN trunk

* Thu Dec 13 2012 Tom Callaway <spot@fedoraproject.org> - 0.1-0.7.20120613svn2401
- add David Rusling's arm fixes

* Wed Sep 12 2012 Tom Callaway <spot@fedoraproject.org> - 0.1-0.6.20120613svn2401
- missing BR

* Wed Jul 11 2012 Tom Callaway <spot@fedoraproject.org> - 0.1-0.5.20120613svn2401
- add missing files causing undefined references

* Tue Jun 26 2012 Tom Callaway <spot@fedoraproject.org> - 0.1-0.3.20120613svn2401
- missing typedefs.h

* Tue Jun 26 2012 Tom Callaway <spot@fedoraproject.org> - 0.1-0.2.20120613svn2401
- fix headers

* Thu Jun 14 2012 Tom Callaway <spot@fedoraproject.org> - 0.1-0.1.20120613svn2401
- initial package

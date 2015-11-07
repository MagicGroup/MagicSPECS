Name:           gsm
Version:        1.0.13
Release:        7%{?dist}
Summary:        Shared libraries for GSM speech compressor
Summary(zh_CN.UTF-8): GSM 语音压缩用的共享库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        MIT
URL:            http://kbs.cs.tu-berlin.de/~jutta/toast.html
Source:         http://kbs.cs.tu-berlin.de/~jutta/gsm/%{name}-%{version}.tar.gz
Patch0:         %{name}-makefile.patch
Patch1:         %{name}-warnings.patch
Patch2:         %{name}-64bit.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define srcver 1.0-pl13
%define soname 1.0.12

%description
Contains runtime shared libraries for libgsm, an implementation of
the European GSM 06.10 provisional standard for full-rate speech
transcoding, prI-ETS 300 036, which uses RPE/LTP (residual pulse
excitation/long term prediction) coding at 13 kbit/s.

GSM 06.10 compresses frames of 162 13-bit samples (8 kHz sampling
rate, i.e. a frame rate of 50 Hz) into 260 bits; for compatibility
with typical UNIX applications, our implementation turns frames of 160
16-bit linear samples into 33-byte frames (1650 Bytes/s).
The quality of the algorithm is good enough for reliable speaker
recognition; even music often survives transcoding in recognizable
form (given the bandwidth limitations of 8 kHz sampling rate).

The interfaces offered are a front end modelled after compress(1), and
a library API.  Compression and decompression run faster than realtime
on most SPARCstations.  The implementation has been verified against the
ETSI standard test patterns.

%description -l zh_CN.UTF-8
GSM 语音压缩用的共享库。

%package        tools
Summary:        GSM speech compressor tools
Summary(zh_CN.UTF-8): GSM 语音压缩工具
Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体

%description    tools
Contains command line utilities for libgsm, an implementation of
the European GSM 06.10 provisional standard for full-rate speech
transcoding, prI-ETS 300 036, which uses RPE/LTP (residual pulse
excitation/long term prediction) coding at 13 kbit/s.

%description tools -l zh_CN.UTF-8 
GSM 语音压缩工具。

%package        devel
Summary:        Header files and development libraries for libgsm
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}

%description    devel
Contains header files and development libraries for libgsm, an
implementation of the European GSM 06.10 provisional standard for
full-rate speech transcoding, prI-ETS 300 036, which uses RPE/LTP
(residual pulse excitation/long term prediction) coding at 13 kbit/s.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -n gsm-%{srcver} -q
%patch0 -p1 -b .mk
%patch1 -p1 -b .warn
%patch2 -p1 -b .64bit

%build
export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fPIC";
make %{?_smp_mflags} all

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}/gsm
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/{man1,man3}

make install \
	INSTALL_ROOT=$RPM_BUILD_ROOT%{_prefix} \
	GSM_INSTALL_INC=$RPM_BUILD_ROOT%{_includedir}/gsm \
	GSM_INSTALL_LIB=$RPM_BUILD_ROOT%{_libdir}

cp -p $RPM_BUILD_DIR/gsm-%{srcver}/lib/libgsm.so.%{soname} $RPM_BUILD_ROOT%{_libdir}
ln -s libgsm.so.%{soname} $RPM_BUILD_ROOT%{_libdir}/libgsm.so.1
ln -s libgsm.so.%{soname} $RPM_BUILD_ROOT%{_libdir}/libgsm.so

# some apps look for this in /usr/include
ln -s gsm/gsm.h $RPM_BUILD_ROOT%{_includedir}

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.a
magic_rpm_clean.sh

%check
# This is to ensure that the patch creates the proper library version.
[ -f $RPM_BUILD_ROOT%{_libdir}/libgsm.so.%{soname} ]
make addtst


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYRIGHT MACHINES README
%{_libdir}/libgsm.so.*

%files tools
%{_bindir}/tcat
%{_bindir}/toast
%{_bindir}/untoast
%{_mandir}/man1/toast.1*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/gsm
%{_includedir}/gsm/gsm.h
%{_includedir}/gsm.h
%{_libdir}/libgsm.so
%{_mandir}/man3/*

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.0.13-7
- 为 Magic 3.0 重建

* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 1.0.13-6
- 为 Magic 3.0 重建

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 1.0.13-4
- 为 Magic 3.0 重建

* Fri Dec 09 2011 Liu Di <liudidi@gmail.com> - 1.0.13-3
- 为 Magic 3.0 重建

* Wed Jul 29 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.13-2
- Fix dangling symlinks for shared lib, thanks to Lucian Langa for pointing out the issue.

* Tue Jul 28 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.13-1.1
- Upload sources

* Tue Jul 28 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.13-1
- Update to 1.0.13

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 11 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.12-6
- Rebuild for GCC 4.3

* Sun Aug 26 2007 Dominik Mierzejewski <rpm[AT]greysector.net> 1.0.12-5
- install symlinks instead of binaries in -devel

* Sat Aug 25 2007 Dominik Mierzejewski <rpm[AT]greysector.net> 1.0.12-4
- rebuild for BuildID
- specfile cleanups

* Sun May 13 2007 Dominik Mierzejewski <rpm[AT]greysector.net> 1.0.12-3
- fix parallel make

* Fri May 11 2007 Dominik Mierzejewski <rpm[AT]greysector.net> 1.0.12-2
- fix some warnings
- fix 64bit testsuite issue as described at gsm homepage
- add compatibility header symlink
- split off binaries into a separate package

* Sun Apr 15 2007 Michael Schwendt <mschwendt[AT]users.sf.net> 1.0.12-1
- Update to Release 1.0 Patchlevel 12.
- Build with -fPIC not just for non-ix86.
- Add check section to ensure proper library version.
- Remove static library.

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.0.10-12
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.0.10-11
- rebuild for FC6

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Mon Jun 27 2005 David Woodhouse <dwmw2@infradead.org>
- 1.0.10-0.lvn.10: Clean up installation

* Sat Jun 25 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> 
- 1.0.10-0.lvn.9: mv libgsm.a only when needed

* Fri Dec 31 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> 
- 1.0.10-0.lvn.8: Use -fPIC on non ix86

* Tue Mar 02 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.0.10-0.lvn.7: moved to rpm.livna.org

* Tue Mar 02 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.0.10-0.fdr.7: applied patch from Ville, remove epoch since it's allowed

* Sat Sep 13 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 0:1.0.10-0.fdr.6: remove second makeinstall

* Sun Sep 07 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 0:1.0.10-0.fdr.5
- added back epochs, I surrender
- fix RPM_OPT_FLAGS hackery

* Fri Jul 18 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.0.10-0.fdr.4: remove epoch mentions

* Sat Jul 05 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.0.10-0.fdr.3
- pull in RPM_OPT_FLAGS in patch instead of using perl to wedge it in
- fix group
- -p'ize ldconfig

* Tue Jun 10 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.0.10-0.fdr.2
- Fix libgsm.so.* being files instead of symlinks

* Thu May 29 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 0:1.0.10-0.fdr.1: initial RPM release

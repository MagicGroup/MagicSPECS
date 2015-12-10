Name:           espeak
Version: 1.48.04
Release:        5%{?dist}
Summary:        Software speech synthesizer (text-to-speech)
Summary(zh_CN.UTF-8): 软件语音合成器（文本转语音）

Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
License:        GPLv3+
URL:            http://espeak.sourceforge.net
Source0:        http://kent.dl.sourceforge.net/sourceforge/espeak/espeak-%{version}-source.zip
Source1:        espeak.1
Patch0:         espeak-1.23-makefile_nostaticlibs.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  portaudio-devel pulseaudio-libs-devel gcc-c++


%description
eSpeak is a software speech synthesizer for English and other languages.

eSpeak produces good quality English speech. It uses a different synthesis
method from other open source TTS engines, and sounds quite different.
It's perhaps not as natural or "smooth", but some people may find the
articulation clearer and easier to listen to for long periods. eSpeak supports
several languages, however in most cases these are initial drafts and need more
work to improve them.

It can run as a command line program to speak text from a file or from stdin.

%description -l zh_CN.UTF-8
软件语音合成器（文本转语音）,支持英语等语言。

%package devel
Summary: Development files for espeak
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
Development files for eSpeak, a software speech synthesizer.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n espeak-%{version}-source
%patch0 -p1 -b .nostaticlibs

# Fix file permissions
find . -type f -exec chmod 0644 {} ";"
# Prepare documentation
rm -rf docs/images/.svn
mv docs html
sed -i 's/\r//' License.txt
# Compile against portaudio v19 (see ReadMe)
cp -f src/portaudio19.h src/portaudio.h
# Don't use the included binary voice dictionaries; we compile these from source
rm -f espeak-data/*_dict


%build
# Compile espeak
cd src
make %{?_smp_mflags} CXXFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS"

# Compile the TTS voice dictionaries
export ESPEAK_DATA_PATH=$RPM_BUILD_DIR/espeak-%{version}-source
cd ../dictsource
for voice in $(../src/speak --voices | awk '{print $2}{print $5}' | egrep -v Language\|File\|/ | uniq); do \
    ../src/speak --compile=$voice; \
done


%install
rm -rf $RPM_BUILD_ROOT
cd $RPM_BUILD_DIR/espeak-%{version}-source/src
make install DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir} INCDIR=%{_includedir}/espeak LIBDIR=%{_libdir}
# Install manpage
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
cp -pf %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man1/
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc $RPM_BUILD_DIR/espeak-%{version}-source/ReadMe $RPM_BUILD_DIR/espeak-%{version}-source/ChangeLog.txt $RPM_BUILD_DIR/espeak-%{version}-source/License.txt $RPM_BUILD_DIR/espeak-%{version}-source/html/
%{_mandir}/man1/espeak.1.gz
%{_bindir}/espeak
%{_datadir}/espeak-data
%{_libdir}/libespeak.so.*


%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/espeak


%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com>
- 更新到 1.48.04-source

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 1.45.05-4
- 为 Magic 3.0 重建

* Mon Sep 19 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.45.05-3
- Build with $RPM_OPT_FLAGS and $RPM_LD_FLAGS.

* Fri Sep 16 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.45.05-2
- Dropped ftbs_ld_libm patch (not needed now)

* Thu Sep 15 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.45.05-1
- New version
- Updated runtime_detection patch
- Dropped gcc_no_libstdc++ patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.43-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 18 2010 Francois Aucamp <faucamp@fedoraproject.org> - 1.43-2
- Added patch declaring explicit libm linking dependency (RHBZ #565186)

* Sat Feb 13 2010 Francois Aucamp <faucamp@fedoraproject.org> - 1.43-1
- Update to version 1.43
- Added patch for runtime detection of pulseaudio, contributed by Kevin Kofler (RHBZ #512190)

* Thu Dec 17 2009 Francois Aucamp <faucamp@fedoraproject.org> - 1.42.04-1
- Update to version 1.42.04
- Revert: build against PortAudio instead of native PulseAudio (RHBZ #512190, #532674)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.40.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 30 2009 Francois Aucamp <faucamp@fedoraproject.org> - 1.40.02-2
- Compile against pulseaudio instead of portaudio (RHBZ #481651)

* Mon Jun 22 2009 Francois Aucamp <faucamp@fedoraproject.org> - 1.40.02-1
- Update to version 1.40.02
- Added patch to compile with GCC and not to link to libstdc++ (not needed)
- Added manpage (thanks goes to Luke Yelavich from Ubuntu for writing it)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 21 2008 Francois Aucamp <faucamp@fedoraproject.org> - 1.39-1
- Update to version 1.39

* Tue Feb 26 2008 Francois Aucamp <faucamp@fedoraproject.org> - 1.31-5
- Export ESPEAK_DATA_PATH in %%build to allow proper compilation of voice dictionaries

* Tue Jan 29 2008 Francois Aucamp <faucamp@fedoraproject.org> - 1.31-4
- Removed libjack patches as they are unnecessary

* Tue Jan 29 2008 Francois Aucamp <faucamp@fedoraproject.org> - 1.31-3
- Added "makefile_libjack" patch to link to libjack
- Added BuildRequires: jack-audio-connection-kit-devel

* Fri Jan 25 2008 Francois Aucamp <faucamp@fedoraproject.org> - 1.31-2
- Removed espeakedit (and associated patches and BuildRequires) from package
  until all phoneme table compilation functions can be moved into espeak (or a
  separate commandline app without wxGTK dependencies)
- Voices are still compiled from source, but using pre-compiled phoneme table
  from upstream until the above issue is resolved

* Thu Jan 24 2008 Francois Aucamp <faucamp@fedoraproject.org> - 1.31-1
- Update to version 1.31
- Compile phoneme tables and voice dictionaries from source instead of
  packaging pre-compiled binary data
- Added espeakedit as Source1
- Added BuildRequires: wxGTK-devel for espeakedit
- Added "makefile_rpmoptflags_wxversion" espeakedit patch to enable
  RPM_OPT_FLAGS and set the correct wxWidgets version
- Added "espeak_data_path" espeakedit patch to be able to set control the
  source directory that espeakedit's compiler uses

* Tue Jan 15 2008 Francois Aucamp <faucamp@fedoraproject.org> - 1.30-1
- Update to version 1.30
- Removed local "synthdata_strlen" patch (included upstream)

* Mon Aug 20 2007 Francois Aucamp <faucamp@csir.co.za> - 1.28-1
- Update to version 1.28
- Added "synthdata_strlen" patch to fix memory allocation issue on x86_64 (RHBZ #252712)
- Modified %%prep to build against portaudio v19 for F8 and later
- Upstream license changed from GPLv2+ to GPLv3+

* Tue Jun 19 2007 Francois Aucamp <faucamp@csir.co.za> - 1.26-1
- Update to version 1.26
- Modified %%prep to build against portaudio v19

* Tue Jun 05 2007 Francois Aucamp <faucamp@csir.co.za> - 1.25-1
- Update to version 1.25

* Tue May 08 2007 Francois Aucamp <faucamp@csir.co.za> - 1.24-1
- Update to version 1.24

* Tue Apr 24 2007 Francois Aucamp <faucamp@csir.co.za> - 1.23-1
- Update to version 1.23
- Added "makefile_nostaticlibs" patch so static libraries aren't installed

* Thu Feb 08 2007 Francois Aucamp <faucamp@csir.co.za> - 1.20-1
- Update to version 1.20
- Solves stack smash bug (RHBZ #227316)

* Fri Jan 26 2007 Francois Aucamp <faucamp@csir.co.za> - 1.19-1
- Update to version 1.19
- Removed "espeak-1.18-makefile_lpthread" patch as it has been included upstream
- Removed "espeak-1.18-makefile_smp" patch as it has been included upstream
- Removed "espeak-1.18-ptr_64bit" patch as it has been solved upstream
- Fixed espeak-data file permissions

* Tue Jan 16 2007 Francois Aucamp <faucamp@csir.co.za> - 1.18-2
- Created "espeak-1.18-ptr_64bit" patch to allow compilation on x86_64 (fixes 64-bit pointer issues)
- Created "espeak-1.18-makefile_smp" patch to allow parallel make ("_smp_mflags")
- Renamed "makefile_lpthread" patch to "espeak-1.18-makefile_lpthread"

* Mon Jan 15 2007 Francois Aucamp <faucamp@csir.co.za> - 1.18-1
- Update to version 1.18
- Dropped statically-linked "speak" executable (replaced by dynamically-linked "espeak" executable)
- Removed the "espeak program name" patch as it has been included upstream
- Removed "espeak program name" patch backup file cleanup from %%install
- Minor modification to "makefile lpthread" patch to account for new lib/executable
- Removed "BIN_NAME" variable from make in %%build (implemented upstream)

* Mon Nov 20 2006 Francois Aucamp <faucamp@csir.co.za> - 1.17-1
- Update to version 1.17
- Removed "makefile install target" patch as it has been included upstream
- Removed "AMD64 sizeof(char *)" patch as it has been included upstream
- Minor modification to "espeak program name" patch to allow patching current version

* Tue Nov 07 2006 Francois Aucamp <faucamp@csir.co.za> - 1.16-4
- Modified patch steps to create backups with different suffixes
- Renamed patch file extensions to .patch
- Added step in %%install to remove patch backup files in documentation

* Sat Nov 04 2006 Francois Aucamp <faucamp@csir.co.za> - 1.16-3
- Fixed source file permissions for -debuginfo package in %%prep
- Added RPM_OPT_FLAGS to "make" command in %%build; removed RPM_OPT_FLAGS makefile patch
- Modified makefile install target patch to include general support for setting compiler optimization flags via CXXFLAGS
- Removed creation of .orig backup files during patching
- Modified patch files to have different suffixes

* Thu Nov 02 2006 Francois Aucamp <faucamp@csir.co.za> - 1.16-2
- Added "install" target to makefile (makefile_install_target.patch)
- Added patch to fix AMD64 sizeof(char *) assumption bug (upstream request ID 1588938)
- Changed "portaudio" BuildRequires to "portaudio-devel"
- Added patch to makefile to allow RPM_OPT_FLAGS
- Added patch to replace all references to "speak" binary with "espeak"
- Moved header files to /usr/include/espeak
- Added rmdir command to "install" to remove empty soundicons directory

* Wed Oct 04 2006 Francois Aucamp <faucamp@csir.co.za> - 1.16-1
- Initial RPM build

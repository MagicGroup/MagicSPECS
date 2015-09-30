Name:           SDL_sound
Version:        1.0.3
Release:        8%{?dist}
Summary:        Library handling decoding of several popular sound file formats
Summary(zh_CN.UTF-8): 解码几种流行声音文件格式的库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://www.icculus.org/SDL_sound
# This is:
# http://www.icculus.org/SDL_sound/downloads/%{name}-%{version}.tar.gz
# With all the files except the Makefiles under decoders/mpglib (patented)
# and PBProjects.tar.gz (contains binaries) removed
Source0:        %{name}-%{version}.tar.gz  
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  SDL-devel flac-devel speex-devel libvorbis-devel libogg-devel
BuildRequires:  mikmod-devel libmodplug-devel physfs-devel doxygen

%description
SDL_sound is a library that handles the decoding of several popular sound file 
formats, such as .WAV and .OGG.

It is meant to make the programmer's sound playback tasks simpler. The 
programmer gives SDL_sound a filename, or feeds it data directly from one of 
many sources, and then reads the decoded waveform data back at her leisure. 
If resource constraints are a concern, SDL_sound can process sound data in 
programmer-specified blocks. Alternately, SDL_sound can decode a whole sound 
file and hand back a single pointer to the whole waveform. SDL_sound can 
also handle sample rate, audio format, and channel conversion on-the-fly 
and behind-the-scenes, if the programmer desires.

%description -l zh_CN.UTF-8
解码几种流行声音文件格式的库

%package        devel
Summary:        %{summary}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       SDL-devel

%description    devel
%{description}

This package contains the headers and libraries for SDL_sound development.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
# Avoid lib64 rpaths
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure


%build
# no smpeg and internal mpglib because of patents!
%configure --disable-dependency-tracking --disable-static \
    --disable-smpeg --disable-mpglib --enable-mikmod --enable-ogg \
    --enable-modplug --enable-speex --enable-flac --enable-midi
make %{?_smp_mflags}
doxygen Doxyfile


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Add namespaces to man pages (livna bug #1181)
cp -a docs/man/man3 man3
pushd man3
mv actual.3 Sound_Sample::actual.3
mv author.3 Sound_DecoderInfo::author.3
mv buffer.3 Sound_Sample::buffer.3
mv buffer_size.3 Sound_Sameple::buffer_size.3
mv channels.3 Sound_AudioInfo::channels.3
mv decoder.3 Sound_Sample::decoder.3
mv description.3 Sound_DecoderInfo::description.3
mv desired.3 Sound_Sample::desired.3
mv extensions.3 Sound_DecoderInfo::extensions.3
mv flags.3 Sound_Sample::flags.3
mv format.3 Sound_AudioInfo::format.3
mv major.3 Sound_Version::major.3
mv minor.3 Sound_Version::minor.3
mv opaque.3 Sound_Sample::opaque.3
mv patch.3 Sound_Version::patch.3
mv rate.3 Sound_AudioInfo::rate.3
mv url.3 Sound_DecoderInfo::url.3
popd

mkdir -p $RPM_BUILD_ROOT/%{_mandir}
mv man3 $RPM_BUILD_ROOT/%{_mandir}

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING README TODO
%{_bindir}/playsound*
%{_libdir}/libSDL_sound-1.0.so.*

%files devel
%defattr(-,root,root,-)
%doc docs/html
%{_libdir}/libSDL_sound*.so
%{_includedir}/SDL/SDL_sound.h
%{_mandir}/man3/*


%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.0.3-8
- 为 Magic 3.0 重建

* Mon Feb 13 2012 Liu Di <liudidi@gmail.com> - 1.0.3-7
- 为 Magic 3.0 重建

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun  1 2010 Ville Skyttä <ville.skytta@iki.fi> - 1.0.3-5
- Rebuild.

* Thu Aug 20 2009 Warren Togami <wtogami@redhat.com> - 1.0.3-4
- rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Apr 21 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0.3-1
- New upstream release 1.0.3

* Sun Feb 17 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0.1-9
- Rebuild for new libmikmod
- Rebuild with gcc 4.3
- Stop shipping pre-generated doxygen docs, now that doxygen is fixed to no
  longer cause multilib conflicts 

* Sun Oct 28 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0.1-8
- Stop unnecessary linking to libvorbisenc (bz 355811)

* Sun Oct 28 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0.1-7
- Remove support for patented sound formats (not used by any package in the
  Fedora-verse), submit to Fedora
- Only include html version of doxygen docs (not latex source)
- Update license tag for new licensing guidelines compliance
- Use prebuild doxygen docs to avoid multilib conflicts

* Sat Mar  3 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.0.1-6
- Rebuild for devel

* Sun Dec  3 2006 Christopher Stone <chris.stone@gmail.com> 1.0.1-5
- Fix livna bug #1181
- Add physfs-devel to BR

* Sat Dec  2 2006 Christopher Stone <chris.stone@gmail.com> 1.0.1-4
- Fix bug #1297
- Whitespace cleanup

* Fri Oct  6 2006 Dams <anvil[AT]livna.org> - 1.0.1-3
- Disabled static
- devel packages Requires:SDL-devel because SDL_sound.h requires SDL.h
- a bit of cleanup

* Fri Oct  6 2006 Dams <anvil[AT]livna.org> - 1.0.1-2
- Added disttag

* Sat Feb 18 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> 0:1.0.1-1
- drop epoch, 0.lvn

* Fri Nov 21 2003 Panu Matilainen <pmatilai@welho.com> 0:1.0.1-0.lvn.1
- Initial RPM release.

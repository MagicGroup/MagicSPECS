%define		inputplugindir	%(xmms-config --input-plugin-dir 2>/dev/null)
%define		xmmsepoch	1

Summary:	MP3 output plugin for XMMS
Name:		xmms-mp3
Version:	1.2.11
Release: 	6.20071117cvs%{?dist}
License:	GPL
Group:		Applications/Multimedia
URL:		http://www.xmms.org/
Source:		http://www.xmms.org/files/1.2.x/xmms-%{version}-20071117cvs.tar.gz
Requires:	xmms-libs = %{xmmsepoch}:%{version}
BuildRequires:	gtk+-devel glib-devel 
BuildRequires:	xmms-devel = %{xmmsepoch}:%{version}
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
%ifarch x86_64
BuildRequires:	libtool 
%endif

# --------------------------------------------------------------------

%description
XMMS is a multimedia (Ogg Vorbis, CDs) player for the X Window System
with an interface similar to Winamp's. XMMS supports playlists and
streaming content and has a configurable interface. 

This is the output plugin needed to play MP3 audio files.

# --------------------------------------------------------------------

%prep
%setup -q -n xmms-%{version}-20071117cvs

# --------------------------------------------------------------------

%build
%configure \
%ifarch athlon i686
	--enable-simd	\
%endif
	--enable-kanji --enable-texthack --enable-arts-shared

perl -pi -e 's#\$\(top_builddir\)/libxmms/libxmms.la##g' Input/mpg123/Makefile
make -C Input/mpg123 \
%ifarch x86_64
  LIBTOOL=/usr/bin/libtool \
%endif
  %{?_smp_mflags} 

# --------------------------------------------------------------------

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{inputplugindir}
install -p -m 0755 Input/mpg123/.libs/libmpg123.so $RPM_BUILD_ROOT%{inputplugindir}

# --------------------------------------------------------------------

%clean
rm -rf $RPM_BUILD_ROOT

# --------------------------------------------------------------------

%files 
%defattr(-,root,root,-)
%{inputplugindir}/libmpg123.so

# --------------------------------------------------------------------

%changelog
* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 1.2.11-6.20071117cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.2.11-5.20071117cvs
- Mass rebuilt for Fedora 19 Features

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.2.11-4.20071117cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.2.11-3.20071117cvs
- rebuild for new F11 features

* Tue Sep 09 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.11-2.20071117cvs
- rebuild against new xmms in rawhide

* Thu Sep 04 2008 Xavier Lamien <lxtnow[at]gmail.com> - 1.2.10-7
- Rebuild against new xmms-lib.

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.2.10-6
- rebuild

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.2.10-5
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Apr  7 2006 Dams <anvil[AT]livna.org> - 1.2.10-4
- Requires: xmms-libs instead of xmms, according to change in FE

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field
- drop Epoch

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Fri Dec 31 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> 0:1.2.10-0.lvn.3
- fix x86_64 build; inside mach the integrated libtool does not work

* Sun May 16 2004 Dams <anvil[AT]livna.org> 0:1.2.10-0.lvn.2
- Added URL to Source0

* Wed Feb 25 2004 Dams <anvil[AT]livna.org> 0:1.2.10-0.lvn.1
- Updated to 1.2.10

* Fri Jan 30 2004 Dams <anvil[AT]livna.org> 0:1.2.9-0.lvn.1
- Updated to 1.2.9

* Tue Sep 30 2003 Dams <anvil[AT]livna.org> 0:1.2.8-0.fdr.2
- Fixed typo in description
- Fixed typo in configure option

* Sat Sep 27 2003 Dams <anvil[AT]livna.org> 0:1.2.8-0.fdr.1
- Spec file cleanup
- updated to xmms 1.2.8 for Fedora Core Test 2
- Using real xmms tarball

* Mon Mar 31 2003 Dams <anvil[AT]livna.org> 0:1.2.7-0.fdr.4
- Removed URL in Source
- Removed scriptlet %post %pre 

* Sun Mar 30 2003 Dams <anvil[AT]livna.org> 0.fdr.3
- Added Epoch
- NPTL Patch applied even if we're on rh8

* Sun Mar 30 2003 Dams <anvil[AT]livna.org>
- Fixed typo in name of the patch.
- Included script to extract sources from xmms tarball

* Wed Feb 19 2003 Dams <anvil[AT]livna.org> 
- Added 3dnow! support when target is athlon

* Tue Feb 18 2003 Dams <anvil[AT]livna.org> 
- Based on the xmms 1.2.7-19.p spec file.

Summary:	The Vorbis General Audio Compression Codec tools
Name:		vorbis-tools
Version:	1.4.0
Release:	5%{?dist}
Epoch:		1
Group:		Applications/Multimedia
License:	GPLv2
URL:		http://www.xiph.org/
Source:		http://downloads.xiph.org/releases/vorbis/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	flac-devel
BuildRequires:	libao-devel
BuildRequires:	libcurl-devel
BuildRequires:	libvorbis-devel
BuildRequires:	speex-devel
Obsoletes:	vorbis < %{epoch}:%{version}-%{release}
Provides:	vorbis = %{epoch}:%{version}-%{release}

%description
Ogg Vorbis is a fully open, non-proprietary, patent- and royalty-free,
general-purpose compressed audio format for audio and music at fixed
and variable bitrates from 16 to 128 kbps/channel.

The vorbis package contains an encoder, a decoder, a playback tool, and a
comment editor.


%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
%find_lang %{name}


%clean 
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README ogg123/ogg123rc-example
%{_bindir}/*
%{_mandir}/man1/*


%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1:1.4.0-5
- 为 Magic 3.0 重建

* Wed Feb 22 2012 Liu Di <liudidi@gmail.com> - 1:1.4.0-4
- 为 Magic 3.0 重建

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 02 2010 Kamil Dudka <kdudka@redhat.com> - 1:1.4.0-2
- rebuilt against libao-1.0.0 (#618171)

* Fri Mar 26 2010 Kamil Dudka <kdudka@redhat.com> - 1:1.4.0-1
- new upstream release

* Wed Nov 25 2009 Kamil Dudka <kdudka@redhat.com> - 1:1.2.0-7
- fix source URL

* Tue Oct 06 2009 Kamil Dudka <kdudka@redhat.com> - 1:1.2.0-6
- upstream patch fixing crash of oggenc --resample (#526653)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 21 2008 Zdenek Prikryl <zprikryl@redhat.com> - 1:1.2.0-3
- fixed seting flags for stderr (#467064)

* Sat May 31 2008 Hans de Goede <j.w.r.degoede@hhs.n> - 1:1.2.0-2
- Stop calling autoconf, this was no longer necessarry and in current
  rawhide breaks us from building (because aclocal.m4 does not match
  the new autoconf version)
- Drop our last 2 patches, they were modifying configure, but since we called
  autoconf after that in effect they were not doing anything, review has
  confirmed that they indeed are no longer needed)
- Drop using system libtool hack, this is dangerous when the libtool used
  to generate ./configure and the one used differ
- Remove various antique checks (for example check if RPM_BUILD_ROOT == /) 
- Drop unnecessary explicit library Requires
- Cleanup BuildRequires

* Tue Mar 11 2008 Jindrich Novy <jnovy@redhat.com> - 1:1.2.0-1
- update to 1.2.0
- remove libcurl and oggdec patches, applied upstream
- drop unneeded autoconf BR
- fix BuildRoot

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:1.1.1.svn20070412-6
- Autorebuild for GCC 4.3

* Thu Nov 15 2007 Hans de Goede <j.w.r.degoede@hhs.n> - 1:1.1.1.svn20070412-5
- Minor specfile cleanups for merge review (bz 226532)

* Thu Oct 04 2007 Todd Zullinger <tmz@pobox.com> - 1:1.1.1.svn20070412-4
- Upstream patch to fix oggdec writing silent wav files (#244757)

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 1:1.1.1.svn20070412-3
- Rebuild for build ID

* Wed May 16 2007 Christopher Aillon <caillon@redhat.com> 1:1.1.1.svn20070412-2.fc7
- Bring back support for http URLs which was broken with the previous update
  See https://bugzilla.redhat.com/240351

* Thu Apr 12 2007 - Bastien Nocera <bnocera@redhat.com> - 1.1.1.svn20070412-1.fc7
- Upgrade to a current SVN snapshot of vorbis-tools to get our FLAC support
  back, after the recent libFLAC upgrade (#229124)
- Remove obsolete UTF8 and Curl mute patches

* Wed Feb 14 2007 Karsten Hopp <karsten@redhat.com> 1.1.1-5
- rebuild with libFLAC.so.8, link with libogg instead of libOggFLAC

* Wed Nov  1 2006 Matthias Clasen <mclasen@redhat.com> - 1:1.1.1-4 
- Rebuild against new curl
- Don't use CURLOPT_MUTE

* Sun Oct 29 2006 Matthias Clasen <mclasen@redhat.com> - 1:1.1.1-3
- Fix charset conversion (#98816)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.1.1-2
- rebuild
- Add missing br libtool

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:1.1.1-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:1.1.1-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 09 2005 John (J5) Palmieri <johnp@redhat.com> 1:1.1.1-1
- Update to version 1.1.1

* Tue Mar 29 2005 John (J5) Palmieri <johnp@redhat.com> 1:1.0.1-6
- rebuild for flac 1.1.2

* Wed Mar 02 2005 John (J5) Palmieri <johnp@redhat.com> 1:1.0.1-5
- rebuild with gcc 4.0

* Tue Jul 28 2004 Colin Walters <walters@redhat.com>
- rebuild

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Dec 12 2003 Bill Nottingham <notting@redhat.com> 1:1.0.1-1
- update to 1.0.1

* Tue Oct 21 2003 Bill Nottingham <notting@redhat.com> 1.0-7
- rebuild (#107673)

* Fri Sep  5 2003 Bill Nottingham <notting@redhat.com> 1.0-6
- fix curl detection so ogg123 gets built (#103831)

* Thu Aug  7 2003 Elliot Lee <sopwith@redhat.com> 1.0-5
- Fix link errors

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 1:1.0-2
- rebuild on all arches

* Fri Jul 18 2002 Bill Nottingham <notting@redhat.com>
- one-dot-oh

* Tue Jul 16 2002 Elliot Lee <sopwith@redhat.com>
- Add builddep on curl-devel

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Feb 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.0rc3-3
- s/Copyright/License/
- Add curl-devel as a build dependency

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan  1 2002 Bill Nottingham <notting@redhat.com>
- update to 1.0rc3

* Mon Aug 13 2001 Bill Nottingham <notting@redhat.com>
- update to 1.0rc2

* Fri Jul 20 2001 Bill Nottingham <notting@redhat.com>
- split libao, libvorbis out

* Tue Jul 10 2001 Bill Nottingham <notting@redhat.com>
- own %%{_libdir}/ao
- I love libtool

* Tue Jun 26 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add links from library major version numbers in rpms

* Tue Jun 19 2001 Bill Nottingham <notting@redhat.com>
- update to rc1

* Fri May  4 2001 Oliver Paukstadt <oliver.paukstadt@millenux.com>
- fixed perl line in spec file to set optims correctly

* Tue Mar 20 2001 Bill Nottingham <notting@redhat.com>
- fix alpha/ia64, again
- use optflags, not -O20 -ffast-math (especially on alpha...)

* Mon Feb 26 2001 Bill Nottingham <notting@redhat.com>
- fix license tag

* Mon Feb 26 2001 Bill Nottingham <notting@redhat.com>
- beta4

* Fri Feb  9 2001 Bill Nottingham <notting@redhat.com>
- fix alpha/ia64

* Thu Feb  8 2001 Bill Nottingham <notting@redhat.com>
- update CVS in prep for beta4

* Wed Feb 07 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed bugzilla bug #25391. ogg123 now usses the OSS driver by default if
  none was specified.

* Tue Jan  9 2001 Bill Nottingham <notting@redhat.com>
- update CVS, grab aRts backend for libao

* Thu Dec 27 2000 Bill Nottingham <notting@redhat.com>
- update CVS

* Fri Dec 01 2000 Bill Nottingham <notting@redhat.com>
- rebuild because of broken fileutils

* Mon Nov 13 2000 Bill Nottingham <notting@redhat.com>
- hack up specfile some, merge some packages

* Sat Oct 21 2000 Jack Moffitt <jack@icecast.org>
- initial spec file created

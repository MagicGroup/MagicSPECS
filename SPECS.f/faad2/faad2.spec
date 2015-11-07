%define xmmsinputdir %(xmms-config --input-plugin-dir)

Summary: Library and frontend for decoding MPEG2/4 AAC
Name: faad2
Version: 2.7
Release: 19%{?dist}
License: GPLv2
Group: Applications/Multimedia
Source0: http://download.sourceforge.net/faac/%{name}-%{version}.tar.bz2
Patch0: faad2-2.7-mp4ff.patch
URL: http://www.audiocoding.com/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: dos2unix
BuildRequires: autoconf, automake, libtool, gcc-c++
BuildRequires: libsndfile-devel >= 1.0.0
BuildRequires: xmms-devel, id3lib-devel, gtk+-devel
BuildRequires: zlib-devel

%description
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch.


%package -n xmms-aac
Summary: X MultiMedia System input plugin to play AAC files
Group: Applications/Multimedia
Requires: %{name} = %{version}, xmms, id3lib
Obsoletes: xmms-faad2 <= %{version}

%description -n xmms-aac
This xmms plugin reads AAC files with and without ID3 tags (version 2.x).
AAC files are MPEG2 or MPEG4 files that can be found in MPEG4 audio files
(.mp4). MPEG4 files with AAC inside can be read by RealPlayer or Quicktime.

%package libs
Summary: Shared libs for %{name}
Summary(zh_CN.UTF-8): %{name} 的共享库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description libs
Shared libraries for %{name}.

%description libs -l zh_CN.UTF-8
%{name} 的动态共享库。

%package static
Summary: Static libs for %{name}
Summary(zh_CN.UTF-8): %{name} 的静态库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description static
Static libraries for %{name}.

%description static -l zh_CN.UTF-8
%{name} 的静态库。

%package devel
Summary: Devel files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
Devel files for %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。


%prep
%setup -q
%patch0 -p1 -b .mp4ff
chmod -x */*.h */*.c
chmod -x */*/*.h */*/*.c
chmod -x */*/*/*.c
dos2unix bootstrap

%build
autoreconf -i
#autoreconf -vif
#sh ./bootstrap
#./configure --help
#exit
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%configure \
  --with-xmms \
  --with-mp4v2
#  --with-drm
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}`xmms-config --input-plugin-dir`
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/manm/faad.man*

%files -n xmms-aac
%defattr(0644,root,root,0755)
%doc plugins/xmms/AUTHORS plugins/xmms/NEWS
%doc plugins/xmms/README plugins/xmms/TODO
%defattr(-,root,root,-)
%{xmmsinputdir}/*.so
%{xmmsinputdir}/*.a
%{xmmsinputdir}/*.la

%files libs
%defattr(-,root,root,0755)
%{_libdir}/libfaad.so.*

%files static
%defattr(-,root,root,0755)
%{_libdir}/libfaad.a
%{_libdir}/libmp4ff.a

%files devel
%defattr(-,root,root,0755)
%{_libdir}/libfaad.so
%{_includedir}/*

%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 2.7-19
- 为 Magic 3.0 重建

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 2.7-18
- 为 Magic 3.0 重建

* Sun Nov 20 2011 Liu Di <liudidi@gmail.com> - 2.7-17
- 为 Magic 3.0 重建

* Sun Mar  1 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1:2.7-12
- Update to 2.7.

* Tue Feb  3 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1:2.6.1-11
- Remove --with-drm.

* Sat Nov 15 2008 Paulo Roma <roma@lcg.ufrj.br> - 1:2.6.1-9
- Applied security patch main_overflow (2008-09-16).
- faad2-libs and xmms-faad2 from a 3rd party repo generate conflicts.
- Using Epoch 1 because of a 3rd party repo messing with epochs.
- Fixed permissions.

* Sun Feb 17 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.6.1-8
- Update to 2.6.1.

* Tue Aug 29 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.5-6
- Update to 2.5.

* Mon Oct  4 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 2.0 final.

* Tue Aug 12 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 2.0rc1.
- Introduced LD_LIBRARY_PATH workaround.
- Removed optional xmms plugin build, it seems mandatory now.
- Added gtk+ build dep for the xmms plugin.

* Wed May 14 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Added xmms plugin build.

* Wed Apr  9 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Spec file cleanup.
- Now exclude .la file.
- Update to latest CVS checkout to fix compile problem.

* Fri Aug 10 2002 Alexander Kurpiers <a.kurpiers@nt.tu-darmstadt.de>
- changes to compile v1.1 release

* Tue Jun 18 2002 Alexander Kurpiers <a.kurpiers@nt.tu-darmstadt.de>
- First RPM.


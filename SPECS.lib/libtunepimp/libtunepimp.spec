
%if 0%{?fedora} > 4
%define _with_mp4 1
%endif

# libtool2 (libltdl) building busted
#define use_autofoo 1

Summary: A library for creating MusicBrainz enabled tagging applications 
Summary(zh_CN.UTF-8): 创建可用 MusicBrainz 标签程序的库
Name:	 libtunepimp
Version: 0.5.3
Release: 24%{?dist}

License: LGPLv2+
Group: 	 System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:	 http://musicbrainz.org/doc/libtunepimp
# see http://musicbrainz.org/doc/libtunepimpDownload
Source0: http://ftp.musicbrainz.org/pub/musicbrainz/libtunepimp-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1: libtunepimp-0.5.3-gcc43.patch
Patch2: libtunepimp-0.5.3-glibc210_strrchr.patch 
# build against curl 7.21
Patch3: libtunepimp-0.5.3-curl.patch
Patch4:	libtunepimp-0.5.3-mpeg4ip.patch

%define pkglibdir %{_libdir}/tunepimp

%if 0%{?use_autofoo}
BuildRequires: automake libtool libtool-ltdl-devel
%endif
BuildRequires: chrpath
BuildRequires: flac-devel
%{?_with_mp4:BuildRequires: mpeg4ip-devel}
BuildRequires: libmpcdec-devel
BuildRequires: libmusicbrainz-devel >= 2.1.0
BuildRequires: libofa-devel curl-devel expat-devel
BuildRequires: libvorbis-devel
BuildRequires: python-devel
BuildRequires: readline-devel ncurses-devel
BuildRequires: taglib-devel 
BuildRequires: zlib-devel

%if 0%{?_with_mp4:1}
Provides:  libtunepimp-mp4 = %{version}-%{release}
%endif

Obsoletes: libtunepimp-tools < %{version}-%{release}
Provides:  libtunepimp-tools = %{version}-%{release}

%if "%{name}" == "libtunepimp"
Obsoletes: libtunepimp5 < %{version}-%{release}
Provides:  libtunepimp5 = %{version}-%{release}
%endif

%description
The TunePimp library is a development library geared towards developers 
who wish to create MusicBrainz enabled tagging applications.

%description -l zh_CN.UTF-8
创建可用 MusicBrainz 标签程序的库。

%package devel
Summary: Headers for developing programs that will use %{name} 
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:   Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
%if "%{name}" == "libtunepimp"
Provides:  libtunepimp5-devel = %{version}-%{release}
%else
Conflicts: libtunepimp-devel
%endif
%description devel
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%global python_ver %(%{__python} -c "import sys ; print sys.version[:3]")
%global python_sitelib  %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")
%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%package -n python-tunepimp
Summary: Python bindings for developing programs that will use %{name} 
Summary(zh_CN.UTF-8): %{name} 的 Python 绑定
Group:   Development/Libraries
Group(zh_CN.UTF-8): 开发/库
%description -n python-tunepimp
%{summary}.

%description -n python-tunepimp -l zh_CN.UTF-8
%{name} 的 Python 绑定。

%prep
%setup -q -n libtunepimp-%{version}

%patch1 -p1 -b .gcc43
%patch2 -p1 -b .glibc210_strrchr.patch
%patch3 -p1 -b .curl
%patch4 -p1

# nuke rpath -- Rex
%if 0%{?use_autofoo}
autoreconf -i -f
%else
# ugly non-autofoo-but-works-with-libtool2 solution
%if "%{_libdir}" != "/usr/lib"
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
%endif
%endif


%build
%configure \
  --disable-static \
  --disable-dependency-tracking \
  --enable-lgpl

make %{?_smp_mflags} PLUGIN_DIR=%{pkglibdir}/plugins

pushd python
%{__python} setup.py build 
popd

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot} PLUGIN_DIR=%{pkglibdir}/plugins

pushd python
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
popd

for foo in \
 %{buildroot}%{_bindir}/puid \
 %{buildroot}%{_libdir}/libtunepimp.so \
 %{buildroot}%{pkglibdir}/plugins/*.tpp ; do
  chrpath --list $foo && chrpath --delete $foo
done

# unpackaged files
rm -f %{buildroot}%{_libdir}/lib*.la
%{!?_with_mp4:rm -f  %{buildroot}%{pkglibdir}/plugins/mp4.tpp}
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog TODO 
# README omitted, it's mostly useless
%doc README.LGPL
%{_bindir}/puid
%{_libdir}/libtunepimp.so.5*
%dir %{pkglibdir}/
%dir %{pkglibdir}/plugins/
%{pkglibdir}/plugins/flac.tpp
%{?_with_mp4:%{pkglibdir}/plugins/mp4.tpp}
%{pkglibdir}/plugins/mpc.tpp
%{pkglibdir}/plugins/speex.tpp
%{pkglibdir}/plugins/vorbis.tpp
%{pkglibdir}/plugins/tta.tpp
%{pkglibdir}/plugins/wav.tpp
%{pkglibdir}/plugins/wma.tpp
%{pkglibdir}/plugins/wv.tpp

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/libtunepimp.so

%files -n python-tunepimp
%defattr(-,root,root,-)
%doc python/examples/trm.py
%{python_sitelib}/tunepimp*


%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 0.5.3-24
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0.5.3-23
- 为 Magic 3.0 重建

* Fri Aug 01 2014 Liu Di <liudidi@gmail.com> - 0.5.3-22
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 02 2011 Than Ngo <than@redhat.com> - 0.5.3-19
- apply patch to build against curl 7.21

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.5.3-17
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.5.3-15
- glibc210_strrchr patch

* Fri Feb 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 05 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.5.3-13
- fix build (libtool(2) and more rpath fun)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.5.3-12
- Rebuild for Python 2.6

* Thu Feb 21 2008 Rex Dieter <rdieter@fedoraproject.org> 0.5.3-11
- gcc43 patch
- include mp4 plugin here

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.5.3-10
- Autorebuild for GCC 4.3

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.5.3-9
- respin (BuildID)

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.5.3-8
- License: LGPLv2+

* Fri Jun 22 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.5.3-7
- fix URL (#245283)

* Wed Jun 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.5.3-6
- go back to unversioned BR: libmpcdec-devel

* Wed Jun 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.5.3-5
- respin (again for libmpcdec), BR: libmpcdec-devel >= 1.2.6 (#244228)

* Wed Jun 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.5.3-4
- respin (for libmpcdec)

* Wed Feb 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.5.3-3
- respin (for flac)

* Fri Dec 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.5.3-2
- respin (for python)

* Wed Nov 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.5.3-1
- libtunepimp-0.5.3

* Tue Oct 31 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.5.2-4
- respin for curl update (fc7)

* Thu Oct 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.5.2-3
- rename python-libtunepimp -> python-tunepimp (to match python
  module name)

* Mon Oct 09 2006 Alex Lancaster <alexl[AT]users.sf.net> 0.5.2-2
- build python-libtunepimp subpackage (#209961)

* Mon Oct 02 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.5.2-1
- libtunepimp-0.5.2

* Tue Sep 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.5.1-2
- drop -tools subpkg

* Thu Sep 14 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.5.1-1
- PLUGIN_DIR patch, fix lib64 issues, make parallel-installable
  with libtunepimp-0.4

* Thu Aug 31 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.4.3-3
- BR: taglib-devel, readline-devel, ncurses-devel

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.4.3-2
- 0.4.3

* Tue Jul 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.4.2-4
- BR: ncurses-devel

* Mon Jul 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.4.2-3
- drop ancient,deprecated Obsoletes/Provides: trm
- fix buffer overflow (bug #198195)
- License: LGPL, we're omitting the non-lgpl bits

* Thu Mar 16 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.4.2-1
- 0.4.2

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Mon Dec 19 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.4.0-5
- update gcc4 patch

* Mon Dec 19 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.4.0-4
- -tools: fix Req: %%name dependancy

* Mon Nov 28 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.4.0-3
- -tools: split out %%_bindir bits (to be multi-arch friendly)

* Sat Nov 19 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.4.0-2
- BR: libmusicbrainz -> libmusicbrainz-devel
- BR: libogg-devel -> libvorbis-devel
- BR: zlib-devel

* Thu Nov 17 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.4.0-1
- 0.4.0
- built with --enable-lgpl which omits mp3 plugin bits

* Mon Jun 13 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.3.0-1
- gcc4 patch
- 0.3.0 (first try)


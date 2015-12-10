%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%global codename DrO_o

Name:			xmms2
Summary: 		A modular audio framework and plugin architecture
Summary(zh_CN.UTF-8): 	一个模块化的音频框架和插件架构

Version:		0.8
Release:		24%{?dist}
License:		LGPLv2+ and GPLv2+ and BSD
Group:			Applications/Multimedia
Group(zh_CN.UTF-8): 	应用程序/多媒体
# We can't use the upstream source tarball as-is, because it includes an mp4 decoder.
# http://downloads.sourceforge.net/xmms2/%{name}-%{version}%{codename}.tar.bz2
# Cleaning it is simple, just rm -rf src/plugins/mp4
Source0:		%{name}-%{version}%{codename}-clean.tar.bz2
Source1:		xmms2-client-launcher.sh
# Use libdir properly for Fedora multilib
Patch1:			xmms2-0.8DrO_o-use-libdir.patch
# Set default output to pulse
Patch2:			xmms2-0.8DrO_o-pulse-output-default.patch
# Don't add extra CFLAGS, we're smart enough, thanks.
Patch4:			xmms2-0.8DrO_o-no-O0.patch
# More sane versioning
Patch5:			xmms2-0.8DrO_o-moresaneversioning.patch
# Fix xsubpp location
Patch6:			xmms2-0.8DrO_o-xsubpp-fix.patch
# libmodplug 0.8.8.5 changed pkgconfig includedir output
Patch7:			xmms2-0.8DrO_o-libmodplug-pkgconfig-change.patch
# libvorbis 1.3.4 changed pkgconfig libs output
Patch8:			xmms2-0.8DrO_o-vorbis-pkgconfig-libs.patch
# Cython 0.20.2 
Patch9:			xmms2-0.8-fixcython.patch
# ffmpeg 2.2
Patch10:		xmms2-0.8DrO_o-ffmpeg-2.2.patch
# Remove deprecated usage on ruby 22
Patch11:			xmms2-0.8DrO_o-ruby22-remove-deprecated-usage.patch

URL:			http://wiki.xmms2.xmms.se/
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:		sqlite-devel, flac-devel, libofa-devel
BuildRequires:		libcdio-paranoia-devel, libdiscid-devel, libsmbclient-devel
BuildRequires:		libmpcdec-devel, gnome-vfs2-devel, jack-audio-connection-kit-devel
BuildRequires:		fftw-devel, libsamplerate-devel, libxml2-devel, alsa-lib-devel
BuildRequires:		libao-devel, libshout-devel, Pyrex, ruby-devel, ruby
BuildRequires:		perl-devel, boost-devel, pulseaudio-libs-devel
BuildRequires:		libmodplug-devel, ecore-devel, gamin-devel
BuildRequires:		doxygen, perl-Pod-Parser
BuildRequires:		pkgconfig(avahi-client), pkgconfig(avahi-glib), pkgconfig(avahi-compat-libdns_sd)
BuildRequires:		libvisual-devel, wavpack-devel, SDL-devel
BuildRequires:		glib2-devel, readline-devel, ncurses-devel
# For /usr/share/perl5/ExtUtils/xsubpp
BuildRequires:		perl-ExtUtils-ParseXS

%description
XMMS2 is an audio framework, but it is not a general multimedia player - it 
will not play videos. It has a modular framework and plugin architecture for 
audio processing, visualisation and output, but this framework has not been 
designed to support video. Also the client-server design of XMMS2 (and the 
daemon being independent of any graphics output) practically prevents direct 
video output being implemented. It has support for a wide range of audio 
formats, which is expandable via plugins. It includes a basic CLI interface 
to the XMMS2 framework, but most users will want to install a graphical XMMS2 
client (such as gxmms2 or esperanza).

%description -l zh_CN.UTF-8
一个模块化的音频框架和插件架构。

%package devel
Summary:	Development libraries and headers for XMMS2
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	glib2-devel, boost-devel
Requires:	pkgconfig
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries and headers for XMMS2. You probably need this to develop
or build new plugins for XMMS2.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package docs
Summary:	Development documentation for XMMS2
Summary(zh_CN.UTF-8): %{name} 的开发文档
Group:		Documentation
Group(zh_CN.UTF-8): 文档
Requires:	%{name} = %{version}-%{release}

%description docs
API documentation for the XMMS2 modular audio framework architecture.

%description docs -l zh_CN.UTF-8
%{name} 的开发文档。

%package python
Summary:	Python support for XMMS2
Summary(zh_CN.UTF-8): %{name} 的 Python 支持
Group:		Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Requires:	%{name} = %{version}-%{release}

%description python
Python bindings for XMMS2.

%description python -l zh_CN.UTF-8
%{name} 的 Python 绑定。

%package perl
Summary:	Perl support for XMMS2
Summary(zh_CN.UTF-8): %{name} 的 Perl 支持
License:	GPL+ or Artistic
Group:		Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Requires:	%{name} = %{version}-%{release}
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description perl
Perl bindings for XMMS2.

%description perl -l zh_CN.UTF-8
%{name} 的 Perl 绑定。

%package ruby
Summary:	Ruby support for XMMS2
Summary(zh_CN.UTF-8): %{name} 的 Ruby 支持
Group:		Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Requires:	%{name} = %{version}-%{release}
Requires:	ruby(release)

%description ruby
Ruby bindings for XMMS2.

%description ruby -l zh_CN.UTF-8
%{name} 的 Ruby 绑定。

%package -n nyxmms2
Summary:	Commandline client for XMMS2
Summary(zh_CN.UTF-8): %{name} 的命令行客户端
Group:		Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Requires:	%{name} = %{version}-%{release}

%description -n nyxmms2
nyxmms2 is the new official commandline client for XMMS2. It can be run in
either shell-mode (if started without arguments), or in inline-mode where
it executes the command passed as argument directly.

%description -n nyxmms2 -l zh_CN.UTF-8
%{name} 的命令行客户端。

%prep
%setup -q -n %{name}-%{version}%{codename}
%patch1 -p1 -b .plugins-use-libdir
%patch2 -p1 -b .default-output-pulse
%patch4 -p1 -b .noO0
%patch5 -p1 -b .versionsanity
%patch7 -p1 -b .modplug_header
%patch8 -p1 -b .vorbis_libs
%patch9 -p1
%patch10 -p1

# This header doesn't need to be executable
chmod -x src/include/xmmsclient/xmmsclient++/dict.h

# Clean up paths in wafadmin
# WAFADMIN_FILES=`find wafadmin/ -type f`
# for i in $WAFADMIN_FILES; do
# 	sed -i 's|/usr/lib|%{_libdir}|g' $i
# done
# sed -i 's|"lib"|"%{_lib}"|g' wscript

%build
export CFLAGS="%{optflags}"
export CPPFLAGS="%{optflags}"
export LIBDIR="%{_libdir}"
export PYTHONDIR="%{python_sitearch}"
export XSUBPP="%{_bindir}/xsubpp"
# Now with ruby22, the following waf fails until applying PATCH9
# Really want to know how to patch against waf beforehand...
./waf configure --prefix=%{_prefix} --libdir=%{_libdir} --with-ruby-libdir=%{ruby_vendorlibdir} --with-ruby-archdir=%{ruby_vendorarchdir} \
  --with-perl-archdir=%{perl_archlib} --with-pkgconfigdir=%{_libdir}/pkgconfig -j1 || true
(
	cd .waf-1.*
	cat %PATCH11 | patch -p2
)
# Hacky, hacky, hacky.
patch -p0 < %{_sourcedir}/xmms2-0.8DrO_o-xsubpp-fix.patch
./waf configure --prefix=%{_prefix} --libdir=%{_libdir} --with-ruby-libdir=%{ruby_vendorlibdir} --with-ruby-archdir=%{ruby_vendorarchdir} \
  --with-perl-archdir=%{perl_archlib} --with-pkgconfigdir=%{_libdir}/pkgconfig -j1
./waf build -v %{?_smp_mflags}
# make the docs
doxygen
magic_rpm_clean.sh

%install
rm -rf %{buildroot}
export LIBDIR="%{_libdir}"
export python_LIBDEST="%{python_sitearch}"
./waf install --destdir=%{buildroot} --prefix=%{_prefix} --libdir=%{_libdir} --with-ruby-libdir=%{ruby_vendorlibdir} --with-ruby-archdir=%{ruby_vendorarchdir} \
  --with-perl-archdir=%{perl_archlib} --with-pkgconfigdir=%{_libdir}/pkgconfig

# exec flags for debuginfo
chmod +x %{buildroot}%{_libdir}/%{name}/* %{buildroot}%{_libdir}/libxmmsclient*.so* %{buildroot}%{python_sitearch}/xmmsclient/xmmsapi.so \
	%{buildroot}%{perl_archlib}/auto/Audio/XMMSClient/XMMSClient.so %{buildroot}%{ruby_vendorarchdir}/xmmsclient_*.so

# Convert to utf-8
for i in %{buildroot}%{_mandir}/man1/*.gz; do
	gunzip $i;
done
for i in %{buildroot}%{_mandir}/man1/*.1 xmms2-0.8DrO_o.ChangeLog; do
	iconv -o $i.iso88591 -f iso88591 -t utf8 $i
	mv $i.iso88591 $i
done

install -m0755 %{SOURCE1} %{buildroot}%{_bindir}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS xmms2-0.8DrO_o.ChangeLog COPYING COPYING.GPL COPYING.LGPL README TODO
%{_bindir}/%{name}*
%{_libdir}/libxmmsclient*.so.*
%{_libdir}/%{name}
%{_mandir}/man1/%{name}*
%{_datadir}/pixmaps/%{name}*
%{_datadir}/%{name}

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/
%{_libdir}/libxmmsclient*.so
%{_libdir}/pkgconfig/%{name}-*.pc

%files docs
%defattr(-,root,root,-)
%doc doc/xmms2/html

%files perl
%defattr(-,root,root,-)
%{perl_archlib}/Audio/
%{perl_archlib}/auto/Audio/

%files python
%defattr(-,root,root,-)
%{python_sitearch}/xmmsclient/

%files ruby
%defattr(-,root,root,-)
%{ruby_vendorlibdir}/xmmsclient.rb
%{ruby_vendorlibdir}/xmmsclient/
%{ruby_vendorarchdir}/xmmsclient_ecore.so
%{ruby_vendorarchdir}/xmmsclient_ext.so
%{ruby_vendorarchdir}/xmmsclient_glib.so

%files -n nyxmms2
%defattr(-,root,root,-)
%{_bindir}/nyxmms2

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 0.8-24
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 0.8-23
- 为 Magic 3.0 重建

* Tue Sep 22 2015 Liu Di <liudidi@gmail.com> - 0.8-22
- 为 Magic 3.0 重建

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 0.8-21
- 为 Magic 3.0 重建

* Fri Jul 04 2014 Liu Di <liudidi@gmail.com> - 0.8-20
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 0.8-18
- Rebuild for boost 1.55.0

* Wed May  7 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8-17
- Patch for libmodplug pkgconfig header dir output change
  (c.f. Debian bug 652139, 724487)
- Patch for vorbisenc pkgconfig libs dir output change

* Tue May  6 2014 Tom Callaway <spot@fedoraproject.org> - 0.8-16
- rebuild for new ruby

* Mon Dec 16 2013 Adrian Reber <adrian@lisas.de> - 0.8-15
- Rebuilt for libcdio-0.92

* Thu Sep 26 2013 Rex Dieter <rdieter@fedoraproject.org> 0.8-14
- add explicit avahi build deps

* Sun Aug 11 2013 Tom Callaway <spot@fedoraproject.org> - 0.8-13
- add missing BuildRequires
- add disgusting hack to this awful package to get it building again. whoever invented waf 
  should be forced to endure severe punishment.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 0.8-11
- Rebuild for boost 1.54.0

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.8-10
- Perl 5.18 rebuild

* Tue Apr 02 2013 Vít Ondruch <vondruch@redhat.com> - 0.8-9
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.8-8
- Rebuild for Boost-1.53.0

* Mon Jan 07 2013 Adrian Reber <adrian@lisas.de> - 0.8-7
- Rebuilt for libcdio-0.90

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.8-5
- Perl 5.16 rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-4
- Rebuilt for c++ ABI breakage

* Wed Feb 08 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec  5 2011 Tom Callaway <spot@fedoraproject.org> - 0.8-1
- update to 0.8

* Sun Nov 20 2011 Adrian Reber <adrian@lisas.de> - 0.7-11
- Rebuild for libcdio-0.83

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.7-10
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.7-9
- Perl 5.14 mass rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 17 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.7-7
- bump for libecore

* Thu Sep 02 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 0.7-6
- Bump for libao

* Sat Jul 31 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.7-5
- Add -j1 to the "./waf configure" line.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.7-4.1
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 29 2010 Mike McGrath <mmcgrath@redhat.com> - 0.7-3.1
- Rebuild to fix broken libcore-ver-svn dep

* Wed Jun 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.7-3
- Mass rebuild with perl-5.12.0

* Tue Jun  1 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.7-2
- Rebuild.

* Fri Jan 22 2010 Adrian Reber <adrian@lisas.de> - 0.6-7
- Rebuild for libcdio-0.82

* Tue Jan 19 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.6-6
- rebuild for new boost

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.6-5
- rebuild against perl 5.10.1

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.6-4
- rebuilt with new openssl

* Tue Aug 11 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.6-3
- BuildRequires: glib2-devel, readline-devel, ncurses-devel

* Tue Aug 11 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.6-2
- BuildRequires: SDL-devel

* Tue Aug 11 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.6-1
- update to 0.6

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> - 0.5-5
- rebuild with new openssl

* Tue Jan 13 2009 Adrian Reber <adrian@lisas.de> - 0.5-4
- Rebuild for libcdio-0.81

* Wed Dec 17 2008 Benjamin Kosnik  <bkoz@redhat.com> - 0.5-3
- Rebuild for boost-1.37.0.

* Wed Dec 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.5-2
- new docs subpackage
- many cleanups from package review

* Thu Dec 4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.5-1
- Initial package for Fedora

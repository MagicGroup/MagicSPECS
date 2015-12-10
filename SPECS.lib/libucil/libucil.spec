Summary:	Library to render text and graphic overlays onto video images
Summary(zh_CN.UTF-8): 在视频图像上渲染文本图形的库
Name:		libucil
Version:	0.9.10
Release:	7%{?dist}
License:	GPLv2+
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:		http://www.unicap-imaging.org/
Source0:	http://www.unicap-imaging.org/downloads/%{name}-%{version}.tar.gz

# check return value of theora_encode_init() (#627890)
Patch0:		libucil-0.9.8-bz627890.patch

# fix some memory leaks
Patch1:		libucil-0.9.10-leaks.patch

# fix some compile-time warnings
Patch2:		libucil-0.9.10-warnings.patch

BuildRequires:	intltool, /usr/bin/perl, perl(XML::Parser), gettext, gtk-doc >= 1.4
BuildRequires:	libunicap-devel, glib2-devel, pango-devel, alsa-lib-devel
BuildRequires:	libtheora-devel, libogg-devel, libvorbis-devel, libpng-devel
Obsoletes:	unicap <= 0.9.7-1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Unicap provides a uniform interface to video capture devices. It allows
applications to use any supported video capture device via a single API.
The related ucil library provides easy to use functions to render text
and graphic overlays onto video images.

%description -l zh_CN.UTF-8
在视频图像上渲染文本图形的库。

%package devel
Summary:	Development files for the ucil library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}, pkgconfig, libunicap-devel
Obsoletes:	unicap-devel <= 0.9.7-1

%description devel
The libucil-devel package includes header files and libraries necessary
for developing programs which use the ucil library. It contains the API
documentation of the library, too.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure --disable-rpath --enable-gtk-doc
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Don't install any static .a and libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}.{a,la}
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/unicap/*.h
%{_datadir}/gtk-doc/html/%{name}

%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 0.9.10-7
- 为 Magic 3.0 重建

* Fri Aug 01 2014 Liu Di <liudidi@gmail.com> - 0.9.10-6
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.9.10-5
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Liu Di <liudidi@gmail.com> - 0.9.10-4
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 06 2010 Kamil Dudka <kdudka@redhat.com> 0.9.10-2
- fix some memory leaks and compile-time warnings

* Mon Oct 04 2010 Robert Scheck <robert@fedoraproject.org> 0.9.10-1
- Upgrade to 0.9.10

* Wed Sep 29 2010 Jesse Keating <jkeating@redhat.com> 0.9.8-6
- Rebuilt for gcc bug 634757

* Wed Sep 15 2010 Kamil Dudka <kdudka@redhat.com> 0.9.8-5
- upstream patch for #632439
- check return value of theora_encode_init() (#627890)

* Wed Aug 25 2010 Kamil Dudka <kdudka@redhat.com> 0.9.8-4
- fix SIGSEGV in ucil_theora_encode_thread (#627161)

* Wed Jun 02 2010 Kamil Dudka <kdudka@redhat.com> 0.9.8-3
- fix SIGSEGV in ucil_alsa_fill_audio_buffer (#572966)
- fix SIGSEGV in ucil_theora_encode_thread (#595863)

* Fri Mar 12 2010 Kamil Dudka <kdudka@redhat.com> 0.9.8-2
- build the package in %%build

* Sun Feb 21 2010 Robert Scheck <robert@fedoraproject.org> 0.9.8-1
- Upgrade to 0.9.8 (#530702, #567109, #567110, #567111)
- Splitting of unicap into libunicap, libucil and libunicapgtk

* Sat Oct 24 2009 Robert Scheck <robert@fedoraproject.org> 0.9.7-1
- Upgrade to 0.9.7 (#530702)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Dan Horak <dan[at]danny.cz> 0.9.5-2
- don't require libraw1394 on s390/s390x

* Sun May 03 2009 Robert Scheck <robert@fedoraproject.org> 0.9.5-1
- Upgrade to 0.9.5

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 0.9.3-2
- Rebuild against gcc 4.4 and rpm 4.6

* Mon Oct 13 2008 Robert Scheck <robert@fedoraproject.org> 0.9.3-1
- Upgrade to 0.9.3 (#466825, thanks to Hans de Goede)
- Enabled libv4l support for the new gspca kernel driver

* Sat Aug 09 2008 Robert Scheck <robert@fedoraproject.org> 0.2.23-4
- Rebuild to get missing dependencies back (#443015, #458527)

* Tue Aug 05 2008 Robert Scheck <robert@fedoraproject.org> 0.2.23-3
- Filter the unicap plugins which overlap with libv4l libraries

* Wed Jul 22 2008 Robert Scheck <robert@fedoraproject.org> 0.2.23-2
- Rebuild for libraw1394 2.0.0

* Mon May 19 2008 Robert Scheck <robert@fedoraproject.org> 0.2.23-1
- Upgrade to 0.2.23
- Corrected packaging of cpi/*.so files (thanks to Arne Caspari)

* Sat May 17 2008 Robert Scheck <robert@fedoraproject.org> 0.2.22-1
- Upgrade to 0.2.22 (#446021)

* Sat Feb 16 2008 Robert Scheck <robert@fedoraproject.org> 0.2.19-3
- Added patch to correct libdir paths (thanks to Ralf Corsepius)

* Mon Feb 04 2008 Robert Scheck <robert@fedoraproject.org> 0.2.19-2
- Changes to match with Fedora Packaging Guidelines (#431381)

* Mon Feb 04 2008 Robert Scheck <robert@fedoraproject.org> 0.2.19-1
- Upgrade to 0.2.19
- Initial spec file for Fedora and Red Hat Enterprise Linux

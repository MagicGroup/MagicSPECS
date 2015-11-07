Summary:	Library for manipulating GIF format image files
Summary(zh_CN.UTF-8): 处理 GIF 格式图像文件的库
Name:		giflib
Version:	4.1.6
Release:	9%{?dist}
License:	MIT
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:		http://www.sourceforge.net/projects/%{name}/
Source:		http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
BuildRequires:	libX11-devel, libICE-devel, libSM-devel, libXt-devel
Provides:	libungif = %{version}-%{release}
Obsoletes:	libungif <= %{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The giflib package contains a shared library of functions for loading and
saving GIF format image files. It is API and ABI compatible with libungif,
the library which supported uncompressed GIFs while the Unisys LZW patent
was in effect.

%description -l zh_CN.UTF-8
处理 GIF 格式图像文件的库。它的 API 和 ABI 兼容  libungif。

%package devel
Summary:	Development tools for programs using the giflib library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}
Provides:	libungif-devel = %{version}-%{release}
Obsoletes:	libungif-devel <= %{version}-%{release}

%description devel
The giflib-devel package includes header files, libraries necessary for
developing programs which use the giflib library to load and save GIF format
image files. It contains the documentation of the giflib library, too.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package utils
Summary:	Programs for manipulating GIF format image files
Summary(zh_CN.UTF-8): 处理 GIF 格式图像的程序
Group:		Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Requires:	%{name} = %{version}-%{release}
Provides:	libungif-progs = %{version}-%{release}
Obsoletes:	libungif-progs <= %{version}-%{release}

%description utils
The giflib-utils package contains various programs for manipulating GIF
format image files. Install it if you need to manipulate GIF format image
files.

%description utils -l zh_CN.UTF-8
处理 GIF 格式图像的程序。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags} all

# Handling of libungif compatibility
MAJOR=`echo '%{version}' | sed -e 's/\([0-9]\+\)\..*/\1/'`
%{__cc} $RPM_OPT_FLAGS -shared -Wl,-soname,libungif.so.$MAJOR -Llib/.libs -lgif -o libungif.so.%{version}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' install

# Handling of libungif compatibility
install -p -m 755 libungif.so.%{version} $RPM_BUILD_ROOT%{_libdir}
ln -sf libungif.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libungif.so.4
ln -sf libungif.so.4 $RPM_BUILD_ROOT%{_libdir}/libungif.so

# Don't install any static .a and libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.{a,la}

# Remove makefile relics from documentation
rm -f doc/Makefile*
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files 
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/* util/giffiltr.c util/gifspnge.c
%{_libdir}/lib*.so
%{_includedir}/*.h

%files utils
%defattr(-,root,root,-)
%{_bindir}/*

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 4.1.6-9
- 为 Magic 3.0 重建

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 4.1.6-7
- 为 Magic 3.0 重建

* Wed Nov 30 2011 Liu Di <liudidi@gmail.com> - 4.1.6-6
- 为 Magic 3.0 重建

* Wed Nov 30 2011 Liu Di <liudidi@gmail.com> - 4.1.6-5
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 09 2009 Robert Scheck <robert@fedoraproject.org> 4.1.6-2
- Solved multilib problems with documentation (#465208, #474538)
- Removed static library from giflib-devel package (#225796 #c1)

* Mon Apr 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 4.1.6-1
- update to 4.1.6

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.1.3-9
- Autorebuild for GCC 4.3

* Tue Mar 13 2007 Karsten Hopp <karsten@redhat.com> 4.1.3-8
- add BR libXt-devel, otherwise X support will be disabled

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 
- rebuild

* Mon May 22 2006 Karsten Hopp <karsten@redhat.de> 4.1.3-7
- buildrequires libICE-devel, libSM-devel

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.1.3-6.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.1.3-6.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov  1 2005 Matthias Clasen <mclasen@redhat.com> 4.1.3-6
- Switch requires to modular X

* Wed Sep 21 2005 Toshio Kuratomi <toshio@tiki-lounge.com> 4.1.3-5
- Merge an option on the empty library link line.
- Obsolete libungif progs package.
- Rename -progs to -utils as FC packages seem to have moved in this direction
  for subpackages.
 
* Tue Sep 20 2005 Toshio Kuratomi <toshio@tiki-lounge.com> 4.1.3-4
- Modify the way we provide libungif compatibility by building an empty
  library that requires libgif.
- Remove chmod in install.  It doesn't seem to be necessary.
- Add a patch to fix a problem with long being 64 bit on x86_64 but the code
  assuming it was 32 bit.
  
* Mon Sep 19 2005 Toshio Kuratomi <toshio@tiki-lounge.com> 4.1.3-1
- Port package from libungif to giflib.

Name:		physfs
Version:	2.0.3
Release:	6%{?dist}
License:	zlib
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Summary:	Library to provide abstract access to various archives
Summary(zh_CN.UTF-8): 提供了多种归档文件抽象层的库
URL:		http://www.icculus.org/physfs/
Source0:	http://www.icculus.org/physfs/downloads/physfs-%{version}.tar.bz2
Patch1:		physfs-2.0.2-system-lzma-sdk.patch
BuildRequires:	doxygen, zlib-devel, readline-devel, libtool, cmake
# Only needed to build a test program.
# BuildRequires:	wxGTK-devel
BuildRequires:	lzma-sdk457-devel

%description
PhysicsFS is a library to provide abstract access to various archives. It is
intended for use in video games, and the design was somewhat inspired by Quake 
3's file subsystem. The programmer defines a "write directory" on the physical 
filesystem. No file writing done through the PhysicsFS API can leave that 
write directory, for security. For example, an embedded scripting language 
cannot write outside of this path if it uses PhysFS for all of its I/O, which 
means that untrusted scripts can run more safely. Symbolic links can be 
disabled as well, for added safety. For file reading, the programmer lists 
directories and archives that form a "search path". Once the search path is 
defined, it becomes a single, transparent hierarchical filesystem. This makes 
for easy access to ZIP files in the same way as you access a file directly on 
the disk, and it makes it easy to ship a new archive that will override a 
previous archive on a per-file basis. Finally, PhysicsFS gives you 
platform-abstracted means to determine if CD-ROMs are available, the user's 
home directory, where in the real filesystem your program is running, etc.

%description -l zh_CN.UTF-8
提供了多种归档文件抽象层的库。

%package devel
Summary:	Development libraries and headers for physfs
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the libraries and headers necessary for developing
packages with physfs functionality.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch1 -p1 -b .system-lzmasdk
rm -rf lzma

%build
%cmake .
make %{?_smp_mflags} LIBTOOL=%{_bindir}/libtool
doxygen

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3
install -m0644 docs/man/man3/* $RPM_BUILD_ROOT%{_mandir}/man3

# Handle man page conflicts (bz #183705)
mv $RPM_BUILD_ROOT%{_mandir}/man3/author.3 $RPM_BUILD_ROOT%{_mandir}/man3/physfs-author.3
mv $RPM_BUILD_ROOT%{_mandir}/man3/description.3 $RPM_BUILD_ROOT%{_mandir}/man3/physfs-description.3
mv $RPM_BUILD_ROOT%{_mandir}/man3/extension.3 $RPM_BUILD_ROOT%{_mandir}/man3/physfs-extension.3
mv $RPM_BUILD_ROOT%{_mandir}/man3/major.3 $RPM_BUILD_ROOT%{_mandir}/man3/physfs-major.3
mv $RPM_BUILD_ROOT%{_mandir}/man3/minor.3 $RPM_BUILD_ROOT%{_mandir}/man3/physfs-minor.3
mv $RPM_BUILD_ROOT%{_mandir}/man3/patch.3 $RPM_BUILD_ROOT%{_mandir}/man3/physfs-patch.3
mv $RPM_BUILD_ROOT%{_mandir}/man3/url.3 $RPM_BUILD_ROOT%{_mandir}/man3/physfs-url.3

# Rename poorly named manpages
for i in Deinit Free Init Malloc Realloc opaque; do
  mv $RPM_BUILD_ROOT%{_mandir}/man3/$i.3 $RPM_BUILD_ROOT%{_mandir}/man3/physfs-$i.3
done

# Fix multilib conflicts
touch -r LICENSE.txt docs/html/*
touch -r LICENSE.txt docs/latex/*

# Get rid of static library.
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.a
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc CHANGELOG.txt CREDITS.txt LICENSE.txt TODO.txt
%{_libdir}/*.so.*

%files devel
%doc docs/html/
%{_bindir}/test_physfs
%{_includedir}/physfs.h
%{_libdir}/*.so
%{_mandir}/man3/*

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 2.0.3-6
- 为 Magic 3.0 重建

* Sat Sep 19 2015 Liu Di <liudidi@gmail.com> - 2.0.3-5
- 为 Magic 3.0 重建

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 22 2013 Tom Callaway <spot@fedoraproject.org> - 2.0.3-1
- update to 2.0.3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec  9 2011 Tom Callaway <spot@fedoraproject.org> - 2.0.2-1
- update to 2.0.2

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.2-2
- fix soname to match 1.0.1 (upstream made it go from .1 to .0 ?)

* Wed Aug 19 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.2-1
- update to 1.0.2 (last in 1.0 series)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.1-9
- do not package the tex docs, the html docs are fine
- drop static lib to see if anyone misses it

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.1-8
- Autorebuild for GCC 4.3

* Mon Oct 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.1-7
- fix multilib conficts

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.1-6
- fix license tag, rebuild for BuildID

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.1-5
- bump for fc6

* Tue Mar  7 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.1-4
- resolve man page conflicts (bz #183705)

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.1-3
- bump for FC-5

* Fri Sep 23 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.1-2
- add docs for devel

* Fri Aug 19 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.1-1
- initial package for Fedora Extras

Summary: Exif and Iptc metadata manipulation library
Summary(zh_CN.UTF-8): Exif 和 Iptc 元数据处理库
Name:	 exiv2
Version: 0.22
Release: 2%{?dist}

License: GPLv2+
Group:	 Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
URL: 	 http://www.exiv2.org/
Source0: http://www.exiv2.org/exiv2-%{version}%{?pre:-%{pre}}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

## upstream patches

BuildRequires: chrpath
BuildRequires: expat-devel
BuildRequires: gettext
BuildRequires: pkgconfig
BuildRequires: zlib-devel
# docs
#BuildRequires: doxygen graphviz libxslt

Requires: %{name}-libs%{?_isa} = %{version}-%{release}


%description
A command line utility to access image metadata, allowing one to:
* print the Exif metadata of Jpeg images as summary info, interpreted values,
  or the plain data for each tag
* print the Iptc metadata of Jpeg images
* print the Jpeg comment of Jpeg images
* set, add and delete Exif and Iptc metadata of Jpeg images
* adjust the Exif timestamp (that's how it all started...)
* rename Exif image files according to the Exif timestamp
* extract, insert and delete Exif metadata (including thumbnails),
  Iptc metadata and Jpeg comments

%description -l zh_CN.UTF-8
Exif 和 Iptc 元数据处理库。

%package devel
Summary: Header files, libraries and development documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:	 Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: pkgconfig
%description devel
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package libs
Summary: Exif and Iptc metadata manipulation library
Summary(zh_CN.UTF-8): %{name} 的运行库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
%description libs
A C++ library to access image metadata, supporting full read and write access
to the Exif and Iptc metadata, Exif MakerNote support, extract and delete 
methods for Exif thumbnails, classes to access Ifd and so on.

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%prep
%setup -q -n %{name}-%{version}%{?pre:-%{pre}}

mkdir doc/html


%build
%configure \
  --disable-rpath \
  --disable-static 

make %{?_smp_mflags} 


%install
rm -rf %{buildroot} 

make install DESTDIR=%{buildroot}
magic_rpm_clean.sh
%find_lang exiv2

## Unpackaged files
rm -fv %{buildroot}%{_libdir}/libexiv2.la

## fix perms on installed lib
ls -l     %{buildroot}%{_libdir}/libexiv2.so.*
chmod 755 %{buildroot}%{_libdir}/libexiv2.so.*

## nuke rpaths
chrpath --list   %{buildroot}%{_bindir}/exiv2 && \
chrpath --delete %{buildroot}%{_bindir}/exiv2


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion exiv2)" = "%{version}"


%clean
rm -rf %{buildroot} 


%files
%defattr(-,root,root,-)
%doc COPYING README
%{_bindir}/exiv2
%{_mandir}/man1/*

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs -f exiv2.lang
%defattr(-,root,root,-)
%{_libdir}/libexiv2.so.11*

%files devel
%defattr(-,root,root,-)
%doc doc/html
%{_includedir}/exiv2/
%{_libdir}/libexiv2.so
%{_libdir}/pkgconfig/exiv2.pc


%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.22-2
- 为 Magic 3.0 重建

* Fri Oct 14 2011 Rex Dieter <rdieter@fedoraproject.org> 0.22-1
- exiv2-0.22

* Tue Sep 27 2011 Rex Dieter <rdieter@fedoraproject.org> 0.21.1-3
- New Tamron 70-300 mm lens improperly recognized (#708403)

* Mon Sep 26 2011 Rex Dieter <rdieter@fedoraproject.org> 0.21.1-2
- gthumb crashes because of bug in exiv2 0.21.1 (#741429)

* Sat Feb 26 2011 Rex Dieter <rdieter@fedoraproject.org> 0.21.1-1
- exiv2-0.21.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Rex Dieter <rdieter@fedoraproject.org> 0.21-2
- Move ldconfig scriptlet calls to -libs (#672361)

* Wed Dec 01 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.21-1
- exiv2-0.21

* Sun May 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.20-1
- exiv2-0.20

* Wed Dec 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.19-1
- exiv2-0.19 (#552275)

* Sun Dec 13 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.18.2-3
- -libs unconditional
- tighten deps using %%?_isa

* Fri Aug 07 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.18.2-2
- (again) drop -fvisibility-inlines-hidden (#496050)

* Fri Jul 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.18.2-1
- exiv2-0.18.2
- drop visibility patch

* Fri Apr 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.18.1-1
- exiv2-0.18.1
- drop -fvisibility-inlines-hidden (#496050)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 18 2008 Rex Dieter <rdieter@fedoraproject.org> 0.18-1
- exiv2-0.18

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 0.17.2-2
- rebuild for pkgconfig deps

* Mon Jun 23 2008 Rex Dieter <rdieter@fedoraproject.org> 0.17.1-1
- exiv2-0.17.1

* Mon Feb 11 2008 Rex Dieter <rdieter@fedoraproject.org> 0.16-2
- respin (gcc43)
- gcc43 patch

* Sun Jan 13 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 0.16-1
- eviv2-0.16

* Mon Dec 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.16-0.3.pre1
- CVE-2007-6353 (#425924)

* Mon Nov 26 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.16-0.2.pre1
- -libs subpkg toggle (f8+)

* Tue Nov 13 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.16-0.1.pre1
- exiv2-0.16-pre1

* Tue Sep 18 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.15-4
- -libs: -Requires: %%name

* Tue Aug 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.15-3
- -libs subpkg to be multilib-friendlier (f8+)

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.15-2
- License: GPLv2+

* Thu Jul 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.15-1
- exiv2-0.15

* Mon Apr 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.14-1
- exiv2-0.14

* Tue Nov 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.12-1
- exiv2-0.12

* Wed Oct 04 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.11-3
- respin

* Tue Sep 19 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.11-2
- BR: zlib-devel

* Tue Sep 19 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.11-1
- exiv2-0.11

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.10-2
- fc6 respin

* Sat Jun 03 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.10-1
- 0.10

* Wed May 17 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.1-3
- cleanup %%description
- set eXecute bit on installed lib.
- no_rpath patch
- deps patch (items get (re)compiled on *every* call to 'make')

* Wed May 17 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.1-2
- %%post/%%postun: /sbin/ldconfig

* Tue May 16 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.1-1
- first try

Name:           liboggz
Version:        1.1.1
Release:        7%{?dist}
Summary:        Simple programming interface for Ogg files and streams
Summary(zh_CN.UTF-8): Ogg 文件和流的简单程序接口

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        BSD
URL:            http://www.annodex.net/
Source0:        http://www.annodex.net/software/liboggz/download/%{name}-%{version}.tar.gz
# Always have oggz_off_t == loff_t even on 64-bit platforms
Patch0:		liboggz-1.1.1-multilib.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libogg-devel >= 1.0
BuildRequires:  doxygen
BuildRequires:  docbook-utils

%description
Oggz provides a simple programming interface for reading and writing
Ogg files and streams. Ogg is an interleaving data container developed
by Monty at Xiph.Org, originally to support the Ogg Vorbis audio
format.

%description -l zh_CN.UTF-8
Ogg 文件和流的简单程序接口。

%package devel
Summary:	Files needed for development using liboggz
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       liboggz = %{version}-%{release}
Requires:       libogg-devel >= 1.0
Requires:       pkgconfig

%description devel
Oggz provides a simple programming interface for reading and writing
Ogg files and streams. Ogg is an interleaving data container developed
by Monty at Xiph.Org, originally to support the Ogg Vorbis audio
format.

This package contains the header files and documentation needed for
development using liboggz.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary:        Documentation for liboggz
Summary(zh_CN.UTF-8): %{name} 的文档
Group:		Documentation
Group(zh_CN.UTF-8): 文档
Requires:	liboggz = %{version}-%{release}

%description doc
Oggz provides a simple programming interface for reading and writing
Ogg files and streams. Ogg is an interleaving data container developed
by Monty at Xiph.Org, originally to support the Ogg Vorbis audio
format.

This package contains HTML documentation needed for development using
liboggz.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .multilib

%build
%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%check
# Tests disabled for moment because of rpath issue
#make check

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall docdir=$RPM_BUILD_ROOT%{_datadir}/doc/%{name}-doc-%{version} \
	     INSTALL="%{__install} -p"

# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# not particularly interested in the tex docs, the html version has everything
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-doc-%{version}/latex

# Multilib fix: ensure generated headers have timestamps
# independent of build time
(cd include/oggz &&
    touch -r oggz_off_t_generated.h.in.multilib \
      $RPM_BUILD_ROOT%{_includedir}/oggz/oggz_off_t_generated.h
)
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

                                                                                
%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING README
# 0 length NEWS file
# %doc NEWS
%{_libdir}/liboggz.so.*
%{_mandir}/man1/*
%{_bindir}/oggz*

%files devel
%defattr(-,root,root)
%{_includedir}/oggz
%{_libdir}/liboggz.so
%{_libdir}/pkgconfig/oggz.pc

%files doc
%defattr(-,root,root)
%doc %{_docdir}/%{name}-doc-%{version}


%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 1.1.1-7
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.1.1-6
- 为 Magic 3.0 重建

* Wed Jul 23 2014 Liu Di <liudidi@gmail.com> - 1.1.1-5
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.1.1-4
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Liu Di <liudidi@gmail.com> - 1.1.1-3
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat May 29 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 1.1.1-1
- Update 1.1.1
- (CVE-2009-3377) CVE-2009-3377 liboggz: unspecified security fixes mentioned in MFSA 2009-63

* Thu Feb 04 2010 Adam Jackson <ajax@redhat.com> 0.9.8-5
- --disable-static, drop the .a files

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 30 2008 Michel Salim <salimma@fedoraproject.org> - 0.9.8-2
- Multilib fixes (bugs #342291, #477291)

* Mon Jul  7 2008 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.9.8-1
- Update to 0.9.8

* Wed May 21 2008 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.9.7-1
- Update to 0.9.7

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.5-2
- Autorebuild for GCC 4.3

* Fri Jan 12 2007 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.5-1
- new upstream release

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.9.4-3
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.4-2
- rebuilt

* Sun Mar 05 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.4-1
- new upstream release
- removed patch, was applied upstream

* Sat Nov 12 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.3-1
- new upstream release

* Mon Jul 18 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.2-1
- new upstream version
- removed patches
- moved devel docs to versioned location

* Mon Jun 13 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.1-2: rpmlint cleanup

* Fri Jun 03 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.1-1: initial package

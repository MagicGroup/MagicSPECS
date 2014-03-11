%global compat_ver xz-4.999.9beta

Summary:	LZMA compression utilities
Name:		xz
Version:	5.1.1
Release:	3alpha%{?dist}
License:	LGPLv2+
Group:		Applications/File
# official upstream release
Source0:	http://tukaani.org/%{name}/%{name}-%{version}alpha.tar.gz
# source created as "make dist" in checked out GIT tree
Source1:	%{compat_ver}.20100401git.tar.bz2
URL:		http://tukaani.org/%{name}/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	%{name}-libs = %{version}-%{release}

%description
XZ Utils are an attempt to make LZMA compression easy to use on free (as in
freedom) operating systems. This is achieved by providing tools and libraries
which are similar to use than the equivalents of the most popular existing
compression algorithms.

LZMA is a general purpose compression algorithm designed by Igor Pavlov as
part of 7-Zip. It provides high compression ratio while keeping the
decompression speed fast.

%package 	libs
Summary:	Libraries for decoding LZMA compression
Group:		System Environment/Libraries
License:	LGPLv2+

%description 	libs
Libraries for decoding files compressed with LZMA or XZ utils.

%package 	compat-libs
Summary:	Compatibility libraries for decoding LZMA compression
Group:		System Environment/Libraries
License:	LGPLv2+

%description 	compat-libs
Compatibility libraries for decoding files compressed with LZMA or XZ utils.
This particular package ships libraries from %{compat_ver} as of 1st of April 2010.

%package 	devel
Summary:	Devel libraries & headers for liblzma
Group:		Development/Libraries
License:	LGPLv2+
Requires:	%{name}-libs = %{version}-%{release}
Requires:	pkgconfig

%description	devel
Devel libraries and headers for liblzma.

%package 	lzma-compat
Summary:	Older LZMA format compatibility binaries
Group:		Development/Libraries
# lz{grep,diff,more} are GPLv2+. Other binaries are LGPLv2+
License:	GPLv2+ and LGPLv2+
Requires:	%{name} = %{version}-%{release}
Obsoletes:	lzma < %{version}
Provides:	lzma = %{version}

%description	lzma-compat
The lzma-compat package contains compatibility links for older
commands that deal with the older LZMA format.

%prep
%setup -q -a1 -n %{name}-%{version}alpha

%build
CFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64" \
CXXFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64" \
%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

pushd %{compat_ver}
%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_docdir}/%{name}
rm -rf %{buildroot}%{_datadir}/locale
cp -r %{compat_ver}/src/liblzma/.libs/liblzma.so.0* %{buildroot}%{_libdir}

%check
LD_LIBRARY_PATH=$PWD/src/liblzma/.libs make check

%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post compat-libs -p /sbin/ldconfig

%postun compat-libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING* ChangeLog NEWS README THANKS TODO
%{_bindir}/*xz*
%{_mandir}/man1/*xz*

%files libs
%defattr(-,root,root,-)
%doc COPYING*
%{_libdir}/lib*.so.5*

%files compat-libs
%defattr(-,root,root,-)
%doc COPYING*
%{_libdir}/lib*.so.0*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/lzma
%{_includedir}/lzma/*.h
%{_includedir}/lzma.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/liblzma.pc

%files lzma-compat
%defattr(-,root,root,-)
%{_bindir}/*lz*
%{_mandir}/man1/*lz*

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 5.1.1-3alpha
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.1-2alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 16 2011 Jindrich Novy <jnovy@redhat.com> 5.1.1alpha-1
- update to 5.1.1alpha

* Mon Jun 20 2011 Jindrich Novy <jnovy@redhat.com> 5.0.3-2
- better to have upstream tarballs in different formats than XZ
  to allow bootstrapping (#714765)

* Mon May 23 2011 Jindrich Novy <jnovy@redhat.com> 5.0.3-1
- update to 5.0.3

* Mon Apr 04 2011 Jindrich Novy <jnovy@redhat.com> 5.0.2-1
- update to 5.0.2

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 29 2011 Jindrich Novy <jnovy@redhat.com> 5.0.1-1
- update to 5.0.1

* Tue Oct 26 2010 Jindrich Novy <jnovy@redhat.com> 5.0.0-4
- call ldconfig for compat-libs and fix description

* Mon Oct 25 2010 Jindrich Novy <jnovy@redhat.com> 5.0.0-3
- introduce compat-libs subpackage with older soname to
  resolve problems with soname bump and for packages requiring
  older xz-4.999.9beta

* Mon Oct 25 2010 Jindrich Novy <jnovy@redhat.com> 5.0.0-2
- rebuild

* Mon Oct 25 2010 Jindrich Novy <jnovy@redhat.com> 5.0.0-1
- update to the new upstream release

* Sat Oct 16 2010 Jindrich Novy <jnovy@redhat.com> 4.999.9-0.3.beta.212.gacbc
- update to latest git snapshot

* Thu Apr 01 2010 Jindrich Novy <jnovy@redhat.com> 4.999.9-0.2.20100401.beta
- sync with upstream (#578925)

* Thu Feb 18 2010 Jindrich Novy <jnovy@redhat.com> 4.999.9-0.2.20091007.beta
- move xz man pages to main package, leave lzma ones where they belong (#566484)

* Wed Oct 07 2009 Jindrich Novy <jnovy@redhat.com> 4.999.9-0.1.20091007.beta
- sync with upstream again

* Fri Oct 02 2009 Jindrich Novy <jnovy@redhat.com> 4.999.9-0.1.20091002.beta
- sync with upstream to generate the same archives on machines with different
  endianess

* Fri Aug 28 2009 Jindrich Novy <jnovy@redhat.com> 4.999.9-0.1.beta
- update to 4.999.9beta

* Mon Aug 17 2009 Jindrich Novy <jnovy@redhat.com> 4.999.8-0.10.beta.20090817git
- sync with upstream because of #517806

* Tue Aug 04 2009 Jindrich Novy <jnovy@redhat.com> 4.999.8-0.9.beta.20090804git
- update to the latest GIT snapshot

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.999.8-0.8.beta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Bill Nottingham <notting@redhat.com> 4.999.8-0.7.beta
- tweak summary
- add %%check section (<tibbs@math.uh.edu>)
 
* Thu Jul 09 2009 Bill Nottingham <notting@redhat.com> 4.999.8-0.6.beta
- fix release versioning to match guidelines
- fix up lzma-compat summary/description
- tweak licensing

* Mon Jun 22 2009 Jindrich Novy <jnovy@redhat.com> 4.999.8beta-0.5
- introduce lzma-compat subpackage

* Fri Jun 19 2009 Jindrich Novy <jnovy@redhat.com> 4.999.8beta-0.4
- try to not to conflict with lzma

* Thu Jun 18 2009 Jindrich Novy <jnovy@redhat.com> 4.999.8beta-0.3
- obsolete but don't provide lzma, they are largely incompatible
- put beta to Release

* Wed Jun 17 2009 Jindrich Novy <jnovy@redhat.com> 4.999.8beta-0.2
- obsolete old lzma
- add Requires: pkgconfig

* Tue Jun 16 2009 Jindrich Novy <jnovy@redhat.com> 4.999.8beta-0.1
- package XZ Utils, based on LZMA Utils packaged by Per Patrice Bouchand

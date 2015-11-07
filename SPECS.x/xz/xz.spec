%global compat_ver xz-4.999.9beta

Summary:	LZMA compression utilities
Summary(zh_CN.UTF-8): LZMA 压缩工具
Name:		xz
Version:	5.2.2
Release:	3%{?dist}
License:	LGPLv2+
Group:		Applications/File
Group(zh_CN.UTF-8): 应用程序/文件
# official upstream release
Source0:	http://tukaani.org/%{name}/%{name}-%{version}.tar.gz

Source100:	colorxzgrep.sh
Source101:	colorxzgrep.csh

# 临时补丁，和 openssl 版本有关
Patch1:		xz-force-use-internalsha.patch

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

%description -l zh_CN.UTF-8
LZMA 压缩工具。

%package 	libs
Summary:	Libraries for decoding LZMA compression
Summary(zh_CN.UTF-8): %{name} 的运行库
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	LGPLv2+

%description 	libs
Libraries for decoding files compressed with LZMA or XZ utils.

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%package 	static
Summary:	Statically linked library for decoding LZMA compression
Summary(zh_CN.UTF-8): %{name} 的静态库
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 开发/库
License:	Public Domain

%description 	static
Statically linked library for decoding files compressed with LZMA or
XZ utils.  Most users should *not* install this.

%description static -l zh_CN.UTF-8
%{name} 的静态库。

%package 	compat-libs
Summary:	Compatibility libraries for decoding LZMA compression
Summary(zh_CN.UTF-8): %{name} 的兼容运行库
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	LGPLv2+

%description 	compat-libs
Compatibility libraries for decoding files compressed with LZMA or XZ utils.
This particular package ships libraries from %{compat_ver} as of 1st of April 2010.

%description compat-libs -l zh_CN.UTF-8
%{name} 的兼容运行库。

%package 	devel
Summary:	Devel libraries & headers for liblzma
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:	LGPLv2+
Requires:	%{name}-libs = %{version}-%{release}
Requires:	pkgconfig

%description	devel
Devel libraries and headers for liblzma.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package 	lzma-compat
Summary:	Older LZMA format compatibility binaries
Summary(zh_CN.UTF-8): 旧版本 LZMA 格式兼容程序
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
# lz{grep,diff,more} are GPLv2+. Other binaries are LGPLv2+
License:	GPLv2+ and LGPLv2+
Requires:	%{name} = %{version}-%{release}
Obsoletes:	lzma < %{version}
Provides:	lzma = %{version}

%description	lzma-compat
The lzma-compat package contains compatibility links for older
commands that deal with the older LZMA format.

%description lzma-compat -l zh_CN.UTF-8
旧版本 LZMA 格式兼容程序。

%prep
%setup -q
%patch1 -p1

for i in `find . -name config.sub`; do
  perl -pi -e "s/ppc64-\*/ppc64-\* \| ppc64p7-\*/" $i
done

%build
CFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64"
%ifarch %{power64}
    CFLAGS=`echo $CFLAGS | xargs -n 1 | sed 's|^-O2$|-O3|g' | xargs -n 100`
%endif
export CFLAGS

%configure
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la

# xzgrep colorization
%global profiledir %{_sysconfdir}/profile.d
mkdir -p %{buildroot}%{profiledir}
install -p -m 644 %{SOURCE100} %{buildroot}%{profiledir}
install -p -m 644 %{SOURCE101} %{buildroot}%{profiledir}
magic_rpm_clean.sh
%find_lang %name || :

%check
LD_LIBRARY_PATH=$PWD/src/liblzma/.libs make check

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files 
%{_bindir}/*xz*
%{_mandir}/man1/*xz*
%{profiledir}/*
%{_docdir}/xz/*

%files libs
%{_libdir}/lib*.so.5*

%files static
%{_libdir}/liblzma.a

%files devel
%dir %{_includedir}/lzma
%{_includedir}/lzma/*.h
%{_includedir}/lzma.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/liblzma.pc

%files lzma-compat
%{_bindir}/*lz*
%{_mandir}/man1/*lz*

%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 5.2.2-3
- 为 Magic 3.0 重建

* Tue Oct 27 2015 Liu Di <liudidi@gmail.com> - 5.2.2-2
- 更新到 5.2.2

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

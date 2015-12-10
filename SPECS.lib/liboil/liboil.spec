Summary: Library of Optimized Inner Loops, CPU optimized functions
Summary(zh_CN.UTF-8): 优化内部循环的库，CPU 优化函数
Name: liboil
Version: 0.3.17
Release: 3%{?dist}
# See COPYING which details everything, various BSD licenses apply
License: BSD
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://liboil.freedesktop.org/
Source: http://liboil.freedesktop.org/download/liboil-%{version}.tar.gz

# https://bugs.freedesktop.org/show_bug.cgi?id=15392
Patch1: liboil-0.3.13-s390.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=435771
Patch4: liboil-0.3.13-disable-ppc64-opts.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: glib2-devel

%description
Liboil is a library of simple functions that are optimized for various CPUs.
These functions are generally loops implementing simple algorithms, such as
converting an array of N integers to floating-poing numbers or multiplying
and summing an array of N numbers. Clearly such functions are candidates for
significant optimization using various techniques, especially by using
extended instructions provided by modern CPUs (Altivec, MMX, SSE, etc.).

%description -l zh_CN.UTF-8
优化内部循环的库，CPU 优化函数。

%package devel
Summary: Development files and static library for liboil
Summary(zh_CN.UTF-8): %name 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}, pkgconfig

%description devel
Liboil is a library of simple functions that are optimized for various CPUs.
These functions are generally loops implementing simple algorithms, such as
converting an array of N integers to floating-poing numbers or multiplying
and summing an array of N numbers. Clearly such functions are candidates for
significant optimization using various techniques, especially by using
extended instructions provided by modern CPUs (Altivec, MMX, SSE, etc.).

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
#%patch1 -p1 -b .s390
%patch4 -p0 -b .disable-ppc64-opts

# Disable Altivec, so that liboil doesn't SIGILL on non-Altivec PPCs
# See https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=252179#c15
#sed -i 's/CFLAGS="$CFLAGS "-maltivec""/CFLAGS="$CFLAGS "-fno-tree-vectorize -Wa,-maltivec""/' configure
#sed -i 's/LIBOIL_CFLAGS -maltivec/LIBOIL_CFLAGS -fno-tree-vectorize -Wa,-maltivec/' configure

%build
%configure
# Remove standard rpath from oil-bugreport
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# multi-jobbed make makes the build fail:
# ./build_prototypes_doc >liboilfuncs-doc.h
# /bin/sh: ./build_prototypes_doc: No such file or directory
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/*.a


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING BUG-REPORTING NEWS README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/oil-bugreport
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%doc %{_datadir}/gtk-doc/html/liboil/


%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 0.3.17-3
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.3.17-2
- 为 Magic 3.0 重建

* Wed Jul 23 2014 Liu Di <liudidi@gmail.com> - 0.3.17-1
- 更新到 0.3.17

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.3.16-3
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Liu Di <liudidi@gmail.com> - 0.3.16-2
- 为 Magic 3.0 重建



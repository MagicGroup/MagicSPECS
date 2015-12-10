%define releasedate 20150728
%define major 4
%define minor 4
%define update 0
%define dotver %{major}.%{minor}
%define sourcebasename tbb%{major}%{minor}_%{releasedate}oss

%define sourcefilename %{sourcebasename}_src.tgz

Name:    tbb
Summary: The Threading Building Blocks library abstracts low-level threading details
Summary(zh_CN.UTF-8): 抽象低级线程信息的线程构建库
Version: %{dotver}
Release: 7.%{releasedate}%{?dist}
License: GPLv2 with exceptions
Group:   Development/Tools
Group(zh_CN.UTF-8): 开发/工具
URL:     http://threadingbuildingblocks.org/

Source0: http://threadingbuildingblocks.org/sites/default/files/software_releases/source/%{sourcebasename}_src.tgz
# These two are downstream sources.
Source6: tbb.pc
Source7: tbbmalloc.pc
Source8: tbbmalloc_proxy.pc

# Propagate CXXFLAGS variable into flags used when compiling C++.
# This so that RPM_OPT_FLAGS are respected.
Patch1: tbb-3.0-cxxflags.patch

# Replace mfence with xchg (for 32-bit builds only) so that TBB
# compiles and works supported hardware.  mfence was added with SSE2,
# which we still don't assume.
Patch2: tbb-4.0-mfence.patch

# Don't snip -Wall from C++ flags.  Add -fno-strict-aliasing, as that
# uncovers some static-aliasing warnings.
# Related: https://bugzilla.redhat.com/show_bug.cgi?id=1037347
Patch3: tbb-4.3-dont-snip-Wall.patch

BuildRequires: libstdc++-devel

%description
Threading Building Blocks (TBB) is a C++ runtime library that
abstracts the low-level threading details necessary for optimal
multi-core performance.  It uses common C++ templates and coding style
to eliminate tedious threading implementation work.

TBB requires fewer lines of code to achieve parallelism than other
threading models.  The applications you write are portable across
platforms.  Since the library is also inherently scalable, no code
maintenance is required as more processor cores become available.

%description -l zh_CN.UTF-8
抽象低级线程信息的线程构建库。

%package devel
Summary: The Threading Building Blocks C++ headers and shared development libraries
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and shared object symlinks for the Threading Building
Blocks (TBB) C++ libraries.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary: The Threading Building Blocks documentation
Summary(zh_CN.UTF-8): %{name} 的文档
Group: Documentation
Group(zh_CN.UTF-8): 文档

%description doc
PDF documentation for the user of the Threading Building Block (TBB)
C++ library.
%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q -n %{sourcebasename}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
make %{?_smp_mflags} CXXFLAGS="$RPM_OPT_FLAGS" tbb_build_prefix=obj
for file in %{SOURCE6} %{SOURCE7} %{SOURCE8}; do
    sed 's/_FEDORA_VERSION/%{major}.%{minor}.%{update}/' ${file} \
        > $(basename ${file})
done

%check
%ifarch ppc64le
make test
%endif

%install
mkdir -p $RPM_BUILD_ROOT/%{_libdir}
mkdir -p $RPM_BUILD_ROOT/%{_includedir}

pushd build/obj_release
    for file in libtbb{,malloc{,_proxy}}; do
        install -p -D -m 755 ${file}.so.2 $RPM_BUILD_ROOT/%{_libdir}
        ln -s $file.so.2 $RPM_BUILD_ROOT/%{_libdir}/$file.so
    done
popd

pushd include
    find tbb -type f ! -name \*.htm\* -exec \
        install -p -D -m 644 {} $RPM_BUILD_ROOT/%{_includedir}/{} \
    \;
popd

for file in %{SOURCE6} %{SOURCE7} %{SOURCE8}; do
    install -p -D -m 644 $(basename ${file}) \
	$RPM_BUILD_ROOT/%{_libdir}/pkgconfig/$(basename ${file})
done
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING doc/Release_Notes.txt
%{_libdir}/*.so.2

%files devel
%doc CHANGES
%{_includedir}/tbb
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files doc
%doc doc/Release_Notes.txt
%doc doc/html

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 4.4-7.20150728
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 4.4-6.20150728
- 为 Magic 3.0 重建

* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 4.4-5.20150728
- 为 Magic 3.0 重建

* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 4.4-4.20150728
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-3.20141204
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 4.3-2.20141204
- Rebuilt for GCC 5 C++11 ABI change

* Mon Jan 19 2015 Petr Machata <pmachata@redhat.com> - 4.3-1.20141204
- Rebase to 4.3u2
- Drop ExclusiveArch

* Thu Sep 25 2014 Karsten Hopp <karsten@redhat.com> 4.1-9.20130314
- enable ppc64le and run 'make test' on that new arch

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-8.20130314
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-7.20130314
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jan 12 2014 Peter Robinson <pbrobinson@fedoraproject.org> 4.1-6.20130314
- Build on aarch64, minor spec cleanups

* Tue Dec  3 2013 Petr Machata <pmachata@redhat.com> - 4.1-5.20130314
- Fix building with -Werror=format-security (tbb-4.1-dont-snip-Wall.patch)

* Thu Oct  3 2013 Petr Machata <pmachata@redhat.com> - 4.1-4.20130314
- Fix %%install to also install include files that are not named *.h

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-3.20130314
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Petr Machata <pmachata@redhat.com> - 4.1-3.20130314
- Enable ARM arches

* Wed May 22 2013 Petr Machata <pmachata@redhat.com> - 4.1-2.20130314
- Fix mfence patch.  Since the __TBB_full_memory_fence macro was
  function-call-like, it stole () intended for function invocation.

* Wed May 22 2013 Petr Machata <pmachata@redhat.com> - 4.1-1.20130314
- Rebase to 4.1 update 3

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-7.20120408
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Petr Machata <pmachata@redhat.com> - 4.0-6.20120408
- Fix build on PowerPC

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-5.20120408
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun  7 2012 Petr Machata <pmachata@redhat.com> - 4.0-4.20120408
- Rebase to 4.0 update 4
- Refresh Getting_Started.pdf, Reference.pdf, Tutorial.pdf
- Provide pkg-config files
- Resolves: #825402

* Thu Apr 05 2012 Karsten Hopp <karsten@redhat.com> 4.0-3.20110809
- tbb builds now on PPC(64)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-2.20110809
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 18 2011 Petr Machata <pmachata@redhat.com> - 4.0-1.20110809
- Rebase to 4.0
  - Port the mfence patch
  - Refresh the documentation bundle

* Tue Jul 26 2011 Petr Machata <pmachata@redhat.com> - 3.0-1.20110419
- Rebase to 3.0-r6
  - Port both patches
  - Package Design_Patterns.pdf
  - Thanks to Richard Shaw for initial rebase patch
- Resolves: #723043

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-3.20090809
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jun 10 2010 Petr Machata <pmachata@redhat.com> - 2.2-2.20090809
- Replace mfence instruction with xchg to make it run on ia32-class
  machines without SSE2.
- Resolves: #600654

* Tue Nov  3 2009 Petr Machata <pmachata@redhat.com> - 2.2-1.20090809
- New upstream 2.2
- Resolves: #521571

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-3.20080605
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2.20080605
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jun 13 2008 Petr Machata <pmachata@redhat.com> - 2.1-1.20080605
- New upstream 2.1
  - Drop soname patch, parallel make patch, and GCC 4.3 patch

* Wed Feb 13 2008 Petr Machata <pmachata@redhat.com> - 2.0-4.20070927
- Review fixes
  - Use updated URL
  - More timestamp preservation
- Initial import into Fedora CVS

* Mon Feb 11 2008 Petr Machata <pmachata@redhat.com> - 2.0-3.20070927
- Review fixes
  - Preserve timestamp of installed files
  - Fix soname not to contain "debug"

* Tue Feb  5 2008 Petr Machata <pmachata@redhat.com> - 2.0-2.20070927
- Review fixes
  - GCC 4.3 patchset
  - Add BR util-linux net-tools
  - Add full URL to Source0
  - Build in debug mode to work around problems with GCC 4.3

* Mon Dec 17 2007 Petr Machata <pmachata@redhat.com> - 2.0-1.20070927
- Initial package.
- Using SONAME patch from Debian.

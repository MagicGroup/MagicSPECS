%define releasedate 20110809
%define major 4
%define minor 0
%define dotver %{major}.%{minor}
%define sourcebasename tbb%{major}%{minor}_%{releasedate}oss
%define sourcefilename %{sourcebasename}_src.tgz

Summary: The Threading Building Blocks library abstracts low-level threading details
Name: tbb
Version: %{dotver}
Release: 3.%{releasedate}%{?dist}
License: GPLv2 with exceptions
Group: Development/Tools
URL: http://threadingbuildingblocks.org/
Source0: http://threadingbuildingblocks.org/uploads/77/175/4.0/tbb40_20110809oss_src.tgz

# Upstream regularly replaces the "Latest" documentation with what's
# actually Latest at that point.  These sources may no longer match
# what's uploaded anymore.
%define docurl http://threadingbuildingblocks.org/uploads/81/91/Latest%%20Open%%20Source%%20Documentation/
%define source_1 CHANGES.txt
%define source_2 Getting_Started.pdf
%define source_3 Reference.pdf
%define source_4 Tutorial.pdf
%define source_5 Design_Patterns.pdf
Source1: %{docurl}/%{source_1}
Source2: %{docurl}/%{source_2}
Source3: %{docurl}/%{source_3}
Source4: %{docurl}/%{source_4}
Source5: %{docurl}/%{source_5}

Patch1: tbb-3.0-cxxflags.patch
Patch2: tbb-4.0-mfence.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libstdc++-devel
# We need "arch" and "hostname" binaries:
BuildRequires: util-linux net-tools
ExclusiveArch: %{ix86} x86_64 ia64

%description
Threading Building Blocks (TBB) is a C++ runtime library that
abstracts the low-level threading details necessary for optimal
multi-core performance.  It uses common C++ templates and coding style
to eliminate tedious threading implementation work.

TBB requires fewer lines of code to achieve parallelism than other
threading models.  The applications you write are portable across
platforms.  Since the library is also inherently scalable, no code
maintenance is required as more processor cores become available.


%package devel
Summary: The Threading Building Blocks C++ headers and shared development libraries
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and shared object symlinks for the Threading Building
Blocks (TBB) C++ libraries.


%package doc
Summary: The Threading Building Blocks documentation
Group: Documentation

%description doc
PDF documentation for the user of the Threading Building Block (TBB)
C++ library.


%prep
%setup -q -n %{sourcebasename}
%patch1 -p1
%patch2 -p1

%build
make %{?_smp_mflags} CXXFLAGS="$RPM_OPT_FLAGS" tbb_build_prefix=obj

cp -p "%{SOURCE1}" "%{SOURCE2}" "%{SOURCE3}" "%{SOURCE4}" "%{SOURCE5}" .

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_libdir}
mkdir -p $RPM_BUILD_ROOT/%{_includedir}

pushd build/obj_release
    for file in libtbb{,malloc}; do
        install -p -D -m 755 ${file}.so.2 $RPM_BUILD_ROOT/%{_libdir}
        ln -s $file.so.2 $RPM_BUILD_ROOT/%{_libdir}/$file.so
    done
popd

pushd include
    find tbb -type f -name \*.h -exec \
        install -p -D -m 644 {} $RPM_BUILD_ROOT/%{_includedir}/{} \
    \;
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc COPYING doc/Release_Notes.txt
%{_libdir}/*.so.2

%files devel
%defattr(-,root,root,-)
%doc %{source_1}
%{_includedir}/tbb
%{_libdir}/*.so

%files doc
%defattr(-,root,root,-)
%doc %{source_2}
%doc %{source_3}
%doc %{source_4}
%doc %{source_5}

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 4.0-3.20110809
- 为 Magic 3.0 重建

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

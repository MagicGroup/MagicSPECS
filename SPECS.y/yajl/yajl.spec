Name: yajl
Version: 2.0.4
Release: 5%{?dist}
Summary: Yet Another JSON Library (YAJL)
Summary(zh_CN.UTF-8): 另一个 JSON 库 (YAJL)

Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License: ISC
URL: http://lloyd.github.com/yajl/

#
# NB, upstream does not provide pre-built tar.gz downloads. Instead
# they make you use the 'on the fly' generated tar.gz from GITHub's
# web interface
#
# The Source0 for any version is obtained by a URL
#
#   http://github.com/lloyd/yajl/tarball/1.0.7
#
# Which causes a download of a archive named after
# the GIT hash corresponding to the version tag
#
#   eg lloyd-yajl-45a1bdb.tar.gz
#
# NB even though the tar.gz is generated on the fly by GITHub it
# will always have identical md5sum
#
# So for new versions, update 'githash' to match the hash of the
# GIT tag associated with updated 'Version:' field just above
%global githash fee1ebe
Source0: lloyd-%{name}-%{version}-0-g%{githash}.tar.gz
Patch1: lloyd-%{name}-%{version}-pkgconfig-location.patch
Patch2: lloyd-%{name}-%{version}-pkgconfig-includedir.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: cmake

%package devel
Summary: Libraries, includes, etc to develop with YAJL
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name} = %{version}-%{release}

%description
Yet Another JSON Library. YAJL is a small event-driven
(SAX-style) JSON parser written in ANSI C, and a small
validating JSON generator.
%description -l zh_CN.UTF-8
另一个 JSON 库。

%description devel
Yet Another JSON Library. YAJL is a small event-driven
(SAX-style) JSON parser written in ANSI C, and a small
validating JSON generator.

This sub-package provides the libraries and includes
necessary for developing against the YAJL library

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n lloyd-%{name}-%{githash}
%patch1 -p1
%patch2 -p1

%build
# NB, we are not using upstream's 'configure'/'make'
# wrapper, instead we use cmake directly to better
# align with Fedora standards
mkdir build
cd build
%cmake ..
make VERBOSE=1 %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd build
make install DESTDIR=$RPM_BUILD_ROOT


# No static libraries
rm -f $RPM_BUILD_ROOT%{_libdir}/libyajl_s.a
magic_rpm_clean.sh

%check
cd test
./run_tests.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog README TODO
%{_bindir}/json_reformat
%{_bindir}/json_verify
%{_libdir}/libyajl.so.2
%{_libdir}/libyajl.so.2.*

%files devel
%defattr(-,root,root,-)
%doc COPYING
%dir %{_includedir}/yajl
%{_includedir}/yajl/yajl_common.h
%{_includedir}/yajl/yajl_gen.h
%{_includedir}/yajl/yajl_parse.h
%{_includedir}/yajl/yajl_tree.h
%{_includedir}/yajl/yajl_version.h
%{_libdir}/libyajl.so
%{_libdir}/pkgconfig/yajl.pc


%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 2.0.4-5
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 2.0.4-4
- 为 Magic 3.0 重建

* Tue Oct 27 2015 Liu Di <liudidi@gmail.com> - 2.0.4-3
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 2.0.4-2
- 为 Magic 3.0 重建

* Mon Aug  6 2012 Daniel P. Berrange <berrange@redhat.com> - 2.0.4-1
- Update to 2.0.4 release (rhbz #845777)
- Fix License tag to reflect change in 2.0.0 series from BSD to ISC

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Daniel P. Berrange <berrange@redhat.com> - 2.0.1-1
- Update to 2.0.1 release

* Tue May  3 2011 Daniel P. Berrange <berrange@redhat.com> - 1.0.12-1
- Update to 1.0.12 release

* Fri Dec 17 2010 Daniel P. Berrange <berrange@redhat.com> - 1.0.11-1
- Update to 1.0.11 release

* Mon Jan 11 2010 Daniel P. Berrange <berrange@redhat.com> - 1.0.7-3
- Fix ignoring of cflags (rhbz #547500)

* Tue Dec  8 2009 Daniel P. Berrange <berrange@redhat.com> - 1.0.7-2
- Change use of 'define' to 'global'

* Mon Dec  7 2009 Daniel P. Berrange <berrange@redhat.com> - 1.0.7-1
- Initial Fedora package

Name:    libatomic_ops
Summary: Atomic memory update operations
Version: 7.4.2
Release: 7%{?dist}

# libatomic_ops MIT, libatomic_ops_gpl GPLv2
License: GPLv2 and MIT
#URL:    http://www.hpl.hp.com/research/linux/atomic_ops/
URL:     https://github.com/ivmai/libatomic_ops/
Source0: http://www.ivmaisoft.com/_bin/atomic_ops/libatomic_ops-%{version}.tar.gz
# updated GPLv2 license text
Source1: http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

## upstreamable patches
# link libatomic_ops_gpl against libatomic_ops for missing symbol(s)
Patch50: libatomic_ops-7.4.2-no_undefined.patch

# re-autofoo for patch50
BuildRequires: automake libtool

%description
Provides implementations for atomic memory update operations on a
number of architectures. This allows direct use of these in reasonably
portable code. Unlike earlier similar packages, this one explicitly
considers memory barrier semantics, and allows the construction of code
that involves minimum overhead across a variety of architectures.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
Files for developing with %{name}.

%package static
Summary: Static library files for %{name}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
%description static
Files for developing with %{name} and linking statically.


%prep
%setup -q

%patch50 -p1 -b .no_undefined

# patch50 introduces rpath (probably due to older libtool), refresh stuff here
autoreconf -fi

install -m644 -p %{SOURCE1} ./COPYING


%build
%configure \
  --enable-shared \
  --disable-silent-rules

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

## unpackaged files
rm -fv %{buildroot}%{_libdir}/lib*.la
# omit dup'd docs
rm -fv %{buildroot}%{_datadir}/libatomic_ops/{COPYING,README*,*.txt}


%check
# ignore failures on powerpc, atomic stack feature not working (#883748)
%ifarch ppc ppc64 ppc64le aarch64
%global arch_ignore ||:
%endif
make check %{?arch_ignore}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING doc/LICENSING.txt
%doc AUTHORS ChangeLog README.md
%{_libdir}/libatomic_ops.so.1*
%{_libdir}/libatomic_ops_gpl.so.1*

%files devel
%doc doc/README*
%{_includedir}/atomic_ops.h
%{_includedir}/atomic_ops_malloc.h
%{_includedir}/atomic_ops_stack.h
%{_includedir}/atomic_ops/
%{_libdir}/libatomic_ops.so
%{_libdir}/libatomic_ops_gpl.so
%{_libdir}/pkgconfig/atomic_ops.pc

%files static
%{_libdir}/libatomic_ops.a
%{_libdir}/libatomic_ops_gpl.a


%changelog
* Sat Nov 21 2015 Liu Di <liudidi@gmail.com> - 7.4.2-7
- 为 Magic 3.0 重建

* Tue Jul  7 2015 Peter Robinson <pbrobinson@fedoraproject.org> 7.4.2-6
- Don't fail check on aarch64

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Rex Dieter <rdieter@fedoraproject.org> 7.4.2-2
- link libatomic_ops_gpl against libatomic_ops for missing symbol(s)

* Tue May 13 2014 Rex Dieter <rdieter@fedoraproject.org> 7.4.2-1
- libatomic_opts-7.4.2
- new upstream/source URLs
- %%check: skip ppc64le too
- License: MIT and GPLv2
- update/longer %%description
- updated GPLv2 license text (with correct address)

* Wed Dec 04 2013 Rex Dieter <rdieter@fedoraproject.org>  7.4.0-1
- separate libatomic_ops lives again!

* Fri Jul 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.2-8.gc
- use gc tarball, tag gc release

* Thu Jul 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.2-7
- devel: Provides: %%name-static ...
- consolidate %%doc's
- %%files: track libs

* Wed May 20 2009 Dan Horak <dan[t]danny.cz> - 1.2-6
- added fix for s390

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 22 2008 Jon Stanley <jonstanley@gmail.com> - 1.2-4
- Fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2-3
- Autorebuild for GCC 4.3

* Tue May 29 2007 Pierre Ossman <drzeus@drzeus.cx> 1.2-2
- Added fix for PPC AO_load_acquire.

* Fri Nov 10 2006 Pierre Ossman <drzeus@drzeus.cx> 1.2-1
- Update to 1.2.

* Sat Sep  9 2006 Pierre Ossman <drzeus@drzeus.cx> 1.1-2
- Fix naming of package.
- General cleanup of spec file.

* Wed Aug 30 2006 Pierre Ossman <drzeus@drzeus.cx> 1.1-1
- Initial package for Fedora Extras.

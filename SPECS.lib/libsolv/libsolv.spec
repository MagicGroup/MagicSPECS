%global gitrev 5bd9589
%{!?ruby_vendorarch: %global ruby_vendorarch %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["vendorarchdir"] ')}
%filter_provides_in %{perl_vendorarch}/.*\.so$
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_provides_in %{ruby_vendorarch}/.*\.so$
%filter_setup

Name:		libsolv
Version:	0.6.4
Release:	4%{?dist}
License:	BSD
Url:		https://github.com/openSUSE/libsolv
# git clone https://github.com/openSUSE/libsolv.git
# git archive %{gitrev} --prefix=libsolv/ | xz > libsolv-%{gitrev}.tar.xz
Source:		libsolv-%{gitrev}.tar.xz
Patch0:		libsolv-rubyinclude.patch
Group:		Development/Libraries
Summary:	Package dependency solver
Summary(zh_CN.UTF-8): 包依赖解决器
BuildRequires:	cmake libdb-devel expat-devel rpm-devel zlib-devel
BuildRequires:	swig perl perl-devel ruby ruby-devel python2-devel
BuildRequires:  xz-devel
%description
A free package dependency solver using a satisfiability algorithm. The
library is based on two major, but independent, blocks:

- Using a dictionary approach to store and retrieve package
  and dependency information.

- Using satisfiability, a well known and researched topic, for
  resolving package dependencies.

%description -l zh_CN.UTF-8
包依赖解决器。

%package devel
Summary:	A new approach to package dependency solving
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	libsolv-tools%{?_isa} = %{version}-%{release}
Requires:	libsolv%{?_isa} = %{version}-%{release}
Requires:	rpm-devel%{?_isa}
Requires:	cmake

%description devel
Development files for libsolv,

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package tools
Summary:	A new approach to package dependency solving
Group:		Development/Libraries
Requires:	gzip bzip2 coreutils
Requires:	libsolv%{?_isa} = %{version}-%{release}

%description tools
Package dependency solver tools.

%package demo
Summary:	Applications demoing the libsolv library
Group:		Development/Libraries
Requires:	curl gnupg2

%description demo
Applications demoing the libsolv library.

%package -n ruby-solv
Summary:	Ruby bindings for the libsolv library
Group:		Development/Languages

%description -n ruby-solv
Ruby bindings for sat solver.

%package -n python-solv
Summary:	Python bindings for the libsolv library
Group:		Development/Languages
Requires:	python

%description -n python-solv
Python bindings for sat solver.

%package -n perl-solv
Summary:	Perl bindings for the libsolv library
Group:		Development/Languages
Requires:	perl

%description -n perl-solv
Perl bindings for sat solver.

%prep
%setup -q -n libsolv
%patch0 -p1 -b .rubyinclude

%check
make ARGS="-V" test

%build
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DENABLE_PERL=1 \
       -DENABLE_PYTHON=1 \
       -DENABLE_RUBY=1 \
       -DUSE_VENDORDIRS=1 \
       -DFEDORA=1 \
       -DENABLE_DEBIAN=1 \
       -DENABLE_ARCHREPO=1 \
       -DENABLE_LZMA_COMPRESSION=1 \
       -DINSTALL_MANDIR=%{_mandir} \
       -DMULTI_SEMANTICS=1

make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT/usr/bin/testsolv
mv %{buildroot}/usr/man %{buildroot}%{_datadir}/
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE* README BUGS
%_libdir/libsolv.so.*
%_libdir/libsolvext.so.*

%files tools
%_bindir/archpkgs2solv
%_bindir/archrepo2solv
%_bindir/deb2solv
%_bindir/deltainfoxml2solv
%_bindir/dumpsolv
%_bindir/installcheck
%_bindir/mergesolv
%_bindir/repo2solv.sh
%_bindir/repomdxml2solv
%_bindir/rpmdb2solv
%_bindir/rpmmd2solv
%_bindir/rpms2solv
%_bindir/updateinfoxml2solv

%files devel
%doc examples/solv.c
%_libdir/libsolv.so
%_libdir/libsolvext.so
%_includedir/solv
%_datadir/cmake/Modules/FindLibSolv.cmake
%{_mandir}/man?/*

%files demo
%_bindir/solv

%files -n perl-solv
%doc examples/p5solv
%{perl_vendorarch}/*

%files -n ruby-solv
%doc examples/rbsolv
%{ruby_vendorarch}/*

%files -n python-solv
%doc examples/pysolv
%{python_sitearch}/*

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 0.6.4-4
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.6.4-3
- 为 Magic 3.0 重建

* Sun Aug 10 2014 Liu Di <liudidi@gmail.com> - 0.6.4-2
- 为 Magic 3.0 重建


* Mon Jul 28 2014 Aleš Kozumplík <akozumpl@redhat.com> - 0.6.4-1
- Rebase to upstream 5bd9589

* Mon Jul 14 2014 Jan Silhan <jsilhan@redhat.com> - 0.6.4-0.git2a5c1c4
- Rebase to upstream 2a5c1c4
- Filename selector can start with a star

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-2.git6d968f1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Aleš Kozumplík <ales@redhat.com> - 0.6.1-1.git6d968f1
- Rebase to upstream 6d968f1
- Fix RhBug:1049209

* Fri Apr 25 2014 Jan Silhan <jsilhan@redhat.com> - 0.6.1-0.gitf78f5de
- Rebase to 0.6.0, upstream commit f78f5de.

* Thu Apr 24 2014 Vít Ondruch <vondruch@redhat.com> - 0.6.0-0.git05baf54.1
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Wed Apr 9 2014 Jan Silhan <jsilhan@redhat.com> - 0.6.0-0.git05baf54
- Rebase to 0.6.0, upstream commit 05baf54.

* Mon Dec 16 2013 Aleš Kozumplík <akozumpl@redhat.com> - 0.4.1-1.gitbcedc98
- Rebase upstream bcedc98
- Fix RhBug:1051917.

* Mon Dec 16 2013 Aleš Kozumplík <akozumpl@redhat.com> - 0.4.1-0.gita8e47f1
- Rebase to 0.4.1, upstream commit a8e47f1.

* Fri Nov 22 2013 Zdenek Pavlas <zpavlas@redhat.com> - 0.4.0-2.git4442b7f
- Rebase to 0.4.0, upstream commit 4442b7f.
- support DELTA_LOCATION_BASE for completeness

* Tue Oct 29 2013 Aleš Kozumplík <akozumpl@redhat.com> - 0.4.0-1.gitd49d319
- Rebase to 0.4.0, upstream commit d49d319.

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 0.3.0-9.gita59d11d
- Perl 5.18 rebuild

* Wed Jul 31 2013 Aleš Kozumplík <akozumpl@redhat.com> - 0.3.0-8.gita59d11d
- Rebase to upstream a59d11d.

* Fri Jul 19 2013 Aleš Kozumplík <akozumpl@redhat.com> - 0.3.0-7.git228d412
- Add build flags, including Deb, Arch, LZMA and MULTI_SEMANTICS. (RhBug:985905)

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.3.0-6.git228d412
- Perl 5.18 rebuild

* Mon Jun 24 2013 Aleš Kozumplík <akozumpl@redhat.com> - 0.3.0-5.git228d412
- Rebase to upstream 228d412.
- Fixes hawkey github issue https://github.com/akozumpl/hawkey/issues/13

* Thu Jun 20 2013 Aleš Kozumplík <akozumpl@redhat.com> - 0.3.0-4.git209e9cb
- Rebase to upstream 209e9cb.
- Package the new man pages.

* Thu May 16 2013 Aleš Kozumplík <akozumpl@redhat.com> - 0.3.0-3.git7399ad1
- Run 'make test' with libsolv build.

* Mon Apr 8 2013 Aleš Kozumplík <akozumpl@redhat.com> - 0.3.0-2.git7399ad1
- Rebase to upstream 7399ad1.
- Fixes RhBug:905209

* Mon Apr 8 2013 Aleš Kozumplík <akozumpl@redhat.com> - 0.3.0-1.gite372b78
- Rebase to upstream e372b78.
- Fixes RhBug:e372b78

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-2.gitf663ca2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 23 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.0.0-17.git6c9d3eb
- Rebase to upstream 6c9d3eb.
- Drop the solv.i stdbool.h fix integrated upstream.
- Dropped the job reasons fix.

* Mon Jul 23 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.0.0-16.git1617994
- Fix build problems with Perl bindings.

* Mon Jul 23 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.0.0-15.git1617994
- Rebuilt after a failed mass rebuild.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.0-14.git1617994
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Aleš Kozumplik <akozumpl@redhat.com> - 0.0.0-13.git1617994%{?dist}
- preliminary fix for JOB resons in solver_describe_decision().

* Sun Jul 1 2012 Aleš Kozumplik <akozumpl@redhat.com> - 0.0.0-12.git1617994%{?dist}
- Rebase to upstream 1617994.
- Support for RPM_ADD_WITH_HDRID.

* Thu Jun  7 2012 Aleš Kozumplik <akozumpl@redhat.com> - 0.0.0-11.gitd39a42b%{?dist}
- Rebase to upstream d39a42b.
- Fix the epochs.
- Move the ruby modules into vendorarch dir, where they are expected.

* Thu May  17 2012 Aleš Kozumplik <akozumpl@redhat.com> - 0.0.0-9.git8cf7650%{?dist}
- Rebase to upstream 8cf7650.
- ruby bindings: fix USE_VENDORDIRS for Fedora.

* Thu Apr  12 2012 Aleš Kozumplik <akozumpl@redhat.com> - 0.0.0-7.gitaf1465a2%{?dist}
- Rebase to the upstream.
- Make repo_add_solv() work without stub repodata.

* Thu Apr  5 2012 Karel Klíč <kklic@redhat.com> - 0.0.0-6.git80afaf7%{?dist}
- Rebuild for the new libdb package.

* Mon Apr  2 2012 Karel Klíč <kklic@redhat.com> - 0.0.0-5.git80afaf7%{?dist}
- Rebuild for the new rpm package.

* Wed Mar 21 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.0.0-4.git80afaf7%{?dist}
- New upstream version, fix the .rpm release number.

* Wed Mar 21 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.0.0-3.git80afaf7%{?dist}
- New upstream version.

* Tue Feb  7 2012 Karel Klíč <kklic@redhat.com> - 0.0.0-2.git857fe28%{?dist}
- Adapted to Ruby 1.9.3 (workaround for broken CMake in Fedora and
  ruby template correction in bindings)

* Thu Feb  2 2012 Karel Klíč <kklic@redhat.com> - 0.0.0-1.git857fe28
- Initial packaging
- Based on Jindra Novy's spec file
- Based on upstream spec file

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%global with_python3 1

%define git 0
%define vcsdate 20140319

Summary: Create deltas between rpms
Summary(zh_CN.UTF-8): 在 rpm 包之间建立三角关系
Name: deltarpm
Version: 3.6
%if 0%{?git}
Release: 0.17.%{vcsdate}git%{?dist}
%else
Release: 4%{?dist}
%endif
License: BSD
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
URL: http://gitorious.org/deltarpm/deltarpm
# Generate source by doing:
# git clone git://gitorious.org/deltarpm/deltarpm
# cd deltarpm
# git archive --format=tar --prefix="deltarpm-git-20110223/" 7ed5208166 | \
#   bzip2 > deltarpm-git-20110223.tar.bz2
%if 0%{?git}
Source0: %{name}-git%{vcsdate}.tar.xz
%else
Source0: ftp://ftp.suse.com/pub/projects/deltarpm/%{name}-%{version}.tar.bz2
%endif
Source1: make_deltarpm_git_package.sh
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: bzip2-devel, xz-devel, rpm-devel, popt-devel
BuildRequires: zlib-devel
BuildRequires: python-devel

%if 0%{?with_python3}
BuildRequires: python3-devel
%endif

%description
A deltarpm contains the difference between an old
and a new version of a rpm, which makes it possible
to recreate the new rpm from the deltarpm and the old
one. You don't have to have a copy of the old rpm,
deltarpms can also work with installed rpms.

%package -n drpmsync
Summary: Sync a file tree with deltarpms
Group: System Environment/Base
Requires: deltarpm = %{version}-%{release}

%description -n drpmsync
This package contains a tool to sync a file tree with
deltarpms.

%package -n deltaiso
Summary: Create deltas between isos containing rpms
Group: System Environment/Base
Requires: deltarpm = %{version}-%{release}

%description -n deltaiso
This package contains tools for creating and using deltasisos,
a difference between an old and a new iso containing rpms.

%package -n python-deltarpm
Summary: Python bindings for deltarpm
Group: System Environment/Base
Requires: deltarpm = %{version}-%{release}

%description -n python-deltarpm
This package contains python bindings for deltarpm.

%if 0%{?with_python3}
%package -n python3-deltarpm
Summary: Python bindings for deltarpm
Group: System Environment/Base
Requires: deltarpm = %{version}-%{release}

%description -n python3-deltarpm
This package contains python bindings for deltarpm.
%endif


%prep
%if 0%{?git}
%setup -q -n %{name}-git%{vcsdate}
%else
%setup -q
%endif

%build
%{__make} %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" \
    bindir=%{_bindir} libdir=%{_libdir} mandir=%{_mandir} prefix=%{_prefix} \
    zlibbundled='' zlibldflags='-lz' zlibcppflags=''
%{__make} %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" \
    bindir=%{_bindir} libdir=%{_libdir} mandir=%{_mandir} prefix=%{_prefix} \
    zlibbundled='' zlibldflags='-lz' zlibcppflags='' \
    python

%install
%{__rm} -rf %{buildroot}
%makeinstall pylibprefix=%{buildroot}

%if 0%{?with_python3}
# nothing to do
%else
rm -rf %{buildroot}%{_libdir}/python3*
%endif


%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc LICENSE.BSD README
%doc %{_mandir}/man8/applydeltarpm*
%doc %{_mandir}/man8/makedeltarpm*
%doc %{_mandir}/man8/combinedeltarpm*
%{_bindir}/applydeltarpm
%{_bindir}/combinedeltarpm
%{_bindir}/makedeltarpm
%{_bindir}/rpmdumpheader

%files -n deltaiso
%defattr(-, root, root, 0755)
%doc LICENSE.BSD README
%doc %{_mandir}/man8/applydeltaiso*
%doc %{_mandir}/man8/makedeltaiso*
%doc %{_mandir}/man8/fragiso*
%{_bindir}/applydeltaiso
%{_bindir}/fragiso
%{_bindir}/makedeltaiso

%files -n drpmsync
%defattr(-, root, root, 0755)
%doc LICENSE.BSD README
%doc %{_mandir}/man8/drpmsync*
%{_bindir}/drpmsync

%files -n python-deltarpm
%defattr(-, root, root, 0755)
%doc LICENSE.BSD
%{python_sitearch}/*

%if 0%{?with_python3}

%files -n python3-deltarpm
%defattr(-, root, root, 0755)
%doc LICENSE.BSD
%{python3_sitearch}/*

%endif

%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 3.6-4
- 为 Magic 3.0 重建

* Thu Jul 30 2015 Liu Di <liudidi@gmail.com> - 3.6-3
- 为 Magic 3.0 重建

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 3.6-2
- 为 Magic 3.0 重建

* Wed Mar 19 2014 Liu Di <liudidi@gmail.com> - 3.6-0.14.20140319git
- 更新到 20140319 日期的仓库源码

* Wed Mar 19 2014 Liu Di <liudidi@gmail.com> - 3.6-0.13.20140319git
- 更新到 20140319 日期的仓库源码

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-0.12.20110223git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 03 2012 David Malcolm <dmalcolm@redhat.com> - 3.6-0.11.20110223git
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 3.6-0.10.20110223git
- remove rhel logic from with_python3 conditional

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-0.9.20110223git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 20 2012 Jindrich Novy <jnovy@redhat.com> - 3.6-0.8.20110223git
- rebuild against new rpm

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-0.7.20110223git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 23 2011 - Jonathan Dieter <jdieter@lesbg.com> - 3.6-0.6.20110223git
- Fix makedeltaiso so it (partially) works when compression formats change
- Fix fix for makedeltaiso so it gets checksums right

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-0.5.20110121git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 - Jonathan Dieter <jdieter@lesbg.com> - 3.6-0.4.20110121git
- Python 3 module now works again

* Tue Jan 18 2011 - Jonathan Dieter <jdieter@lesbg.com> - 3.6-0.4.20110118git
- Re-enable Python 3 support, but it still won't work even though it builds
- Remove upstreamed patches

* Tue Jan 18 2011 - Richard W.M. Jones <rjones@redhat.com> - 3.6-0.3.20101230git
- Disable Python 3 support, since it is quite broken.

* Thu Dec 30 2010 Jonathan Dieter <jdieter@lesbg.com> - 3.6-0.1.20101230git
- Update to current git
- Temporary extra verbosity patch
- Add groups to subpackages for EL5

* Thu Jul  8 2010 Jonathan Dieter <jdieter@lesbg.com> - 3.6-0.1.20100708git
- Deltarpm can now limit memory usage when generating deltarpms

* Wed Feb 10 2010 Thomas Spura <tomspur@fedoraproject.org> - 3.5-0.7.20100121git
- build python3-deltarpm

* Thu Jan 21 2010 Jonathan Dieter <jdieter@lesbg.com> - 3.5-0.6.20100121git
- Make rpmio link explicit

* Tue Dec 08 2009 Jesse Keating <jkeating@redhat.com> - 3.5-0.5.20090913git
- Rebuild for new rpm

* Wed Sep 30 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 3.5-0.4.20090913git
- Update patch to properly detect when an rpm is built with an rsync-friendly
  zlib and bail out.

* Wed Sep 30 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 3.5-0.3.20090913git
- Make building with system zlib selectable at build time.
- Fix cfile_detect_rsync() to detect rsync even if we don't have a zlib capable
  of making rsync-friendly compressed files.

* Wed Sep 30 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 3.5-0.2.20090913git
- Correct prerelease rlease numbering.
- Build against the system zlib, not the bundled library.  This remedies the
  fact that the included zlib is affected by CAN-2005-1849.

* Sun Sep 13 2009 Jonathan Dieter <jdieter@lesbg.com> - 3.5-0.git.20090913
- Merge python error patch upstream

* Thu Sep 10 2009 Bill Nottingham <notting@redhat.com> - 3.5-0.git.20090831.1.4
- fix python bindings to not require kernel >= 2.6.27

* Wed Sep  9 2009 Bill Nottingham <notting@redhat.com> - 3.5-0.git.20090831.1.3
- fix python bindings to:
  - call _exit(), not exit()
  - properly pythonize errors
  - not leak file descriptors

* Mon Aug 31 2009 Jonathan Dieter <jdieter@lesbg.com> - 3.5-0.git.20090831.1
- Add python bindings sub-package
- Fix build error

* Mon Aug 17 2009 Jonathan Dieter <jdieter@gmail.com> - 3.5-0.git.20090729.1
- Explain where we get the source from
- Split *deltaiso commands into deltaiso subpackage (#501953)

* Wed Jul 29 2009 Jonathan Dieter <jdieter@gmail.com> - 3.5-0.git.20090729
- Fix bug in writing Fedora's xz-compressed rpms (surely that's the last one)

* Mon Jul 27 2009 Jonathan Dieter <jdieter@gmail.com> - 3.5-0.git.20090727.1
- Fix bug in reading Fedora's xz-compressed rpms

* Mon Jul 27 2009 Jonathan Dieter <jdieter@gmail.com> - 3.5-0.git.20090727
- Update to current upstream git repository
- Add upstream xz compression support
- Drop all patches (they're now in upstream)
- Fix spelling mistakes (#505713)
- Fix url error (#506179)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 22 2009 Jonathan Dieter <jdieter@gmail.com> - 3.4-16
- Split drpmsync into a separate subpackage (#489231)

* Thu Mar 26 2009 Jonathan Dieter <jdieter@gmail.com> - 3.4-15
- Fix bug when checking sequence with new sha256 file digests

* Tue Mar 24 2009 Jonathan Dieter <jdieter@gmail.com> - 3.4-14
- Add support for rpms with sha256 file digests

* Fri Mar 06 2009 Jesse Keating <jkeating@redhat.com> - 3.4-13
- Rebuild for new rpm libs

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jul 13 2008 Jonathan Dieter <jdieter@gmail.com> - 3.4-11
- Rebuild for rpm 4.6

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.4-10
- Autorebuild for GCC 4.3

* Mon Jan  7 2008 Jonathan Dieter <jdieter@gmail.com> - 3.4-9
- Add patch that allows deltarpm to rebuild rpms from deltarpms that have
  had the rpm signature added after their creation.  The code came from
  upstream.
- Drop nodoc patch added in 3.4-4 as most packages in repository have been
  updated since April-May 2007 and this patch was supposed to be temporary.

* Wed Aug 29 2007 Jonathan Dieter <jdieter@gmail.com> - 3.4-6
- Bring in popt-devel in BuildRequires to fix build in x86_64

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 3.4-5
- Rebuild for selinux ppc32 issue.

* Wed Jul 11 2007 Jonathan Dieter <jdieter@gmail.com> - 3.4-4
- Fix prelink bug
- Ignore verify bits on doc files as they were set incorrectly in older
  versions of rpm.  Without this patch, deltarpm will not delta doc files
  in rpm created before April-May 2007

* Tue Jun  5 2007 Jeremy Katz <katzj@redhat.com> - 3.4-3
- include colored binaries from non-multilib-dirs so that deltas can work 
  on multilib platforms

* Wed May 09 2007 Adam Jackson <ajax@redhat.com> 3.4-2
- Add -a flag to work around multilib ignorance. (#238964)

* Tue Mar 06 2007 Adam Jackson <ajax@redhat.com> 3.4-1
- Update to 3.4 (#231154)

* Mon Feb 12 2007 Adam Jackson <ajax@redhat.com> 3.3-7
- Add RPM_OPT_FLAGS to make line. (#227380)

* Mon Feb 05 2007 Adam Jackson <ajax@redhat.com> 3.3-6
- Fix rpm db corruption in rpmdumpheader.  (#227326)

* Mon Sep 11 2006 Mihai Ibanescu <misa@redhat.com> - 3.3-5
- Rebuilding for new toolset

* Thu Aug 17 2006 Mihai Ibanescu <misa@redhat.com> - 3.3-4
- Removing BuildRequires: gcc

* Tue Aug 15 2006 Mihai Ibanescu <misa@redhat.com> - 3.3-3
- Fedora packaging guidelines build

* Tue Aug  8 2006 Mihai Ibanescu <misa@redhat.com> - 3.3-2
- Added BuildRequires: rpm-devel, gcc

* Sat Dec 03 2005 Dries Verachtert <dries@ulyssis.org> - 3.3-1 - 3768/dries
- Initial package.

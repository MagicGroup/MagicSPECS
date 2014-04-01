Summary: An API for Run-time Code Generation
License: LGPLv2+
Name: dyninst
Group: Development/Libraries
Release: 6%{?dist}
URL: http://www.dyninst.org
Version: 8.1.2
Exclusiveos: linux
#Right now dyninst does not know about the following architectures
ExcludeArch: s390 s390x %{arm}

# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  git clone http://git.dyninst.org/dyninst.git; cd dyninst
#  git archive --format=tar.gz --prefix=dyninst/ v8.1.2 > dyninst-8.1.2.tar.gz
#  git clone http://git.dyninst.org/docs.git; cd docs
#  git archive --format=tar.gz v8.1.1 > dyninst-docs-8.1.1.tar.gz
# Verify the commit ids with:
#  gunzip -c dyninst-8.1.2.tar.gz | git get-tar-commit-id
#  gunzip -c dyninst-docs-8.1.1.tar.gz | git get-tar-commit-id
Source0: %{name}-%{version}.tar.gz
Source1: %{name}-docs-8.1.1.tar.gz
Patch1: dyninst-rpm-build-flags.patch
Patch2: dyninst-install-testsuite.patch
Patch3: dyninst-pokeuser.patch
Patch4: dyninst-Werror-format-security.patch
Patch5: dyninst-8.1.2-testsuite-opt.patch
BuildRequires: libdwarf-devel >= 20111030
BuildRequires: elfutils-libelf-devel
BuildRequires: boost-devel

# Extra requires just for the testsuite
BuildRequires: gcc-gfortran glibc-static libstdc++-static nasm

# Testsuite files should not provide/require anything
%{?filter_setup:
%filter_provides_in %{_libdir}/dyninst/testsuite/
%filter_requires_in %{_libdir}/dyninst/testsuite/
%filter_setup
}

%description

Dyninst is an Application Program Interface (API) to permit the insertion of
code into a running program. The API also permits changing or removing
subroutine calls from the application program. Run-time code changes are
useful to support a variety of applications including debugging, performance
monitoring, and to support composing applications out of existing packages.
The goal of this API is to provide a machine independent interface to permit
the creation of tools and applications that use run-time code patching.

%package doc
Summary: Documentation for using the Dyninst API
Group: Documentation
%description doc
dyninst-doc contains API documentation for the Dyninst libraries.

%package devel
Summary: Header files for the compiling programs with Dyninst
Group: Development/System
Requires: dyninst = %{version}-%{release}
Requires: boost-devel
%description devel
dyninst-devel includes the C header files that specify the Dyninst user-space
libraries and interfaces. This is required for rebuilding any program
that uses Dyninst.

%package static
Summary: Static libraries for the compiling programs with Dyninst
Group: Development/System
Requires: dyninst-devel = %{version}-%{release}
%description static
dyninst-static includes the static versions of the library files for
the dyninst user-space libraries and interfaces.

%package testsuite
Summary: Programs for testing Dyninst
Group: Development/System
Requires: dyninst-devel = %{version}-%{release}
%description testsuite
dyninst-testsuite includes the test harness and target programs for
making sure that dyninst works properly.

%prep
%setup -q -n %{name}-%{version} -c
%setup -q -T -D -a 1

pushd dyninst
%patch1 -p1 -b .buildflags
%patch2 -p1 -b .testsuite
%patch3 -p1 -b .pokeuser
%patch4 -p1 -d testsuite -b .format-security
%patch5 -p1 -b .testsuite-opt
popd


%build

cd dyninst

%configure --includedir=%{_includedir}/dyninst --libdir=%{_libdir}/dyninst
make %{?_smp_mflags} VERBOSE_COMPILATION=1

%install

cd dyninst
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{_libdir}/dyninst" > %{buildroot}/etc/ld.so.conf.d/%{name}-%{_arch}.conf

# Ugly hack to fix permissions
chmod 644 %{buildroot}%{_includedir}/dyninst/*
chmod 644 %{buildroot}%{_libdir}/dyninst/*.a

# Uglier hack to mask testsuite files from debuginfo extraction.  Running the
# testsuite requires debuginfo, so extraction is useless.  However, debuginfo
# extraction is still nice for the main libraries, so we don't want to disable
# it package-wide.  The permissions are restored by attr(755,-,-) in files.
chmod 644 %{buildroot}%{_libdir}/dyninst/testsuite/*

magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)

%dir %{_libdir}/dyninst
%{_libdir}/dyninst/*.so.*

%doc dyninst/COPYRIGHT
%doc dyninst/LGPL

%config(noreplace) /etc/ld.so.conf.d/*

%files doc
%defattr(-,root,root,-)
%doc dynC_API.pdf
%doc DyninstAPI.pdf
%doc InstructionAPI.pdf
%doc ParseAPI.pdf
%doc PatchAPI.pdf
%doc ProcControlAPI.pdf
%doc StackwalkerAPI.pdf
%doc SymtabAPI.pdf

%files devel
%defattr(-,root,root,-)
%{_includedir}/dyninst
%{_libdir}/dyninst/*.so

%files static
%defattr(-,root,root,-)
%{_libdir}/dyninst/*.a

%files testsuite
%defattr(-,root,root,-)
%{_bindir}/parseThat
%dir %{_libdir}/dyninst/testsuite/
# Restore the permissions that were hacked out above, during install.
%attr(755,root,root) %{_libdir}/dyninst/testsuite/*

%changelog
* Wed Dec 11 2013 Josh Stone <jistone@redhat.com> 8.1.2-6
- Fix rhbz1040715 (testsuite g++ optimization)

* Tue Dec 03 2013 Josh Stone <jistone@redhat.com> 8.1.2-5
- Fix rhbz1037048 (-Werror=format-security FTBFS)

* Mon Aug 05 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.2-4
- Fix rhbz991889 (FTBFS).

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 8.1.2-2
- Rebuild for boost 1.54.0

* Tue Jun 18 2013 Josh Stone <jistone@redhat.com> 8.1.2-1
- Update to release 8.1.2.

* Fri Mar 15 2013 Josh Stone <jistone@redhat.com> 8.1.1-1
- Update to release 8.1.1.
- Drop the backported dyninst-test2_4-kill-init.patch.
- Drop the now-upstreamed dyninst-unused_vars.patch.
- Update other patches for context.
- Patch the installed symlinks to be relative, not $(DEST) filled.

* Tue Feb 26 2013 Josh Stone <jistone@redhat.com> 8.0-7
- testsuite: Require dyninst-devel for the libdyninstAPI_RT.so symlink

* Tue Feb 26 2013 Josh Stone <jistone@redhat.com> 8.0-6
- Fix the testsuite path to include libtestlaunch.so

* Mon Feb 25 2013 Josh Stone <jistone@redhat.com> 8.0-5
- Add a dyninst-testsuite package.
- Patch test2_4 to protect against running as root.
- Make dyninst-static require dyninst-devel.

* Thu Feb 14 2013 Josh Stone <jistone@redhat.com> 8.0-4
- Patch make.config to ensure rpm build flags are not discarded.

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 8.0-3
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 8.0-2
- Rebuild for Boost-1.53.0

* Tue Nov 20 2012 Josh Stone <jistone@redhat.com>
- Tweak the configure/make commands
- Disable the testsuite via configure.
- Set the private includedir and libdir via configure.
- Set VERBOSE_COMPILATION for make.
- Use DESTDIR for make install.

* Mon Nov 19 2012 Josh Stone <jistone@redhat.com> 8.0-1
- Update to release 8.0.
- Updated "%files doc" to reflect renames.
- Drop the unused BuildRequires libxml2-devel.
- Drop the 7.99.x version-munging patch.

* Fri Nov 09 2012 Josh Stone <jistone@redhat.com> 7.99.2-0.29
- Rebase to git e99d7070bbc39c76d6d528db530046c22681c17e

* Mon Oct 29 2012 Josh Stone <jistone@redhat.com> 7.99.2-0.28
- Bump to 7.99.2 per abi-compliance-checker results

* Fri Oct 26 2012 Josh Stone <jistone@redhat.com> 7.99.1-0.27
- Rebase to git dd8f40b7b4742ad97098613876efeef46d3d9e65
- Use _smp_mflags to enable building in parallel.

* Wed Oct 03 2012 Josh Stone <jistone@redhat.com> 7.99.1-0.26
- Rebase to git 557599ad7417610f179720ad88366c32a0557127

* Thu Sep 20 2012 Josh Stone <jistone@redhat.com> 7.99.1-0.25
- Rebase on newer git tree.
- Bump the fake version to 7.99.1 to account for ABI differences.
- Enforce the minimum libdwarf version.
- Drop the upstreamed R_PPC_NUM patch.

* Wed Aug 15 2012 Karsten Hopp <karsten@redhat.com> 7.99-0.24
- check if R_PPC_NUM is defined before using it, similar to R_PPC64_NUM

* Mon Jul 30 2012 Josh Stone <jistone@redhat.com> 7.99-0.23
- Rebase on newer git tree.
- Update license files with upstream additions.
- Split documentation into -doc subpackage.
- Claim ownership of %{_libdir}/dyninst.

* Fri Jul 27 2012 William Cohen <wcohen@redhat.com> - 7.99-0.22
- Correct requires for dyninst-devel.

* Wed Jul 25 2012 Josh Stone <jistone@redhat.com> - 7.99-0.21
- Rebase on newer git tree
- Update context in dyninst-git.patch
- Drop dyninst-delete_array.patch
- Drop dyninst-common-makefile.patch

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.99-0.20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 William Cohen <wcohen@redhat.com> - 7.99-0.19
- Patch common/i386-unknown-linux2.4/Makefile to build.

* Fri Jul 13 2012 William Cohen <wcohen@redhat.com> - 7.99-0.18
- Rebase on newer git tree the has a number of merges into it.
- Adjust spec file to allow direct use of git patches
- Fix to eliminate unused varables.
- Proper delete for array.

* Thu Jun 28 2012 William Cohen <wcohen@redhat.com> - 7.99-0.17
- Rebase on newer git repo.

* Thu Jun 28 2012 William Cohen <wcohen@redhat.com> - 7.99-0.16
- Eliminate dynptr.h file use with rebase on newer git repo.

* Mon Jun 25 2012 William Cohen <wcohen@redhat.com> - 7.99-0.14
- Rebase on newer git repo.

* Tue Jun 19 2012 William Cohen <wcohen@redhat.com> - 7.99-0.12
- Fix static library and header file permissions.
- Use sources from the dyninst git repositories.
- Fix 32-bit library versioning for libdyninstAPI_RT_m32.so.

* Wed Jun 13 2012 William Cohen <wcohen@redhat.com> - 7.99-0.11
- Fix library versioning.
- Move .so links to dyninst-devel.
- Remove unneded clean section.

* Fri May 11 2012 William Cohen <wcohen@redhat.com> - 7.0.1-0.9
- Clean up Makefile rules.

* Sat May 5 2012 William Cohen <wcohen@redhat.com> - 7.0.1-0.8
- Clean up spec file.

* Wed May 2 2012 William Cohen <wcohen@redhat.com> - 7.0.1-0.7
- Use "make install" and do staged build.
- Use rpm configure macro.

* Thu Mar 15 2012 William Cohen <wcohen@redhat.com> - 7.0.1-0.5
- Nuke the bundled boost files and use the boost-devel rpm instead.

* Mon Mar 12 2012 William Cohen <wcohen@redhat.com> - 7.0.1-0.4
- Initial submission of dyninst spec file.

# https://fedoraproject.org/wiki/Packaging:Haskell

%global ghc_compiler_version 7.8.4
%global alex_version 3.1.4
%global cabal_install_version 1.18.1.0
%global happy_version 1.19.5

%global HTTP_version 4000.2.10
%global HUnit_version 1.2.5.2
%global html_version 1.0.1.2
%global mtl_version 2.1.3.1
%global network_version 2.4.2.3
%global parallel_version 3.2.0.4
%global parsec_version 3.1.5
%global QuickCheck_version 2.7.6
%global random_version 1.0.1.1
%global regex_base_version 0.93.2
%global regex_compat_version 0.95.1
%global regex_posix_version 0.95.2
%global stm_version 2.4.2
%global syb_version 0.4.1
%global text_version 1.1.1.3
%global xhtml_version 3000.2.1
%global zlib_version 0.5.4.1
# 2012.4
%global async_version 2.0.1.5
%global primitive_version 0.5.2.1
%global split_version 0.2.2
%global vector_version 0.10.9.1
# 2013.2
%global attoparsec_version 0.11.3.4
%global case_insensitive_version 1.1.0.3
%global hashable_version 1.2.2.0
%global unordered_containers_version 0.2.4.0
# 2014.2
%global hscolour_version 1.20.3

%global separate_packages QuickCheck|HTTP|HUnit|alex|cabal-install|happy|html|mtl|network|parallel|parsec|random|regex-base|regex-compat|regex-posix|stm|syb|text|zlib|async|primitive|split|vector|attoparsec|case-insensitive|hashable|unordered-containers|xhtml|hscolour

%global upstream_version 2014.2.0.0

Name:           haskell-platform
Version:        %{upstream_version}.2
# Since library subpackages are versioned:
# - release can only be reset if all library versions get bumped simultaneously
#   (eg for a major release)
# - minor release numbers should be incremented monotonically
Release:        5%{?dist}
Summary:        Standard Haskell distribution

Group:          Development/Tools
License:        BSD
URL:            http://www.haskell.org/platform/
Source0:        http://www.haskell.org/platform/download/%{version}/%{name}-%{upstream_version}-srcdist.tar.gz
Patch1:         haskell-platform-2014.2.0.0-version-bumps.patch

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros-extra

BuildRequires:  alex = %{alex_version}
BuildRequires:  cabal-install = %{cabal_install_version}
BuildRequires:  ghc-compiler = %{ghc_compiler_version}
# GLUT
BuildRequires:  freeglut-devel%{?_isa}
BuildRequires:  happy = %{happy_version}
# OpenGL
BuildRequires:  mesa-libGL-devel%{?_isa},mesa-libGLU-devel%{?_isa}
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-deepseq-devel
BuildRequires:  ghc-haskell98-devel
BuildRequires:  ghc-HUnit-devel = %{HUnit_version}
BuildRequires:  ghc-HTTP-devel = %{HTTP_version}
BuildRequires:  ghc-html-devel = %{html_version}
BuildRequires:  ghc-mtl-devel = %{mtl_version}
BuildRequires:  ghc-network-devel = %{network_version}
BuildRequires:  ghc-parallel-devel = %{parallel_version}
BuildRequires:  ghc-parsec-devel = %{parsec_version}
BuildRequires:  ghc-QuickCheck-devel = %{QuickCheck_version}
BuildRequires:  ghc-random-devel = %{random_version}
BuildRequires:  ghc-regex-base-devel = %{regex_base_version}
BuildRequires:  ghc-regex-compat-devel = %{regex_compat_version}
BuildRequires:  ghc-regex-posix-devel = %{regex_posix_version}
BuildRequires:  ghc-stm-devel = %{stm_version}
BuildRequires:  ghc-syb-devel = %{syb_version}
%ifarch %{ghc_arches_with_ghci}
BuildRequires:  ghc-template-haskell-devel
%endif
BuildRequires:  ghc-text-devel = %{text_version}
BuildRequires:  ghc-time-devel
BuildRequires:  ghc-xhtml-devel = %{xhtml_version}
BuildRequires:  ghc-zlib-devel = %{zlib_version}
# part of HP-2012.4
BuildRequires:  ghc-async-devel = %{async_version}
BuildRequires:  ghc-primitive-devel = %{primitive_version}
BuildRequires:  ghc-split-devel = %{split_version}
BuildRequires:  ghc-vector-devel = %{vector_version}
# part of HP-2013.2
BuildRequires:  ghc-attoparsec-devel = %{attoparsec_version}
BuildRequires:  ghc-case-insensitive-devel = %{case_insensitive_version}
BuildRequires:  ghc-hashable-devel = %{hashable_version}
BuildRequires:  ghc-unordered-containers-devel = %{unordered_containers_version}
# part of HP-2014.2
BuildRequires:  ghc-hscolour-devel = %{hscolour_version}
BuildRequires:  hscolour = %{hscolour_version}

# ghci "ghc" library is not officially part of hackage-platform
Requires:       ghc-compiler = %{ghc_compiler_version}
Requires:       alex = %{alex_version}
Requires:       cabal-install >= %{cabal_install_version}
Requires:       happy = %{happy_version}
Requires:       ghc-haskell-platform-devel = %{version}-%{release}
Requires:       hscolour = %{hscolour_version}

%description
Haskell Platform is a suite of stable and well used Haskell libraries
and tools.  It provides a good starting environment for Haskell development.


%global BSDHaskellReport BSD%{space}and%{space}HaskellReport

%global haskell_platform_version %{version}

%if %{defined ghclibdir}
%ghc_lib_subpackage fgl 5.5.0.1
%ghc_lib_subpackage -c mesa-libGLU-devel%{?_isa} GLURaw 1.4.0.1
%ghc_lib_subpackage -c freeglut-devel%{?_isa} GLUT 2.5.1.1
# used by lambdabot-utils
%ghc_lib_subpackage haskell-src 1.0.1.6
%ghc_lib_subpackage OpenGL 2.9.2.0
%ghc_lib_subpackage -c mesa-libGL-devel%{?_isa} OpenGLRaw 1.5.0.0
%endif

%package -n ghc-haskell-platform-devel
Summary:        Haskell Platform library development files
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
%{?ghc_packages_list:Requires: %(echo %{ghc_packages_list} | sed -e "s/\([^ ]*\)-\([^ ]*\)/ghc-\1-devel = \2-%{release},/g")}
# pull in all of ghc for least surprise
# even though libghc is not formally part of HP
Requires:       ghc = %{ghc_compiler_version}
Requires:       ghc-HUnit-devel = %{HUnit_version}
Requires:       ghc-HTTP-devel = %{HTTP_version}
Requires:       ghc-html-devel = %{html_version}
Requires:       ghc-mtl-devel = %{mtl_version}
Requires:       ghc-network-devel = %{network_version}
Requires:       ghc-parallel-devel = %{parallel_version}
Requires:       ghc-parsec-devel = %{parsec_version}
Requires:       ghc-QuickCheck-devel = %{QuickCheck_version}
Requires:       ghc-random-devel = %{random_version}
Requires:       ghc-regex-base-devel = %{regex_base_version}
Requires:       ghc-regex-compat-devel = %{regex_compat_version}
Requires:       ghc-regex-posix-devel = %{regex_posix_version}
Requires:       ghc-stm-devel = %{stm_version}
Requires:       ghc-syb-devel = %{syb_version}
Requires:       ghc-text-devel = %{text_version}
Requires:       ghc-xhtml-devel = %{xhtml_version}
Requires:       ghc-zlib-devel = %{zlib_version}
# part of HP-2012.4
Requires:       ghc-async-devel = %{async_version}
Requires:       ghc-primitive-devel = %{primitive_version}
Requires:       ghc-split-devel = %{split_version}
Requires:       ghc-vector-devel = %{vector_version}
# part of HP-2013.2
Requires:       ghc-attoparsec-devel = %{attoparsec_version}
Requires:       ghc-case-insensitive-devel = %{case_insensitive_version}
Requires:       ghc-hashable-devel = %{hashable_version}
Requires:       ghc-unordered-containers-devel = %{unordered_containers_version}
# part of HP-2014.2
Requires:       ghc-hscolour-devel = %{hscolour_version}
# added in F17 devel cycle
Obsoletes:      ghc-haskell-platform < %{version}-%{release}

%description -n ghc-haskell-platform-devel
This provides the haskell-platform meta library package.


%global version %{haskell_platform_version}


%prep
%setup -q -n %{name}-%{upstream_version}
%patch1 -p1 -b .orig

# hack for h-p.cabal in top dir
mkdir packages/%{name}-%{version}
cp LICENSE hptool/Setup.hs packages/%{name}-%{version}


%ifarch aarch64
# bz#1210323
cabal-tweak-dep-ver alex '==3.1.3' ''
cabal-tweak-dep-ver cabal-install '==1.18.0.5' ''
cabal-tweak-dep-ver happy '==1.19.4' ''
cabal-tweak-dep-ver hscolour '==1.20.3' ''
%else
cabal-tweak-dep-ver alex '==3.1.3' '==3.1.4'
cabal-tweak-dep-ver cabal-install '==1.18.0.5' '==%{cabal_install_version}'
cabal-tweak-dep-ver happy '==1.19.4' '==1.19.5'
# HsColour reports 1.20
cabal-tweak-dep-ver hscolour '==1.20.3' '==1.20'
%endif
mv %{name}.cabal packages/%{name}-%{version}


%build
HOME=$PWD
%define cabal_configure_options --user
cd packages
for i in $(egrep -v "^(%{?separate_packages})-" ../etc/build.packages) %{name}-%{version}; do
name=$(echo $i | sed -e "s/\(.*\)-.*/\1/")
ver=$(echo $i | sed -e "s/.*-\(.*\)/\1/")
cd $name-$ver
case $name in
haskell-platform)
%ghc_lib_build_without_haddock $name $ver
;;
*)
%ghc_lib_build $name $ver
./Setup register --inplace
;;
esac
cd ..
done
cd ..


%install
HOME=$PWD

cd packages
for i in $(egrep -v "^(%{?separate_packages})-" ../etc/build.packages) %{name}-%{version}; do
name=$(echo $i | sed -e "s/\(.*\)-.*/\1/")
ver=$(echo $i | sed -e "s/.*-\(.*\)/\1/")
cd $name-$ver
%ghc_lib_install $name $ver
# for ghc-7.8
#%%ghc_gen_filelists $name $ver
echo "%doc packages/$name-$ver/LICENSE" >> ghc-$name.files
cd ..
done

mv */*.files ..
cd ..

%ghc_strip_dynlinked

rm %{buildroot}/%{_docdir}/ghc-%{name}*/LICENSE


%post -n ghc-haskell-platform-devel
%ghc_pkg_recache


%postun -n ghc-haskell-platform-devel
%ghc_pkg_recache


%files
%doc packages/%{name}-%{version}/LICENSE


%files -n ghc-haskell-platform-devel -f ghc-haskell-platform-devel.files
%doc packages/haskell-platform-%{version}/LICENSE


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2014.2.0.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 Jens Petersen <petersen@redhat.com> - 2014.2.0.0.3-4
- bump cabal-install to 1.18.1.0 and allow newer versions

* Fri Apr 10 2015 Jens Petersen <petersen@redhat.com> - 2014.2.0.0.2-3
- workaround build-tools version detection failures on aarch64 (#1210323)

* Fri Apr  3 2015 Jens Petersen <petersen@redhat.com> - 2014.2.0.0.2-2
- bump alex to 3.1.4
- bump cabal-install to 1.18.0.8
- bump happy to 1.19.5
- bump QuickCheck to 2.7.6

* Fri Feb  6 2015 Jens Petersen <petersen@redhat.com> - 2014.2.0.0.1-1
- use ghc-7.8.4
- bump attoparsec to 0.11.3.4
- bump text to 1.1.1.3

* Wed Aug 20 2014 Jens Petersen <petersen@redhat.com> - 2014.2.0.0-1
- update to haskell-platform-2014.2
- ghc-7.8.3+ ships xhtml
- cgi dropped
- requires hscolour

* Tue Jul  8 2014 Jens Petersen <petersen@redhat.com> - 2013.2.0.0-37
- rebuild for F21

* Mon Apr 21 2014 Jens Petersen <petersen@redhat.com> - 2013.2.0.0-36
- fix build for versioned docdirs

* Mon Apr 21 2014 Jens Petersen <petersen@redhat.com> - 2013.2.0.0-35
- alex and syb are separate packages again

* Mon Apr 14 2014 Jens Petersen <petersen@redhat.com> - 2013.2.0.0-34
- cabal-install, happy, parallel, regex-compat are now separate packages

* Thu Mar 27 2014 Jens Petersen <petersen@redhat.com> - 2013.2.0.0-33
- transformers lib is now separate package

* Wed Mar 26 2014 Jens Petersen <petersen@redhat.com> - 2013.2.0.0-32
- QuickCheck and HTTP are separate packages again

* Mon Mar 17 2014 Jens Petersen <petersen@redhat.com> - 2013.2.0.0-31
- HUnit is a separate package again
- network is a separate package again

* Thu Feb  6 2014 Jens Petersen <petersen@redhat.com>
- only show cabal-install upgrade notice for verbose

* Mon Feb  3 2014 Jens Petersen <petersen@redhat.com> - 2013.2.0.0-30
- parsec is now a separate package again
- async is now a new separate package

* Wed Jan  8 2014 Jens Petersen <petersen@redhat.com> - 2013.2.0.0-29
- regex-posix is now a separate package

* Fri Jan  3 2014 Jens Petersen <petersen@redhat.com> - 2013.2.0.0-28
- html and regex-base are now separate packages

* Wed Dec  4 2013 Jens Petersen <petersen@redhat.com> - 2013.2.0.0-27
- mtl and zlib are now separate packages again

* Thu Oct 31 2013 Jens Petersen <petersen@redhat.com> - 2013.2.0.0-26
- fix alex patching for ppc and s390 archs

* Sat Oct 26 2013 Jens Petersen <petersen@redhat.com> - 2013.2.0.0-25
- random and stm are separate packages again

* Fri Jul 26 2013 Jens Petersen <petersen@redhat.com> - 2013.2.0.0-24
- fix packaging of license files when building without shared libraries
- tweaks for F20 unversioned docdir

* Sat May  4 2013 Jens Petersen <petersen@redhat.com> - 2013.2.0.0-23
- update to 2013.2.0.0
- new packages: GLURaw, OpenGLRaw
- new depends: attoparsec, case-insensitive, hashable, unordered-containers
- use ghc_fix_dynamic_rpath
- text lib is separate package again

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.4.0.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec  6 2012 Jens Petersen <petersen@redhat.com> - 2012.4.0.0-21
- vector was patched to build on all archs (#883479)

* Wed Dec  5 2012 Jens Petersen <petersen@redhat.com> - 2012.4.0.0-20
- keep split, vector, and primitive in their own existing src packages
- allow building on ghc archs without ghci: ie without vector library (#883479)

* Sat Oct 20 2012 Jens Petersen <petersen@redhat.com> - 2012.4.0.0-19
- update to 2012.4.0.0
- new subpackages: async, split, vector, and primitive (vector dep)
- drop explicit BR hscolour

* Mon Jul 23 2012 Jens Petersen <petersen@redhat.com> - 2012.2.0.0-18
- also apply the alex fix-bang-pattern patch for s390 and s390x

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.2.0.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 2012.2.0.0-16
- change prof BRs to devel

* Thu Jun  7 2012 Jens Petersen <petersen@redhat.com> - 2012.2.0.0-15
- update to 2012.2.0.0
- build the whole of haskell-platform now from this package
  and subpackage like ghc's libraries
- add alex fix-bang-pattern.diff patch from Debian to fix build on ppc archs
  - requires BR alex
- drop common_summary and common_description for subpackaging
- no longer need to unset debug_package
- make sure all the dynamically linked files get stripped
- needs ghc-rpm-macros 0.95.2 or later to build
- use chrpath to fix the program RPATHs when dynamically linked to HP libs

* Wed May  9 2012 Jens Petersen <petersen@redhat.com> - 2011.4.0.741-2
- update cabal-install to 0.14.0

* Sat Mar 24 2012 Jens Petersen <petersen@redhat.com> - 2011.4.0.741-1
- update to ghc-7.4.1 and latest libraries
- temporarily just a meta-package

* Wed Mar 21 2012 Jens Petersen <petersen@redhat.com> - 2011.4.0.0-7
- require ghc-compiler instead of ghc to avoid the ghc lib

* Fri Jan 20 2012 Jens Petersen <petersen@redhat.com> - 2011.4.0.0-6
- update to cabal2spec-0.25.2

* Thu Jan 19 2012 Jens Petersen <petersen@redhat.com> - 2011.4.0.0-5
- update the description

* Thu Jan 19 2012 Jens Petersen <petersen@redhat.com> - 2011.4.0.0-4
- update the source url

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011.4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jan  1 2012 Jens Petersen <petersen@redhat.com> - 2011.4.0.0-2
- define ghc_without_shared since ghc-haskell-platform-devel no longer
  requires ghc-haskell-platform

* Wed Dec 28 2011 Jens Petersen <petersen@redhat.com> - 2011.4.0.0-1
- update to 2011.4.0.0
- reenable ppc64
- drop ghc-haskell-platform subpackage
- require ghc-libraries instead of ghc-devel

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 2011.2.0.1-2
- ghc_arches replaces ghc_excluded_archs (cabal2spec-0.23.2)

* Mon Jun 20 2011 Jens Petersen <petersen@redhat.com> - 2011.2.0.1-1
- update to 2011.2.0.1: ghc-7.0.3 and text-0.11.0.6
- update source url
- use ghc_excluded_archs
- exclude ppc64: no QuickCheck
- bump ghc to 7.0.4
- use top_prefix for path to haskell-platform subdir in large tarball
- drop upstream_version

* Fri May 27 2011 Jens Petersen <petersen@redhat.com> - 2011.2.0.0-5
- drop the prof subpackage

* Wed May 25 2011 Jens Petersen <petersen@redhat.com> - 2011.2.0.0-4
- add ppc64 arch

* Mon Mar 28 2011 Jens Petersen <petersen@redhat.com> - 2011.2.0.0-3
- remove duplicate license file from ghc-haskell-platform

* Mon Mar 28 2011 Jens Petersen <petersen@redhat.com> - 2011.2.0.0-2
- fix the install scripts:
- ghc_reindex_haddock is now redundant
- use ghc_pkg_recache

* Fri Mar 11 2011 Jens Petersen <petersen@redhat.com> - 2011.2.0.0-1
- 2011.2.0.0 final

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 2011.1.0.0-0.6
- Enable build on sparcv9

* Tue Feb 15 2011 Jens Petersen <petersen@redhat.com> - 2011.1.0.0-0.5
- update to latest haskell-platform-2011.1 snapshot

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011.1.0.0-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 22 2011 Jens Petersen <petersen@redhat.com> - 2011.1.0.0-0.3
- make ghc-haskell-platform-devel require ghc-devel and ghc_devel_requires
- build with ghc_lib_build and without_haddock

* Tue Jan 18 2011 Jens Petersen <petersen@redhat.com> - 2011.1.0.0-0.2
- update to cabal2spec-0.22.4

* Sun Dec  5 2010 Jens Petersen <petersen@redhat.com> - 2011.1.0.0-0.1
- update to 2011.1.0.0 alpha snapshot

* Fri Nov 26 2010 Jens Petersen <petersen@redhat.com> - 2010.2.0.0.701-1
- bump some versions for ghc-7.0.1
- add hscolour
- no haddock documentation to build
- remove duplicate LICENSE file

* Fri Jul 23 2010 Jens Petersen <petersen@redhat.com> - 2010.2.0.0-1
- update to 2010.2.0.0 final release (no actual changes)

* Sun Jul 18 2010 Jens Petersen <petersen@redhat.com> - 2010.2.0.0-0.1
- drop debuginfo again: ghc_strip_dynlinked got fixed in ghc-rpm-macros-0.8.1

* Fri Jul 16 2010 Jens Petersen <petersen@redhat.com> - 2010.2.0.0-0.1
- update to 2010.2.0.0 RC
- obsolete ghc-haskell-platform-doc in line with ghc-rpm-macros-0.8.0
- add License to base library too

* Sun Jun 27 2010 Jens Petersen <petersen@redhat.com> - 2010.1.0.0.6123-1
- bump ghc to 6.12.3
- sync cabal2spec-0.22.1
- enable debugging for now to avoid empty strip error

* Thu Apr 29 2010 Jens Petersen <petersen@redhat.com> - 2010.1.0.0.6122-1
- break haskell-platform-2010.1.0.0 with ghc-6.12.2

* Wed Mar 24 2010 Jens Petersen <petersen@redhat.com> - 2010.1.0.0-1
- update to 2010.1.0.0 beta release
- update versions of alex, cgi, network, parallel, QuickCheck, HTTP
- new deepseq dep (#576482)

* Thu Jan 28 2010 Jens Petersen <petersen@redhat.com> - 2009.3.1.20100115-0.2
- add filelist for shared libs
- update devel post and postun

* Sat Jan 16 2010 Jens Petersen <petersen@redhat.com> - 2009.3.1.20100115-0.1
- update to darcs snapshot patched for ghc-6.12.1
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use common_summary and common_description
- use ghc_lib_package and ghc_pkg_deps
- build shared library
- drop redundant buildroot and its install cleaning

* Mon Sep 28 2009 Jens Petersen <petersen@redhat.com> - 2009.2.0.2-3
- fix rpmlint warnings (bos, #523883)

* Mon Sep 28 2009 Jens Petersen <petersen@redhat.com> - 2009.2.0.2-2
- add all the buildrequires (#523883)
- create ghcpkgdir since metapackage
- nothing in bindir

* Thu Sep 17 2009 Jens Petersen <petersen@redhat.com> - 2009.2.0.2-1
- initial packaging for Fedora

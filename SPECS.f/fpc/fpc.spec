Name:           fpc
Version:        2.6.4
Release:        1%{?dist}
Summary:        Free Pascal Compiler
Summary(zh_CN.UTF-8): 自由的 Pascal 编译器

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        GPLv2+ and LGPLv2+ with exceptions
URL:            http://www.freepascal.org/
Source0:        ftp://ftp.freepascal.org/pub/fpc/dist/${version}/source/fpcbuild-%{version}.tar.gz
# rc1 version
#Source0:        ftp://ftp.freepascal.org/pub/fpc/beta/2.6.2-rc1/source/fpcbuild-2.6.2rc1.tar.gz
# This is only needed when useprebuiltcompiler is defined.
# But it's not in an 'if defined' block, since the file has to be included in the srpm
# Thus you should enable this line when useprebuildcompiler is defined for any target
# Source1:        http://www.cnoc.nl/fpc/%{name}-%{version}.compiler.bin.tar.gz
# Configuration templates:
Source2:        fpc.cft
Source3:        fppkg.cfg
Source4:        default.cft

Requires:       gpm, ncurses, binutils
%if ! %{defined useprebuiltcompiler}
BuildRequires:  fpc
%endif
BuildRequires:  tetex, tetex-latex, tetex-fonts

ExcludeArch:    s390 s390x

%description

Free Pascal is a free 32/64bit Pascal Compiler. It comes with a run-time
library and is fully compatible with Turbo Pascal 7.0 and nearly Delphi
compatible. Some extensions are added to the language, like function
overloading and generics. Shared libraries can be linked. This package
contains command-line compiler and utils. Provided units are the runtime
library (RTL), free component library (FCL) and the base and extra packages.

%package doc
Summary:        Free Pascal Compiler - documentation and examples
Group:          Documentation

%description doc

The fpc-doc package contains the documentation (in pdf format) and examples
of Free Pascal.

%package src
Summary:        Free Pascal Compiler - sources
Group:          Development/Languages

%description src

The fpc-src package contains the sources of Free Pascal, for documentation or
automatical-code generation purposes.

%define smart _smart 

%define fpcdebugopt -gl
%ifarch ppc
%define ppcname ppcppc
%else
%ifarch x86_64
%define ppcname ppcx64
%else
%ifarch ppc64
%define ppcname ppcppc64
%else
%define ppcname ppc386
%endif
%endif
%endif

%prep
%if %{defined useprebuiltcompiler}
%setup -a1 -n fpcbuild-%{version}rc1 -q
%else
%setup -n fpcbuild-%{version}rc1 -q
%endif

%build
# The source-files:
mkdir -p fpc_src
cp -a fpcsrc/rtl fpc_src
cp -a fpcsrc/packages fpc_src
rm -rf fpc_src/packages/extra/amunits
rm -rf fpc_src/packages/extra/winunits

%if %{defined useprebuiltcompiler}
STARTPP=`pwd`/startcompiler/%{ppcname}
%else
STARTPP=%{ppcname}
%endif
%define fpcopt -k"--build-id"
cd fpcsrc
NEWPP=`pwd`/compiler/%{ppcname}
NEWFPDOC=`pwd`/utils/fpdoc/fpdoc
DATA2INC=`pwd`/utils/data2inc
make %{?_smp_mflags} compiler_cycle FPC=${STARTPP} OPT='%{fpcopt} %{fpcdebugopt}'
make %{?_smp_mflags} rtl_clean rtl%{smart} FPC=${NEWPP} OPT='%{fpcopt}'
make %{?_smp_mflags} packages%{smart} FPC=${NEWPP} OPT='%{fpcopt}'
make %{?_smp_mflags} ide_all FPC=${NEWPP} OPT='%{fpcopt} %{fpcdebugopt}'
make %{?_smp_mflags} utils_all FPC=${NEWPP} DATA2INC=${DATA2INC} OPT='%{fpcopt} %{fpcdebugopt}'

cd ..
# FIXME: -j1 as there is a race - seen on "missing" `rtl.xct'.
make -j1 -C fpcdocs pdf FPC=${NEWPP} FPDOC=${NEWFPDOC}

%install
rm -rf %{buildroot}
cd fpcsrc
FPCMAKE=`pwd`/utils/fpcm/fpcmake
NEWPP=`pwd`/compiler/%{ppcname}
INSTALLOPTS="-j1 FPC=${NEWPP} FPCMAKE=${FPCMAKE} \
                INSTALL_PREFIX=%{buildroot}%{_prefix} \
                INSTALL_LIBDIR=%{buildroot}%{_libdir} \
                INSTALL_BASEDIR=%{buildroot}%{_libdir}/%{name}/%{version} \
                CODPATH=%{buildroot}%{_libdir}/%{name}/lexyacc \
                INSTALL_DOCDIR=%{buildroot}%{_defaultdocdir}/%{name}-%{version} \
                INSTALL_BINDIR=%{buildroot}%{_bindir}
                INSTALL_EXAMPLEDIR=%{buildroot}%{_defaultdocdir}/%{name}-%{version}/examples"
make compiler_distinstall ${INSTALLOPTS}
make rtl_distinstall ${INSTALLOPTS}
make packages_distinstall ${INSTALLOPTS}
make ide_distinstall ${INSTALLOPTS}
make utils_distinstall ${INSTALLOPTS}
cd ../install
make -C doc ${INSTALLOPTS}
make -C man ${INSTALLOPTS} INSTALL_MANDIR=%{buildroot}%{_mandir}
cd ..
make -C fpcdocs pdfinstall ${INSTALLOPTS}

# create link
ln -sf ../%{_lib}/%{name}/%{version}/%{ppcname} %{buildroot}%{_bindir}/%{ppcname}

# Create a version independent compiler-configuration file with build-id
# enabled by default
# For this purpose some non-default templates are used. So the samplecfg
# script could not be used and fpcmkcfg is called directly.
%{buildroot}%{_bindir}/fpcmkcfg -p -t %{SOURCE2} -d "basepath=%{_exec_prefix}" -o %{buildroot}%{_sysconfdir}/fpc.cfg
# Create the IDE configuration files
%{buildroot}%{_bindir}/fpcmkcfg -p -1 -d "basepath=%{_libdir}/%{name}/\$fpcversion" -o %{buildroot}%{_libdir}/%{name}/%{version}/ide/text/fp.cfg
%{buildroot}%{_bindir}/fpcmkcfg -p -2 -o %{buildroot}%{_libdir}/%{name}/%{version}/ide/text/fp.ini
# Create the fppkg configuration files
%{buildroot}%{_bindir}/fpcmkcfg -p -t %{SOURCE3} -d CompilerConfigDir=%{_sysconfdir}/fppkg -d arch=%{_arch} -o %{buildroot}%{_sysconfdir}/fppkg.cfg
%{buildroot}%{_bindir}/fpcmkcfg -p -t %{SOURCE4} -d fpcbin=%{_bindir}/fpc -d GlobalPrefix=%{_exec_prefix} -d lib=%{_lib} -o %{buildroot}%{_sysconfdir}/fppkg/default_%{_arch}

# Include the COPYING-information for the compiler/rtl/fcl in the documentation
cp -a fpcsrc/compiler/COPYING.txt %{buildroot}%{_defaultdocdir}/%{name}-%{version}/COPYING
cp -a fpcsrc/rtl/COPYING.txt %{buildroot}%{_defaultdocdir}/%{name}-%{version}/COPYING.rtl
cp -a fpcsrc/rtl/COPYING.FPC %{buildroot}%{_defaultdocdir}/%{name}-%{version}/COPYING.FPC

# The source-files:
mkdir -p %{buildroot}%{_datadir}/fpcsrc
cp -a fpc_src/* %{buildroot}%{_datadir}/fpcsrc/

# Workaround:
# newer rpm versions do not allow garbage
# delete lexyacc
rm -rf %{buildroot}%{_libdir}/%{name}/lexyacc

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.cfg
%config(noreplace) %{_sysconfdir}/fppkg.cfg
%config(noreplace) %{_sysconfdir}/fppkg/default_%{_arch}
%dir %{_defaultdocdir}/%{name}-%{version}/
%doc %{_defaultdocdir}/%{name}-%{version}/NEWS
%doc %{_defaultdocdir}/%{name}-%{version}/README
%doc %{_defaultdocdir}/%{name}-%{version}/readme.ide
%doc %{_defaultdocdir}/%{name}-%{version}/faq*
%doc %{_defaultdocdir}/%{name}-%{version}/COPYING*
%{_mandir}/*/*

%files doc
%defattr(-,root,root,-)
%dir %{_defaultdocdir}/%{name}-%{version}/
%doc %{_defaultdocdir}/%{name}-%{version}/*.pdf
%doc %{_defaultdocdir}/%{name}-%{version}/examples

%files src
%defattr(-,root,root,-)
%{_datadir}/fpcsrc

%changelog
* Sat Nov 24 2012 Bruno Wolff III <bruno@wolff.to> - 2.6.2-0.1.rc1
- Use standard versioning, so non-rc versions will be higher
- Fix issue with some things using 'rc1' appended to version name and others not

* Sat Nov 3 2012 Joost van der Sluis <joost@cnoc.nl> - 2.6.2rc1-1
- Upgrade to upstream release 2.6.2rc1.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 14 2012 Karsten Hopp <karsten@redhat.com> 2.6.0-2
- define ppcname on ppc64

* Fri Jan 27 2012 Joost van der Sluis <joost@cnoc.nl> - 2.6.0-1
- Upgrade to upstream release 2.6.0.
- Do not use samplecfg for generating the configuration files anymore, but
  call fpcmkcfg directly.
- Changed the name of the project from Freepascal to Free Pascal

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 5 2011 Joost van der Sluis <joost@cnoc.nl> - 2.4.2-1
- Upgrade to upstream release 2.4.2.

* Sat Oct 23 2010 Joost van der Sluis <joost@cnoc.nl> - 2.4.2-0.1.rc1
- Upgrade to upstream release 2.4.2rc1.

* Wed May  5 2010 Joost van der Sluis <joost@cnoc.nl> - 2.4.0-1.fc14
- Drop fpc-2.2.4-stackexecute.patch since bug was fixed in 2.4.0

* Tue May  4 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 2.4.0-0.fc14
- Upgrade to upstream release 2.4.0.
  - Drop fpc-2.2.4-r12475.patch as present in 2.4.0.
- Base the .spec build on upstream released archive (fpcbuild-2.4.0.tar.gz).
- Remove the obsolete .spec BuildRoot tag.
- Remove BuildRequires for binutils and glibc-devel as guaranteed as always
  provided in Fedora Packaging Guidlines.
- Remove Requires glibc as guaranteed on a Fedora system.
- Add %%{?_smp_mflags} and -j1 appropriately, applied one -j1 workaround.
- Change {compiler,rtl}/COPYING to COPYING.txt.

* Tue Oct 6 2009 Joost van der Sluis <joost@cnoc.nl> 2.2.4-4
- fixed procvar parameter passing on ppc/sysv (by value instead of by
  reference -- except for method procvars, for tmethod record compatibility) 

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Dan Horak <dan[at]danny.cz> 2.2.4-2
- Exclude s390/s390x architectures

* Sun Apr 19 2009 Joost van der Sluis <joost@cnoc.nl> 2.2.4-1
- Updated to version 2.2.4

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Oct 25 2008 Joost van der Sluis <joost@cnoc.nl> 2.2.2-3
- Do not distribute the RTL and packages with debug-info included
- Fix the location of the fpc-binary in the samplecfg script

* Sun Oct 19 2008 Joost van der Sluis <joost@cnoc.nl> 2.2.2-2
- Pass -z noexecstack to the linker from within the configuration file fpc.cfg (fpc-bug #11563)
- Added patch to fix fpc-bug #11837 for usage with newer gtk2-versions

* Wed Aug 13 2008 Joost van der Sluis <joost@cnoc.nl> 2.2.2-1
- Updated to version 2.2.2
- Disabled debuginfo for ppc64 again
- Detect 32 or 64 bit compilation in the configuration file fpc.cfg

* Sun Jun 22 2008 Joost van der Sluis <joost@cnoc.nl> 2.2.2rc1-1
- Updated to version 2.2.2rc1
- Enabled debuginfo for ppc64 again
- Do not strip the debugdata on x86_64 anymore
- Packages_base, packages_fcl and packages_extra are merged into packages
- Don't install packages_fv separately anymore
- Fix for incorrect path in official fpc 2.2.2rc1-sourcefile
- Updated licence-tag from "GPL and modified LGPL" to fedora-tag "GPLv2+ and LGPLv2+ with exceptions"
- Removed UsePrebuildcompiler define for ppc64

* Wed Apr 16 2008 Joost van der Sluis <joost@cnoc.nl> 2.2.0-12
- Fix for DWARF-debug generation - fixes some more build problems on x86_64 and F9, bugzilla 337051

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.2.0-11
- Autorebuild for GCC 4.3

* Mon Oct 16 2007 Joost van der Sluis <joost@cnoc.nl> 2.2.0-10
- Strip the debuginfo from grab_vcsa and ppudump, since debugedit chokes on it
- Only strip debugdata on x86_64

* Mon Oct 16 2007 Joost van der Sluis <joost@cnoc.nl> 2.2.0-9
- Strip the debuginfo from mkxmlrpc, since debugedit chokes on it

* Mon Oct 16 2007 Joost van der Sluis <joost@cnoc.nl> 2.2.0-8
- Strip the debuginfo from h2pas, since debugedit chokes on it

* Mon Oct 16 2007 Joost van der Sluis <joost@cnoc.nl> 2.2.0-7
- Include the startcompiler on all targets, for the srpm-building

* Mon Oct 16 2007 Joost van der Sluis <joost@cnoc.nl> 2.2.0-6
- Disabled debuginfo for ppc64 only
- Enabled smart-linking on ppc64
- Added a patch for building documentation without fpc already installed

* Mon Oct 16 2007 Joost van der Sluis <joost@cnoc.nl> 2.2.0-5
- Disabled debuginfo

* Mon Oct 16 2007 Joost van der Sluis <joost@cnoc.nl> 2.2.0-4
- Enabled BuildId, added it to fpc.cfg

* Mon Oct 16 2007 Joost van der Sluis <joost@cnoc.nl> 2.2.0-3
- Disabled smart-linking on ppc64

* Mon Oct 16 2007 Joost van der Sluis <joost@cnoc.nl> 2.2.0-2
- Buildrequirement fpc is not needed when using a pre-built compiler binary

* Sun Oct 14 2007 Joost van der Sluis <joost@cnoc.nl> 2.2.0-1
- Updated to version 2.2.0
- Updated description
- Enabled smart-linking for ppc
- Do not include the built binary-files in fpc-src
- Added support for ppc64
- Added support to configuration file for dual 32/64 bit installations
- Fixed and enabled debug-package 

* Sat Sep 16 2006 Joost van der Sluis <joost@cnoc.nl> 2.0.4-2
- Fixed documentation building on powerpc

* Fri Sep 15 2006 Joost van der Sluis <joost@cnoc.nl> 2.0.4-1
- Updated to version 2.0.4

* Wed Mar 1 2006 Joost van der Sluis <joost@cnoc.nl> 2.0.2-4
- Rebuild for Fedora Extras 5

* Tue Dec 20 2005 Joost van der Sluis <joost@cnoc.nl> 2.0.2-3
- Disabled smart-linking for ppc

* Tue Dec 20 2005 Joost van der Sluis <joost@cnoc.nl> 2.0.2-2
- Updated fpc-2.0.2-G5.patch

* Tue Dec 20 2005 Joost van der Sluis <joost@cnoc.nl> 2.0.2-1
- Updated to version 2.0.2

* Wed Aug 17 2005 Joost van der Sluis <joost@cnoc.nl> 2.0.0-4
- Added %%{?dist} to release.

* Wed Aug 17 2005 Joost van der Sluis <joost@cnoc.nl> 2.0.0-3
- replaced the ppcpcc-2.1.1 startcompilercompiler for the
  ppcppc-2.0.0 startcompiler 

* Wed Aug 17 2005 Joost van der Sluis <joost@cnoc.nl> 2.0.0-2
- Added a patch for compilation on POWER5, and provided
  the new ppcppc binary/startcompiler

* Fri Aug 5 2005 Joost van der Sluis <joost@cnoc.nl> 2.0.0-1
- Removed gpm-devel requirement
- Fixed a type in the -src description

* Tue Jul 28 2005 Joost van der Sluis <joost@cnoc.nl> 2.0.0-1
- Added some requirements
- Added COPYING-info to %%doc

* Tue Jun 28 2005 Joost van der Sluis <joost@cnoc.nl> 2.0.0-0.6
- Only rtl, fcl and packages are added to src-subpackage
- Silenced post-script
- disabled the debuginfo-package

* Sat Jun 5 2005 Joost van der Sluis <joost@cnoc.nl> 2.0.0-0.5
- Added doc-subpackage
- Added src-subpackage

* Fri Jun 3 2005 Joost van der Sluis <joost@cnoc.nl> 2.0.0-0.4
- New fix for lib64 on x86_64
- small patches from Jens Petersen <petersen@redhat.com>

* Thu May 26 2005 Joost van der Sluis <joost@cnoc.nl> 2.0.0-0.3
- replaced 'lib' and 'lib64' by %%{_lib}

* Tue May 24 2005 Joost van der Sluis <joost@cnoc.nl> 2.0.0-0.2
- Fixed for lib64 on x86_64
- Changed summary, description and license
- Removed examples from installation
- Make clean removed from clean-section
- Clean-up
- replaced $RPM_BUILD_ROOT by %%{buildroot}

* Mon May 23 2005 Joost van der Sluis <joost@cnoc.nl> 2.0.0-0.1
- Initial build.

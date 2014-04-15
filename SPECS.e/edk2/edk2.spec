%define SVNDATE 20131114
%define SVNREV  14844

# More subpackages to come once licensing issues are fixed
Name:		edk2
Version:	%{SVNDATE}svn%{SVNREV}
Release:	1%{?dist}
Summary:	EFI Development Kit II

# There are no formal releases from upstream.
# Tarballs are created with:

# svn export -r ${SVNREV} \
#     https://edk2.svn.sourceforge.net/svnroot/edk2/trunk/edk2 edk2-r${SVNREV}
# rm -rf edk2-r${SVNREV}/BaseTools/Bin
# rm -rf edk2-r${SVNREV}/ShellBinPkg
# rm -rf edk2-r${SVNREV}/FatBinPkg
# tar -cv edk2-r${SVNREV} | xz -6 > edk2-r${SVNREV}.tar.xz
Source0:	edk2-r%{SVNREV}.tar.xz
Patch1:		basetools-arm.patch

License:	BSD
Group:		Applications/Emulators
URL:		http://sourceforge.net/apps/mediawiki/tianocore/index.php?title=EDK2

# We need to build tools everywhere, but how is still an open question
# https://bugzilla.redhat.com/show_bug.cgi?id=992180
ExclusiveArch:	%{ix86} x86_64 %{arm}

BuildRequires:	python2-devel
BuildRequires:	libuuid-devel

Requires:	edk2-tools%{?_isa} = %{version}-%{release}

%description
EDK II is a development code base for creating UEFI drivers, applications
and firmware images.

%package tools
Summary:	EFI Development Kit II Tools
Group:		Development/Tools
Requires:	edk2-tools-python = %{version}-%{release}

%description tools
This package provides tools that are needed to
build EFI executables and ROMs using the GNU tools.

%package tools-python
Summary:	EFI Development Kit II Tools
Group:		Development/Tools
Requires:	python
BuildArch:      noarch

%description tools-python
This package provides tools that are needed to build EFI executables
and ROMs using the GNU tools.  You do not need to install this package;
you probably want to install edk2-tools only.

%package tools-doc
Summary:	Documentation for EFI Development Kit II Tools
Group:		Development/Tools

%description tools-doc
This package documents the tools that are needed to
build EFI executables and ROMs using the GNU tools.

%prep
%setup -q -n %{name}-r%{SVNREV}
%patch1 -p1

%build
source ./edksetup.sh

# Build is broken if MAKEFLAGS contains -j option.
unset MAKEFLAGS
make -C $WORKSPACE/BaseTools

%install
mkdir -p %{buildroot}%{_bindir}
install	\
	BaseTools/Source/C/bin/BootSectImage \
	BaseTools/Source/C/bin/EfiLdrImage \
	BaseTools/Source/C/bin/EfiRom \
	BaseTools/Source/C/bin/GenCrc32 \
	BaseTools/Source/C/bin/GenFfs \
	BaseTools/Source/C/bin/GenFv \
	BaseTools/Source/C/bin/GenFw \
	BaseTools/Source/C/bin/GenPage \
	BaseTools/Source/C/bin/GenSec \
	BaseTools/Source/C/bin/GenVtf \
	BaseTools/Source/C/bin/GnuGenBootSector \
	BaseTools/Source/C/bin/LzmaCompress \
	BaseTools/Source/C/bin/Split \
	BaseTools/Source/C/bin/VfrCompile \
	BaseTools/Source/C/bin/VolInfo \
	%{buildroot}%{_bindir}

ln -f %{buildroot}%{_bindir}/GnuGenBootSector \
	%{buildroot}%{_bindir}/GenBootSector

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -R BaseTools/Source/Python %{buildroot}%{_datadir}/%{name}/Python

find %{buildroot}%{_datadir}/%{name}/Python -name "*.pyd" | xargs rm

for i in BPDG GenDepex GenFds GenPatchPcdTable PatchPcdValue TargetTool Trim UPT; do
  echo '#!/bin/sh
PYTHONPATH=%{_datadir}/%{name}/Python
export PYTHONPATH
exec python '%{_datadir}/%{name}/Python/$i/$i.py' "$@"' > %{buildroot}%{_bindir}/$i
  chmod +x %{buildroot}%{_bindir}/$i
done

%files tools
%{_bindir}/BootSectImage
%{_bindir}/EfiLdrImage
%{_bindir}/EfiRom
%{_bindir}/GenBootSector
%{_bindir}/GenCrc32
%{_bindir}/GenFfs
%{_bindir}/GenFv
%{_bindir}/GenFw
%{_bindir}/GenPage
%{_bindir}/GenSec
%{_bindir}/GenVtf
%{_bindir}/GnuGenBootSector
%{_bindir}/LzmaCompress
%{_bindir}/Split
%{_bindir}/VfrCompile
%{_bindir}/VolInfo

%files tools-python
%{_bindir}/BPDG
%{_bindir}/GenDepex
%{_bindir}/GenFds
%{_bindir}/GenPatchPcdTable
%{_bindir}/PatchPcdValue
%{_bindir}/TargetTool
%{_bindir}/Trim
%{_bindir}/UPT
%{_datadir}/%{name}/Python/

%files tools-doc
%doc BaseTools/UserManuals/BootSectImage_Utility_Man_Page.rtf
%doc BaseTools/UserManuals/EfiLdrImage_Utility_Man_Page.rtf
%doc BaseTools/UserManuals/EfiRom_Utility_Man_Page.rtf
%doc BaseTools/UserManuals/GenBootSector_Utility_Man_Page.rtf
%doc BaseTools/UserManuals/GenCrc32_Utility_Man_Page.rtf
%doc BaseTools/UserManuals/GenDepex_Utility_Man_Page.rtf
%doc BaseTools/UserManuals/GenFds_Utility_Man_Page.rtf
%doc BaseTools/UserManuals/GenFfs_Utility_Man_Page.rtf
%doc BaseTools/UserManuals/GenFv_Utility_Man_Page.rtf
%doc BaseTools/UserManuals/GenFw_Utility_Man_Page.rtf
%doc BaseTools/UserManuals/GenPage_Utility_Man_Page.rtf
%doc BaseTools/UserManuals/GenPatchPcdTable_Utility_Man_Page.rtf
%doc BaseTools/UserManuals/GenSec_Utility_Man_Page.rtf
%doc BaseTools/UserManuals/GenVtf_Utility_Man_Page.rtf
%doc BaseTools/UserManuals/LzmaCompress_Utility_Man_Page.rtf
%doc BaseTools/UserManuals/PatchPcdValue_Utility_Man_Page.rtf
%doc BaseTools/UserManuals/SplitFile_Utility_Man_Page.rtf
%doc BaseTools/UserManuals/TargetTool_Utility_Man_Page.rtf
%doc BaseTools/UserManuals/Trim_Utility_Man_Page.rtf
%doc BaseTools/UserManuals/VfrCompiler_Utility_Man_Page.rtf
%doc BaseTools/UserManuals/VolInfo_Utility_Man_Page.rtf

%changelog
* Thu Nov 14 2013 Paolo Bonzini <pbonzini@redhat.com> - 20131114svn14844-1
- Upgrade to r14844.
- Remove upstreamed parts of patch 1.

* Fri Nov 8 2013 Paolo Bonzini <pbonzini@redhat.com> - 20130515svn14365-7
- Make BaseTools compile on ARM.

* Fri Aug 30 2013 Paolo Bonzini <pbonzini@redhat.com> - 20130515svn14365-6
- Revert previous change; firmware packages should be noarch, and building
  BaseTools twice is simply wrong.

* Mon Aug 19 2013 Kay Sievers <kay@redhat.com> - 20130515svn14365-5
- Add sub-package with EFI shell

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130515svn14365-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 23 2013 Dan Horák <dan[at]danny.cz> 20130515svn14365-3
- set ExclusiveArch

* Thu May 16 2013 Paolo Bonzini <pbonzini@redhat.com> 20130515svn14365-2
- Fix edk2-tools-python Requires

* Wed May 15 2013 Paolo Bonzini <pbonzini@redhat.com> 20130515svn14365-1
- Split edk2-tools-doc and edk2-tools-python
- Fix Python BuildRequires
- Remove FatBinPkg at package creation time.
- Use fully versioned dependency.
- Add comment on how to generate the sources.

* Thu May 2 2013 Paolo Bonzini <pbonzini@redhat.com> 20130502.g732d199-1
- Create.

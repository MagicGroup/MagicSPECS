%define _hardened_build 1
Name:           bochs
Version:        2.6.8
Release:        8%{?dist}
Summary:        Portable x86 PC emulator
Summary(zh_CN.UTF-8): 可移植的 X86 PC 仿真器
Group:          Applications/Emulators
Group(zh_CN.UTF-8): 应用程序/模拟器
License:        LGPLv2+
URL:            http://bochs.sourceforge.net/
# Using cvs checkout done 4/29/2010, see upstream bug 2994370
#Source0:        bochs-2.4.5.cvs.tar.gz
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

Patch0: %{name}-0001_bx-qemu.patch
#Patch1: %{name}-0006_qemu-bios-use-preprocessor-for-pci-link-routing.patch
#Patch2: %{name}-0007_bios-add-26-pci-slots,-bringing-the-total-to-32.patch
Patch3: %{name}-0008_qemu-bios-provide-gpe-_l0x-methods.patch
Patch4: %{name}-0009_qemu-bios-pci-hotplug-support.patch
#Patch5: %{name}-0011_read-additional-acpi-tables-from-a-vm.patch
#Patch6: %{name}-0012_remove_eh_frame_from_bios.patch
Patch7: %{name}-nonet-build.patch
# Update configure for aarch64 (bz #925112)
Patch8: bochs-aarch64.patch
Patch9: bochs-2.6.8-fix-formatsec.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libXt-devel libXpm-devel SDL-devel readline-devel byacc
BuildRequires:  docbook-utils
BuildRequires:  gtk2-devel
%ifarch %{ix86} x86_64
BuildRequires:  svgalib-devel
BuildRequires:  dev86 iasl
%endif
Requires:       %{name}-bios = %{version}-%{release}
Requires:       seavgabios-bin

%description
Bochs is a portable x86 PC emulation software package that emulates
enough of the x86 CPU, related AT hardware, and BIOS to run DOS,
Windows '95, Minix 2.0, and other OS's, all on your workstation.

%description -l zh_CN.UTF-8
Bochs 是一个可移植的 X86 PC 仿真器，用来模拟 x86 CPU，相关的 AT 硬件
和 BIOS ，可以运行 DOS, Windows '95, Minix 2.0 及其它 OS。

%package        debugger
Summary:        Bochs with builtin debugger
Summary(zh_CN.UTF-8): 内置调试工具的 Bochs
Group:          Applications/Emulators
Group(zh_CN.UTF-8): 应用程序/模拟器
Requires:       %{name} = %{version}-%{release}

%description    debugger
Special version of bochs compiled with the builtin debugger.

%description debugger -l zh_CN.UTF-8
内置调试工具的 Bochs。

%package        gdb
Summary:        Bochs with support for debugging with gdb
Summary(zh_CN.UTF-8): 可以使用 gdb 调试的 Bochs
Group:          Applications/Emulators
Group(zh_CN.UTF-8): 应用程序/模拟器
Requires:       %{name} = %{version}-%{release}

%description    gdb
Special version of bochs compiled with a gdb stub so that the software running
inside the emulator can be debugged with gdb.

%description gdb -l zh_CN.UTF-8
可以让运行在仿真器上的程序使用 gbd 调试的 bochs。

%ifarch %{ix86} x86_64
# building firmwares are quite tricky, because they often have to be built on
# their native architecture (or in a cross-capable compiler, that we lack in
# koji), and deployed everywhere. Recent koji builders support a feature
# that allow us to build packages in a single architecture, and create noarch
# subpackages that will be deployed everywhere. Because the package can only
# be built in certain architectures, the main package has to use
# BuildArch: <nativearch>, or something like that.
# Note that using ExclusiveArch is _wrong_, because it will prevent the noarch
# packages from getting into the excluded repositories.
%package	bios
Summary:        Bochs bios
Group:          Applications/Emulators
Group(zh_CN.UTF-8): 应用程序/模拟器
BuildArch:      noarch
Provides:       bochs-bios-data = 2.3.8.1
Obsoletes:      bochs-bios-data < 2.3.8.1


%description bios
Bochs BIOS is a free implementation of a x86 BIOS provided by the Bochs project.
It can also be used in other emulators, such as QEMU

%description bios -l zh_CN.UTF-8
这是 Bochs 项目组提供的一个自由实现的 x86 BIOS，也可以被其它仿真器，比如 QEMU 使用。
%endif

%package        devel
Summary:        Bochs header and source files
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Applications/Emulators
Group(zh_CN.UTF-8): 应用程序/模拟器
Requires:       %{name} = %{version}-%{release}

%description    devel
Header and source files from bochs source.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1
#%patch1 -p1
#%patch2 -p1
%patch3 -p1
%patch4 -p1
#%patch5 -p1
#%patch6 -p1
%patch7 -p0 -z .nonet
# Update configure for aarch64 (bz #925112)
%patch8 -p1
%patch9 -p1

# Fix up some man page paths.
sed -i -e 's|/usr/local/share/|%{_datadir}/|' doc/man/*.*

# remove executable bits from sources to make rpmlint happy with the debuginfo
chmod -x `find -name '*.cc' -o -name '*.h' -o -name '*.inc'`
# Fix CHANGES encoding
iconv -f ISO_8859-2 -t UTF8 CHANGES > CHANGES.tmp
mv CHANGES.tmp CHANGES


%build
%ifarch %{ix86} x86_64
ARCH_CONFIGURE_FLAGS=--with-svga
%endif
# Note: the CPU level, MMX et al affect what the emulator will emulate, they
# are not properties of the build target architecture.
# Note2: passing --enable-pcidev will change bochs license from LGPLv2+ to
# LGPLv2 (and requires a kernel driver to be usefull)
CONFIGURE_FLAGS=" \
  --enable-plugins \
  --enable-ne2000 \
  --enable-pci \
  --enable-all-optimizations \
  --enable-clgd54xx \
  --enable-sb16=linux \
  --enable-3dnow
  --with-x11 \
  --with-nogui \
  --with-term \
  --with-rfb \
  --with-sdl \
  --without-wx \
  --enable-cpu-level=6 \
  --enable-disasm \
  --enable-usb \
  --enable-usb-ohci \
  $ARCH_CONFIGURE_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS -DPARANOID"

%configure $CONFIGURE_FLAGS --enable-x86-debugger --enable-debugger
make %{?_smp_mflags}
mv bochs bochs-debugger
make dist-clean

%configure $CONFIGURE_FLAGS --enable-x86-debugger --enable-gdb-stub
make %{?_smp_mflags}
mv bochs bochs-gdb
make dist-clean

%configure $CONFIGURE_FLAGS
make %{?_smp_mflags}

%ifarch %{ix86} x86_64
cd bios
make bios
cp BIOS-bochs-latest BIOS-bochs-kvm
%endif

%install
rm -rf $RPM_BUILD_ROOT _installed-docs
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_prefix}/share/bochs/VGABIOS*
ln -s %{_prefix}/share/seavgabios/vgabios-cirrus.bin $RPM_BUILD_ROOT%{_prefix}/share/bochs/vgabios-cirrus
ln -s %{_prefix}/share/seavgabios/vgabios-isavga.bin $RPM_BUILD_ROOT%{_prefix}/share/bochs/vgabios-isavga
ln -s %{_prefix}/share/seavgabios/vgabios-qxl.bin $RPM_BUILD_ROOT%{_prefix}/share/bochs/vgabios-qxl
ln -s %{_prefix}/share/seavgabios/vgabios-stdvga.bin $RPM_BUILD_ROOT%{_prefix}/share/bochs/vgabios-stdvga
ln -s %{_prefix}/share/seavgabios/vgabios-vmware.bin $RPM_BUILD_ROOT%{_prefix}/share/bochs/vgabios-vmware
%ifnarch %{ix86} x86_64
rm -rf $RPM_BUILD_ROOT%{_prefix}/share/bochs/*{BIOS,bios}*
%endif
install -m 755 bochs-debugger bochs-gdb $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{_docdir}/bochs _installed-docs
rm $RPM_BUILD_ROOT%{_mandir}/man1/bochs-dlx.1*

mkdir -p $RPM_BUILD_ROOT%{_prefix}/include/bochs/disasm
cp -pr disasm/*.h $RPM_BUILD_ROOT%{_prefix}/include/bochs/disasm/
cp -pr disasm/*.cc $RPM_BUILD_ROOT%{_prefix}/include/bochs/disasm/
cp -pr disasm/*.inc $RPM_BUILD_ROOT%{_prefix}/include/bochs/disasm/
cp -pr config.h $RPM_BUILD_ROOT%{_prefix}/include/bochs/

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc _installed-docs/* README-*
%{_bindir}/bochs
#{_bindir}/bxcommit
%{_bindir}/bximage
# Note: must include *.la in %{_libdir}/bochs/plugins/
%{_libdir}/bochs/
%{_mandir}/man1/bochs.1*
#{_mandir}/man1/bxcommit.1*
%{_mandir}/man1/bximage.1*
%{_mandir}/man5/bochsrc.5*
%dir %{_datadir}/bochs/
%{_datadir}/bochs/keymaps/

%ifarch %{ix86} x86_64
%files bios
%defattr(-,root,root,-)
%{_datadir}/bochs/BIOS*
%{_datadir}/bochs/vgabios*
%{_datadir}/bochs/SeaBIOS-README
%{_datadir}/bochs/bios.bin-*
%endif


%files debugger
%defattr(-,root,root,-)
%{_bindir}/bochs-debugger

%files gdb
%defattr(-,root,root,-)
%{_bindir}/bochs-gdb

%files devel
%defattr(-,root,root,-)
%{_prefix}/include/bochs/

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 2.6.8-8
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 2.6.8-7
- 为 Magic 3.0 重建

* Fri Sep 18 2015 Liu Di <liudidi@gmail.com> - 2.6.8-6
- 为 Magic 3.0 重建

* Wed Aug 14 2013 Jon Ciesla <limburgher@gmail.com> - 2.6.2-5
- Add back one of the man page munging lines.

* Tue Aug 13 2013 Jon Ciesla <limburgher@gmail.com> - 2.6.2-4
- Drop noop man page munging.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 28 2013 Cole Robinson <crobinso@redhat.com> - 2.6.2-2
- Update configure for aarch64 (bz #925112)

* Tue May 28 2013 Jon Ciesla <limburgher@gmail.com> - 2.6.2-1
- 2.6.2.

* Mon May 27 2013 Dan Horák <dan[at]danny.cz> - 2.6.1-4
- fix non-x86 build

* Sat May 25 2013 Jon Ciesla <limburgher@gmail.com> - 2.6.1-3
- Fix bios symlinks.

* Sat May 25 2013 Jon Ciesla <limburgher@gmail.com> - 2.6.1-2
- Require seavgabios-bin, vgabios has been retired.

* Wed Apr 10 2013 Jon Ciesla <limburgher@gmail.com> - 2.6.1-1
- 2.6.1.
- pci patches upstreamed.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 04 2012 Jon Ciesla <limburgher@gmail.com> - 2.6-1
- Update to 2.6.
- eh_frame patch upstreamed.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 13 2012 Jon Ciesla <limburgher@gmail.com> - 2.5.1-4
- Add hardened build.

* Tue Mar 13 2012 Jon Ciesla <limburgher@gmail.com> - 2.5.1-3
- Add devel package.

* Tue Feb 21 2012 Jon Ciesla <limburgher@gmail.com> - 2.5.1-2
- Compile with disasm, BZ 798437.

* Fri Jan 20 2012 Jon Ciesla <limburgher@gmail.com> - 2.5.1-1
- Update to 2.5.1.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 30 2011 Jon Ciesla <limburgher@gmail.com> - 2.5-1
- Update to 2.5.
- Disabled vbe, vesa bios extensions.

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.4.6-2
- Rebuild for new libpng

* Thu Feb 24 2011 Jon Ciesla <limb@jcomserv.net> 2.4.6-1
- Update to 2.4.6.

* Mon Feb 14 2011 Chris Lalancette <clalance@redhat.com> - 2.4.5-3
- Add patch so rombios builds with gcc 4.6.0.
- Cleanup spec file to get rid of old cruft.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Apr 29 2010 Jon Ciesla <limb@jcomserv.net> 2.4.5-1
- Update to 2.4.5.
- Updated read additional tables patch.
- Using cvs checkout done 4/29/2010, see upstream bug 2994370.

* Tue Dec 08 2009 Jon Ciesla <limb@jcomserv.net> 2.4.2-1
- Update to 2.4.2.
- Removed patches 1-4, 9, upstreamed.
- Updated to included bios, as bios is no longer at old location.

* Fri Dec 04 2009 Jon Ciesla <limb@jcomserv.net> 2.3.8-0.9.git04387139e3b
- Include symlinks to VGABIOS in vgabios rpm, BZ 544310.
- Enable cpu level 6.

* Fri Jul 31 2009 Glauber Costa <glommer@redhat.com> - 2:0.10.50-14.kvm88
- replace kvm-bios with a more modern version, and refresh instructions on how to get it.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.8-0.7.git04387139e3b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 11 2009 Glauber Costa <glommer@redhat.com> 2.3.8-0.6.git04387139e3b
- Fix Obsoletes/Provides pair.

* Wed Mar 11 2009 Glauber Costa <glommer@redhat.com> 2.3.8-0.5.git04387139e3b
- kvm needs a slightly different bios due to irq routing, so build it too.
  from kvm source. This is not ideal, but avoids the creation of yet another
  noarch subpackage.

* Fri Mar 06 2009 Glauber Costa <glommer@redhat.com> 2.3.8-0.4.git04387139e3b
- Provide and Obsolete bochs-bios-data to make sure no one is harmed during
  updates.

* Thu Mar 05 2009 Glauber Costa <glommer@redhat.com> 2.3.8-0.3.git04387139e3b
- added patches ;-)

* Thu Mar 05 2009 Glauber Costa <glommer@redhat.com> 2.3.8-0.2.git04387139e3b
- this time with sources added.

* Thu Mar 05 2009 Glauber Costa <glommer@redhat.com> 2.3.8-0.1.git04387139e3b
- updated to git 04387139e3b, and applied qemu's patch ontop.

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 18 2008 Hans de Goede <hdegoede@redhat.com> 2.3.7-2
- Remove dlxlinux sub package, we cannot build this from source (rh 476878)

* Mon Jun  9 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.3.7-1
- New upstream release 2.3.7

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.3.6-3
- Autorebuild for GCC 4.3

* Fri Jan 11 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.3.6-2
- Fix compilation with gcc 4.3

* Mon Dec 24 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.3.6-1
- New upstream release 2.3.6

* Sun Sep 16 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.3.5-1
- New upstream release 2.3.5

* Wed Aug 22 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.3-7
- Fix CVE-2007-2894 (really fix bz 241799)

* Sun Aug  5 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.3-6
- Update License tag for new Licensing Guidelines compliance

* Wed Jul 18 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.3-5
- Fix CVE-2007-2893 (bz 241799)

* Mon Dec 18 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.3-4
- rebuilt without wxGTK as wxGTK is even more broken with wxGTK 2.8 then it
  was with 2.6

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 2.3-3
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.3-2
- Add -debugger and -gdb sub packages which contain special versions of
  bochs compiled with the buildin debugger resp. the gdb-stub (bz 206508)

* Sun Aug 27 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.3-1
- New upstream version 2.3 (final)

* Thu Aug 10 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.3-0.1.pre3
- New upstream version 2.3.pre3

* Mon Jul 17 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.3-0.1.pre2
- New upstream version 2.3.pre2
- Drop upstreamed wx26 patch

* Wed Feb 15 2006 Hans de Goede <j.w.r.degoede@hhs.nl> - 2.2.6-1
- New upstream version 2.2.6
- Rebuild for new gcc4.1 and glibc
- Remove --enable-pae as that requires a CPU level of 6 with the new version
- Remove a few configure switches which are identical to the
  upstream defaults and thus don't do anything
- Add --enable-clgd54xx
- Add --with-svga which adds support for svgalib as display (x86(_64) only)
- Fix compile with wxGTK-2.6 and unconditionalize wxGTK build

* Fri Dec 16 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.2.1-2
- Adapt to modular X.
- Fix build with g++ 4.1.0.
- Conditionalize wxGTK build and default it to off (build failures w/2.6.x).
- Use sed instead of dos2unix and perl during build.

* Sat Jul  9 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.2.1-1
- 2.2.1, precision patch applied upstream.

* Sun May 29 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.2-2
- Try to fix x86_64 build.

* Sat May 28 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.2-1
- 2.2, buildpaths and fpu-regparms patches applied upstream, pthread and
  ncurses linking hacks no longer needed.
- Use upstream default display library, wx is clunky with wxGTK2 2.4.x.
- Enable 3DNow! emulation and the SDL display library.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 2.1.1-3
- rebuild on all arches

* Fri Apr  8 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.1.1-2
- rebuilt

* Sun Dec  5 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.1.1-1
- Update to 2.1.1.
- Enable PAE and 4M pages support.
- Loosen version in dlxlinux to main dependency.
- BuildRequire ncurses-devel instead of ncurses-c++-devel for FC3.
- Apply upstream fpu-regparm patch to fix the build on FC3.

* Fri Jan 16 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.1-0.fdr.2
- Fix RFB linking, force pthreads.
- dos2unix some -dlxlinux files.

* Mon Jan 12 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.1-0.fdr.1
- Update to 2.1.
- Make sure everything is built with GTK2.
- Add "--with debugger" rpmbuild option.
- Put SDL build behind the "--with sdl" rpmbuild option due to startup crashes.

* Sun Nov 30 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.1-0.fdr.0.3.pre2
- Update to 2.1pre2.

* Tue Oct 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.1-0.fdr.0.2.pre1
- Remove .cvsignore from docs.

* Sat Oct 11 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.1-0.fdr.0.1.pre1
- Update to 2.1pre1.
- Enable 3DNow! on athlon.
- Other cosmetic tweaks.

* Sat Jul 19 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.0.2-0.fdr.3
- List wanted GUIs explicitly, exclude svgalib (bug 306).

* Wed May 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.0.2-0.fdr.2
- Rebuild with wxGTK2.

* Tue May 20 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.0.2-0.fdr.1
- First Fedora release, based on upstream SRPM.

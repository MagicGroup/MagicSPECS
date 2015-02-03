Summary: Fast compression and decompression utilities.
Summary(zh_CN.UTF-8): 快速压缩和解压缩的工具。
Name: ncompress
Version: 4.2.4.4
Release: 1%{?dist}
License: distributable
Group: Applications/File
Group(zh_CN.UTF-8): 应用程序/文件
URL:    http://ncompress.sourceforge.net/
Source: http://prdownloads.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz

# allow to build ncompress
# ~> downstream
Patch0: ncompress-4.2.4.4-make.patch

# from dist-git commit 0539779d937
# (praiskup: removed redundant part as -DNOFUNCDEF is defined)
# ~> downstream
Patch1: ncompress-4.2.4.4-lfs.patch

# exit when too long filename is given (do not segfault)
# ~> #unknown
# ~> downstream
Patch2: ncompress-4.2.4.4-filenamelen.patch

# permit files > 2GB to be compressed
# ~> #126775
Patch3: ncompress-4.2.4.4-2GB.patch

# do not fail to compress on ppc/s390x
# ~> #207001
Patch4: ncompress-4.2.4.4-endians.patch

# use memmove instead of memcpy
# ~> 760657
# ~> downstream
Patch5: ncompress-4.2.4.4-memmove.patch

# silence gcc warnings
# ~> downstream
Patch6: ncompress-4.2.4.4-silence-gcc.patch

BuildRequires: gcc glibc-devel fileutils
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
The ncompress package contains the compress and uncompress file
compression and decompression utilities, which are compatible with the
original UNIX compress utility (.Z file extensions).  These utilities
can't handle gzipped (.gz file extensions) files, but gzip can handle
compressed files.

Install ncompress if you need compression/decompression utilities
which are compatible with the original UNIX compress utility.

%description -l zh_CN.UTF-8
ncompress 软件包包括用来压缩和解压文件的压缩和解压工具。它们与原本的 UNIX 
压缩工具 (.Z 文件扩展名) 兼容。这些工具不能处理 gzip 处理的文件 (.gz 文件
扩展名)，但是 gzip 能处理压缩过的文件。 如果您需要与原本的 UNIX 压缩工具
兼容的压缩/解压工具，请安装 ncompress 软件包。

%prep
%setup -q

# configure build system
# ~> downstream
%patch0 -p1 -b .configure-buildsystem

%ifarch sparc m68k armv4l ppc s390 s390x ppc64 sparc64
ARCH_FLAGS="$ARCH_FLAGS -DBYTEORDER=1234"
%endif

%ifarch alpha ia64
ARCH_FLAGS="$ARCH_FLAGS -DNOALLIGN=0"
%endif

sed "s/\$(ARCH_FLAGS)/$ARCH_FLAGS/" Makefile.def > Makefile

%patch1 -p1 -b .lfs
%patch2 -p1 -b .filenamelen
%patch3 -p1 -b .2GB
%patch4 -p1 -b .endians
%patch5 -p1 -b .memmove
%patch6 -p1 -b .silence-gcc
 

%build
make CFLAGS="%{optflags} %{?nc_endian} %{?nc_align}"

%install
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
install -p -m755 compress $RPM_BUILD_ROOT/%{_bindir}
ln -sf compress $RPM_BUILD_ROOT/%{_bindir}/uncompress
install -p -m644 compress.1 $RPM_BUILD_ROOT%{_mandir}/man1
ln -sf compress.1 $RPM_BUILD_ROOT%{_mandir}/man1/uncompress.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/compress
%{_bindir}/uncompress
%{_mandir}/man1/*
%doc LZW.INFO README

%changelog
* Mon Jan 26 2015 Liu Di <liudidi@gmail.com> - 4.2.4.4-1
- 更新到 4.2.4.4

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 4.2.4-47
- 为 Magic 3.0 重建

* Thu Jan 19 2012 Liu Di <liudidi@gmail.com> - 4.2.4-46
- 为 Magic 3.0 重建

* Tue Oct 10 2006 Liu Di <liudidi@gmail.com> - 4.2.4-41mgc
- rebuild for Magic

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 4.2.4-47
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Peter Vrabec <pvrabec@redhat.com> 4.2.4-46
- fix endian problem (#207001)

* Thu Aug 10 2006 Peter Vrabec <pvrabec@redhat.com> 4.2.4-45
- fix bss buffer underflow CVE-2006-1168 (#201919)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.2.4-44.1
- rebuild

* Fri Apr 21 2006 Peter Vrabec <pvrabec@redhat.com> 4.2.4-44
- fix problems with compressing zero-sized files (#189215, #189216)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.2.4-43.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.2.4-43.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Sep 22 2005 Peter Vrabec <pvrabec@redhat.com> 4.2.4-43
- compress zero-sized files when -f is used(#167615)

* Fri Mar 18 2005 Peter Vrabec <pvrabec@redhat.com>
- rebuilt

* Thu Feb 08 2005 Peter Vrabec <pvrabec@redhat.com>
- rebuilt

* Tue Oct 05 2004 Than Ngo <than@redhat.com> 4.2.4-40
- permit files > 2GB to be compressed (#126775).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 4.2.4-32
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Trond Eivind Glomsr鴇 <teg@redhat.com> 4.2.4-30
- Don't strip when installing

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Feb 27 2002 Trond Eivind Glomsr鴇 <teg@redhat.com> 4.2.4-28
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Nov 26 2001 Trond Eivind Glomsr鴇 <teg@redhat.com> 4.2.4-26
- Rebuild, to fix problem with broken man page (#56654)

* Wed Nov 21 2001 Trond Eivind Glomsr鴇 <teg@redhat.com> 4.2.4-25
- Exit, don't segfault, when given too long filenames

* Sat Jun 09 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- s390x change

* Tue May  8 2001 Trond Eivind Glomsr鴇 <teg@redhat.com>
- Make it support large files (structs, stats, opens and of course:
  _don't use signed longs for file size before and after compression_.)
  This should fix #39470

* Thu Apr 26 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add s390x, patch from Oliver Paukstadt <oliver.paukstadt@millenux.com>

* Mon Nov 13 2000 Oliver Paukstadt <oliver.paukstadt@millenux.com>
- add s390 to the bigendian arch list

* Thu Aug 17 2000 Trond Eivind Glomsr鴇 <teg@redhat.com>
- change category to Applications/File, to match
  gzip and bzip2 
- rename the spec file to ncompress.spec
- add ppc to the bigendian arch list

* Fri Jul 21 2000 Trond Eivind Glomsr鴇 <teg@redhat.com>
- rebuild

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 13 2000 Trond Eivind Glomsr鴇 <teg@redhat.com>
- update URL
- use %%{_mandir}

* Wed May  5 2000 Bill Nottingham <notting@redhat.com>
- fix %build for ia64

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 14)

* Tue Jan 12 1999 Cristian Gafton <gafton@redhat.com>
- build on armv4l too
- build for 6.0

* Thu Aug 13 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- fixed the spec file

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

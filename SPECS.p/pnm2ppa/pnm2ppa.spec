Name: pnm2ppa
Summary: Drivers for printing to HP PPA printers.
Summary(zh_CN.UTF-8): 打印到 HP PPA 打印机的驱动程序。
Epoch: 1
Obsoletes: ppa
Version: 1.04
Release: 18%{?dist}
URL: http://sourceforge.net/projects/pnm2ppa 
Source: http://download.sourceforge.net/pnm2ppa/pnm2ppa-%{version}.tar.gz
Source1: http://www.httptech.com/ppa/files/ppa-0.8.6.tar.gz
Patch2: pbm2ppa-20000205.diff
Patch3: pnm2ppa-redhat.patch
License: GPL
Group: Applications/Publishing
Group(zh_CN.UTF-8): 应用程序/出版
Buildroot: /var/tmp/pnm2ppa-buildroot
%define topdir pnm2ppa-%{version}

%description
Pnm2ppa is a color driver for HP PPA host-based printers such as the
HP710C, 712C, 720C, 722C, 820Cse, 820Cxi, 1000Cse, and 1000Cxi.
Pnm2ppa accepts Ghostscript output in PPM format and sends it to the
printer in PPA format.

Install pnm2ppa if you need to print to a PPA printer.

%description -l zh_CN.UTF-8
Pnm2ppa 是一个用于 HP PPA 基于主机的打印机的颜色驱动程序，这类打印机
包括：HP710C、712C、720C、722C、820Cse、 820Cxi、1000Cse、以及 1000Cxi。
Pnm2ppa 接受 PPM 格式的 Ghostscript 输出，并把它用 PPA 格式发送给打印机。

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q -n %{topdir}

#pbm2ppa source
%setup -T -D -a 1 -n %{topdir}
%patch2 -p0
%patch3 -p1 -b .rh

%build
make 
cd pbm2ppa-0.8.6
make


%install
install -d $RPM_BUILD_ROOT/usr/bin
install -d $RPM_BUILD_ROOT/etc
install -d $RPM_BUILD_ROOT%{_mandir}/man1
make INSTALLDIR=$RPM_BUILD_ROOT/usr/bin CONFDIR=$RPM_BUILD_ROOT/etc \
    MANDIR=$RPM_BUILD_ROOT%{_mandir}/man1 install 
install -m 0755 utils/Linux/detect_ppa $RPM_BUILD_ROOT/usr/bin/
install -m 0755 utils/Linux/test_ppa $RPM_BUILD_ROOT/usr/bin/
install -m 0755 pbm2ppa-0.8.6/pbm2ppa  $RPM_BUILD_ROOT/usr/bin/
install -m 0755 pbm2ppa-0.8.6/pbmtpg   $RPM_BUILD_ROOT/usr/bin/
install -m 0644 pbm2ppa-0.8.6/pbm2ppa.conf   $RPM_BUILD_ROOT/etc
install -m 0644 pbm2ppa-0.8.6/pbm2ppa.1   $RPM_BUILD_ROOT%{_mandir}/man1

chmod 644 docs/en/LICENSE
mkdir -p pbm2ppa
for file in CALIBRATION CREDITS INSTALL INSTALL-MORE LICENSE README ; do
  install -m 0644 pbm2ppa-0.8.6/$file pbm2ppa/$file
done

%clean
rm -rf $RPM_BUILD_ROOT 

%files 
%defattr(-,root,root)
%doc docs/en/CREDITS docs/en/INSTALL docs/en/LICENSE docs/en/README
%doc docs/en/RELEASE-NOTES docs/en/TODO
%doc docs/en/INSTALL.REDHAT.txt docs/en/COLOR.txt docs/en/CALIBRATION.txt
%doc docs/en/INSTALL.REDHAT.html docs/en/COLOR.html docs/en/CALIBRATION.html
%doc test.ps
%doc pbm2ppa
/usr/bin/pnm2ppa
/usr/bin/pbm2ppa
/usr/bin/pbmtpg
/usr/bin/calibrate_ppa
/usr/bin/test_ppa
/usr/bin/detect_ppa
%{_mandir}/man1/pnm2ppa.1*
%{_mandir}/man1/pbm2ppa.1*
%config /etc/pnm2ppa.conf
%config /etc/pbm2ppa.conf

%changelog
* Fri Jul 24 2015 Liu Di <liudidi@gmail.com> - 1:1.04-18
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1:1.04-17
- 为 Magic 3.0 重建

* Thu Jan 26 2012 Liu Di <liudidi@gmail.com> - 1:1.04-16
- 为 Magic 3.0 重建

* Tue Oct 10 2006 Liu Di <liudidi@gmail.coM> - 1:1.04-13mgc
- rebuild for Magic

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.04-13.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:1.04-13.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:1.04-13.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 16 2005 Tim Waugh <twaugh@redhat.com> 1:1.04-13
- Rebuild for new GCC.

* Wed Feb  9 2005 Tim Waugh <twaugh@redhat.com> 1:1.04-12
- s/Copyright:/License:/.
- s/Serial:/Epoch:/.
- Rebuilt.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 19 2004 Tim Waugh <twaugh@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Nov 20 2002 Tim Powers <timp@redhat.com>
- rebuild in current collinst

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Mon Dec 11 2000 Crutcher Dunnavant <crutcher@redhat.com>
- Upgrade to 1.04, editied the pbm2ppa patch to add <string.h>
- to pbmtpg.c, which uses strmp, edited the redhat patch to
- apply cleanly.

* Thu Aug 16 2000 Bill Nottingham <notting@redhat.com>
- tweak summary

* Thu Aug  3 2000 Bill Nottingham <notting@redhat.com>
- build upstream package

* Tue Jul 11 2000 Duncan Haldane <duncan_haldane@users.sourceforge.net>
- updated for 1.0 release.

* Mon Jul 10 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- remove execute bits from config file and man-page

* Sun Apr 09 2000 <duncan_haldane@users.sourceforge.net>
- added optional updated rhs-printfilter  files

* Thu Feb 10 2000 Bill Nottingham <notting@redhat.com>
- adopt upstream package

* Sun Feb 6 2000 <duncan_haldane@users.sourceforge.net>
- new pnm2ppa release,  and add pbm2ppa driver.

* Thu Jan 7 2000 <duncan_haldane@users.sourceforge.net>
- created rpm




Name:           gocr
Version:	0.48
Release:        6%{?dist}
Summary:        GNU Optical Character Recognition program
Summary(zh_CN.UTF-8): GNU 文字识别程序

Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
License:        GPLv2+
URL:            http://jocr.sourceforge.net/
Source0:        http://www-e.uni-magdeburg.de/jschulen/ocr/gocr-%{version}.tar.gz
Patch0:         gocr-0.46-perms.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  netpbm-devel
# Needed for conversion programs
Requires:       gzip, bzip2, /usr/bin/djpeg, netpbm-progs, transfig
Obsoletes:      %{name}-devel <= 0.45-4

%description
GOCR is an OCR (Optical Character Recognition) program, developed under the
GNU Public License. It converts scanned images of text back to text files.
Joerg Schulenburg started the program, and now leads a team of developers.

GOCR can be used with different front-ends, which makes it very easy to port
to different OSes and architectures. It can open many different image
formats, and its quality have been improving in a daily basis.

%description -l zh_CN.UTF-8 
GOCR 一个 OCR 程序，可以把扫描的图像转成文字文件。

%prep
%setup -q
%patch0 -p1 -b .perms


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
# Don't ship static library
rm -rf $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_includedir}
# Don't ship buggy Tcl/Tk frontend
rm $RPM_BUILD_ROOT/%{_bindir}/gocr.tcl
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS BUGS CREDITS doc/gocr.html gpl.html HISTORY README
%doc REMARK.txt REVIEW TODO
%lang(de) %doc READMEde.txt
%{_bindir}/gocr
%{_mandir}/man1/gocr.1*

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.48-6
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 0.48-5
- 更新到 0.48

* Mon Apr 14 2014 Liu Di <liudidi@gmail.com> - 0.49-4
- 更新到

* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 0.49-4
- 更新到

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.49-4
- 为 Magic 3.0 重建

* Tue Nov 27 2012 Liu Di <liudidi@gmail.com> - 0.49-3
- 为 Magic 3.0 重建

* Wed Nov 16 2011 Tomas Smetana <tsmetana@redhat.com> - 0.49-2
- rebuild because of libnetpbm

* Tue Nov 15 2011 Tomas Smetana <tsmetana@redhat.com> - 0.49-1
- new upstream release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 02 2010 Adam Tkac <atkac redhat com> - 0.48-2
- require /usr/bin/djpeg instead of libjpeg to be compatible with both
  libjpeg and libjpeg-turbo

* Tue Jan 19 2010 Tomas Smetana <tsmetana@redhat.com> - 0.48-1
- new upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 23 2009 Tomas Smetana <tsmetana@redhat.com> - 0.46-1
- new upstream release

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.45-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 04 2008 Tomas Smetana <tsmetana@redhat.com> - 0.45-4
- and obsolete the devel package

* Thu Sep 04 2008 Tomas Smetana <tsmetana@redhat.com> - 0.45-3
- remove the unusable devel package again (related #344721)

* Wed Feb 13 2008 Tomas Smetana <tsmetana@redhat.com> - 0.45-2
- rebuild (gcc-4.3)

* Mon Jan 28 2008 Patrice Dumas <pertusus@free.fr> - 0.45-1
- update to 0.45
- rename gocr-0.44-man.patch to gocr-0.45-perms.patch and
  fix library and header permissions

* Mon Jan 14 2008 Tomas Smetana <tsmetana@redhat.com> - 0.44-4
- build devel package (with static library)

* Tue Aug 21 2007 - Orion Poplawski <orion@cora.nwra.com> - 0.44-3
- Update license tag to GPLv2+
- Rebuild for BuildID

* Wed Mar 21 2007 - Orion Poplawski <orion@cora.nwra.com> - 0.44-2
- Bump release to fix import tag issue

* Fri Mar 02 2007 - Orion Poplawski <orion@cora.nwra.com> - 0.44-1
- Update to 0.44

* Mon Dec 18 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.43-1
- Update to 0.43
- Don't ship frontends

* Wed Nov 22 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.41-3
- Add more requires

* Tue Nov 21 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.41-2
- Split TCL/Tk GUI into -tk sub-package
- Ship GTK+ GUI

* Mon Nov 20 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.41-1
- Initial Fedora Extras Version

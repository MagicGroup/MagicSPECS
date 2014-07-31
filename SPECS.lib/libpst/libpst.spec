Summary:            Utilities to convert Outlook .pst files to other formats
Summary(zh_CN.UTF-8): 转换 Outlook .pst 文件到其它格式的工具
Name:               libpst
Version: 0.6.63
Release: 1%{?dist}
License:            GPLv2+
Group:              Applications/Productivity
Group(zh_CN.UTF-8): 应用程序/生产力
Source:             http://www.five-ten-sg.com/%{name}/packages/%{name}-%{version}.tar.gz
BuildRoot:          %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
URL:                http://www.five-ten-sg.com/%{name}/
Requires:           ImageMagick
Requires:           %{name}-libs = %{version}-%{release}
BuildRequires:      ImageMagick freetype-devel gd-devel libjpeg-devel zlib-devel python-devel boost-devel

%{!?python_sitelib:  %global python_sitelib  %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}


%description
The Libpst utilities include readpst which can convert email messages
to both mbox and MH mailbox formats, pst2ldif which can convert the
contacts to .ldif format for import into ldap databases, and pst2dii
which can convert email messages to the DII load file format used by
Summation.

%description -l zh_CN.UTF-8
转换 Outlook .pst 文件到其它格式的工具，包括 mbox 和 MH 邮箱格式，
导入 ladp 数据库用的 .ldif 格式，及 Summation 使用的 DII 文件格式。


%package libs
Summary:            Shared library used by the pst utilities
Summary(zh_CN.UTF-8): %{name} 的共享库
Group:              Development/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description libs
The libpst-libs package contains the shared library used by the pst
utilities.

%description libs -l zh_CN.UTF-8
%{name} 的共享库。

%package python
Summary:            Python bindings for libpst
Summary(zh_CN.UTF-8): libpst 的 Python 绑定
Group:              Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:           python
Requires:           %{name}-libs = %{version}-%{release}

%description python
The libpst-python package allows you to use the libpst shared object
from python code.

%description python -l zh_CN.UTF-8
libpst 的 Python 绑定。

%package devel
Summary:            Library links and header files for libpst application development
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:              Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:           pkgconfig
Requires:           %{name}-libs = %{version}-%{release}

%description devel
The libpst-devel package contains the library links and header files
you'll need to develop applications using the libpst shared library.
You do not need to install it if you just want to use the libpst
utilities.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package devel-doc
Summary:            Documentation for libpst.so for libpst application development
Summary(zh_CN.UTF-8): %{name} 的开发文档
Group:              Documentation
Group(zh_CN.UTF-8): 文档
Requires:           %{name}-doc = %{version}-%{release}

%description devel-doc
The libpst-devel-doc package contains the doxygen generated
documentation for the libpst.so shared library.

%description devel-doc -l zh_CN.UTF-8
%{name} 的开发文档。

%package doc
Summary:            Documentation for the pst utilities in html format
Summary(zh_CN.UTF-8): %{name} 的文档
Group:              Documentation
Group(zh_CN.UTF-8): 文档

%description doc
The libpst-doc package contains the html documentation for the pst
utilities.  You do not need to install it if you just want to use the
libpst utilities.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q


%build
%configure --enable-libpst-shared
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/libpst.la
rm $RPM_BUILD_ROOT%{_libdir}/libpst.a
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post libs -p /sbin/ldconfig


%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*


%files libs
%defattr(-,root,root,-)
%{_libdir}/libpst.so.*
%doc COPYING


%files python
%defattr(-,root,root,-)
%{python_sitearch}/_*.so
%exclude %{python_sitearch}/*.a
%exclude %{python_sitearch}/*.la


%files devel
%defattr(-,root,root,-)
%{_libdir}/libpst.so
%{_includedir}/%{name}-4/
%{_libdir}/pkgconfig/libpst.pc


%files devel-doc
%defattr(-,root,root,-)
%{_datadir}/doc/%{name}-%{version}/devel/


%files doc
%defattr(-,root,root,-)
%dir %{_datadir}/doc/%{name}-%{version}/
%{_datadir}/doc/%{name}-%{version}/*.html
%{_datadir}/doc/%{name}-%{version}/AUTHORS
%{_datadir}/doc/%{name}-%{version}/COPYING
%{_datadir}/doc/%{name}-%{version}/ChangeLog
%{_datadir}/doc/%{name}-%{version}/NEWS
%{_datadir}/doc/%{name}-%{version}/README


%changelog
* Mon Jul 28 2014 Liu Di <liudidi@gmail.com> - 0.6.63-1
- 更新到 0.6.63

* Sat Apr 20 2013 Liu Di <liudidi@gmail.com> - 0.6.55-4
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.6.55-3
- 为 Magic 3.0 重建

* Tue Aug 09 2012 Carl Byington <carl@five-ten-sg.com> - 0.6.55-2
- rebuild for python

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.54-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 08 2012 Carl Byington <carl@five-ten-sg.com> - 0.6.55-1
- preserve bcc headers
- document -C switch to set default character set
- space after colon is not required in header fields

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.54-5
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.54-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 24 2011 Carl Byington <carl@five-ten-sg.com> - 0.6.54-3
- bump versions and prep for fedora build

* Wed Nov 30 2011 Petr Pisar <ppisar@redhat.com> - 0.6.53-3
- Rebuild against boost-1.48

* Wed Nov 14 2011 Carl Byington <carl@five-ten-sg.com> - 0.6.54-2
- failed to bump version number

* Fri Nov 04 2011 Carl Byington <carl@five-ten-sg.com> - 0.6.54-1
- embedded rfc822 messages might contain rtf encoded bodies

* Fri Sep 02 2011 Petr Pisar <ppisar@redhat.com> - 0.6.53-2
- Rebuild against boost-1.47

* Sun Jul 10 2011 Carl Byington <carl@five-ten-sg.com> - 0.6.53-1
- add Status: header in output
- allow fork for parallel processing of individual email folders
  in separate mode
- proper handling of --with-boost-python option

* Sun May 22 2011 Carl Byington <carl@five-ten-sg.com> - 0.6.52-1
- fix dangling freed pointer in embedded rfc822 message processing
- allow broken outlook internet header field - it sometimes contains
  fragments of the message body rather than headers

* Sun Apr 17 2011 Carl Byington <carl@five-ten-sg.com> - 0.6.51-1
- fix for buffer overrun; attachment size from the secondary
  list of mapi elements overwrote proper size from the primary
  list of mapi elements.
  fedora bugzilla 696263

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.49-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Thomas Spura <tomspur@fedoraproject.org> - 0.6.49-3
- rebuild for new boost

* Fri Dec 24 2010 Carl Byington <carl@five-ten-sg.com> - 0.6.50-1
- rfc2047 and rfc2231 encoding for non-ascii headers and
  attachment filenames.

* Wed Sep 29 2010 jkeating - 0.6.49-2
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Carl Byington <carl@five-ten-sg.com> - 0.6.49-1
- fix to ignore embedded objects that are not email messages
  fedora bugzilla 633498

* Thu Sep 02 2010 Carl Byington <carl@five-ten-sg.com> - 0.6.48-1
- fix for broken internet headers from Outlook
- fix ax_python.m4 to look for python2.7
- use mboxrd from quoting for output formats with multiple messages per file
- use no from quoting for output formats with single message per file

* Sat Jul 31 2010 Carl Byington <carl@five-ten-sg.com> - 0.6.47-6
- rebuild for python dependencies

* Mon Jul 26 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.47-4
- hack up configure so that it looks for python 2.7

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.47-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 07 2010 Carl Byington <carl@five-ten-sg.com> - 0.6.47-2
- Subpackage Licensing, add COPYING to -libs.
- patches from Kenneth Berland for solaris

* Fri May 07 2010 Carl Byington <carl@five-ten-sg.com> - 0.6.47-1
- patches from Kenneth Berland for solaris

* Thu Jan 21 2010 Carl Byington <carl@five-ten-sg.com> - 0.6.46-1
- prefer libpthread over librt for finding sem_init function.

* Thu Jan 21 2010 Carl Byington <carl@five-ten-sg.com> - 0.6.45-2
- rebuild for new boost package

* Wed Nov 18 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.45-1
- patch from Hugo DesRosiers to export categories and notes into vcards.
- extend that patch to export categories into vcalendar appointments also.

* Sun Sep 20 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.44-1
- patch from Lee Ayres to add file name extensions in separate mode.
- allow mixed items types in a folder in separate mode.

* Thu Sep 12 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.43-1
- decode more of the pst format, some minor bug fixes
- add support for code pages 1200 and 1201.
- add readpst -t option to select output item types, which can
  now be used to process folders containing mixed item types.
- fix segfault with embedded appointments
- add readpst -u option for Thunderbird mode .size and .type files
- better detection of embedded rfc822 message attachments

* Thu Sep 03 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.42-1
- patch from Fridrich Strba to build with DJGPP DOS cross-compiler.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 23 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.41-1
- fix ax_python detection - should not use locate command
- checking for fedora versions is not needed

* Tue Jun 23 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.40-1
- fedora 11 has python2.6
- remove pdf version of the man pages

* Sun Jun 21 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.39-1
- fedora > 10 moved to boost-python-devel

* Sun Jun 21 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.38-1
- add python interface to the shared library.
- bump soname to version 4 for many changes to the interface.
- better decoding of recurrence data in appointments.
- remove readpstlog since debug log files are now plain text.
- add readpst -j option for parallel jobs for each folder.
- make nested mime multipart/alternative to hold the text/html parts.

* Fri Apr 17 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.37-1
- add pst_attach_to_mem() back into the shared library interface.
- fix memory leak caught by valgrind.

* Tue Apr 14 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.36-1
- build separate -doc and -devel-doc subpackages.
- other spec file cleanup

* Wed Apr 08 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.35-1
- properly add trailing mime boundary in all modes.
- build separate libpst, libpst-libs, libpst-devel rpms.

* Thu Mar 19 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.34-1
- avoid putting mixed item types into the same output folder.

* Tue Mar 17 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.33-1
- compensate for iconv conversion to utf-7 that produces strings that
  are not null terminated.
- don't produce empty attachment files in separate mode.

* Sat Mar 14 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.32-1
- fix ppc64 compile error

* Sat Mar 14 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.31-1
- bump version for fedora cvs tagging mistake

* Sat Mar 14 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.30-1
- track character set individually for each mapi element.
- remove charset option from pst2ldif since we get that from each
  object now.
- avoid emitting bogus empty email messages into contacts and
  calendar files.

* Tue Feb 24 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.29-1
- fix for 64bit on Fedora 11

* Tue Feb 24 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.28-1
- improve decoding of multipart/report and message/rfc822 mime types.
- improve character set handling.
- fix embedded rfc822 messages with attachments.

* Sat Feb 07 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.27-1
- fix for const correctness on Fedora 11

* Sat Feb 07 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.26-1
- patch from Fridrich Strba for building on mingw and general
- cleanup of autoconf files.
- add processing for pst files of type 0x0f.
- strip and regenerate all MIME headers to avoid duplicates.
- do a better job of making unique MIME boundaries.
- only use base64 coding when strictly necessary.

* Fri Jan 16 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.25-1
- improve handling of content-type charset values in mime parts

* Thu Dec 11 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.24-1
- patch from Chris Eagle to build on cygwin

* Thu Dec 04 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.23-1
- bump version to avoid cvs tagging mistake in fedora

* Fri Nov 28 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.22-1
- patch from David Cuadrado to process emails with type PST_TYPE_OTHER
- base64_encode_multiple() may insert newline, needs larger malloc
- subject lines shorter than 2 bytes could segfault

* Tue Oct 21 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.21-1
- fix title bug with old schema in pst2ldif.
- also escape commas in distinguished names per rfc4514.

* Thu Oct 09 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.20-1
- add configure option --enable-dii=no to remove dependency on libgd.
- many fixes in pst2ldif by Robert Harris.
- add -D option to include deleted items, from Justin Greer
- fix from Justin Greer to add missing email headers
- fix from Justin Greer for my_stristr()
- fix for orphan children when building descriptor tree
- avoid writing uninitialized data to debug log file
- remove unreachable code
- create dummy top-of-folder descriptor if needed for corrupt pst files

* Sun Sep 14 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.19-1
- Fix base64 encoding that could create long lines.
- Initial work on a .so shared library from Bharath Acharya.

* Thu Aug 28 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.18-1
- Fixes for iconv on Mac from Justin Greer.

* Tue Aug 05 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.17-1
- More fixes for 32/64 bit portability on big endian ppc.

* Tue Aug 05 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.16-1
- Use inttypes.h for portable printing of 64 bit items.

* Wed Jul 30 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.15-1
- Patch from Robert Simpson for file handle leak in error case.
- Fix for missing length on lz decompression, bug found by Chris White.

* Sun Jun 15 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.14-1
- Fix my mistake in debian packaging.

* Fri Jun 13 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.13-1
- Patch from Robert Simpson for encryption type 2.

* Tue Jun 10 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.12-1
- Patch from Joachim Metz for debian packaging and
- fix for incorrect length on lz decompression

* Tue Jun 03 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.11-1
- Use ftello/fseeko to properly handle large files.
- Document and properly use datasize field in b5 blocks.
- Fix some MSVC compile issues and collect MSVC dependencies into one place.

* Thu May 29 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.10-1
- Patch from Robert Simpson for doubly-linked list code and arrays of unicode strings.

* Fri May 16 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.9
- Patch from Joachim Metz for 64 bit compile.
- Fix pst format documentation for 8 byte backpointers.

* Wed Mar 05 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.8
- Initial version of pst2dii to convert to Summation dii load file format
- changes for Fedora packaging guidelines (#434727)

* Tue Jul 10 2007 Carl Byington <carl@five-ten-sg.com> - 0.5.5
- merge changes from Joe Nahmias version

* Sun Feb 19 2006 Carl Byington <carl@five-ten-sg.com> - 0.5.3
- initial spec file using autoconf and http://www.fedora.us/docs/rpm-packaging-guidelines.html


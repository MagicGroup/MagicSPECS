Summary: Conversion between character sets and surfaces
Summary(zh_CN.UTF-8): 字符集和曲面之间的转换
Name: recode
Version: 3.6
Release: 35%{?dist}
License: GPLv2+
Group: Applications/File
Group(zh_CN.UTF-8): 应用程序/文件
Source: http://recode.progiciels-bpi.ca/archives/recode-%{version}.tar.gz
Patch0: recode.patch
Patch1: recode-3.6-getcwd.patch
Patch2: recode-bool-bitfield.patch
Patch3: recode-flex-m4.patch
Patch4: recode-automake.patch
Patch5: recode-format-security.patch
Url: http://recode.progiciels-bpi.ca/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post): /sbin/install-info
Requires(post): /sbin/ldconfig
Requires(preun): /sbin/install-info
Requires(postun): /sbin/ldconfig

BuildRequires: libtool


%description
The `recode' converts files between character sets and usages.
It recognises or produces nearly 150 different character sets
and is able to transliterate files between almost any pair. When exact
transliteration are not possible, it may get rid of the offending
characters or fall back on approximations.  Most RFC 1345 character sets
are supported.

%description -l zh_CN.UTF-8
字符集和曲面之间的转换。

%package devel
Summary: Header files for development using recode
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
The `recode' library converts files between character sets and usages.
The library recognises or produces nearly 150 different character sets
and is able to transliterate files between almost any pair. When exact
transliteration are not possible, it may get rid of the offending
characters or fall back on approximations. Most RFC 1345 character sets
are supported.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。


%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .getcwd
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1
rm m4/libtool.m4
rm acinclude.m4

%build
autoreconf -fiv
%configure --disable-static
make %{?_smp_mflags}

%check
make check

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall
magic_rpm_clean.sh
%find_lang %{name} || %define nolang 1

# remove unpackaged file from the buildroot
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# remove libtool archives
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la


%post
/sbin/ldconfig
/sbin/install-info %{_infodir}/recode.info.gz %{_infodir}/dir --entry="* recode: (recode).                        Conversion between character sets and surfaces." || :

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/recode.info.gz %{_infodir}/dir --entry="* recode: (recode).                        Conversion between character sets and surfaces." || :
fi

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%if 0%{nolang}
%files
%else
%files -f %{name}.lang
%endif
%defattr(-,root,root)
%doc AUTHORS COPYING* ChangeLog NEWS README THANKS TODO
%{_mandir}/*/*
%{_infodir}/recode.info*
%{_bindir}/*
%{_libdir}/*.so.0*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/*

%changelog
* Sat Sep 12 2015 Liu Di <liudidi@gmail.com> - 3.6-35
- 为 Magic 3.0 重建

* Mon Jul 23 2012 Zoltan Kota <zoltank[AT]gmail.com> 3.6-34
- Add patch for fixing build with new automake.
  (Fixes failed Fedora_18_Mass_Rebuild.)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 21 2012 Zoltan Kota <zoltank[AT]gmail.com> 3.6-32
- Corrected summary of the devel subpackage. Fixing bug #817947.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 7 2010 Zoltan Kota <z.kota[AT]gmx.net> 3.6-29
- Fix build on x86_64. Run autoreconf to update config files.
  autoconf >= 2.64 needs to patch the flex.m4 file.
  Fixing FTBFS bug #564601.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.6-26
- Autorebuild for GCC 4.3

* Wed Jan 16 2008 Zoltan Kota <z.kota[AT]gmx.net> 3.6-25
- add patch for gcc43

* Wed Aug 22 2007 Zoltan Kota <z.kota[AT]gmx.net> 3.6-24
- update license tag
- rebuild

* Tue Apr 03 2007 Zoltan Kota <z.kota[AT]gmx.net> 3.6-23
- rebuild

* Fri Sep 01 2006 Zoltan Kota <z.kota[AT]gmx.net> 3.6-22
- rebuild

* Mon Feb 13 2006 Zoltan Kota <z.kota[AT]gmx.net> 3.6-21
- rebuild

* Thu Dec 22 2005 Zoltan Kota <z.kota[AT]gmx.net> 3.6-20
- rebuild

* Fri Aug 26 2005 Zoltan Kota <z.kota[AT]gmx.net> 3.6-19
- fix requires
- disable static libs and remove libtool archives
- add %%doc

* Fri Aug 26 2005 Zoltan Kota <z.kota[AT]gmx.net> 3.6-18
- add dist tag
- specfile cleanup

* Thu May 26 2005 Bill Nottingham <notting@redhat.com> 3.6-17
- rebuild for Extras

* Mon Mar 07 2005 Than Ngo <than@redhat.com> 3.6-16
- cleanup

* Sat Mar 05 2005 Than Ngo <than@redhat.com> 3.6-15
- rebuilt

* Wed Feb 09 2005 Than Ngo <than@redhat.com> 3.6-14
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Than Ngo <than@redhat.com> 3.6-11 
- add a patch file from kota@szbk.u-szeged.hu (bug #115524)

* Thu Nov 20 2003 Thomas Woerner <twoerner@redhat.com> 3.6-10
- Fixed RPATH (missing make in %%build)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 3.6-7
- rebuild on all arches
- remove unpackaged file from the buildroot

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 15 2002 Bill Nottingham <notting@redhat.com> 3.6-4
- add ldconfig %post/%postun

* Tue Feb 26 2002 Than Ngo <than@redhat.com> 3.6-3
- rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Nov 13 2001 Than Ngo <than@redhat.com> 3.6-1
- initial RPM for 8.0

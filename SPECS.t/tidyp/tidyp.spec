Summary:	Clean up and pretty-print HTML/XHTML/XML
Summary(zh_CN.UTF-8): 清理和完善打印 HTML/XHTML/XML
Name:		tidyp
Version:	1.04
Release:	2%{?dist}
License:	W3C
Group:		Applications/Text
Group(zh_CN.UTF-8): 应用程序/文本
Url:		http://www.tidyp.com/
Source0:	http://github.com/downloads/petdance/tidyp/tidyp-%{version}.tar.gz
Patch0:		tidyp-1.02-format.patch
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
Requires:	libtidyp%{?_isa} = %{version}-%{release}

%description
tidyp is a fork of tidy on SourceForge. The library name is "tidyp", and the
command-line tool is also "tidyp" but all internal API stays the same.

%description -l zh_CN.UTF-8
这是 tidy 的一个移植。

%package -n libtidyp
Summary:	Shared libraries for tidyp
Summary(zh_CN.UTF-8): %{name} 的运行库
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description -n libtidyp
Shared libraries for tidyp.

%description -n libtidyp -l zh_CN.UTF-8
%{name} 的运行库。

%package -n libtidyp-devel
Summary:	Development files for libtidyp
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	libtidyp%{?_isa} = %{version}-%{release}

%description -n libtidyp-devel
Development files for libtidyp.

%description -n libtidyp-devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1

# Fix permissions for debuginfo
chmod -x src/{mappedio.*,version.h}

# Fix timestamp order to avoid trying to re-run autotools
touch aclocal.m4
find . -name Makefile.in -exec touch {} \;
touch configure

%build
%configure --disable-static --disable-dependency-tracking
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
magic_rpm_clean.sh

%check
make check

%clean
rm -rf %{buildroot}

%post -n libtidyp -p /sbin/ldconfig

%postun -n libtidyp -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc ChangeLog README
%{_bindir}/tidyp

%files -n libtidyp
%defattr(-,root,root,-)
%{_libdir}/libtidyp-%{version}.so.0*

%files -n libtidyp-devel
%defattr(-,root,root,-)
%{_includedir}/tidyp/
%{_libdir}/libtidyp.so
%exclude %{_libdir}/libtidyp.la

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.04-2
- 为 Magic 3.0 重建

* Sat Oct 03 2015 Liu Di <liudidi@gmail.com> - 1.04-1
- 更新到 1.04

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.02-7
- 为 Magic 3.0 重建

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> 1.02-6
- rebuilt for gcc 4.7 in Rawhide

* Thu Aug 11 2011 Paul Howarth <paul@city-fan.org> 1.02-5
- fix mangling of output file names (#725651)

* Wed Feb  9 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.02-4
- rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 Jesse Keating <jkeating@redhat.com> 1.02-3
- rebuilt for gcc bug (#634757)

* Fri Jul 23 2010 Paul Howarth <paul@city-fan.org> 1.02-2
- re-jig for Fedora submission
- add ChangeLog and README as %%doc
- upstream URL now http://www.tidyp.com/
- drop obsolete of old libtidyp versions in main package

* Mon May 10 2010 Paul Howarth <paul@city-fan.org> 1.02-1
- update to 1.02
  - metatag check fixed
  - missing files for "make check" included
- drop upstreamed metatag patch
- fix dist tag for RHEL-6 Beta
- touch autotools-generated files in order to prevent attempted
  re-running of autotools at build time

* Mon Apr 26 2010 Paul Howarth <paul@city-fan.org> 1.00-1
- update to 1.00
  - removed -Wextra compiler flag for gcc, incompatible with older versions
  - added "check" and "tags" make targets
  - removed commented-out code
- add %%check section, using test data from upstream git since it was omitted
  from the distribution tarball
- drop upstreamed parts of patches
- merge autotools patch into cflags patch
- add patch to update "generator" metatag properly

* Mon Mar  1 2010 Paul Howarth <paul@city-fan.org> 0.99-2
- main package renamed to tidyp, as per upstream
- new subpackage libtidyp (same split as tidy in Fedora)
- upstream has now provided a proper tarball, with pre-built configure script,
  so rework build system patches and drop autotools buildreqs
- reworked upstream tarball no longer includes docs

* Wed Feb 17 2010 Paul Howarth <paul@city-fan.org> 0.99-1
- libtidyp forked from tidy
- add patches to autotools build to make it work more sanely


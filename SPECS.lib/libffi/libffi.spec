%global multilib_arches %{ix86} ppc %{power64} s390 s390x x86_64

Name:		libffi
Version: 3.2.1
Release:	7%{?dist}
Summary:	A portable foreign function interface library
Summary(zh_CN.UTF-8): 可移植的外部函数接口库

Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	BSD
URL:		http://sourceware.org/libffi
Source0:	ftp://sourceware.org/pub/libffi/libffi-%{version}.tar.gz
# part of upstream commit 5feacad4
Source1:	ffi-multilib.h
Source2:	ffitarget-multilib.h
Patch0:		libffi-3.1-fix-include-path.patch
Patch1:		libffi-3.1-fix-exec-stack.patch
# part of upstream commit 5feacad4
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Compilers for high level languages generate code that follow certain
conventions.  These conventions are necessary, in part, for separate
compilation to work.  One such convention is the "calling convention".
The calling convention is a set of assumptions made by the compiler
about where function arguments will be found on entry to a function.  A
calling convention also specifies where the return value for a function
is found.  

Some programs may not know at the time of compilation what arguments
are to be passed to a function.  For instance, an interpreter may be
told at run-time about the number and types of arguments used to call a
given function.  `Libffi' can be used in such programs to provide a
bridge from the interpreter program to compiled code.

The `libffi' library provides a portable, high level programming
interface to various calling conventions.  This allows a programmer to
call any function specified by a call interface description at run time.

FFI stands for Foreign Function Interface.  A foreign function
interface is the popular name for the interface that allows code
written in one language to call code written in another language.  The
`libffi' library really only provides the lowest, machine dependent
layer of a fully featured foreign function interface.  A layer must
exist above `libffi' that handles type conversions for values passed
between the two languages.  

%description -l zh_CN.UTF-8
可移植的外部函数接口库。

%package	devel
Summary:	Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}
Requires:       pkgconfig
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1 -b .fixpath
%patch1 -p1

%build
autoreconf -fisv
%configure --disable-static
#临时性措施
%ifarch x86_64
sed -i "s/libffi-3.1\/include//g" x86_64-magic-linux-gnu/include/Makefile
%endif
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# Determine generic arch target name for multilib wrapper
basearch=%{_arch}
%ifarch %{ix86}
basearch=i386
%endif

%ifarch %{multilib_arches}
# Do header file switcheroo to avoid file conflicts on systems where you
# can have both a 32- and 64-bit version of the library, and they each need
# their own correct-but-different versions of the headers to be usable.
for i in ffi ffitarget; do
  mv $RPM_BUILD_ROOT%{_includedir}/$i.h $RPM_BUILD_ROOT%{_includedir}/$i-${basearch}.h
done
install -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_includedir}/ffi.h
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_includedir}/ffitarget.h
%endif
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%post devel
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/libffi.info.gz

%preun devel
if [ $1 = 0 ] ;then
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/libffi.info.gz
fi

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc LICENSE README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*.pc
%{_includedir}/ffi*.h
%{_libdir}/*.so
%{_mandir}/man3/*.gz
%{_infodir}/libffi.info.gz

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 3.2.1-7
- 更新到 3.2.1

* Thu Jul 17 2014 Liu Di <liudidi@gmail.com> - 3.1-6
- 为 Magic 3.0 重建

* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 3.1-5
- 更新到 3.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Tom Callaway <spot@fedoraproject.org> - 3.0.13-4
- fix typos in wrapper headers

* Mon May 27 2013 Tom Callaway <spot@fedoraproject.org> - 3.0.13-3
- make header files multilib safe

* Sat May 25 2013 Tom Callaway <spot@fedoraproject.org> - 3.0.13-2
- fix incorrect header pathing (and .pc file)

* Wed Mar 20 2013 Anthony Green <green@redhat.com> - 3.0.13-1
- update to 3.0.13

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 14 2013 Dennis Gilmore <dennis@ausil.us> - 3.0.11-1
- update to 3.0.11

* Fri Nov 02 2012 Deepak Bhole <dbhole@redhat.com> - 3.0.10-4
- Fixed source location

* Fri Aug 10 2012 Dennis Gilmore <dennis@ausil.us> - 3.0.10-3
- drop back to 3.0.10, 3.0.11 was never pushed anywhere as the soname bump broke buildroots
- as 3.0.11 never went out no epoch needed.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 13 2012 Anthony Green <green@redhat.com> - 3.0.11-1
- Upgrade to 3.0.11.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 23 2011 Anthony Green <green@redhat.com> - 3.0.10-1
- Upgrade to 3.0.10. 

* Fri Mar 18 2011 Dan Horák <dan[at]danny.cz> - 3.0.9-3
- added patch for being careful when defining relatively generic symbols

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 29 2009 Anthony Green <green@redhat.com> - 3.0.9-1
- Upgrade

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 08 2008 Anthony Green <green@redhat.com> 3.0.5-1
- Upgrade to 3.0.5

* Fri Feb 15 2008 Anthony Green <green@redhat.com> 3.0.1-1
- Upgrade to 3.0.1

* Fri Feb 15 2008 Anthony Green <green@redhat.com> 2.99.9-1
- Upgrade to 2.99.9
- Require pkgconfig for the devel package.
- Update summary.

* Fri Feb 15 2008 Anthony Green <green@redhat.com> 2.99.8-1
- Upgrade to 2.99.8

* Thu Feb 14 2008 Anthony Green <green@redhat.com> 2.99.7-1
- Upgrade to 2.99.7

* Thu Feb 14 2008 Anthony Green <green@redhat.com> 2.99.6-1
- Upgrade to 2.99.6

* Thu Feb 14 2008 Anthony Green <green@redhat.com> 2.99.4-1
- Upgrade to 2.99.4

* Thu Feb 14 2008 Anthony Green <green@redhat.com> 2.99.3-1
- Upgrade to 2.99.3

* Thu Feb 14 2008 Anthony Green <green@redhat.com> 2.99.2-1
- Created.

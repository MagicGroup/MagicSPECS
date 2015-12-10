%define debug_package %{nil}
%define	name	smake
%define	serial	7
%define	prefix	/usr

%define	major	1.2

Summary:	The Schily smake program.
Summary(zh_CN.UTF-8): Schily smake 程序
Name:		%{name}
Version:	1.2.5
Release:	3%{?dist}
Epoch:		%{serial}
Prefix:		%{prefix}
License:	GPL
Group:		Developement/Tools
Group(zh_CN.UTF-8): 开发/工具
Vendor:		Joerg Schilling <schilling@fokus.gmd.de>
URL:		http://www.fokus.gmd.de/research/cc/glone/employees/joerg.schilling/private/smake.html
Source:		http://downloads.sourceforge.net/project/s-make/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Smake is the only make program with automake features, it is the only program
that works on unknown platforms..

Smake executes command sequences based on relations of modification dates of
files. The command sequences are taken from a set of rules found in a makefile
or in the set of implicit rules. The argument target is typically a program
that is to be built from the known rules.

If no -f option is present, smake looks for SMakefile then for Makefile and
then for makefile in the named order.

If no target is specified on the command line, smake uses the first target that
could be found in makefilename and that does not start with a dot ('.').

If a target has no explicit entry in the makefile smake tries to use implicit
rules or the .DEFAULT rule.

Unlike most other make programs, smake propagates all command line macros to
sub makes. This is a big advantage with hierarchical makefile systems.
Propagation is done in a POSIX compliant way using the MAKEFLAGS= environment.

Unlike other make programs, smake includes a set of automake features that
allow to implement portable, layered, object oriented makefiles.

%description -l zh_CN.UTF-8
Schily smake 程序。

%package devel
Summary: Development package for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
Files for development with %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-%{version}

%build
make INS_BASE=/usr INS_RBASE=/ DESTDIR=$RPM_BUILD_ROOT MANDIR=man DEFAULTS_DIR=/usr/share/smake STRIPFLAGS=-s RUNPATH=

%install
make INS_BASE=/usr INS_RBASE=/ DESTDIR=$RPM_BUILD_ROOT MANDIR=man DEFAULTS_DIR=/usr/share/smake STRIPFLAGS=-s install RUNPATH=
chmod 644 $RPM_BUILD_ROOT/usr/lib/lib*.a
if [ "%_lib" != "lib" ] ; then
  mkdir -p $RPM_BUILD_ROOT/usr/%_lib
  mv $RPM_BUILD_ROOT/usr/lib/lib*.a $RPM_BUILD_ROOT/usr/%_lib
fi
rm -Rf $RPM_BUILD_ROOT/usr/lib/profiled

mkdir $RPM_BUILD_ROOT/usr/share/smake
mv $RPM_BUILD_ROOT/usr/lib/defaults.smk $RPM_BUILD_ROOT/usr/share/smake/defaults.smk
magic_rpm_clean.sh

%clean
[ -d ${RPM_BUILD_ROOT} ] && rm -rf ${RPM_BUILD_ROOT};

%files
%defattr(-, root, root)
%{_mandir}/man1/*
%attr(544,root,root) %{_bindir}/smake
%dir %{_datadir}/smake
%{_datadir}/smake/defaults.smk

%files devel
%defattr(-, root, root)
%{_mandir}/man5/*
%dir %{_includedir}/schily
%{_includedir}/schily/*
%{_libdir}/lib*.a

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 7:1.2.5-3
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 7:1.2.5-2
- 为 Magic 3.0 重建

* Mon Sep 28 2015 Liu Di <liudidi@gmail.com> - 7:1.2.5-1
- 更新到 1.2.5



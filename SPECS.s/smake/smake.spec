%define	name	smake
%define	serial	7
%define	prefix	/usr

%define	major	1.2

Summary:	The Schily smake program.
Summary(zh_CN.UTF-8): Schily smake 程序
Name:		%{name}
Version:	1.2a49
Release:	1%{?dist}
Epoch:		%{serial}
Prefix:		%{prefix}
License:	GPL
Group:		Developement/Tools
Group(zh_CN.UTF-8): 开发/工具
Vendor:		Joerg Schilling <schilling@fokus.gmd.de>
URL:		http://www.fokus.gmd.de/research/cc/glone/employees/joerg.schilling/private/smake.html
Source:		%{name}-%{version}.tar.bz2
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

%prep
%setup -q -n %{name}-%{major}

%build
if [ ! -z "`which smake 2>/dev/null`" ]; then
    export MAKEPROG='smake';
elif [ ! -z "`which gmake 2>/dev/null`" ]; then
    export MAKEPROG='gmake';
else
    export MAKEPROG='make';
fi

${MAKEPROG};

%install
[ -d ${RPM_BUILD_ROOT} ] && rm -rf ${RPM_BUILD_ROOT};

if [ ! -z "`which smake 2>/dev/null`" ]; then
    export MAKEPROG='smake';
elif [ ! -z "`which gmake 2>/dev/null`" ]; then
    export MAKEPROG='gmake';
else
    export MAKEPROG='make';
fi

${MAKEPROG} "INS_BASE=${RPM_BUILD_ROOT}%{prefix}" install

# libschily.a installed by cdrtools, no need for it here...
[ -f "${RPM_BUILD_ROOT}%{prefix}/lib/libschily.a" ] && \
    rm -f "${RPM_BUILD_ROOT}%{prefix}/lib/libschily.a";

mkdir smake-rpmdocs
cp AN-%{version} PORTING README* smake/defaults.smk smake-rpmdocs
chmod 644 smake-rpmdocs/*

rm -rf %{buildroot}%{_includedir}
rm -f  %{buildroot}%{_prefix}/lib/profiled/libschily.a
magic_rpm_clean.sh

%clean
[ -d ${RPM_BUILD_ROOT} ] && rm -rf ${RPM_BUILD_ROOT};

%files
%defattr(-,root,root)
%doc smake-rpmdocs/*

%config(noreplace) %{prefix}/lib/defaults.smk

%{prefix}/bin/smake
#{prefix}/include/align.h
#{prefix}/include/avoffset.h

%{prefix}/man/man1/smake.1*
%{prefix}/man/man5/makerules.5*
%{prefix}/man/man5/makefiles.5*

%changelog


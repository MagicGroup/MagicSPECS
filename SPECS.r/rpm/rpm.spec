# build against xz?
%bcond_without xz
# just for giggles, option to build with internal Berkeley DB
%bcond_with int_bdb
# run internal testsuite?
%bcond_without check
# disable plugins initially
%bcond_with plugins

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define rpmhome /usr/lib/rpm

%define rpmver 4.11.2
%define srcver %{rpmver}%{?snapver:-%{snapver}}

%define bdbname libdb
%define bdbver 5.3.15
%define dbprefix db

Summary: The RPM package management system
Name: rpm
Version: %{rpmver}
Release: %{?snapver:0.%{snapver}.}11%{?dist}.1
Group: System Environment/Base
Url: http://www.rpm.org/
Source0: http://rpm.org/releases/rpm-4.11.x/%{name}-%{srcver}.tar.bz2
%if %{with int_bdb}
Source1: db-%{bdbver}.tar.gz
%else
BuildRequires: libdb-devel
%endif
Source10: libsymlink.attr

# Disable autoconf config.site processing (#962837)
Patch1: rpm-4.11.x-siteconfig.patch
# Fedora specspo is setup differently than what rpm expects, considering
# this as Fedora-specific patch for now
Patch2: rpm-4.9.90-fedora-specspo.patch
# In current Fedora, man-pages pkg owns all the localized man directories
Patch3: rpm-4.9.90-no-man-dirs.patch
# gnupg2 comes installed by default, avoid need to drag in gnupg too
Patch4: rpm-4.8.1-use-gpg2.patch
Patch5: rpm-4.9.90-armhfp.patch
#conditionally applied patch for arm hardware floating point
Patch6: rpm-4.9.0-armhfp-logic.patch
# Generate kmod(basename.ko) provides for kernel
Patch7: rpm-4.11.2-kmod-find-provides.patch

# Patches already in upstream
# Filter soname dependencies by name
Patch100: rpm-4.11.x-filter-soname-deps.patch
Patch102: rpm-4.11.x-do-not-filter-ld64.patch
Patch103: rpm-4.11.1-file-triplet-check.patch
Patch104: rpm-4.11.1-caps-double-free.patch
Patch105: rpm-4.11.1-empty-lua-script.patch
Patch106: rpm-4.11.1-ppc64le.patch
Patch107: rpm-4.11.1-application-provides.patch
Patch108: rpm-4.11.1-py3-fixes.patch

# These are not yet upstream
Patch301: rpm-4.6.0-niagara.patch
Patch302: rpm-4.7.1-geode-i686.patch
# Probably to be upstreamed in slightly different form
Patch304: rpm-4.9.1.1-ld-flags.patch
# Compressed debuginfo support (#833311)
Patch305: rpm-4.10.0-dwz-debuginfo.patch
# Minidebuginfo support (#834073)
Patch306: rpm-4.10.0-minidebuginfo.patch
# Fix CRC32 after dwz (#971119)
Patch307: rpm-4.11.2-sepdebugcrcfix.patch
# To be upstreamed in slightly different form
Patch308: rpm-4.11.0.1-setuppy-fixes.patch
# Temporary Patch to provide support for updates
Patch400: rpm-4.10.90-rpmlib-filesystem-check.patch

# 修改 find-lang.sh 脚本，允许无翻译文件
Patch1000: rpm-4.11.2-allowemptylang.patch

# Mips64el
Patch2000: rpm-4.11.2-mips64el.patch

# Partially GPL/LGPL dual-licensed and some bits with BSD
# SourceLicense: (GPLv2+ and LGPLv2+ with exceptions) and BSD 
License: GPLv2+

Requires: coreutils
%if %{without int_bdb}
# db recovery tools, rpmdb_util symlinks
Requires: %{_bindir}/%{dbprefix}_stat
%endif
Requires: popt%{_isa} >= 1.10.2.1
Requires: curl

%if %{without int_bdb}
BuildRequires: %{bdbname}-devel%{_isa}
%endif

%if %{with check}
BuildRequires: fakechroot
%endif

# XXX generally assumed to be installed but make it explicit as rpm
# is a bit special...
BuildRequires: magic-rpm-config
BuildRequires: gawk
BuildRequires: elfutils-devel%{_isa} >= 0.112
BuildRequires: elfutils-libelf-devel%{_isa}
BuildRequires: readline-devel%{_isa} zlib-devel%{_isa}
BuildRequires: nss-devel%{_isa}
BuildRequires: nss-softokn-freebl-devel%{_isa}
# The popt version here just documents an older known-good version
BuildRequires: popt-devel%{_isa} >= 1.10.2
BuildRequires: file-devel%{_isa}
BuildRequires: gettext-devel%{_isa}
BuildRequires: ncurses-devel%{_isa}
BuildRequires: bzip2-devel%{_isa} >= 0.9.0c-2
BuildRequires: python-devel%{_isa} >= 2.6
BuildRequires: python3-devel%{_isa} >= 3.2
BuildRequires: lua-devel%{_isa} >= 5.1
BuildRequires: libcap-devel%{_isa}
BuildRequires: libacl-devel%{_isa}
%if ! %{without xz}
BuildRequires: xz-devel%{_isa} >= 4.999.8
%endif
# Only required by sepdebugcrcfix patch
BuildRequires: binutils-devel

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The RPM Package Manager (RPM) is a powerful command line driven
package management system capable of installing, uninstalling,
verifying, querying, and updating software packages. Each software
package consists of an archive of files along with information about
the package like its version, a description, etc.

%package libs
Summary:  Libraries for manipulating RPM packages
Group: Development/Libraries
License: GPLv2+ and LGPLv2+ with exceptions
Requires: rpm = %{version}-%{release}
# librpm uses cap_compare, introduced sometimes between libcap 2.10 and 2.16.
# A manual require is needed, see #505596
Requires: libcap%{_isa} >= 2.16

%description libs
This package contains the RPM shared libraries.

%package build-libs
Summary:  Libraries for building and signing RPM packages
Group: Development/Libraries
License: GPLv2+ and LGPLv2+ with exceptions
Requires: rpm-libs%{_isa} = %{version}-%{release}
Requires: %{_bindir}/gpg2

%description build-libs
This package contains the RPM shared libraries for building and signing
packages.

%package devel
Summary:  Development files for manipulating RPM packages
Group: Development/Libraries
License: GPLv2+ and LGPLv2+ with exceptions
Requires: rpm = %{version}-%{release}
Requires: rpm-libs%{_isa} = %{version}-%{release}
Requires: rpm-build-libs%{_isa} = %{version}-%{release}
Requires: popt-devel%{_isa}

%description devel
This package contains the RPM C library and header files. These
development files will simplify the process of writing programs that
manipulate RPM packages and databases. These files are intended to
simplify the process of creating graphical package managers or any
other tools that need an intimate knowledge of RPM packages in order
to function.

This package should be installed if you want to develop programs that
will manipulate RPM packages and databases.

%package build
Summary: Scripts and executable programs used to build packages
Group: Development/Tools
Requires: rpm = %{version}-%{release}
Requires: elfutils >= 0.128 binutils
Requires: findutils sed grep gawk diffutils file patch >= 2.5
Requires: tar unzip gzip bzip2 cpio xz
Requires: pkgconfig >= 1:0.24
Requires: /usr/bin/gdb-add-index
# Technically rpmbuild doesn't require any external configuration, but
# creating distro-compatible packages does. To make the common case
# "just work" while allowing for alternatives, depend on a virtual
# provide, typically coming from redhat-rpm-config.
Requires: system-rpm-config
Conflicts: ocaml-runtime < 3.11.1-7

%description build
The rpm-build package contains the scripts and executable programs
that are used to build packages using the RPM Package Manager.

%package sign
Summary: Package signing support
Group: System Environment/Base
Requires: rpm-build-libs%{_isa} = %{version}-%{release}

%description sign
This package contains support for digitally signing RPM packages.

%package python
Summary: Python 2 bindings for apps which will manipulate RPM packages
Group: Development/Libraries
Requires: rpm = %{version}-%{release}

%description python
The rpm-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by RPM Package Manager libraries.

This package should be installed if you want to develop Python 2
programs that will manipulate RPM packages and databases.

%package python3
Summary: Python 3 bindings for apps which will manipulate RPM packages
Group: Development/Libraries
Requires: rpm = %{version}-%{release}

%description python3
The rpm-python3 package contains a module that permits applications
written in the Python programming language to use the interface
supplied by RPM Package Manager libraries.

This package should be installed if you want to develop Python 3
programs that will manipulate RPM packages and databases.

%package apidocs
Summary: API documentation for RPM libraries
Group: Documentation
BuildArch: noarch

%description apidocs
This package contains API documentation for developing applications
that will manipulate RPM packages and databases.

%package cron
Summary: Create daily logs of installed packages.
Group: System Environment/Base
BuildArch: noarch
Requires: crontabs logrotate rpm = %{version}-%{release}

%description cron
This package contains a cron job which creates daily logs of installed
packages on a system.

%prep
%setup -q -n %{name}-%{srcver} %{?with_int_bdb:-a 1}
%patch1 -p1 -b .siteconfig
%patch2 -p1 -b .fedora-specspo
%patch3 -p1 -b .no-man-dirs
%patch4 -p1 -b .use-gpg2
%patch7 -p1 -b .kmod-provides

%patch100 -p1 -b .filter-soname-deps
%patch102 -p1 -b .dont-filter-ld64

%patch301 -p1 -b .niagara
%patch302 -p1 -b .geode
%patch304 -p1 -b .ldflags
%patch305 -p1 -b .dwz-debuginfo
%patch306 -p1 -b .minidebuginfo
%patch307 -p1 -b .sepdebugcrcfix
%patch308 -p1 -b .setuppy-fixes

%patch400 -p1 -b .rpmlib-filesystem-check

%patch5 -p1 -b .armhfp
# this patch cant be applied on softfp builds
%ifnarch armv3l armv4b armv4l armv4tl armv5tel armv5tejl armv6l armv7l
%patch6 -p1 -b .armhfp-logic
%endif

%patch1000 -p1
%patch2000 -p1

%if %{with int_bdb}
ln -s db-%{bdbver} db
%endif

%build
%if %{without int_bdb}
#CPPFLAGS=-I%{_includedir}/db%{bdbver} 
#LDFLAGS=-L%{_libdir}/db%{bdbver}
%endif
CPPFLAGS="$CPPFLAGS `pkg-config --cflags nss`"
CFLAGS="$RPM_OPT_FLAGS"
export CPPFLAGS CFLAGS LDFLAGS

# Using configure macro has some unwanted side-effects on rpm platform
# setup, use the old-fashioned way for now only defining minimal paths.
./configure \
    --prefix=%{_usr} \
    --sysconfdir=%{_sysconfdir} \
    --localstatedir=%{_var} \
    --sharedstatedir=%{_var}/lib \
    --libdir=%{_libdir} \
    --build=%{_target_platform} \
    --host=%{_target_platform} \
    --with-vendor=magic \
    %{!?with_int_bdb: --with-external-db} \
    %{!?with_plugins: --disable-plugins} \
    --with-lua \
    --without-selinux \
    --with-cap \
    --with-acl \
    --enable-python

make %{?_smp_mflags}

pushd python
%{__python} setup.py build
%{__python3} setup.py build
popd

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR="$RPM_BUILD_ROOT" install

# We need to build with --enable-python for the self-test suite, but we
# actually package the bindings built with setup.py (#531543#c26)
rm -rf $RPM_BUILD_ROOT/%{python_sitearch}
pushd python
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd


# Save list of packages through cron
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.daily
install -m 755 scripts/rpm.daily ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.daily/rpm

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
install -m 644 scripts/rpm.log ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/rpm

mkdir -p ${RPM_BUILD_ROOT}/usr/lib/tmpfiles.d
echo "r /var/lib/rpm/__db.*" > ${RPM_BUILD_ROOT}/usr/lib/tmpfiles.d/rpm.conf

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm
mkdir -p $RPM_BUILD_ROOT%{rpmhome}/macros.d

install -m 644 %{SOURCE10} ${RPM_BUILD_ROOT}%{rpmhome}/fileattrs/libsymlink.attr

mkdir -p $RPM_BUILD_ROOT/var/lib/rpm
for dbi in \
    Basenames Conflictname Dirnames Group Installtid Name Obsoletename \
    Packages Providename Requirename Triggername Sha1header Sigmd5 \
    __db.001 __db.002 __db.003 __db.004 __db.005 __db.006 __db.007 \
    __db.008 __db.009
do
    touch $RPM_BUILD_ROOT/var/lib/rpm/$dbi
done

# plant links to relevant db utils as rpmdb_foo for documention compatibility
%if %{without int_bdb}
for dbutil in dump load recover stat upgrade verify
do
    ln -s ../../bin/%{dbprefix}_${dbutil} $RPM_BUILD_ROOT/%{rpmhome}/rpmdb_${dbutil}
done
%endif

magic_rpm_clean.sh
%find_lang %{name}

find $RPM_BUILD_ROOT -name "*.la"|xargs rm -f

# avoid dragging in tonne of perl libs for an unused script
chmod 0644 $RPM_BUILD_ROOT/%{rpmhome}/perldeps.pl

# compress our ChangeLog, it's fairly big...
bzip2 -9 ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with check}
%check
make check
[ "$(ls -A tests/rpmtests.dir)" ] && cat tests/rpmtests.log
%endif

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post build-libs -p /sbin/ldconfig
%postun build-libs -p /sbin/ldconfig

%posttrans
# XXX this is klunky and ugly, rpm itself should handle this
dbstat=/usr/lib/rpm/rpmdb_stat
if [ -x "$dbstat" ]; then
    if "$dbstat" -e -h /var/lib/rpm 2>&1 | grep -q "doesn't match library version \| Invalid argument"; then
        rm -f /var/lib/rpm/__db.* 
    fi
fi
exit 0

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc GROUPS COPYING CREDITS ChangeLog.bz2 doc/manual/[a-z]*

/usr/lib/tmpfiles.d/rpm.conf
%dir %{_sysconfdir}/rpm

%attr(0755, root, root) %dir /var/lib/rpm
%attr(0644, root, root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/lib/rpm/*

/bin/rpm
%{_bindir}/rpm2cpio
%{_bindir}/rpmdb
%{_bindir}/rpmkeys
%{_bindir}/rpmquery
%{_bindir}/rpmverify

%{_mandir}/man8/rpm.8*
%{_mandir}/man8/rpmdb.8*
%{_mandir}/man8/rpmkeys.8*
%{_mandir}/man8/rpm2cpio.8*

# 有清理语言脚本的情况下，这些文件会被删除
# XXX this places translated manuals to wrong package wrt eg rpmbuild
#%lang(fr) %{_mandir}/fr/man[18]/*.[18]*
#%lang(ko) %{_mandir}/ko/man[18]/*.[18]*
#%lang(ja) %{_mandir}/ja/man[18]/*.[18]*
#%lang(pl) %{_mandir}/pl/man[18]/*.[18]*
#%lang(ru) %{_mandir}/ru/man[18]/*.[18]*
#%lang(sk) %{_mandir}/sk/man[18]/*.[18]*

%attr(0755, root, root) %dir %{rpmhome}
%{rpmhome}/macros
%{rpmhome}/macros.d
%{rpmhome}/rpmpopt*
%{rpmhome}/rpmrc

%{rpmhome}/rpmdb_*
%{rpmhome}/rpm.daily
%{rpmhome}/rpm.log
%{rpmhome}/rpm.supp
%{rpmhome}/rpm2cpio.sh
%{rpmhome}/tgpg

%{rpmhome}/platform

%files libs
%defattr(-,root,root)
%{_libdir}/librpmio.so.*
%{_libdir}/librpm.so.*
%if %{with plugins}
%{_libdir}/rpm-plugins
%endif

%files build-libs
%defattr(-,root,root)
%{_libdir}/librpmbuild.so.*
%{_libdir}/librpmsign.so.*

%files build
%defattr(-,root,root)
%{_bindir}/rpmbuild
%{_bindir}/gendiff
%{_bindir}/rpmspec

%{_mandir}/man1/gendiff.1*
%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmdeps.8*
%{_mandir}/man8/rpmspec.8*

%{rpmhome}/brp-*
%{rpmhome}/check-*
%{rpmhome}/debugedit
#这个是做什么用的？
%{rpmhome}/sepdebugcrcfix
%{rpmhome}/find-debuginfo.sh
%{rpmhome}/find-lang.sh
%{rpmhome}/*provides*
%{rpmhome}/*requires*
%{rpmhome}/*deps*
%{rpmhome}/*.prov
%{rpmhome}/*.req
%{rpmhome}/config.*
%{rpmhome}/mkinstalldirs
%{rpmhome}/macros.p*
%{rpmhome}/fileattrs

%files sign
%defattr(-,root,root)
%{_bindir}/rpmsign
%{_mandir}/man8/rpmsign.8*

%files python
%defattr(-,root,root)
%{python_sitearch}/rpm
%{python_sitearch}/rpm_python-%{version}-py2.7.egg-info

%files python3
%defattr(-,root,root)
%{python3_sitearch}/rpm
%{python3_sitearch}/rpm_python-%{version}-py%{python3_version}.egg-info

%files devel
%defattr(-,root,root)
%{_mandir}/man8/rpmgraph.8*
%{_bindir}/rpmgraph
%{_libdir}/librp*[a-z].so
%{_libdir}/pkgconfig/rpm.pc
%{_includedir}/rpm

%files cron
%defattr(-,root,root)
%{_sysconfdir}/cron.daily/rpm
%config(noreplace) %{_sysconfdir}/logrotate.d/rpm

%files apidocs
%defattr(-,root,root)
%doc COPYING doc/librpm/html/*

%changelog
* Fri Jan 03 2014 Liu Di <liudidi@gmail.com> - 4.11.1-11.1
- 为 Magic 3.0 重建



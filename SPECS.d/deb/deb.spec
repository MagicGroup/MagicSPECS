%define debhelper_ver 9.20120909

Name:           deb
BuildRequires:  gcc-c++ ncurses-devel texlive-latex zlib-devel
Url:            http://www.debian.org
License:        GPL v2 or later
Group: Applications/Archiving
Group(zh_CN.UTF-8): 应用程序/归档
Provides:       dpkg dpkg-dev debhelper dselect dpkg-doc
Requires:       cpio patch make html2text
Version:        1.16.9
Release:        2%{?dist}
Summary:        Tools for Debian Packages
Summary(zh_CN.UTF-8): Debian Linux 使用的包管理系统
Source:		http://ftp.debian.org/debian/pool/main/d/dpkg/dpkg_%{version}.tar.xz
Source1:        http://ftp.debian.org/debian/pool/main/d/debhelper/debhelper_%{debhelper_ver}.tar.gz
Source2:        dpkg-requires.sh
Patch1:		debhelper-no-localized-manpages.diff 
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
#编译时需要使用 dpkg 命令
#BuildRequires:	deb
%define __perl_requires  %{SOURCE2}

%description
This package contains tools for working with Debian packages. It makes
it possible to create and extract Debian packages. If Alien is
installed, the packages can be converted to RPMs.

This package contains the following Debian packages: dpkg, dselect,
dpkg-doc, dpkg-dev, and debhelper.



Authors:
--------
    Klee Dienes <klee@mit.edu>
    Joey Hess <joeyh@master.debian.org>

%description -l zh_CN.UTF-8
这个包包含了安装和移除 Debian 系统的包的 dpkg 程序，及建立和解开 deb 
源包的 dpkg-dev 程序，还有 debhelper, dselect, dpkg-doc 等。

%package devel 
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel 
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。

%package static
Summary: Static library for %{name}
Summary(zh_CN.UTF-8): %{name} 的静态库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description static
%{summary}.

%description static -l zh_CN.UTF-8
%{name} 的开发文件。


%prep
%setup -q -n dpkg-%{version} -b 1
pushd ../debhelper
%patch1 -p1
popd
# update arch table
sed -n '/linux-gnu/ s/linux-gnu/magic-linux/p' debian/archtable > debian/archtable.tmp
echo "mips64el-linux-gnu		mips64el" >> debian/archtable.tmp
echo "mips64el-magic-linux		mips64el" >> debian/archtable.tmp
echo "mips64el	mips64el	mips64el		64	little" >> cputable
cat debian/archtable.tmp >> debian/archtable
rm debian/archtable.tmp

%build
export CFLAGS="$RPM_OPT_FLAGS"
%configure\
	--without-selinux \
	--localstatedir=%{_localstatedir}/lib\
	--libdir=%{_prefix}/lib
make %{?_smp_mflags}
# This makes debhelper man pages
cd ../debhelper
make VERSION='%{debhelper_ver}'

%install
##
# dpkg stuff
##
%makeinstall
# locales
magic_rpm_clean.sh
%{find_lang} dpkg
%{find_lang} dselect
#%{find_lang} dpkg-dev
cat dpkg.lang dselect.lang > deb.lang
# docs
install -d -m 755 $RPM_BUILD_ROOT/%{_docdir}/deb/dpkg
install -m 644 ABOUT-NLS $RPM_BUILD_ROOT/%{_docdir}/deb/dpkg
install -m 644 AUTHORS $RPM_BUILD_ROOT/%{_docdir}/deb/dpkg
install -m 644 COPYING $RPM_BUILD_ROOT/%{_docdir}/deb/dpkg
install -m 644 doc/triggers.txt $RPM_BUILD_ROOT/%{_docdir}/deb/dpkg
install -m 644 NEWS $RPM_BUILD_ROOT/%{_docdir}/deb/dpkg
install -m 644 README* $RPM_BUILD_ROOT/%{_docdir}/deb/dpkg
install -m 644 THANKS $RPM_BUILD_ROOT/%{_docdir}/deb/dpkg
install -m 644 TODO $RPM_BUILD_ROOT/%{_docdir}/deb/dpkg
install -m 644 debian/changelog $RPM_BUILD_ROOT/%{_docdir}/deb/dpkg
##
# debhelper stuff
##
cd ../debhelper
# autoscripts
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/debhelper/autoscripts
install -m 644 autoscripts/* $RPM_BUILD_ROOT%{_datadir}/debhelper/autoscripts
# perl modules:
install -d -m 755 $RPM_BUILD_ROOT%{perl_vendorlib}/Debian/Debhelper
install -d -m 755 $RPM_BUILD_ROOT%{perl_vendorlib}/Debian/Debhelper/Sequence
install -m 644 Debian/Debhelper/Sequence/*.pm $RPM_BUILD_ROOT%{perl_vendorlib}/Debian/Debhelper/Sequence
install -m 644 Debian/Debhelper/*.pm $RPM_BUILD_ROOT%{perl_vendorlib}/Debian/Debhelper
# docs:
install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/deb/debhelper/examples
install -m 644 examples/* $RPM_BUILD_ROOT%{_docdir}/deb/debhelper/examples
install -m 644 doc/* $RPM_BUILD_ROOT%{_docdir}/deb/debhelper
install -m 644 debian/{changelog,copyright} $RPM_BUILD_ROOT%{_docdir}/deb/debhelper
# man pages:
install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man1
install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man7
install -m 644 *.1 $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 debhelper.7 $RPM_BUILD_ROOT%{_mandir}/man7
# binaries:
install -d -m 755 $RPM_BUILD_ROOT%{_bindir}
install -m 755 dh_*[^1-9] $RPM_BUILD_ROOT%{_bindir}
##
# remove update-alternatives stuff (included in separate package)
##
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/alternatives
rm -rf $RPM_BUILD_ROOT%{_localstatedir}/lib/dpkg/alternatives
rm -rf $RPM_BUILD_ROOT%{_bindir}/update-alternatives
rm -rf $RPM_BUILD_ROOT%{_sbindir}/update-alternatives
rm -rf $RPM_BUILD_ROOT%{_mandir}/man8/update-alternatives.8
rm -rf $RPM_BUILD_ROOT%{_mandir}/*/man8/update-alternatives.8

#这段有些问题
%ifarch x86_64
sed -i 's/\/.*deb-%{version}-%{release}.x86_64//g' %{buildroot}%{perl_vendorlib}/Dpkg.pm
sed -i 's/\/.*deb-%{version}-%{release}.x86_64//g' %{buildroot}%{_datadir}/dpkg/default.mk
%endif

%ifarch %{ix86}
sed -i 's/\/.*deb-%{version}-%{release}.i386//g' %{buildroot}%{perl_vendorlib}/Dpkg.pm
sed -i 's/\/.*deb-%{version}-%{release}.i386//g' %{buildroot}%{_datadir}/dpkg/default.mk
%endif

%ifarch mips64el
sed -i 's/\/.*deb-%{version}-%{release}.mips64el//g' %{buildroot}%{perl_vendorlib}/Dpkg.pm
sed -i 's/\/.*deb-%{version}-%{release}.mips64el//g' %{buildroot}%{_datadir}/dpkg/default.mk
%endif

mv %{buildroot}%{_sbindir}/install-info %{buildroot}%{_sbindir}/dpkg-install-info

%clean
rm -rf $RPM_BUILD_ROOT

%post
mkdir -p %{_localstatedir}/lib/dpkg
cd %{_localstatedir}/lib/dpkg
for f in diversions statoverride status ; do
    [ ! -f $f ] && touch $f
done
exit 0

%files -f deb.lang
%defattr(-,root,root)
%doc %{_docdir}/deb
%doc %{_mandir}/man*/*
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/dpkg/*
%{_datadir}/dpkg
%{_datadir}/debhelper
%{perl_vendorlib}/Debian
%{perl_vendorlib}/Dpkg
%{perl_vendorlib}/Dpkg.pm

%files devel 
%defattr(-,root,root,-)
%{_includedir}/dpkg/*.h
%{_libdir}/pkgconfig/*.pc

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.16.1.1-2
- 为 Magic 3.0 重建

* Thu Oct 27 2011 Liu Di <liudidi@gmail.com> - 1.16.1.1-1
- 升级到 1.16.1.1

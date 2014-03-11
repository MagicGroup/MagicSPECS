%define build_java 0
Summary: Timezone data
Summary(zh_CN.UTF-8): 时区数据
Name: tzdata
Version: 2011n
%define tzdata_version %{version}
%define tzcode_version 2009e
Release: 3%{?dist}
License: Public Domain
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
URL: ftp://elsie.nci.nih.gov/pub/

# The tzdata-base-0.tar.bz2 is a simple building infrastructure and
# a test suite.  It is occasionally updated from glibc sources, and as
# such is under LGPLv2+, but none of this ever gets to be part of
# final zoneinfo files.
Source0: tzdata-base-0.tar.bz2
# These are official upstream.
Source1: ftp://elsie.nci.nih.gov/pub/tzdata%{tzdata_version}.tar.gz
Source2: ftp://elsie.nci.nih.gov/pub/tzcode%{tzcode_version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gawk, glibc, perl
%if 0%{build_java}
BuildRequires: java-devel
%endif
BuildRequires: glibc-common >= 2.5.90-7
Conflicts: glibc-common <= 2.3.2-63
BuildArch: noarch

%description
This package contains data files with rules for various timezones around
the world.

%description -l zh_CN.UTF-8
这个包包含了全世界各种时区的带有规则的数据文件。

%if 0%{build_java}
%package java
Summary: Timezone data for Java
Summary(zh_CN.UTF-8): java 的时区数据
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
Source3: javazic.tar.gz
Patch0: javazic-fixup.patch

%description java
This package contains timezone information for use by Java runtimes.

%description java -l zh_CN.UTF-8
java 的时区数据。
%endif

%prep
%setup -q -n tzdata
mkdir tzdata%{tzdata_version}
tar xzf %{SOURCE1} -C tzdata%{tzdata_version}
mkdir tzcode%{tzcode_version}
tar xzf %{SOURCE2} -C tzcode%{tzcode_version}
sed -e 's|@objpfx@|'`pwd`'/obj/|' \
    -e 's|@datadir@|%{_datadir}|' \
  Makeconfig.in > Makeconfig

%if 0%{build_java}
mkdir javazic
tar zxf %{SOURCE3} -C javazic
pushd javazic
%patch0

# Hack alert! sun.tools may be defined and installed in the
# VM. In order to guarantee that we are using IcedTea/OpenJDK
# for creating the zoneinfo files, rebase all the packages
# from "sun." to "rht.". Unfortunately, gcj does not support
# any of the -Xclasspath options, so we must go this route
# to ensure the greatest compatibility.
mv sun rht
find . -type f -name '*.java' -print0 \
    | xargs -0 -- sed -i -e 's:sun\.tools\.:rht.tools.:g' \
                         -e 's:sun\.util\.:rht.util.:g'
popd
%endif

%build
make
grep -v tz-art.htm tzcode%{tzcode_version}/tz-link.htm > tzcode%{tzcode_version}/tz-link.html

%if 0%{build_java}
pushd javazic
javac -source 1.5 -target 1.5 -classpath . `find . -name \*.java`
popd
pushd tzdata%{tzdata_version}
java -classpath ../javazic/ rht.tools.javazic.Main -V %{version} \
  -d ../zoneinfo/java \
  africa antarctica asia australasia europe northamerica pacificnew \
  southamerica backward etcetera solar87 solar88 solar89 systemv \
  ../javazic/tzdata_jdk/gmt ../javazic/tzdata_jdk/jdk11_backward
popd
%endif

%install
rm -fr $RPM_BUILD_ROOT
sed -i 's|@install_root@|%{buildroot}|' Makeconfig
make install

%if 0%{build_java}
cp -pr zoneinfo/java $RPM_BUILD_ROOT%{_datadir}/javazi
%endif

magic_rpm_clean.sh

%check
echo ====================TESTING=========================
make check || :
echo ====================TESTING END=====================

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_datadir}/zoneinfo
%doc tzcode%{tzcode_version}/README
%doc tzcode%{tzcode_version}/Theory
%doc tzcode%{tzcode_version}/tz-link.html

%if 0%{build_java}
%files java
%defattr(-,root,root)
%{_datadir}/javazi
%endif

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 2011n-3
- 为 Magic 3.0 重建



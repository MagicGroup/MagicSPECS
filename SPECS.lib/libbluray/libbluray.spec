%global snapshot 0
%global tarball_date 20111023
%global git_hash e037110f11e707e223b715f70920913afecfe297
%global git_short %(echo '%{git_hash}' | cut -c -13)
%define JAVA 0

Name:           libbluray
Version: 0.6.0
%if %{snapshot}
Release:        0.9.%{tarball_date}git%{git_short}%{?dist}
%else
Release:        3%{?dist}
%endif
Summary:        Library to access Blu-Ray disks for video playback 
Summary(zh_CN.UTF-8): 为视频回放访问蓝光光盘的库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://www.videolan.org/developers/libbluray.html
%if %{snapshot}
# Use the commands below to generate a tarball.
# git clone git://git.videolan.org/libbluray.git
# cd libbluray
# git archive --format=tar %{git_hash} --prefix=libbluray/ | bzip2 > ../libbluray-$( date +%Y%m%d )git%{git_short}.tar.bz2
Source0:        %{name}-%{tarball_date}git%{git_short}.tar.bz2
%else
Source0:        ftp://ftp.videolan.org/pub/videolan/%{name}/%{version}/%{name}-%{version}.tar.bz2
%endif
# Fixed upstream, will not be needed for next upstream release
Source1:        libbluray-0.2.1-bdj_build.xml
Source2:        libbluray-0.2.1-bdj_java_subdir.tar.bz2
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%if %{snapshot}
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
%endif
%if %{JAVA}
%ifnarch ppc64
BuildRequires:  java-devel >= 1:1.6.0 
BuildRequires:  jpackage-utils
BuildRequires:  ant
%endif
%endif
BuildRequires:  libxml2-devel
BuildRequires:  doxygen
BuildRequires:  texlive-latex
BuildRequires:  graphviz


%description
This package is aiming to provide a full portable free open source bluray
library, which can be plugged into popular media players to allow full bluray
navigation and playback on Linux. It will eventually be compatible with all
current titles, and will be easily portable and embeddable in standard players
such as mplayer and vlc.

%description -l zh_CN.UTF-8
这个包的目的是提供一个完全可移植的开源蓝光库。它可以嵌入到标准的播放器，比如
mplayer 或 vlc 中。

%if %{JAVA}
%ifnarch ppc64
%package        java
Summary:        BDJ support for %{name}
Summary(zh_CN.UTF-8): %{name} 的 BDJ 支持
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       java >= 1:1.6.0 
Requires:       jpackage-utils

%description    java
The %{name}-java package contains the jar file needed to add BDJ support to
%{name}.

%description java -l zh_CN.UTF-8
%{name} 的 BDJ 支持需要的 jar 文件。
%endif
%endif

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%if %{snapshot}
%setup -q -n %{name}
%else
%setup -q
install -Dp -m 644 %{SOURCE1} src/libbluray/bdj/build.xml
tar xjf %{SOURCE2}
%endif


%build
%if %{snapshot}
autoreconf -vif
%endif
%configure --disable-static \
           --enable-examples \
%if %{JAVA}
%ifnarch ppc64
           --enable-bdjava --with-jdk=%{_jvmdir}/java-1.7.0
%endif
%endif

make %{?_smp_mflags}
make doxygen-pdf
# Remove uneeded script
rm -f doc/doxygen/html/installdox 


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%if %{JAVA}
%ifnarch ppc64
# Install BD-J jar
install -Dp -m 644 src/.libs/libbluray.jar  $RPM_BUILD_ROOT%{_javadir}/libbluray.jar
%endif
%endif

# Install test utilities
for i in clpi_dump index_dump mobj_dump mpls_dump sound_dump
do install -Dp -m 0755 src/$i $RPM_BUILD_ROOT%{_bindir}/$i; done;
for i in bd_info bdsplice hdmv_test libbluray_test list_titles 
do install -Dp -m755 src/.libs/$i %{buildroot}%{_bindir}/$i; done
%if %{JAVA}
%ifnarch ppc64
install -Dp -m755 src/examples/.libs/bdj_test %{buildroot}%{_bindir}/bdj_test;
%endif
%endif
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING player_wrappers README.txt
%{_libdir}/*.so.*
%{_bindir}/*


%if %{JAVA}
%ifnarch ppc64
%files java
%defattr(-,root,root,-)
%{_javadir}/libbluray.jar
%endif
%endif

%files devel
%defattr(-,root,root,-)
%doc doc/doxygen/html doc/doxygen/libbluray.pdf
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libbluray.pc


%changelog
* Thu Jul 10 2014 Liu Di <liudidi@gmail.com> - 0.6.0-3
- 更新到 0.6.0

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.2.1-3
- 为 Magic 3.0 重建

* Thu Mar 15 2012 Rex Dieter <rdieter@fedoraproject.org> 0.2.1-3
- make build non-fatal when using doxygen-1.8 (doesn't produce installdox anymore)

* Wed Feb 01 2012 Xavier Bachelot <xavier@bachelot.org> 0.2.1-2
- Rebuild for openjdk 7.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 01 2011 Xavier Bachelot <xavier@bachelot.org> 0.2.1-1
- First upstream official release.
- Fix BD-J build (missing files in upstream tarball).
- Have subpackages require an arch-specific base package.

* Sun Oct 23 2011 Xavier Bachelot <xavier@bachelot.org> 0.2-0.7.20111023gite037110f11e70
- Update to latest snapshot.

* Sat Jul 16 2011 Xavier Bachelot <xavier@bachelot.org> 0.2-0.6.20110710git51d7d60a96d06
- Don't build java subpackage on ppc64, no java-1.6.0-devel package.

* Sun Jul 10 2011 Xavier Bachelot <xavier@bachelot.org> 0.2-0.5.20110710git51d7d60a96d06
- Update to latest snapshot.

* Sat May 14 2011 Xavier Bachelot <xavier@bachelot.org> 0.2-0.4.20110514git46ee2766038e9
- Update to latest snapshot.
- Drop -static subpackage.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-0.3.20110126gitbbf11e43bd82e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Xavier Bachelot <xavier@bachelot.org> 0.2-0.2.20110126gitbbf11e43bd82e
- Update to latest snapshot.
- Split the BDJ support to a -java subpackage.

* Fri Jan 07 2011 Xavier Bachelot <xavier@bachelot.org> 0.2-0.1.20110107git0e5902ff9a6f1
- Update to latest snapshot.
- Add BR: libxml2-devel for metadata parser.
- Add BR: graphviz for doc generation.

* Thu Oct 28 2010 Xavier Bachelot <xavier@bachelot.org> 0.1-0.3.20101028gitc32862b77dea4
- Update to latest snapshot.
- Install BDJ jar.

* Thu Oct 21 2010 Xavier Bachelot <xavier@bachelot.org> 0.1-0.2.20101021git144a204c02687
- Fix release tag.
- Update to latest snapshot.

* Thu Aug 19 2010 Xavier Bachelot <xavier@bachelot.org> 0.1-0.1.20100819
- Initial Fedora release.

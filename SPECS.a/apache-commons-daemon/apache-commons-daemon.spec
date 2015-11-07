
%global base_name   daemon
%global short_name  commons-%{base_name}

Name:           apache-%{short_name}
Version:        1.0.15
Release:        9%{?dist}
Summary:        Defines API to support an alternative invocation mechanism
License:        ASL 2.0
Group:          Applications/System
URL:            http://commons.apache.org/%{base_name}
Source0:        http://archive.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Patch1:         apache-commons-daemon-JAVA_OS.patch
# backport from https://fisheye6.atlassian.com/changelog/commons?cs=1458896
Patch2:         apache-commons-daemon-secondary.patch
# backport from http://svn.apache.org/viewvc?view=revision&revision=1533345
# https://issues.apache.org/jira/browse/DAEMON-308
Patch3:         apache-commons-daemon-aarch64.patch
# Add mips64el support
Patch4:         apache-commons-daemon-mips64el.diff
BuildRequires:  maven-local
BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  jpackage-utils
BuildRequires:  apache-commons-parent
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  xmlto


Provides:       jakarta-%{short_name} = 1:%{version}-%{release}
Obsoletes:      jakarta-%{short_name} <= 1:1.0.1


%description
The scope of this package is to define an API in line with the current
Java Platform APIs to support an alternative invocation mechanism
which could be used instead of the public static void main(String[])
method.  This specification covers the behavior and life cycle of what
we define as Java daemons, or, in other words, non interactive
Java applications.

%package        jsvc
Summary:        Java daemon launcher
Group:          Applications/System
Provides:       jsvc = 1:%{version}-%{release}

Provides:       jakarta-%{short_name}-jsvc = 1:%{version}-%{release}
Obsoletes:      jakarta-%{short_name}-jsvc <= 1:1.0.1

%description    jsvc
%{summary}.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Documentation
Requires:       jpackage-utils
BuildArch:      noarch

Provides:       jakarta-%{short_name}-javadoc = 1:%{version}-%{release}
Obsoletes:      jakarta-%{short_name}-javadoc <= 1:1.0.1

%description    javadoc
%{summary}.


%prep
%setup -q -n %{short_name}-%{version}-src
%patch1 -p1 -b .java_os
%patch2 -p1 -b .secondary
%patch3 -p1 -b .aarch64
%patch4 -p1 -b .mips64el

# remove java binaries from sources
rm -rf src/samples/build/

chmod 644 src/samples/*
cd src/native/unix
xmlto man man/jsvc.1.xml


%build

# build native jsvc
pushd src/native/unix
%configure --with-java=%{java_home}
# this is here because 1.0.2 archive contains old *.o
make clean
make %{?_smp_mflags}
popd

# build jars
%mvn_file  : %{short_name} %{name}
%mvn_alias : org.apache.commons:%{short_name}
%mvn_build


%install
# install native jsvc
install -Dpm 755 src/native/unix/jsvc $RPM_BUILD_ROOT%{_bindir}/jsvc
install -Dpm 644 src/native/unix/jsvc.1 $RPM_BUILD_ROOT%{_mandir}/man1/jsvc.1

%mvn_install


%files -f .mfiles
%doc LICENSE.txt PROPOSAL.html NOTICE.txt RELEASE-NOTES.txt src/samples
%doc src/docs/*


%files jsvc
%doc LICENSE.txt NOTICE.txt
%{_bindir}/jsvc
%{_mandir}/man1/jsvc.1*


%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt


%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.0.15-9
- 为 Magic 3.0 重建

* Tue Aug 12 2014 Liu Di <liudidi@gmail.com> - 1.0.15-8
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.15-6
- Use Requires: java-headless rebuild (#1067528)

* Mon Nov 25 2013 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1.0.15-5
- Add AArch64 support from upstream - Resolves: rhbz #1034162

* Thu Sep 26 2013 Dan Horák <dan[at]danny.cz> - 1.0.15-4
- add back support for secondary arches (s390x, ppc64)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr  5 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.15-2
- Bump release number

* Fri Apr  5 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.15-1
- Update to upstream version 1.0.15
- Remove 0001-execve-path-warning.patch (fixed upstream)
- Remove patches for s390x and ppc64 (accepted upstream in DAEMON-289)

* Wed Feb 13 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.13-1
- Update to upstream version 1.0.13

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0.12-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jan 24 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.12-1
- Update to upstream version 1.0.12
- Install NOTICE files

* Tue Jan 15 2013 Michal Srb <msrb@redhat.com> - 1.0.11-2
- Build with xmvn
- Spec file cleanup

* Tue Dec 11 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.11-1
- Update to upstream version 1.0.11

* Fri Aug 17 2012 Karsten Hopp <karsten@redhat.com> 1.0.10-5
- add ppc64 as known arch

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 23 2012 Dan Horák <dan[at]danny.cz> - 1.0.10-3
- add s390x as known arch

* Thu Mar 29 2012 Dennis Gilmore <dennis@ausil.us> - 1.0.10-2
- $supported_os and $JAVA_OS in configure do not always match 
- on arches that override supported_os to be the arch we can not find headers

* Thu Jan 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.10-1
- Update to latest upstream (1.0.10)
- Several bugfixes concerning libcap and building upstream

* Thu Jan 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.8-1
- Update to latest upstream (1.0.8)
- Drop s390/ppc patches (upstream seems to already include them)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 15 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.7-1
- Update to latest upstream (1.0.7)
- Fix CVE-2011-2729

* Wed Jul 20 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.6-1
- Update to latest upstream (1.0.6)
- Cleanups according to new guidelines

* Mon May  9 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.5-5
- Use mvn-rpmbuild instead of mvn-local (changes in maven)

* Wed May  4 2011 Dan Horák <dan[at]danny.cz> - 1.0.5-4
- updated the s390x patch

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.5-2
- Fix bug 669259 (execve warning segfault)

* Tue Jan 18 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.5-1
- Update to latest version
- Use maven 3 to build
- Versionless jars & javadocs
- Use apache-commons-parent for BR

* Tue Oct 26 2010 Chris Spike <chris.spike@arcor.de> 1.0.4-2
- Added fix to remove java binaries from sources

* Tue Oct 26 2010 Chris Spike <chris.spike@arcor.de> 1.0.4-1
- Updated to 1.0.4

* Fri Oct 22 2010 Chris Spike <chris.spike@arcor.de> 1.0.3-1
- Updated to 1.0.3
- Cleaned up BRs

* Thu Jul  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.2-4
- Add license to javadoc subpackage

* Fri Jun  4 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.2-3
- Make javadoc subpackage noarch

* Tue Jun  1 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.2-2
- Fix add_to_maven_depmap call
- Added depmap for old groupId
- Unified use of `install`

* Wed May 12 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.2-1
- Rename and rebase to apache-commons-daemon
- Get rid of gcj, native conditional compilation
- Build with maven
- Update patches to cleanly apply on new version, remove unneeded
- Clean up whole spec

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.1-8.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 03 2009 Karsten Hopp <karsten@redhat.com> 1.0.1-7.8
- ppc needs a similar patch

* Tue Mar 03 2009 Karsten Hopp <karsten@redhat.com> 1.0.1-7.7
- add configure patch for s390x

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.1-7.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:1.0.1-6.6
- drop repotag

* Fri Feb 08 2008 Permaine Cheung <pcheung@redhat.com> - 1:1.0.1-6jpp.5
- Add configure patch for ia64 from Doug Chapman

* Mon Sep 24 2007 Permaine Cheung <pcheung@redhat.com> - 1:1.0.1-6jpp.4
- Add execve path warning patch from James Ralston

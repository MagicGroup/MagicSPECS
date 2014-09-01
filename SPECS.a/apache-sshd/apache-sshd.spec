Name: apache-sshd
Version: 0.11.0
Release: 3%{?dist}
Summary: Apache SSHD
License: ASL 2.0
URL: http://mina.apache.org/sshd-project/

Source0: http://www.apache.org/dist/mina/sshd/%{version}/%{name}-%{version}-src.tar.gz

BuildArch: noarch

BuildRequires: apache-mina
BuildRequires: bouncycastle >= 1.46
BuildRequires: bouncycastle-pkix
BuildRequires: bouncycastle-pg
BuildRequires: jzlib >= 1.1.0
BuildRequires: maven-local
BuildRequires: maven-plugin-bundle
BuildRequires: maven-plugin-testing-harness
BuildRequires: maven-shared
BuildRequires: tomcat-lib >= 7.0.25

# This is needed to avoid generating a version specific requirement for the
# bouncycastle package:
AutoReqProv: no
Requires: jpackage-utils
Requires: mvn(com.jcraft:jzlib)
Requires: mvn(org.apache.mina:mina-core)
Requires: mvn(org.apache.tomcat:tomcat-coyote)
#Requires: mvn(org.bouncycastle:bcprov-jdk15on)
Requires: mvn(org.bouncycastle:bcpkix-jdk15on)
Requires: mvn(org.bouncycastle:bcpg-jdk15on)
Provides: mvn(org.apache.sshd:sshd) = %{version}
Provides: mvn(org.apache.sshd:sshd-core) = %{version}
Provides: mvn(org.apache.sshd:sshd-sftp) = %{version}
Provides: mvn(org.apache.sshd:sshd:pom:) = %{version}


%description
Apache SSHD is a 100% pure java library to support the SSH protocols on both
the client and server side.


%package javadoc
Summary: API documentation for %{name}

%description javadoc
This package provides %{name}.


%prep
%setup -q

# Use tomcat-coyote instead of unavailable tomcat-apr
sed -i "s,<groupId>tomcat,<groupId>org.apache.tomcat,;s,<artifactId>tomcat-apr,<artifactId>tomcat-coyote,;s,<version>5.5.23,<version>7.0.52," pom.xml */pom.xml

# Build the core only:
%pom_disable_module assembly
%pom_disable_module sshd-pam

# Disable the plugins that we don't need:
%pom_remove_plugin :maven-remote-resources-plugin
# Too many files with unapproved license
%pom_remove_plugin org.apache.rat:apache-rat-plugin

%build

# Skip the tests as they don't run correctly with the current
# version of the jzlib compression library:
%mvn_build -f


%install
%mvn_install


%files -f .mfiles
%dir %{_javadir}/%{name}
%doc LICENSE.txt
%doc NOTICE.txt


%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt
%doc NOTICE.txt


%changelog
* Fri Aug 15 2014 Liu Di <liudidi@gmail.com> - 0.11.0-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 05 2014 gil cattaneo <puntogil@libero.it> - 0.11.0-1
- Update to upstream 0.11.0 (rhbz#1094049)

* Wed Nov 27 2013 Juan Hernandez <juan.hernandez@redhat.com> - 0.9.0-3
- Revert to upstream version 0.8.0 due to bug 1021273. Note that the
  version number can't go backwards, so it stays at 0.9.0.

* Mon Sep 30 2013 Juan Hernandez <juan.hernandez@redhat.com> - 0.9.0-2
- Fix bouncycastle requirement

* Mon Sep 30 2013 Juan Hernandez <juan.hernandez@redhat.com> - 0.9.0-1
- Update to upstream 0.9.0

* Mon Aug 05 2013 gil cattaneo <puntogil@libero.it> 0.7.0-5
- rebuilt rhbz#991979
- swith to Xmvn
- adapt to new guideline
- use pom macros
- remove rpmlint warnings

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0.7.0-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 26 2012 Juan Hernandez <juan.hernandez@redhat.com> - 0.7.0-1
- Update to upstream 0.7.0

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 14 2012 Juan Hernandez <juan.hernandez@redhat.com> 0.6.0-2
- Corrected the source URL

* Sun Feb 12 2012 Juan Hernandez <juan.hernandez@redhat.com> 0.6.0-1
- Initial packaging

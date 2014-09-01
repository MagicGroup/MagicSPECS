Name:          sshj
Version:       0.8.1
Release:       9%{?dist}
Summary:       SSHv2 library for Java
License:       ASL 2.0
URL:           http://schmizz.net/sshj/
Source0:       https://github.com/shikhar/sshj/archive/v%{version}.tar.gz
# Thanks to Michal Srb
# Update bouncycastle to 1.50
Patch0:        sshj-0.8.1-port-to-bouncycastle-1.50.patch
BuildRequires: java-devel

BuildRequires: mvn(com.jcraft:jzlib) >= 1.1.0-2
BuildRequires: mvn(org.bouncycastle:bcprov-jdk15on)
BuildRequires: mvn(org.bouncycastle:bcpkix-jdk15on)
BuildRequires: mvn(org.slf4j:slf4j-api)

# test deps
BuildRequires: mvn(ch.qos.logback:logback-classic)
BuildRequires: mvn(ch.qos.logback:logback-core)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.mina:mina-core)
BuildRequires: mvn(org.apache.sshd:sshd-core)
BuildRequires: mvn(org.mockito:mockito-all)

BuildRequires: maven-local
BuildRequires: maven-assembly-plugin
BuildRequires: maven-plugin-bundle
BuildRequires: maven-source-plugin
BuildRequires: maven-surefire-provider-junit

BuildArch:     noarch

%description
SSH, scp and sftp library for Java.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
%patch0 -p1

# SmokeTest.setUp:37 ? NoClassDefFound org/apache/mina/core/service/IoHandler
%pom_add_dep org.apache.mina:mina-core::test

# NoClassDefFound org/bouncycastle/openssl/PEMReader apache sshd
rm -r src/test/java/net/schmizz/sshj/SmokeTest.java
# NoClassDefFoundError: Could not initialize class org.mockito.internal.creation.jmock.ClassImposterizer$3
rm -r src/test/java/net/schmizz/sshj/sftp/PacketReaderTest.java \
 src/test/java/net/schmizz/sshj/sftp/SFTPClientTest.java

# Some classes moved from JUnit to hamcrest
sed -i -e 's/org.junit.internal.matchers/org.hamcrest.core/' src/test/java/net/schmizz/sshj/transport/verification/OpenSSHKnownHostsTest.java
%mvn_file :%{name} %{name}

%build

%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc CONTRIBUTORS LICENSE NOTICE README.rst

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Fri Aug 15 2014 Liu Di <liudidi@gmail.com> - 0.8.1-9
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 0.8.1-7
- Use Requires: java-headless rebuild (#1067528)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 02 2013 gil cattaneo <puntogil@libero.it> 0.8.1-5
- build with XMvn
- minor changes to adapt to current guideline

* Mon Apr 22 2013 Tomas Radej <tradej@redhat.com> - 0.8.1-4
- Fixed tests for new JUnit and hamcrest

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0.8.1-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jul 25 2012 gil cattaneo <puntogil@libero.it> 0.8.1-1
- Update to 0.8.1

* Mon Jul 02 2012 gil cattaneo <puntogil@libero.it> 0.8.0-1
- initial rpm

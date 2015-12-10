Name:           jsch-agent-proxy
Version:        0.0.7
Release:        9%{?dist}
Summary:        Proxy to ssh-agent and Pageant in Java
License:        BSD
URL:            http://www.jcraft.com/jsch-agent-proxy/
BuildArch:      noarch

Source0:        https://github.com/ymnk/jsch-agent-proxy/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(com.jcraft:jsch)
BuildRequires:  mvn(com.trilead:trilead-ssh2)
BuildRequires:  mvn(net.java.dev.jna:jna)
BuildRequires:  mvn(net.java.dev.jna:platform)
BuildRequires:  mvn(net.schmizz:sshj)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-ssh-external)
BuildRequires:  mvn(org.sonatype.oss:oss-parent:pom:)

%description
jsch-agent-proxy is a proxy program to OpenSSH ssh-agent and Pageant
included Putty.  It will be easily integrated into JSch, and users
will be allowed to use those programs in authentications.  This
software has been developed for JSch, but it will be easily applicable
to other ssh2 implementations in Java.  This software is licensed
under BSD style license.

%package connector-factory
Summary:        Connector factory for jsch-agent-proxy

%description connector-factory
%{summary}.

%package core
Summary:        jsch-agent-proxy core module

%description core
%{summary}.

%package jsch
Summary:        JSch connector for jsch-agent-proxy

%description jsch
%{summary}.

%package pageant
Summary:        Pageant connector for jsch-agent-proxy

%description pageant
%{summary}.

%package sshagent
Summary:        ssh-agent connector for jsch-agent-proxy

%description sshagent
%{summary}.

%package sshj
Summary:        sshj connector for jsch-agent-proxy

%description sshj
%{summary}.

%package trilead-ssh2
Summary:        trilead-ssh2 connector for jsch-agent-proxy

%description trilead-ssh2
%{summary}.

%package usocket-jna
Summary:        USocketFactory implementation using JNA

%description usocket-jna
%{summary}.

%package usocket-nc
Summary:        USocketFactory implementation using Netcat

%description usocket-nc
%{summary}.

%package        javadoc
Summary:        API documentation for %{name}

%description    javadoc
This package provides %{summary}.

%prep
%setup -q

# Put parent POM together with core module
%mvn_package :jsch.agentproxy jsch.agentproxy.core

%build
%mvn_build -s

%install
%mvn_install

%files core -f .mfiles-jsch.agentproxy.core
%dir %{_javadir}/%{name}
%doc README README.md
%doc LICENSE.txt

%files connector-factory -f .mfiles-jsch.agentproxy.connector-factory
%files jsch -f .mfiles-jsch.agentproxy.jsch
%files pageant -f .mfiles-jsch.agentproxy.pageant
%files sshagent -f .mfiles-jsch.agentproxy.sshagent
%files sshj -f .mfiles-jsch.agentproxy.sshj
%files trilead-ssh2 -f .mfiles-jsch.agentproxy.svnkit-trilead-ssh2
%files usocket-jna -f .mfiles-jsch.agentproxy.usocket-jna
%files usocket-nc -f .mfiles-jsch.agentproxy.usocket-nc

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.0.7-9
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 0.0.7-8
- 为 Magic 3.0 重建

* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 0.0.7-7
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.0.7-5
- Use Requires: java-headless rebuild (#1067528)

* Tue Jan  7 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.7-4
- Enable trilead-ssh2 module

* Mon Jan  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.7-3
- Fix directory ownership

* Mon Jan  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.7-2
- Fix a typo in javadoc pkg description
- Install README files

* Mon Jan  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.7-1
- Initial packaging


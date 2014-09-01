%global patchlvl 4

Name:           trilead-ssh2
Version:        217
Release:        5.jenkins%{patchlvl}%{?dist}
Summary:        SSH-2 protocol implementation in pure Java

# project is under BSD, but some parts are MIT licensed
# see LICENSE.txt for more information
License:        BSD and MIT
URL:            https://github.com/jenkinsci/trilead-ssh2
Source0:        https://github.com/jenkinsci/%{name}/archive/%{name}-build%{version}-jenkins-%{patchlvl}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(junit:junit)

BuildArch:      noarch

%description
Trilead SSH-2 for Java is a library which implements the SSH-2 protocol in pure
Java (tested on J2SE 1.4.2 and 5.0). It allows one to connect to SSH servers
from within Java programs. It supports SSH sessions (remote command execution
and shell access), local and remote port forwarding, local stream forwarding,
X11 forwarding and SCP. There are no dependencies on any JCE provider, as all
crypto functionality is included.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{name}-%{name}-build%{version}-jenkins-%{patchlvl}

# compat symlink/alias
%mvn_file  : %{name}/%{name} %{name}
%mvn_alias : "org.tmatesoft.svnkit:trilead-ssh2" "com.trilead:trilead-ssh2"

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc LICENSE.txt HISTORY.txt README.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt


%changelog
* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 217-5.jenkins4
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 217-4.jenkins4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 02 2014 Michal Srb <msrb@redhat.com> - 217-3.jenkins4
- Build version 217 from Jenkins sources

* Mon Jan 06 2014 Michal Srb <msrb@redhat.com> - 217-2
- Remove unneeded files
- Add POM file to sources

* Mon Jan 06 2014 Michal Srb <msrb@redhat.com> - 217-1
- Adapt to current packaging guidelines
- Build with XMvn
- Update to upstream version 217
- Add alias (Resolves: rhbz#1048829)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 215-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 16 2013 Tom Callaway <spot@fedoraproject.org> - 215-1
- update to 215

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 213-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 213-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 213-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 213-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 213-7
- Add maven metadata
- Drop gcj support
- Changes according to new guidelines (no clean section/buildroot)
- Versionless jars & javadocs

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 213-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 30 2009 Robert Marcano <robert@marcanoonline.com> - 213-5
- Fix Bug 492759, bad javadoc package group

* Tue Feb 16 2009 Robert Marcano <robert@marcanoonline.com> - 213-4
- Renaming package because main project moved, based on ganymed-ssh2

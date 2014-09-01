Name:          jsr-311
Version:       1.1.1
Release:       10%{?dist}
Summary:       JAX-RS: Java API for RESTful Web Services
License:       CDDL
URL:           http://jsr311.java.net
# svn export https://svn.java.net/svn/jsr311~svn/tags/jsr311-api-1.1.1 jsr-311-1.1.1
# tar cvzf jsr-311-1.1.1.tgz jsr-311-1.1.1
Source0:       %{name}-%{version}.tgz
# Patch the POM:
Patch0:        %{name}-pom.patch

BuildRequires: java-devel

BuildRequires: buildnumber-maven-plugin
BuildRequires: junit
BuildRequires: maven-local
BuildRequires: maven-plugin-bundle
BuildRequires: maven-source-plugin

BuildArch:     noarch

Provides:      javax.ws.rs

%description
JAX-RS: Java API for RESTful Web Services

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
%patch0

%build

%mvn_file :jsr311-api %{name} javax.ws.rs/%{name}
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/javax.ws.rs/

%files javadoc -f .mfiles-javadoc

%changelog
* Fri Aug 15 2014 Liu Di <liudidi@gmail.com> - 1.1.1-10
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.1.1-8
- Use Requires: java-headless rebuild (#1067528)

* Mon Aug 12 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.1-7
- Add javax.ws.rs provides and directory

* Mon Aug 05 2013 gil cattaneo <puntogil@libero.it> 1.1.1-6
- rebuilt rhbz#992645
- swith to Xmvn
- adapt to new guideline

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.1.1-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 10 2011 Juan Hernandez <juan.hernandez@redhat.com> 1.1.1-1
- Adapted (mostly copied, in fact) from the corresponding package from Mageia
  (http://www.mageia.org) with support from Gil Cattaneo <puntogil@libero.it>.

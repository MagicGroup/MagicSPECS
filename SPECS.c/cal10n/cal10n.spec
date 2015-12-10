Name:           cal10n
Version:        0.7.7
Release:        8%{?dist}
Summary:        Compiler assisted localization library (CAL10N)
License:        MIT
URL:            http://cal10n.qos.ch
Source0:        http://cal10n.qos.ch/dist/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.maven.plugins:maven-site-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-artifact-manager)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)

%description
Compiler Assisted Localization, abbreviated as CAL10N (pronounced as "calion") 
is a java library for writing localized (internationalized) messages.
Features:
    * java compiler verifies message keys used in source code
    * tooling to detect errors in message keys
    * native2ascii tool made superfluous, as you can directly encode bundles 
      in the most convenient charset, per locale.
    * good performance (300 nanoseconds per key look-up)
    * automatic reloading of resource bundles upon change


%package javadoc
Summary:        API documentation for %{name}

%description javadoc
%{summary}.

%package -n maven-%{name}-plugin
Summary:        CAL10N maven plugin

%description -n maven-%{name}-plugin
Maven plugin verifying that the codes defined in
an enum type match those in the corresponding resource bundles. 

%prep
%setup -q 
find . -name \*.jar -delete
%pom_xpath_remove pom:extensions
%pom_add_dep org.apache.maven:maven-artifact maven-%{name}-plugin
%pom_disable_module %{name}-site
%pom_disable_module maven-%{name}-plugin-smoke
%mvn_package :*-{plugin} @1

%build
%mvn_build -- -Dproject.build.sourceEncoding=ISO-8859-1

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc LICENSE.txt

%files -n maven-%{name}-plugin -f .mfiles-plugin

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 0.7.7-8
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.7.7-7
- 为 Magic 3.0 重建

* Wed Aug 13 2014 Liu Di <liudidi@gmail.com> - 0.7.7-6
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.7-4
- Remove wagon-ssh build extension

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.7-4
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.7-2
- Simplify BuildRequires
- Convert patch to POM macro
- Update to current packaging guidelines

* Wed Mar 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.7-1
- Update to upstream version 0.7.7

* Fri Mar 15 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.6-1
- Update to upstream version 0.7.6

* Wed Feb 27 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.5-1
- Update to upstream version 0.7.5
- A maintenance release containing only minor fixes

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0.7.4-11
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Aug 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.4-10
- Install LICENSE file
- Remove rpm bug workaround

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 28 2012 Alexander Kurtakov <akurtako@redhat.com> 0.7.4-8
- Fix for OpenJDK 7 build.
- Adapt to current guidelines.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 8 2011 Alexander Kurtakov <akurtako@redhat.com> 0.7.4-6
- Build with maven 3.x.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 25 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.4-4
- Fix pom filenames (Resolves rhbz#655792)
- Add several packages to Requires
- Remove versioned jars and javadocs

* Wed Sep 8 2010 Alexander Kurtakov <akurtako@redhat.com> 0.7.4-3
- Fix build failure (javadoc:aggregate).

* Mon Jul 19 2010 Alexander Kurtakov <akurtako@redhat.com> 0.7.4-2
- BR maven-site-plugin.

* Mon Jul 19 2010 Alexander Kurtakov <akurtako@redhat.com> 0.7.4-1
- Update to 0.7.4.

* Wed Feb 3 2010 Alexander Kurtakov <akurtako@redhat.com> 0.7.2-2
- Removed not needed external repo definitions.
- Use _mavenpomdir.

* Wed Feb 3 2010 Alexander Kurtakov <akurtako@redhat.com> 0.7.2-1
- Initial package

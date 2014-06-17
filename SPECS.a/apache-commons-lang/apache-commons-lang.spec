
%global base_name       lang
%global short_name      commons-%{base_name}

Name:           apache-%{short_name}
Version:        2.6
Release:        16%{?dist}
Summary:        Provides a host of helper utilities for the java.lang API
License:        ASL 2.0
Group:          Development/Libraries
URL:            http://commons.apache.org/%{base_name}
Source0:        http://archive.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Patch1:         0002-Fix-FastDateFormat-for-Java-7-behaviour.patch

BuildArch:      noarch
BuildRequires:  maven-local
BuildRequires:  apache-commons-parent
BuildRequires:  maven-surefire-provider-junit

%description
The standard Java libraries fail to provide enough methods for
manipulation of its core classes. The Commons Lang Component provides
these extra methods.
The Commons Lang Component provides a host of helper utilities for the
java.lang API, notably String manipulation methods, basic numerical
methods, object reflection, creation and serialization, and System
properties. Additionally it contains an inheritable enum type, an
exception structure that supports multiple types of nested-Exceptions
and a series of utilities dedicated to help with building methods, such
as hashCode, toString and equals.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Documentation

%description    javadoc
%{summary}.

%prep
%setup -q -n %{short_name}-%{version}-src
%patch1 -p1
sed -i 's/\r//' *.txt *.html

# "enum" is used as a Java identifier, which is prohibited in Java >= 1.5
%pom_add_plugin org.apache.maven.plugins:maven-javadoc-plugin . "
    <configuration><source>1.3</source></configuration>"


%mvn_file  : %{name} %{short_name}
%mvn_alias : org.apache.commons: %{base_name}:%{base_name}
# this package needs to be compiled with -source 1.3 option
%mvn_config buildSettings/compilerSource 1.3

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc PROPOSAL.html LICENSE.txt RELEASE-NOTES.txt NOTICE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 2.6-16
- 为 Magic 3.0 重建

* Thu May 29 2014 Alexander Kurtakov <akurtako@redhat.com> 2.6-15
- Drop old jakarta provides/obsoletes.

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.6-14
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 22 2013 Michal Srb <msrb@redhat.com> - 2.6-12
- Rebuild

* Tue Apr 09 2013 Michal Srb <msrb@redhat.com> - 2.6-11
- Properly specify XMvn's compilerSource option

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.6-9
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Jan 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.6-8
- Build with xmvn

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 22 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.6-6
- Add backported fix for JDK 1.7

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 27 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.6-4
- Use new add_maven_depmap macro
- Fix maven3 build

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.6-2
- Fix commons-lang symlink

* Tue Jan 18 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.6-1
- Update to 2.6
- Versionless jars & javadocs
- Use maven 3 to build

* Wed Nov 10 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.5-7
- Use apache-commons-parent instead of maven-*

* Thu Jul  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.5-6
- Add license to javadoc subpackage

* Wed May 26 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.5-5
- Add another old depmap to prevent groupId dependency problems

* Fri May 21 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.5-4
- Correct depmap filename for backward compatibility

* Mon May 17 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.5-3
- Fix maven depmap JPP name to short_name

* Mon May 10 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.5-2
- Added export for MAVEN_LOCAL_REPO and mkdir
- Added more add_to_maven_depmap to assure backward compatibility
- Add symlink to short_name.jar

* Mon May 10 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.5-1
- Rename and rebase of jakarta-commons-lang
- Re-did whole spec file to use maven, dropped gcj support

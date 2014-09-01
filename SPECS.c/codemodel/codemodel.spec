Name:         codemodel
Version:      2.6
Release:      16%{?dist}
Summary:      Java library for code generators
License:      CDDL and GPLv2
URL:          http://codemodel.java.net
# svn export https://svn.java.net/svn/codemodel~svn/tags/codemodel-project-2.6/ codemodel-2.6
# tar -zcvf codemodel-2.6.tar.gz codemodel-2.6
Source0:      %{name}-%{version}.tar.gz
# Remove the dependency on istack-commons (otherwise it will be a
# recursive dependency with the upcoming changes to that package):
Patch0:       %{name}-remove-istack-commons-dependency.patch

BuildArch:     noarch

BuildRequires: maven-local
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-release-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: mvn(net.java:jvnet-parent:pom:)
BuildRequires: mvn(org.apache.ant:ant)
BuildRequires: mvn(junit:junit)


%description
CodeModel is a Java library for code generators; it provides a way to
generate Java programs in a way much nicer than PrintStream.println().
This project is a spin-off from the JAXB RI for its schema compiler
to generate Java source files.

%package javadoc
Summary: Javadocs for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep

# Unpack and patch the original source:
%setup -q
%patch0 -p1

# Remove bundled jar files:
find . -name '*.jar' -print -delete

%build

%mvn_file :%{name} %{name}
%mvn_file :%{name}-annotation-compiler %{name}-annotation-compiler
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.html

%files javadoc -f .mfiles-javadoc
%doc LICENSE.html

%changelog
* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 2.6-16
- 为 Magic 3.0 重建

* Tue Jun 24 2014 Michael Simacek <msimacek@redhat.com> - 2.6-15
- Chnage jvnet-parent BR to jvnet-parent:pom

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Michael Simacek <msimacek@redhat.com> - 2.6-13
- Change maven-surefire-provider-junit4 dependency to
  maven-surefire-provider-junit

* Thu Mar 20 2014 Michael Simacek <msimacek@redhat.com> - 2.6-12
- Remove BR java-devel

* Thu Mar 13 2014 Michael Simacek <msimacek@redhat.com> - 2.6-11
- Drop manual requires

* Mon Aug 05 2013 gil cattaneo <puntogil@libero.it> 2.6-10
- rebuilt FTBFS in rawhide
- swith to Xmvn
- adapt to new guideline

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.6-7
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Jul 21 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.6-6
- Add maven-enforcer-plugin as build time dependeny

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 31 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.6-4
- Restore the dependency on jvnet-parent
- Remove the dependency on istack-commons

* Tue Feb 14 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.6-3
- Added build requirement for maven-surefire-provider-junit4

* Tue Feb 14 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.6-2
- Cleanup of the spec file

* Mon Jan 16 2012 Marek Goldmann <mgoldman@redhat.com> 2.6-1
- Initial packaging


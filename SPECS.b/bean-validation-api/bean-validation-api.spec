%global namedreltag .Final
%global namedversion %{version}%{?namedreltag}

Name:             bean-validation-api
Version:          1.1.0
Release:          3%{dist}
Summary:          Bean Validation API (JSR 349)
License:          ASL 2.0
URL:              http://beanvalidation.org/
Source0:          https://github.com/beanvalidation/beanvalidation-api/archive/%{namedversion}.tar.gz

BuildRequires:    java-devel

# test deps
BuildRequires:    mvn(org.testng:testng)

BuildRequires:    maven-local
BuildRequires:    maven-plugin-bundle
BuildRequires:    maven-surefire-provider-testng

BuildArch:        noarch

%description
This package contains Bean Validation (JSR-349) API.

%package javadoc
Summary:          Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n beanvalidation-api-%{namedversion}

# Disable javadoc jar
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-javadoc-plugin']/pom:executions"
# Disable source jar
%pom_remove_plugin :maven-source-plugin

%build

%mvn_file : %{name}
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc license.txt

%files javadoc -f .mfiles-javadoc
%doc license.txt

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.1.0-2
- Use Requires: java-headless rebuild (#1067528)

* Wed Jul 24 2013 gil cattaneo <puntogil@libero.it> 1.1.0-1
- update to 1.1.0.Final
- adapt to current guideline
- resolve rpmlint warning

* Thu Feb 14 2013 Marek Goldmann <mgoldman@redhat.com> - 1.0.0-8
- Fixed build issue

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0.0-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 09 2012 Marek Goldmann <mgoldman@redhat.com> 1.0.0-4
- Relocated jars to _javadir

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 29 2011 Marek Goldmann <mgoldman@redhat.com> 1.0.0-2
- Added license file to distribution

* Tue Aug 16 2011 Marek Goldmann <mgoldman@redhat.com> 1.0.0-1
- Initial packaging


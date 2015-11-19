%global short_name      taglibs-standard

Name:           tomcat-taglibs-standard
Version:        1.2.5
Release:        1%{?dist}
Epoch:          0
Summary:        Apache Standard Taglib
License:        ASL 2.0
URL:            http://tomcat.apache.org/taglibs/
Source0:        http://apache.cbox.biz/tomcat/taglibs/taglibs-standard-%{version}/taglibs-standard-%{version}-source-release.zip
Patch0: servlet31.patch

BuildArch:      noarch
BuildRequires:  maven-local
BuildRequires:  mvn(javax.el:el-api)
BuildRequires:  mvn(javax.servlet.jsp:jsp-api)
BuildRequires:  mvn(javax.servlet:servlet-api)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-checkstyle-plugin)
BuildRequires:  mvn(org.apache.taglibs:taglibs-parent:pom:)
BuildRequires:  mvn(org.easymock:easymock)
BuildRequires:  mvn(xalan:xalan)

Obsoletes: jakarta-taglibs-standard < 1.1.2-13

%description
An implementation of the JSP Standard Tag Library (JSTL).

%package        javadoc
Summary:        Javadoc for %{name}
Obsoletes: jakarta-taglibs-standard-javadoc < 1.1.2-13

%description    javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{short_name}-%{version}
%patch0 -b .sav
%mvn_alias org.apache.taglibs:taglibs-standard-impl javax.servlet:jstl
%mvn_alias org.apache.taglibs:taglibs-standard-impl org.eclipse.jetty.orbit:javax.servlet.jsp.jstl
%mvn_alias org.apache.taglibs:taglibs-standard-compat org.eclipse.jetty.orbit:org.apache.taglibs.standard.glassfish

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE
%doc README_src.txt README_bin.txt NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE
%doc NOTICE

%changelog
* Thu Jun 18 2015 Alexander Kurtakov <akurtako@redhat.com> 0:1.2.5-1
- Update to upstream 1.2.5

* Thu Mar 5 2015 Alexander Kurtakov <akurtako@redhat.com> 0:1.2.3-2
- Fix url.

* Wed Mar 4 2015 Alexander Kurtakov <akurtako@redhat.com> 0:1.2.3-1
- Initial package.

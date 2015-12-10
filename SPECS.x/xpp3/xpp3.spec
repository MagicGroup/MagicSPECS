%define oversion 1.1.4c

Summary:        XML Pull Parser
Summary(zh_CN.UTF-8): XML 解析器
Name:           xpp3
Version:        1.1.4
Release:        6.c%{?dist}
License:        ASL 1.1
URL:            http://www.extreme.indiana.edu/xgws/xsoap/xpp/mxp1/index.html
Source0:        http://www.extreme.indiana.edu/dist/java-repository/xpp3/distributions/xpp3-%{oversion}_src.tgz
Source1:        http://repo1.maven.org/maven2/xpp3/xpp3/%{oversion}/xpp3-%{oversion}.pom
Source2:        http://repo1.maven.org/maven2/xpp3/xpp3_xpath/%{oversion}/xpp3_xpath-%{oversion}.pom
Source3:        http://repo1.maven.org/maven2/xpp3/xpp3_min/%{oversion}/xpp3_min-%{oversion}.pom
Patch0:         %{name}-link-docs-locally.patch
Requires:       java-headless
BuildRequires:  javapackages-tools
BuildRequires:  ant
BuildRequires:  junit
BuildRequires:  xml-commons-apis
Requires:       junit
Requires:       xml-commons-apis
Requires:       java-headless

BuildArch:      noarch

%description
XML Pull Parser 3rd Edition (XPP3) MXP1 is an XmlPull
parsing engine that is based on ideas from XPP and in
particular XPP2 but completely revised and rewritten to
take best advantage of latest JIT JVMs such as Hotspot in JDK 1.4.

%description -l zh_CN.UTF-8
XML 解析器。

%package minimal
Summary:        Minimal XML Pull Parser
Summary(zh_CN.UTF-8): 迷你版本的 XML 解析器
Requires:       junit
Requires:       xml-commons-apis
Requires:       java-headless

%description minimal
Minimal XML pull parser implementation.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{oversion}
# remove all binary libs
find -name \*.jar -delete

%patch0

# "src/java/addons_tests" does not exist
sed -i 's|depends="junit_main,junit_addons"|depends="junit_main"|' build.xml

%build
export CLASSPATH=$(build-classpath xml-commons-apis junit)
ant xpp3 junit apidoc

%install
install -d -m 755 %{buildroot}%{_javadir}
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}

# JARs
install -p -m 644 build/%{name}-%{oversion}.jar \
    %{buildroot}%{_javadir}/%{name}.jar
install -p -m 644 build/%{name}_xpath-%{oversion}.jar \
    %{buildroot}%{_javadir}/%{name}-xpath.jar
install -p -m 644 build/%{name}_min-%{oversion}.jar \
    %{buildroot}%{_javadir}/%{name}-minimal.jar

# POMs
install -p -m 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
install -p -m 644 %{SOURCE2} %{buildroot}%{_mavenpomdir}/JPP-%{name}-xpath.pom
install -p -m 644 %{SOURCE3} %{buildroot}%{_mavenpomdir}/JPP-%{name}-minimal.pom

# XMvn metadata
%add_maven_depmap
%add_maven_depmap JPP-%{name}-xpath.pom %{name}-xpath.jar
%add_maven_depmap JPP-%{name}-minimal.pom %{name}-minimal.jar -f minimal

# Javadocs
cp -pr doc/api/* %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%doc README.html LICENSE.txt doc/*

%files minimal -f .mfiles-minimal
%doc LICENSE.txt

%files javadoc
%doc %{_javadocdir}/%{name}

%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 1.1.4-6.c
- 为 Magic 3.0 重建

* Tue Oct 27 2015 Liu Di <liudidi@gmail.com> - 1.1.4-5.c
- 为 Magic 3.0 重建

* Wed Aug 13 2014 Liu Di <liudidi@gmail.com> - 1.1.4-4.c
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-3.c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.4-2.c
- Use Requires: java-headless rebuild (#1067528)

* Wed Feb 19 2014 Michal Srb <msrb@redhat.com> - 1.1.4-1.c
- Update to upstream version 1.1.4c

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.3.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.3.8-9
- General specfile cleanup
- Update to current packaging guidelines

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.3.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.3.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.3.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.3.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  2 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.1.3.8-4
- Fix pom filenames (Resolves rhbz#655829)
- Changes according to new guidelines (versionless jars)
- Fix few packaging problems (post/postun deps)

* Mon Jun 14 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.1.3.8-3.4
- Add maven poms and depmaps.

* Wed Mar 10 2010 Peter Lemenkov <lemenkov@gmail.com> - 0:1.1.3.8-3.3
- *-javadoc must also require jpackage-utils (for %%{_javadocdir})

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.3.8-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.3.8-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Sep  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.1.3.8-1.2
- fix license tag
- drop jpp tag

* Mon Feb 12 2007 Fernando Nasser <fnasser@redhat.com> - 0:1.1.3.8-1jpp.1
- Import
- Fix per Fedora spec

* Mon Feb 12 2007 Fernando Nasser <fnasser@redhat.com> - 0:1.1.3.8-1jpp
- Upgrade to 1.1.3.8
- Remove vendor and distribution tags

* Mon Feb 27 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.1.3.4-1.o.2jpp
- First JPP 1.7 build

* Tue Dec 20 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.1.3.4-1.o.1jpp
- Upgrade to 1.1.3.4-O
- Now includes xpath support

* Thu Aug 26 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.1.3.4-1.d.2jpp
- Build with ant-1.6.2

* Tue Jun 01 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.1.3.4-1.d.1jpp
- Update to 1.1.3.4

* Mon May  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.1.2-1.a.3jpp
- Fix non-versioned javadoc symlinking.

* Mon Apr 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.1.2-1.a.2jpp
- Include non-versioned javadoc symlink.

* Tue Apr  1 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.1.2-1.a.1jpp
- First JPackage release.

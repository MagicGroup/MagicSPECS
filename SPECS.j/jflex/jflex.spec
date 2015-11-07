Summary:        Fast Scanner Generator
Summary(zh_CN.UTF-8): 快速扫描器生成器
Name:           jflex
Version:        1.6.1
Release:        4%{?dist}
License:        BSD
URL:            http://jflex.de/
BuildArch:      noarch

# ./create-tarball.sh %%{version}
Source0:        %{name}-%{version}-clean.tar.gz
Source2:        %{name}.desktop
Source3:        %{name}.png
Source4:        %{name}.1
Source5:        create-tarball.sh

BuildRequires:  maven-local
BuildRequires:  ant
BuildRequires:  emacs
BuildRequires:  jflex
BuildRequires:  junit
BuildRequires:  java-devel
BuildRequires:  java_cup
BuildRequires:  desktop-file-utils
Requires:       emacs-filesystem >= %{_emacs_version}

%description
JFlex is a lexical analyzer generator (also known as scanner
generator) for Java, written in Java.  It is also a rewrite of the
very useful tool JLex which was developed by Elliot Berk at Princeton
University.  As Vern Paxson states for his C/C++ tool flex: They do
not share any code though.  JFlex is designed to work together with
the LALR parser generator CUP by Scott Hudson, and the Java
modification of Berkeley Yacc BYacc/J by Bob Jamison.  It can also be
used together with other parser generators like ANTLR or as a
standalone tool.

%description -l zh_CN.UTF-8
快速扫描器生成器。

%package javadoc
Summary:        API documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的 API 文档

%description javadoc
This package provides %{summary}.

%description javadoc -l zh_CN.UTF-8
%{name} 的 API 文档。

%prep
%setup -q
%mvn_file : %{name}
%pom_add_dep java_cup:java_cup

%pom_remove_plugin :maven-antrun-plugin
%pom_remove_plugin :jflex-maven-plugin

# Tests fail with 320k stacks (default on i686), so lets increase
# stack to 16M to avoid stack overflows.  See rhbz#1119308
%pom_xpath_inject "pom:plugin[pom:artifactId='maven-surefire-plugin']/pom:configuration" "<argLine>-Xss16384k</argLine>"

%build
java -jar /usr/share/java/java_cup.jar -parser LexParse -interface -destdir src/main/java src/main/cup/LexParse.cup
jflex -d src/main/java/jflex --skel src/main/jflex/skeleton.nested src/main/jflex/LexScan.flex
%mvn_build

# Compile Emacs jflex-mode source
%{_emacs_bytecompile} lib/jflex-mode.el

%install
%mvn_install

install -d -m 755 %{buildroot}%{_mandir}/man1
install -d -m 755 %{buildroot}%{_emacs_sitelispdir}/%{name}
install -d -m 755 %{buildroot}%{_datadir}/pixmaps

# wrapper script for direct execution
%jpackage_script jflex.Main "" "" jflex:java_cup jflex true

# manpage
install -p -m 644 %{SOURCE4} %{buildroot}%{_mandir}/man1

# .desktop + icons
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE2}
install -p -m 644 %{SOURCE3} %{buildroot}%{_datadir}/pixmaps/%{name}.png

# Emacs files
install -p -m 644 lib/jflex-mode.el %{buildroot}%{_emacs_sitelispdir}/%{name}
install -p -m 644 lib/jflex-mode.elc %{buildroot}%{_emacs_sitelispdir}/%{name}
magic_rpm_clean.sh

%files -f .mfiles
%doc doc
%doc COPYRIGHT
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_emacs_sitelispdir}/%{name}

%files javadoc
%doc COPYRIGHT
%doc %{_javadocdir}/%{name}


%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.6.1-4
- 为 Magic 3.0 重建

* Fri Jul 24 2015 Liu Di <liudidi@gmail.com> - 1.6.1-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 17 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6.1-1
- Update to upstream version 1.6.1

* Tue Jul  8 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6.0-1
- Update to upstream version 1.6.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.1-1
- Update to upstream version 1.5.1

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.0-3
- Use Requires: java-headless rebuild (#1067528)

* Tue Jan 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.0-2
- Fix license tag

* Mon Jan 27 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5.0-1
- Update to upstream version 1.5.0
- Build with Maven

* Fri Aug 02 2013 Michal Srb <msrb@redhat.com> - 0:1.4.3-16
- Add create-tarball.sh script to SRPM

* Thu Jun 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4.3-15
- Fix javadoc generation
- Update to current packaging guidelines

* Thu Jun 20 2013 Michal Srb <msrb@redhat.com> - 0:1.4.3-14
- Build from clean tarball
- Install license file with javadoc package

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 22 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4.3-12
- Install Emacs jflex-mode

* Thu Nov 22 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4.3-11
- Remove bundled java_cup sources
- Resolves: rhbz#877051

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May  2 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4.3-9
- Fix license tag
- Import manpage from Debian's jflex 1.4.1-3 (GPL+)

* Thu Apr 19 2012 Jaromir Capik <jcapik@redhat.com> - 0:1.4.3-8
- Desktop file generated
- Icon created from the GPL licensed logo

* Mon Mar 12 2012 Jaromir Capik <jcapik@redhat.com> - 0:1.4.3-7
- Wrapper script generated
- Minor spec file changes according to the latest guidelines

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 15 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4.3-4
- Add dependency on java_cup in the maven pom.xml.

* Mon Feb 15 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4.3-3
- Require java_cup.

* Wed Jan 20 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4.3-3
- Provide JFlex.jar.
- Don't put java_cup classes in the jar.

* Fri Jan 8 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4.3-2
- Add maven pom and depmaps.

* Fri Jan 8 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4.3-1
- Update to 1.4.3.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.1-0.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.1-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.4.1-0.3
- drop repotag

* Mon Mar 03 2008 Matt Wringe <mwringe@redhat.com> - 0:1.4.1-0jpp.2
- Add missing buildrequires on java_cup

* Fri Feb 22 2008 Matt Wringe <mwringe@redhat.com> - 0:1.4.1-0jpp.1
- Patch build file to allow bootstrap building

* Mon Feb 18 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0:1.4.1-0jpp.1
- Naive attempt to update to newer version

* Mon Apr 02 2007 Matt Wringe <mwringe@redhat.com> - 0:1.3.5-2jpp.2
- Add patches jflex-CharSet_java.patch and jflex-StateSet_java.patch
  to allow building with the new gcj

* Mon Feb 12 2007 Matt Wringe <mwringe@redhat.com> - 0:1.3.5-2jpp.1
- Remove javadoc post and postun sections due to new jpp standard 
- Update makefile patch to compress jar
- Fix rpmlint issues

* Wed Jan 04 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.3.5-2jpp
- First JPP 1.7 build

* Wed Nov 16 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.3.5-1jpp
- First JPackage release

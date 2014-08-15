
%global base_name       el
%global short_name      commons-%{base_name}


Name:           apache-%{short_name}
Version:        1.0
Release:        31%{?dist}
Summary:        The Apache Commons Extension Language
License:        ASL 1.1
URL:            http://commons.apache.org/%{base_name}
BuildArch:      noarch
Source0:        http://archive.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Source1:        http://repo1.maven.org/maven2/%{short_name}/%{short_name}/%{version}/%{short_name}-%{version}.pom
Patch0:         %{short_name}-%{version}-license.patch
Patch1:         %{short_name}-eclipse-manifest.patch
Patch2:         %{short_name}-enum.patch
BuildRequires:  ant
BuildRequires:  tomcat-jsp-2.2-api
BuildRequires:  tomcat-servlet-3.0-api
BuildRequires:  junit

%description
An implementation of standard interfaces and abstract classes for
javax.servlet.jsp.el which is part of the JSP 2.0 specification.

%package        javadoc
Summary:        API documentation for %{name}

Provides:       jakarta-%{short_name}-javadoc = 0:%{version}-%{release}
Obsoletes:      jakarta-%{short_name}-javadoc < 0:%{version}-%{release}


%description    javadoc
%{summary}.


%prep
%setup -q -n %{short_name}-%{version}-src
%patch0 -p1 -b .license
%patch1 -p1
%patch2 -p1

# remove all precompiled stuff
find . -type f -name "*.jar" -exec rm -f {} \;

cat > build.properties <<EOBP
build.compiler=modern
junit.jar=$(build-classpath junit)
servlet-api.jar=$(build-classpath tomcat-servlet-3.0-api)
jsp-api.jar=$(build-classpath tomcat-jsp-2.2-api)
servletapi.build.notrequired=true
jspapi.build.notrequired=true
EOBP

# workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1015612
find . -iname 'ELParser.java' -exec sed -i 's:enum:enum1:g' \{\} \;

%build
export CLASSPATH=
export OPT_JAR_LIST=:
%{ant} \
  -Dfinal.name=%{short_name} \
  -Dj2se.javadoc=%{_javadocdir}/java \
  jar javadoc


%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -p -m 644 dist/%{short_name}.jar %{buildroot}%{_javadir}/%{name}.jar
ln -sf %{name}.jar %{buildroot}%{_javadir}/%{short_name}.jar

# pom
install -pD -T -m 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{short_name}.pom
%add_maven_depmap JPP-%{short_name}.pom %{short_name}.jar -a "org.apache.commons:commons-el"

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%doc LICENSE.txt STATUS.html
%{_javadir}/%{name}.jar
%{_javadir}/%{short_name}.jar
%{_mavenpomdir}/JPP-%{short_name}.pom

%files javadoc
%doc LICENSE.txt
%{_javadocdir}/%{name}


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-30
- Use .mfiles generated during build

* Tue Oct 08 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-29
- Remove versioned symlinks
- Add workaround for rhbz#1015612

* Mon Aug 05 2013 Michal Srb <msrb@redhat.com> - 1.0-28
- Switch to %%add_maven_depmap (Resolves: #991969)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 7 2012 Alexander Kurtakov <akurtako@redhat.com> 1.0-25
- Adapt to current guidelines.
- Build against tomcat 7.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-21
- Add license to javadoc subpackage

* Tue May 25 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-20
- Use tomcat6-jsp and tomcat6-servlet APIs

* Mon May 24 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-19
- Renamed package (jakarta-commons-el->apache-commons-el)
- Dropped epoch, cleanup spec

* Thu Sep 09 2009 Fernando Nasser <fnasser@redhat.com> - 0:1.0-18.1
- Merge with upstream for:
  Add pom and depmap fragment
  Removal of ghost symlink
  Some spec file cleanups
- Build without AOT compilation

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-11.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 08 2009 David Walluck <dwalluck@redhat.com> 0:1.0-18
- fix scriptlets

* Wed Jul 08 2009 David Walluck <dwalluck@redhat.com> 0:1.0-17
- fix pom install

* Wed Jul 08 2009 David Walluck <dwalluck@redhat.com> 0:1.0-16
- add pom

* Mon Apr 27 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 0:1.0-10.5
- Fix FTBFS: added BR: tomcat5-jsp-2.0-api (resolves BZ#497179).

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 David Walluck <dwalluck@redhat.com> 0:1.0-15
- fix component-info.xml

* Wed Jan 21 2009 David Walluck <dwalluck@redhat.com> 0:1.0-14
- fix jar name in repolib

* Tue Jan 20 2009 David Walluck <dwalluck@redhat.com> 0:1.0-13
- fix repolib location

* Tue Jan 20 2009 David Walluck <dwalluck@redhat.com> 0:1.0-12
- add repolib

* Wed Aug 13 2008 David Walluck <dwalluck@redhat.com> 0:1.0-11
- update header

* Wed Aug 13 2008 David Walluck <dwalluck@redhat.com> 0:1.0-10
- build for JPackage 5

* Mon Jul 14 2008 Andrew Overholt <overholt@redhat.com> 0:1.0-9.4
- Update OSGi metadata for Eclipse 3.4.

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.0-9.3
- drop repotag
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.0-9jpp.2
- Autorebuild for GCC 4.3

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.0-8jpp.2
- Rebuild for selinux ppc32 issue.

* Wed Jul 11 2007 Ben Konrath <bkonrath@redhat.com> - 0:1.0-8jpp.1
- Add eclipse-manifest patch.
  From Fernando Nasser <fnasser@redhat.com>:
- Specify source 1.4 due to use of enum as identifier

* Fri Feb 09 2007 Fernando Nasser <fnasser@redhat.com> - 0:1.0-7jpp.1
- Remove duplicate name tag
- Rebuild

* Thu Aug 17 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0-7jpp.1
- Merge with upstream

* Thu Aug 17 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0-7jpp
- Fix AOT support

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:1.0-5jpp_4fc
- Rebuilt

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:1.0-5jpp_3fc
- rebuild

* Fri May 19 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0-5jpp_2fc
- Build with gcj_support enabled
- Add missing BR for jsp (API)

* Fri May 19 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0-6jpp
- Add AOT support

* Fri May 19 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0-5jpp_1fc
- First build for FC6

* Fri May 19 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0-5jpp_0fc
- Add gcj_support

* Wed Apr 26 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0-5jpp
- First JPP 1.7 build

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 0:1.0-4jpp_6fc
- stop scriptlet spew

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0:1.0-4jpp_5fc
- bump again for double-long bug on ppc(64)

* Wed Dec 21 2005 Jesse Keating <jkeating@redhat.com> - 0:1.0-4jpp_4fc
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> - 0:1.0-4jpp_3fc
- rebuilt

* Tue Jul 19 2005 Gary Benson <gbenson at redhat.com> - 0:1.0-4jpp_2fc
- Build on ia64, ppc64, s390 and s390x.
- Switch to aot-compile-rpm.

* Thu Jun 14 2005 Gary Benson <gbenson at redhat.com> - 0:1.0-4jpp_1fc
- Upgrade to 1.0-4jpp.

* Thu May 26 2005 Gary Benson <gbenson at redhat.com> - 0:1.0-4jpp
- Don't bundle servletapi sources (which weren't used anyway).

* Thu May 26 2005 Gary Benson <gbenson@redhat.com> - 0:1.0-3jpp_1fc
- Upgrade to 1.0-3jpp.
- Rearrange how BC-compiled stuff is built and installed.
- Don't bundle servletapi sources (which weren't used anyway).

* Mon May 23 2005 Gary Benson <gbenson@redhat.com> - 0:1.0-2jpp_3fc
- Add alpha to the list of build architectures (#157522).
- Use absolute paths for rebuild-gcj-db.

* Thu May  5 2005 Gary Benson <gbenson@redhat.com> - 0:1.0-2jpp_2fc
- BC-compile.

* Thu Jan 20 2005 Gary Benson <gbenson@redhat.com> - 0:1.0-2jpp_1fc
- Build into Fedora.

* Thu Oct 21 2004 Fernando Nasser <fnasser@redhat.com> - 0:1.0-2jpp_2rh
- Rebuild (no changes)

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:1.0-3jpp
- Rebuild with ant-1.6.2

* Wed Jul 14 2004 Fernando Nasser <fnasser@redhat.com> - 0:1.0-2jpp_1rh
- Merge with upstream version that removes dependency on ant-optional

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:1.0-2jpp
- Upgrade to Ant 1.6.X

* Fri Jan  9 2004 Kaj J. Niemi <kajtzu@fi.basen.net> - 0:1.0-1jpp
- First build for JPackage

* Wed Dec 17 2003 Kaj J. Niemi <kajtzu@fi.basen.net> - 0:1.0-0.2
- With Javadocs

* Wed Dec 17 2003 Kaj J. Niemi <kajtzu@fi.basen.net> - 0:1.0-0.1
- First build

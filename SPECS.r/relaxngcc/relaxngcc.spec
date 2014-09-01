Name: relaxngcc
Version: 1.12
Release: 7%{?dist}
Summary: RELAX NG Compiler Compiler
Group: Development/Libraries

License: ASL 1.1

Url: http://relaxngcc.sourceforge.net/en/index.htm

Source0: http://prdownloads.sourceforge.net/relaxngcc/relaxngcc-20031218.zip
Source1: %{name}-build.xml

BuildRequires: ant
BuildRequires: javacc
BuildRequires: jpackage-utils
BuildRequires: msv-msv
BuildRequires: msv-xsdlib
BuildRequires: relaxngDatatype
BuildRequires: xerces-j2
BuildRequires: xml-commons-apis
BuildRequires: dos2unix

Requires: msv-msv
Requires: msv-xsdlib
Requires: relaxngDatatype
Requires: xerces-j2
Requires: xml-commons-apis

BuildArch: noarch


%description
RelaxNGCC is a tool for generating Java source code from a given RELAX NG
grammar. By embedding code fragments in the grammar like yacc or JavaCC, you can
take appropriate actions while parsing valid XML documents against the grammar.


%package javadoc
Group: Development/Libraries
Summary: Javadoc for %{name}
Requires: jpackage-utils


%description javadoc
This package contains javadoc for %{name}.


%prep

# Prepare the original sources:
%setup -q -n relaxngcc-20031218

# Remove all the binary files:
find . -name '*.class' -delete
find . -name '*.jar' -delete

# Remove the sources that will be generated with JavaCC:
rm src/relaxngcc/javabody/*.java

# Remove to avoid dependency on commons-jelly:
rm src/relaxngcc/maven/ChildAntProjectTag.java

# Some of the sources don't use the correct end of line encoding, so to be
# conservative fix all of them:
find . -type f -exec dos2unix {} \;

# Some of the source files contain characters outside of the ASCII set that
# cause problems when compiling, so make sure that they are translated to
# ASCCI:
sources='
src/relaxngcc/builder/SwitchBlockInfo.java
'
for source in ${sources}
do
  native2ascii -encoding UTF8 ${source} ${source}
done


%build

# Populate the lib directory with references to the jar files required for the
# build:
mkdir lib
pushd lib
  ln -sf $(build-classpath msv-msv) .
  ln -sf $(build-classpath relaxngDatatype) .
  ln -sf $(build-classpath xerces-j2) .
  ln -sf $(build-classpath msv-xsdlib) .
  ln -sf $(build-classpath javacc) .
popd

# Put the ant build files in place:
cp %{SOURCE1} build.xml

# Run the ant build:
ant jar javadoc


%install

# Jar files:
mkdir -p %{buildroot}%{_javadir}
install -pm 644 relaxngcc.jar %{buildroot}%{_javadir}/%{name}.jar

# Javadoc files:
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr javadoc/* %{buildroot}%{_javadocdir}/%{name}/.


%files
%{_javadir}/*
%doc src/HOWTO-readAutomata.txt LICENSE.txt readme.txt
%doc doc/*


%files javadoc
%{_javadocdir}/*
%doc LICENSE.txt

%changelog
* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 1.12-7
- 为 Magic 3.0 重建

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 14 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.12-3
- Changed license to ASL 1.1

* Tue Feb 14 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.12-2
- Cleanups of the spec file

* Sat Jan 21 2012 Marek Goldmann <mgoldman@redhat.com> 1.12-1
- Initial packaging

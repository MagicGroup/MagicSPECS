Name:           sinjdoc
Version:        0.5
Release:        13%{?dist}
Summary:        Documentation generator for Java source code

Group:          Development/Tools
# No version given.
License:        GPL+
URL:            http://cscott.net/Projects/GJ/sinjdoc-latest/
Source0:        http://cscott.net/Projects/GJ/sinjdoc-latest/sinjdoc-0.5.tar.gz
Patch0:         sinjdoc-annotations.patch
Patch1:         sinjdoc-autotools-changes.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: eclipse-ecj >= 3.2.1
BuildRequires: gcc-java >= 4.0.2
BuildRequires: java-gcj-compat-devel >= 1.0.70
BuildRequires: java_cup >= 0.10

Requires:         java_cup >= 0.10
Requires:         libgcj >= 4.1.2
Requires(post):   java-gcj-compat >= 1.0.70
Requires(postun): java-gcj-compat >= 1.0.70

Obsoletes: gjdoc <= 0.7.7-14.fc7

%description
This package contains Sinjdoc a tool for generating Javadoc-style
documentation from Java source code

%prep
%setup -q
%patch0 -p0
%patch1 -p0

%build
aclocal
automake
autoconf
%configure
make %{?_smp_mflags}

%install
cat > sinjdoc << EOF
#!/bin/sh
%{_bindir}/gij -classpath \
  %{_javadir}/java_cup-runtime.jar:%{_javadir}/sinjdoc.jar \
  net.cscott.sinjdoc.Main "\$@"
EOF
install -d 755 $RPM_BUILD_ROOT%{_bindir}
install -m 655 sinjdoc $RPM_BUILD_ROOT%{_bindir}/sinjdoc
install -d 755 $RPM_BUILD_ROOT%{_javadir}
install -D -m 644 sinjdoc.jar $RPM_BUILD_ROOT%{_javadir}/sinjdoc.jar
aot-compile-rpm

%post
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi

%postun
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_bindir}/sinjdoc
%{_javadir}/sinjdoc.jar
%{_libdir}/gcj/%{name}

%changelog
* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 29 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.5-12
- Fix FTBFS

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.5-7
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.5-6
- Autorebuild for GCC 4.3

* Thu Nov 29 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 0.5-5
- Fix URL field.
- Fix Source0 field.
- Own sinjdoc gcj directory.
- Resolves: rhbz#246367

* Tue Apr  3 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 0.5-4
- Obsolete gjdoc.

* Tue Mar 27 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 0.5-3
- Fix wrapper script argument quoting.

* Mon Mar 19 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 0.5-2
- Initial build in Fedora Core.

* Mon Mar 15 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 0.5-1
- Initial release.

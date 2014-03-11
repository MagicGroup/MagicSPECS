%global gem_name cucumber

Summary:        Tool to execute plain-text documents as functional tests
Name:           rubygem-%{gem_name}
Version: 1.2.1
Release: 3%{?dist}
Group:          Development/Languages
License:        MIT
URL:            http://cukes.info
Source0:        http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       ruby(release)
Requires:       ruby(rubygems)
Requires:       rubygem(term-ansicolor) >= 1.0.5
Requires:       rubygem(diff-lcs) >= 1.1.2
Requires:       rubygem(builder) >= 2.1.2
Requires:       rubygem(gherkin) >= 2.4.5
Requires:       rubygem(json) >= 1.4.6
BuildRequires:  rubygems-devel
BuildArch:      noarch
Provides:       rubygem(%{gem_name}) = %{version}

%description
Cucumber lets software development teams describe how software should behave
in plain text. The text is written in a business-readable domain-specific
language and serves as documentation, automated tests and development-aid.


%prep
%setup -q -c  -T
%gem_install -n %{SOURCE0}

%build


%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

rm -f $RPM_BUILD_ROOT%{gem_instdir}/.rvmrc
rm -f $RPM_BUILD_ROOT%{gem_instdir}/.gitattributes
rm -f $RPM_BUILD_ROOT%{gem_instdir}/.gitmodules
rm -f $RPM_BUILD_ROOT%{gem_instdir}/.yardopts
rm -f $RPM_BUILD_ROOT%{gem_instdir}/.travis.yml
rm -f $RPM_BUILD_ROOT%{gem_instdir}/Gemfile.lock
rm -f $RPM_BUILD_ROOT%{gem_instdir}/.rspec
find $RPM_BUILD_ROOT%{gem_instdir} -type f | grep '.gitignore' | xargs rm -f

# Remove zero-length documentation files
find $RPM_BUILD_ROOT%{gem_docdir} -empty -delete



%files
%defattr(-,root,root,-)
%{_bindir}/cucumber
%dir %{gem_instdir}
%{gem_instdir}/bin
%{gem_instdir}/features
%{gem_instdir}/gem_tasks
%{gem_libdir}
%{gem_instdir}/fixtures
%{gem_instdir}/spec
%{gem_instdir}/cucumber.yml
%{gem_instdir}/cucumber.gemspec
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/examples
%doc %{gem_docdir}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/History.md
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/Gemfile
%doc %{gem_instdir}/legacy_features
%{gem_cache}
%{gem_spec}


%changelog
* Sat Feb 23 2013 Vít Ondruch <vondruch@redhat.com> - 1.2.1-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Drop useless build requires.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 13 2012 Mo Morsi <mmorsi@redhat.com> - 1.2.1-1
- Update cucumber to version 1.2.1

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 27 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.1.9-1
- Update cucumber to version 1.1.9

* Wed Feb 01 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.0.1-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 12 2011 Mo Morsi <mmorsi@redhat.com> - 1.0.1-1
- update to latest upstream release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Michal Fojtik <mfojtik@redhat.com> - 0.10.0-1
- Version bump

* Mon Sep 27 2010 Michal Fojtik <mfojtik@redhat.com> - 0.9.0-4
- Fixed JSON version again

* Fri Sep 24 2010 Michal Fojtik <mfojtik@redhat.com> - 0.9.0-3
- Fixed JSON version

* Fri Sep 24 2010 Michal Fojtik <mfojtik@redhat.com> - 0.9.0-2
- Fixed gherkin version in dependency list

* Fri Sep 24 2010 Michal Fojtik <mfojtik@redhat.com> - 0.9.0-1
- Version bump to match upstream
- Fixed dependency issue with new gherkin package

* Wed Aug 04 2010 Michal Fojtik <mfojtik@redhat.com> - 0.8.3-4
- Fixed JSON version

* Wed Aug 04 2010 Michal Fojtik <mfojtik@redhat.com> - 0.8.3-3
- Removed JSON patch (JSON updated in Fedora)

* Wed Aug 01 2010 Michal Fojtik <mfojtik@redhat.com> - 0.8.3-2
- Patched Rakefile and replaced rspec beta version dependency
- Patched Rakefile and downgraded JSON dependency

* Wed Jun 30 2010 Michal Fojtik <mfojtik@redhat.com> - 0.8.3-1
- Newer release

* Sun Oct 18 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.4.2-1
- Newer release

* Mon Oct 12 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.4.0-1
- Newer release

* Fri Jun 26 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.3.10-3
- Get rid of duplicate files (thanks to Mamoru Tasaka)

* Mon Jun 08 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.3.10-2
- Use geminstdir macro where appropriate
- Do not move examples around
- Depend on ruby(abi)
- Replace defines with globals

* Fri Jun 05 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.3.10-1
- Package generated by gem2rpm
- Move examples into documentation
- Remove empty files
- Fix up License

# Generated from puppet-lint-0.2.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name puppet-lint
%global rubyabi 1.9.1

Name: rubygem-%{gem_name}
Version: 1.1.0
Release: 5%{?dist}
Summary: Ensure your Puppet manifests conform with the Puppetlabs style guide
Group: Development/Languages
License: MIT
URL: http://puppet-lint.com/
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Patch already accepted upstream and will be in the next release
# https://github.com/rodjek/puppet-lint/pull/141
%if 0%{?fedora} >= 19
Requires: ruby(release)
BuildRequires: ruby(release)
%else
Requires: ruby(abi) >= %{rubyabi}
BuildRequires: ruby(abi) >= %{rubyabi}
%endif
Requires: ruby(rubygems)
BuildRequires: rubygems-devel
BuildRequires: ruby
# Leaving these out as rspec 3+ isn't in Fedora or epel yet.
# BuildRequires: rubygem(rspec) => 3.0
# BuildRequires: rubygem(rspec) < 4
# BuildRequires: rubygem(rspec-its) => 1.0
# BuildRequires: rubygem(rspec-its) < 2
# BuildRequires: rubygem(rspec-collection_matchers) => 1.0
# BuildRequires: rubygem(rspec-collection_matchers) < 2
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Checks your Puppet manifests against the Puppetlabs
style guide and alerts you to any discrepancies.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
mkdir -p .%{gem_dir}

# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# gem install installs into a directory.  We set that to be a local
# directory so that we can move it into the buildroot in install
gem install --local --install-dir ./%{gem_dir} \
            --bindir ./%{_bindir} \
            --force --rdoc %{gem_name}-%{version}.gem

%install
mkdir -p %{buildroot}%{gem_dir}
cp -ap ./%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -ap ./%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x
# remove unecisary execute bit
chmod a-x %{buildroot}%{gem_instdir}/lib/puppet-lint/bin.rb

%check
# Leaving these out as rspec 3+ isn't in Fedora or epel yet.
# cd %{buildroot}%{gem_instdir}
# rspec -Ilib spec

%files
%dir %{gem_instdir}
%{_bindir}/puppet-lint
%{gem_instdir}/bin
%{gem_libdir}
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/LICENSE
%exclude %{gem_cache}
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/README.md
%{gem_instdir}/spec

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.1.0-5
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.1.0-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jan 14 2015 Russell Harrison <rharrison@fedoraproject.org> 1.1.0-1
- Upstream update to 1.1.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 14 2013 Russell Harrison <rharrison@fedoraproject.org> 0.3.2-3
- Update for Ruby 2.0 in F19+

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Russell Harrison <rharrison@fedoraproject.org> 0.3.2-1
- New upstream version. http://puppet-lint.com/changelog/
- Remove exit code patch. Fixed in upstream

* Tue Sep 25 2012 Russell Harrison <rharrison@fedoraproject.org> 0.2.1-3
- Drop requirement for the puppet package
- Pull in all of rspec as build requires
- Moving files not required at run time to the doc subpackage
- Excluding files not meant for packaging instead of removing them durring install
- Other fixes requested durring package review

* Wed Sep 12 2012 Russell Harrison <rharrison@fedoraproject.org> 0.2.1-2
- Patch to pass exit value to the shell https://github.com/rodjek/puppet-lint/pull/141

* Fri Sep  7 2012 Russell Harrison <rharrison@fedoraproject.org> - 0.2.1-1
- New upstream version
- Updated URL for new upstream website

* Sun Aug 26 2012 Russell Harrison <rharrison@fedoraproject.org> - 0.2.0-1
- Initial package

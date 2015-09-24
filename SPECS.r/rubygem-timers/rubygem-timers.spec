# Generated from timers-1.1.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name timers

Name: rubygem-%{gem_name}
Version: 4.0.1
Release: 1%{?dist}
Summary: Pure Ruby one-shot and periodic timers
Group: Development/Languages
License: MIT
URL: https://github.com/celluloid/timers
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(hitimes)
BuildRequires: rubygem(rspec)
BuildArch: noarch

%description
Schedule procs to run after a certain time using any API that accepts a timeout

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

sed -i '/#!/d' %{buildroot}%{gem_instdir}/Rakefile


%check
pushd .%{gem_instdir}
# Bundler is used only for development. No need to install it.
sed -i '/bundler/ s/^/#/' spec/spec_helper.rb

# We don't care about code coverage.
sed -i '/[Cc]overalls/ s/^/#/' spec/spec_helper.rb

# ruby-prof is not in Fedora yet, but I don't think we are interested in
# profiler output anyway.
# https://bugzilla.redhat.com/show_bug.cgi?id=1116021
sed -i '/ruby-prof/ s/^/#/' spec/performance_spec.rb

rspec spec
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/AUTHORS.md
%{gem_instdir}/CHANGES.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/spec
%{gem_instdir}/timers.gemspec

%changelog
* Mon Jun 22 2015 Vít Ondruch <vondruch@redhat.com> - 4.0.1-1
- Update to timers 4.0.1.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jan 26 2014 Achilleas Pipinellis <axilleas@axilleas.me> - 2.0.0-1
- Update to 2.0.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 03 2013 Axilleas Pipinellis <axilleas@axilleas.me> - 1.1.0-2
- Fix Summary/Description tags

* Thu May 30 2013 Axilleas Pipinellis <axilleas@axilleas.me> - 1.1.0-1
- Initial package

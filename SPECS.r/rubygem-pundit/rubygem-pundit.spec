# Generated from pundit-0.2.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name pundit

Name: rubygem-%{gem_name}
Version: 1.0.1
Release: 1%{?dist}
Summary: Object oriented authorization for Rails
Group: Development/Languages
License: MIT
URL: https://github.com/elabs/pundit
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(activemodel) >= 3.0.0
BuildRequires: rubygem(actionpack) >= 3.0.0
BuildRequires: rubygem(rspec) => 2.0
BuildRequires: rubygem(rspec) < 3.1
BuildArch: noarch

%description
Object oriented authorization for Rails applications.


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
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Fix permissions
chmod a-x %{buildroot}%{gem_instdir}/lib/generators/pundit/policy/templates/policy.rb

%check

# We don't need pry
sed -i '6d' spec/spec_helper.rb
rspec2 spec

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.travis.yml
%exclude %{gem_instdir}/.gitignore
%doc %{gem_instdir}/LICENSE.txt
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CODE_OF_CONDUCT.md
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/spec

%changelog
* Mon Aug 24 2015 Josef Stribny <jstribny@redhat.com> - 1.0.1-1
- Update to 1.0.1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jul 28 2014 Josef Stribny <jstribny@redhat.com> - 0.2.3-2
- Fix permissions

* Tue Jul 15 2014 Josef Stribny <jstribny@redhat.com> - 0.2.3-1
- Initial package

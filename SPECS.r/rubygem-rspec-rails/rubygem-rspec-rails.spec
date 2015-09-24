# Generated from rspec-rails-2.6.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rspec-rails

# Circular dependency with rubygem-ammeter.
%{?_with_bootstrap: %global bootstrap 1}

Name: rubygem-%{gem_name}
Version: 3.3.3
Release: 1%{?dist}
Summary: RSpec for Rails
Group: Development/Languages
License: MIT
URL: http://github.com/rspec/rspec-rails
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/rspec/rspec-rails.git && cd rspec-rails && git checkout v3.3.3
# tar czvf rspec-rails-3.3.3-tests.tgz features/ spec/
Source1: %{gem_name}-%{version}-tests.tgz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
%if ! 0%{?bootstrap}
#BuildRequires: rubygem(cucumber)
BuildRequires: rubygem(actionmailer)
BuildRequires: rubygem(activerecord)
BuildRequires: rubygem(ammeter)
BuildRequires: rubygem(bundler)
BuildRequires: rubygem(railties)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(sqlite3)
%endif
BuildArch: noarch

%description
RSpec for Rails-3+.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%if ! 0%{?bootstrap}
%check
pushd .%{gem_instdir}
tar xzvf %{SOURCE1}

# Bundler is used to execute two tests, so give him Gemfile.
echo "gem 'rspec', :require => false" > Gemfile

# I have no idea why this is passing upstream, since when RSpec are not supposed
# to be loaded, then RSpec::Support can't exist.
sed -i '/uninitialized constant RSpec::Support/ s/::Support//' spec/sanity_check_spec.rb

rspec -rspec_helper -rbundler spec

# Needs to generate a rails test application or ship pregenerated one (see
# generate:app rake task). This would be quite fragile.
# cucumber
popd
%endif

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/License.txt
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/Capybara.md
%doc %{gem_instdir}/Changelog.md
%doc %{gem_instdir}/README.md


%changelog
* Tue Aug 04 2015 Vít Ondruch <vondruch@redhat.com> - 3.3.3-1
- Update to rspec-rails 3.3.3.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 25 2015 Vít Ondruch <vondruch@redhat.com> - 3.2.1-1
- Update to rspec-rails 3.2.1.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 12 2014 Vít Ondruch <vondruch@redhat.com> - 2.14.1-1
- Update to rspec-rails 2.14.1.

* Fri Aug 16 2013 Mamoru TASAKA <mtasaka@fedoraproject.og> - 2.14.0-2
- Enable test suite again

* Fri Aug 16 2013 Mamoru TASAKA <mtasaka@fedoraproject.og> - 2.14.0-1
- Update to rspec-rails 2.14.0
- Still tests is disabled for now

* Mon Aug 12 2013 Josef Stribny <jstribny@redhat.com> - 2.13.0-4
- Relax Rails deps and disable tests for now

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.13.0-2
- Enable test suite again

* Thu Mar 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.13.0-1
- Update to rspec-rails 2.13.0

* Mon Mar 11 2013 Vít Ondruch <vondruch@redhat.com> - 2.12.0-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.12.0-2
- Enable test suite again

* Wed Jan  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.12.0-1
- Update to rspec-rails 2.12.0

* Tue Oct 16 2012 Vít Ondruch <vondruch@redhat.com> - 2.11.4-1
- Update to rspec-rails 2.11.4.

* Sat Oct 13 2012 Vít Ondruch <vondruch@redhat.com> - 2.11.0-1
- Update to rspec-rails 2.11.0.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 06 2012 Vít Ondruch <vondruch@redhat.com> - 2.8.1-2
- Tests enabled.

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 2.8.1-1
- Rebuilt for Ruby 1.9.3.
- Update to rspec-rails 2.8.1.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 20 2011 Vít Ondruch <vondruch@redhat.com> - 2.6.1-3
- Fixed .gemspec to contain correct dependencies (rhbz#747405).

* Tue Aug 23 2011 Vít Ondruch <vondruch@redhat.com> - 2.6.1-2
- Rebuilt due to the trailing slash bug of rpm-4.9.1

* Tue Jun 07 2011 Vít Ondruch <vondruch@redhat.com> - 2.6.1-1
- Updated to the rspec-rails 2.6.1

* Mon May 23 2011 Vít Ondruch <vondruch@redhat.com> - 2.6.0-1
- Initial package

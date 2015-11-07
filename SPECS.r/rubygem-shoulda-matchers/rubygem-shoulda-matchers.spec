# Generated from shoulda-matchers-2.6.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name shoulda-matchers

Name: rubygem-%{gem_name}
Version: 2.8.0
Release: 2%{?dist}
Summary: Making tests easy on the fingers and eyes
Group: Development/Languages
License: MIT
URL: https://github.com/thoughtbot/shoulda-matchers
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(activeresource)
BuildRequires: rubygem(bcrypt)
BuildRequires: rubygem(byebug)
BuildRequires: rubygem(coffee-rails)
BuildRequires: rubygem(jbuilder)
BuildRequires: rubygem(jquery-rails)
BuildRequires: rubygem(protected_attributes)
BuildRequires: rubygem(rails)
BuildRequires: rubygem(rspec-rails)
BuildRequires: rubygem(sass-rails)
BuildRequires: rubygem(sdoc)
BuildRequires: rubygem(shoulda-context)
BuildRequires: rubygem(spring)
BuildRequires: rubygem(sqlite3)
BuildRequires: rubygem(therubyracer)
BuildRequires: rubygem(turbolinks)
BuildRequires: rubygem(uglifier)
BuildRequires: rubygem(web-console)
BuildArch: noarch

%description
shoulda-matchers provides Test::Unit- and RSpec-compatible one-liners that
test common Rails functionality. These tests would otherwise be much longer,
more complex, and error-prone.


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

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Fix permissions.
# https://github.com/thoughtbot/shoulda-matchers/pull/744
chmod a-x %{buildroot}%{gem_instdir}/doc_config/yard/templates/default/fulldoc/html/css/bootstrap.css

%check
pushd .%{gem_instdir}

# It is easier to recreate the Gemfile to use local versions of gems.
rm Gemfile.lock
cat << GF > Gemfile
source 'https://rubygems.org'

gem 'activeresource'
gem 'bcrypt'
gem 'protected_attributes'
gem 'rspec-rails'
gem 'rails'
gem 'sqlite3'
# Required for /spec/acceptance/rails_integration_spec.rb:55
# but we don't have spring-commands-rspec in Fedora yet.
# gem 'spring'
GF

# Seems that AR changed the way how the ranges are checked. Disable the
# offending tests for now.
# https://github.com/thoughtbot/shoulda-matchers/issues/743
sed -i '/active_record_can_raise_range_error?/ a\      return false' spec/support/unit/helpers/active_record_versions.rb

# RSpec doesn't suppor #expects anymore.
# https://github.com/thoughtbot/shoulda-matchers/commit/093268eac41ec3fe86d37eb316c2ab15ae3b9a46
sed -i 's/double.expects/allow(double).to receive/' spec/unit/shoulda/matchers/doublespeak/stub_implementation_spec.rb

bundle exec rspec spec/unit

# minitest-reporters is not available in Fedora yet.
mv spec/acceptance/independent_matchers_spec.rb{,.disabled}

# JS runtime is needed.
sed -i "/bundle.remove_gem 'uglifier'/ a\        bundle.add_gem 'therubyracer'" spec/support/acceptance/helpers/step_helpers.rb

bundle exec rspec spec/acceptance

popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
# This would just complicate licensing due to bundled JS/CSS without any
# real benefit.
%exclude %{gem_instdir}/doc_config
%license %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Appraisals
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/Gemfile*
%{gem_instdir}/NEWS.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/cucumber.yml
%{gem_instdir}/gemfiles
%doc %{gem_instdir}/docs.watchr
%{gem_instdir}/script
%{gem_instdir}/shoulda-matchers.gemspec
%{gem_instdir}/spec
%{gem_instdir}/tasks

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.8.0-2
- 为 Magic 3.0 重建

* Fri Jun 26 2015 Vít Ondruch <vondruch@redhat.com> - 2.8.0-1
- Update to should-matchers 2.8.0.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jul 07 2014 Vít Ondruch <vondruch@redhat.com> - 2.6.1-3
- Workaround RoR 4.1.2+ compatibility issue.
- Relax Rake dependency.

* Thu Jul 03 2014 Vít Ondruch <vondruch@redhat.com> - 2.6.1-2
- Add missing BR: rubygem(shoulda-context).
- Updated upstream URL.
- Relaxed BR: ruby dependency.

* Mon Jun 30 2014 Vít Ondruch <vondruch@redhat.com> - 2.6.1-1
- Initial package

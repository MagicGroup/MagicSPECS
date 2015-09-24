# Generated from rails-observers-0.1.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rails-observers

Name: rubygem-%{gem_name}
Version: 0.1.2
Release: 6%{?dist}
Summary: Rails observer (removed from core in Rails 4.0)
Group: Development/Languages
License: MIT
URL: https://github.com/rails/rails-observers
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Fixing tests for Rails 4.1+.
# https://github.com/rails/rails-observers/pull/26
Patch0: rubygem-rails-observers-0.1.2-substituting-ActiveRecord-TestCase-with-ActiveSupport-TestCase.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(activerecord-deprecated_finders)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(rails) => 4.0
BuildRequires: rubygem(rails) < 5
BuildRequires: rubygem(sqlite3)
BuildRequires: ruby
BuildArch: noarch

%description
Rails observer (removed from core in Rails 4.0). ActiveModel::Observer,
ActiveRecord::Observer and ActionController::Caching::Sweeper extracted
from Rails.

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

# Remove shebang from non-executable Rakefile
sed -i "/#\!\/usr\/bin\/env rake/d" Rakefile

%patch0 -p1

%build
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
# Needs bundler
rm ./test/rake_test.rb

# Fix Mocha 1.x+ compatibility.
sed -i "/minitest/ a\require 'mocha/setup'" test/observing_test.rb

ruby -Ilib:test -e "Dir.glob './test/*_test.rb', &method(:require)"
ruby -Ilib:test -e "Dir.glob './test/generators/*_test.rb', &method(:require)"
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%{gem_spec}
%license %{gem_instdir}/LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/%{gem_name}.gemspec.erb
%{gem_instdir}/test

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 19 2014 Josef Stribny <jstribny@redhat.com> - 0.1.2-5
- Fix tests

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Oct 04 2013 Josef Stribny <jstribny@redhat.com> - 0.1.2-3
- Add mocha to build deps and enable test suite

* Thu Aug 01 2013 Josef Stribny <jstribny@redhat.com> - 0.1.2-2
- Improve the removal of the shebang
- fix the description and summary

* Wed Jul 31 2013 Josef Stribny <jstribny@redhat.com> - 0.1.2-1
- Initial package

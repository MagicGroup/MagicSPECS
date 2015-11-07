# Generated from shoulda-3.5.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name shoulda

Name: rubygem-%{gem_name}
Version: 3.5.0
Release: 3%{?dist}
Summary: Making tests easy on the fingers and eyes
Group: Development/Languages
License: MIT
URL: https://github.com/thoughtbot/shoulda
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Fix test suite to work with Rails 4.1 and locally installed gems.
Patch0: rubygem-shoulda-3.5.0-test-fixes.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(aruba)
BuildRequires: rubygem(cucumber)
BuildRequires: rubygem(rails)
BuildRequires: rubygem(shoulda-context)
BuildRequires: rubygem(shoulda-matchers)
BuildRequires: rubygem(sqlite3)
BuildRequires: rubygem(rspec-rails)
BuildArch: noarch

%description
Making tests easy on the fingers and eyes.


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

pushd .%{gem_instdir}
%patch0 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Fix wrong-file-end-of-line-encoding for rpmlint.
sed -i 's/\r$//' %{buildroot}%{gem_instdir}/MIT-LICENSE


# Run the test suite
%check
cp .%{gem_spec} .%{gem_instdir}/shoulda.gemspec

pushd .%{gem_instdir}

# Relax version dependencies.
sed -i -r 's/(dependency\(%q<.*>), \[".*"\]/\1/' shoulda.gemspec

# Drop useless dependency.
sed -i '/appraisal/d' shoulda.gemspec

# rspec-rails 3.x compatibility.
# https://github.com/thoughtbot/shoulda/pull/257

# -fs option was removed from RSpec.
sed -i '/SPEC_OPTS=-fs/ s/fs/fd/' features/rails_integration.feature

# RSpec Rails use rails_helper now.
# https://github.com/rspec/rspec-rails/tree/3-3-maintenance/features/upgrade#default-helper-files-created-in-rspec-3x-have-changed
sed -i 's/spec_helper/rails_helper/' features/rails_integration.feature

cucumber
popd

%files
%doc %{gem_instdir}/MIT-LICENSE
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Appraisals
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/features
%{gem_instdir}/gemfiles
%{gem_instdir}/shoulda.gemspec

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 3.5.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 26 2014 Vít Ondruch <vondruch@redhat.com> - 3.5.0-1
- Update to Shoulda 3.5.0.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 08 2013 Vít Ondruch <vondruch@redhat.com> - 2.11.3-7
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 2.11.3-4
- Rebuilt for Ruby 1.9.3.

* Sun Jan 08 2012 <stahnma@fedoraproject.org> - 2.11.3-2
- Jumped in to help with FTBFS bz#715949

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 01 2010 Michael Stahnke <stahnma@fedoraproject.org> - 2.11.3-1
- New version
- Fix many broken tests 
- Split into -doc package

* Sat Jan  9 2010 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.10.2-2
- Fix BuildRequires
- First package

# Generated from coffee-rails-3.2.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name coffee-rails

Summary: Coffee Script adapter for the Rails asset pipeline
Name: rubygem-%{gem_name}
Version: 4.1.0
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/rails/coffee-rails
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(coffee-script) >= 2.2.0
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(railties) => 4.0.0
BuildRequires: rubygem(railties) < 5.0.0
BuildRequires: rubygem(sprockets-rails)
BuildRequires: rubygem(therubyracer)
BuildRequires: rubygem(tzinfo)
BuildArch: noarch

%description
Coffee Script adapter for the Rails asset pipeline.


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

%check
pushd .%{gem_instdir}
# Disable Bundler.
sed -i '/require .bundler\/setup./ s/^/#/' test/test_helper.rb

# Explicitly require ActionController to workaround "uninitialized constant
# ActionController::Live" issue.
# https://github.com/rails/rails/issues/15918
# Explicitly require Shellwords to avoid "undefined method `shellescape'" error.
# https://github.com/rails/rails/issues/15919
ruby -raction_controller -rshellwords -I.:test:lib -e 'Dir.glob("test/**/*_test.rb").each {|t| require t}'
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_instdir}/.*
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Gemfile
%{gem_instdir}/%{gem_name}.gemspec*
%{gem_instdir}/Rakefile
%{gem_instdir}/gemfiles
%{gem_instdir}/test

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 4.1.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Feb 16 2015 Josef Stribny <jstribny@redhat.com> - 4.1.0-1
- Update to 4.1.0

* Wed Jun 25 2014 Vít Ondruch <vondruch@redhat.com> - 4.0.1-1
- Update to coffee-rails 4.0.1.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 05 2013 Josef Stribny <jstribny@redhat.com> - 4.0.0-1
- Update to coffee-rails 4.0.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 14 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 3.2.2-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jul 23 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 3.2.2-1
- Initial package

# Generated from sass-rails-3.2.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name sass-rails

Name: rubygem-%{gem_name}
Version: 5.0.4
Release: 2%{?dist}
Summary: Sass adapter for the Rails asset pipeline
Group: Development/Languages
License: MIT
URL: https://github.com/rails/sass-rails
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/rails/sass-rails.git && cd sass-rails
# git checkout v5.0.4 && tar czvf sass-rails-5.0.4-tests.tgz ./test
Source1: sass-rails-%{version}-tests.tgz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(bundler)
BuildRequires: rubygem(sqlite3)
BuildRequires: rubygem(tilt)
BuildRequires: rubygem(rails)
BuildRequires: rubygem(sass)
BuildArch: noarch

%description
Sass adapter for the Rails asset pipeline.


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

%check
pushd .%{gem_instdir}
tar xf %{SOURCE1}

# Copy in .gemspec and use the sass-rails sources
cp %{buildroot}%{gem_spec} sass-rails.gemspec
echo 'gem "sass-rails", :path => "."' >> Gemfile

ruby -I.:test -e 'Dir.glob "test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 5.0.4-2
- 为 Magic 3.0 重建

* Wed Sep 16 2015 Vít Ondruch <vondruch@redhat.com> - 5.0.4-1
- Update to sass-rails 5.0.4.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Vít Ondruch <vondruch@redhat.com> - 5.0.3-1
- Update to sass-rails 5.0.3.

* Mon Feb 16 2015 Josef Stribny <jstribny@redhat.com> - 5.0.1-1
- Update to 5.0.1

* Tue Jul 01 2014 Vít Ondruch <vondruch@redhat.com> - 4.0.3-1
- Update to sass-rails 4.0.3.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 05 2013 Josef Stribny <jstribny@redhat.com> - 4.0.0-1
- Update to sass-rails 4.0.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Vít Ondruch <vondruch@redhat.com> - 3.2.6-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to sass-rails 3.2.6.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jul 23 2012 Vít Ondruch <vondruch@redhat.com> - 3.2.5-1
- Initial package

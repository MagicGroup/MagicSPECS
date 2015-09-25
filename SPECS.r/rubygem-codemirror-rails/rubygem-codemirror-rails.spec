# Generated from codemirror-rails-4.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name codemirror-rails

Name: rubygem-%{gem_name}
Version: 4.2
Release: 3%{?dist}
Summary: Use CodeMirror with Rails 3
Group: Development/Languages
License: MIT
URL: https://rubygems.org/gems/codemirror-rails
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(rails) => 3.0
BuildRequires: rubygem(rails) < 5
BuildRequires: rubygem(sqlite3)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(capybara)
BuildArch: noarch
%description
This gem provides CodeMirror assets for your Rails 3 application.


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

#%%check
#pushd .%{gem_instdir}
# Ged rid of Bundler
#sed -i -e '2,8d' test/dummy/config/boot.rb
#sed -i -e '5d' test/dummy/config/application.rb
#ruby -Ilib -Itest -e 'Dir.glob "./test/integration/*.rb", &method(:require)'
#popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.gitignore
%{gem_spec}
%{gem_instdir}/LICENSE
%{gem_instdir}/vendor

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/doc
%{gem_instdir}/test
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile
%{gem_instdir}/%{gem_name}.gemspec

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 4.2-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jul 15 2014 Josef Stribny <jstribny@redhat.com> - 4.2-1
- Initial package

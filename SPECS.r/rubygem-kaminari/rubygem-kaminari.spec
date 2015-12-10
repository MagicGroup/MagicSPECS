# Generated from kaminari-0.16.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name kaminari

Name: rubygem-%{gem_name}
Version: 0.16.1
Release: 5%{?dist}
Summary: A pagination engine plugin for Rails 3+ and other modern frameworks
Group: Development/Languages
License: MIT
URL: https://github.com/amatsuda/kaminari
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: rubygems-devel
BuildRequires: rubygem(tzinfo)
BuildRequires: rubygem(rspec) < 3.0
BuildRequires: rubygem(rspec-rails)
BuildRequires: rubygem(sqlite3)
BuildRequires: rubygem(rr)
BuildRequires: rubygem(capybara) >= 1.0
BuildRequires: rubygem(database_cleaner)
BuildRequires: rubygem(rails) >= 3.0.0
BuildArch: noarch

%description
Kaminari is a Scope & Engine based, clean, powerful, agnostic,
customizable and sophisticated paginator for Rails 3+.


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
#pushd .%%{gem_instdir}
# Ged rid of Bundler
#sed -i -e '9,10d' spec/spec_helper.rb
# Problem in Fedora's current database_cleaner
# https://github.com/DatabaseCleaner/database_cleaner/issues/224
#rspec -Ilib \
#      -rkaminari \
#      -rkaminari/railtie \
#      -ractive_record \
#      -rkaminari/models/array_extension \
#      -rkaminari/models/active_record_relation_methods \
#      -rkaminari/models/active_record_model_extension \
#      spec
#popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.document
%exclude %{gem_instdir}/.gemtest
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.rspec
%exclude %{gem_instdir}/.travis.yml
%{gem_spec}
%{gem_instdir}/app
%{gem_instdir}/config
%doc %{gem_instdir}/MIT-LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/CHANGELOG.rdoc
%{gem_instdir}/gemfiles
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/spec

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.16.1-5
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.16.1-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.16.1-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jul 15 2014 Josef Stribny <jstribny@redhat.com> - 0.16.1-1
- Initial package

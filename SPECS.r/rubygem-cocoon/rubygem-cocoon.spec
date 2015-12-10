# Generated from cocoon-1.2.6.gem by gem2rpm -*- rpm-spec -*-
%global gem_name cocoon

Name: rubygem-%{gem_name}
Version: 1.2.6
Release: 7%{?dist}
Summary: Easier nested forms with standard forms, formtastic and simple-form
Group: Development/Languages
License: MIT
URL: http://github.com/nathanvda/cocoon
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: rubygems-devel

# Missing railties dependency in upstream
# https://github.com/nathanvda/cocoon/issues/226
Requires: rubygem(railties)

# For tests
#BuildRequires: rubygem(rails) >= 4.0.0
#BuildRequires: rubygem(sqlite3)
#BuildRequires: rubygem(json_pure)
#BuildRequires: rubygem(rspec-rails) >= 2.8.0
#BuildRequires: rubygem(rspec) >= 2.8.0
#BuildRequires: rubygem(actionpack) >= 4.0.0
#BuildRequires: rubygem(simplecov)
#BuildRequires: rubygem(nokogiri)
#BuildRequires: rubygem(psych)

# These gems are not yet in Fedora
#BuildRequires: rubygem(jeweler)
#BuildRequires: rubygem(racc)
#BuildRequires: rubygem(generator_spec)
BuildArch: noarch

%if 0%{?fedora} <= 20
Requires: ruby(release)
Requires: ruby(rubygems)
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
Unobtrusive nested forms handling, using jQuery. Use this and discover
cocoon-heaven.


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

# Get rid of shebang in non-executable script
sed -i -e '1d' %{buildroot}/%{gem_instdir}/spec/dummy/script/rails

# generator_spec is not in fedora
#%%check
#pushd .%%{gem_instdir}
# Ged rid of Bundler
#sed -i -e '2,8d' spec/dummy/config/boot.rb
#sed -i -e '9d' spec/dummy/config/application.rb
#rspec -rrails/generators spec
#popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.travis.yml
%{gem_spec}
%{gem_instdir}/app
%doc %{gem_instdir}/MIT-LICENSE

%files doc
%exclude %{gem_instdir}/spec/dummy/public/stylesheets/.gitkeep
%doc %{gem_docdir}
%doc %{gem_instdir}/README.markdown
%doc %{gem_instdir}/History.md
%doc %{gem_instdir}/VERSION
%{gem_instdir}/gemfiles
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile
%{gem_instdir}/spec
%{gem_instdir}/%{gem_name}.gemspec

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.2.6-7
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.2.6-6
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.2.6-5
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 04 2014 Josef Stribny <jstribny@redhat.com> - 1.2.6-3
- Prefer %%exclude, fix path in %%install

* Mon Aug 04 2014 Josef Stribny <jstribny@redhat.com> - 1.2.6-2
- Fix lenght of summary, shebang in non-executable script

* Tue Jul 15 2014 Josef Stribny <jstribny@redhat.com> - 1.2.6-1
- Initial package
